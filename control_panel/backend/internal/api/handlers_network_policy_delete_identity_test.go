package api

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"

	"github.com/gin-gonic/gin"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

type apiNoopTaskHandler struct{}

func (apiNoopTaskHandler) Run(_ context.Context, _ *db.Task, reporter *tasks.Reporter) error {
	reporter.Succeed()
	return nil
}

func TestDeleteNetworkPolicyCapturesSubmittedIdentity(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "network-policy-delete.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	engine := tasks.NewEngine(store)
	engine.Register("k8s_delete_np", apiNoopTaskHandler{})
	client := fake.NewSimpleClientset(&networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{
		Name: "allow-notebook", Namespace: "ns1", UID: "uid-original", ResourceVersion: "17",
		Labels: map[string]string{"managed-by": "control-panel"},
	}})
	handlers := &k8sHandlers{eng: engine, store: store, client: client}
	gin.SetMode(gin.TestMode)
	router := gin.New()
	router.DELETE("/network-policies/:name", handlers.deleteNetworkPolicy)

	req := httptest.NewRequest(http.MethodDelete, "/network-policies/allow-notebook?namespace=ns1", nil)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, req)
	if response.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s, want 202", response.Code, response.Body.String())
	}
	var body struct {
		TaskID int64 `json:"task_id"`
	}
	if err := json.Unmarshal(response.Body.Bytes(), &body); err != nil {
		t.Fatal(err)
	}
	task, err := store.GetTask(context.Background(), body.TaskID)
	if err != nil {
		t.Fatal(err)
	}
	var params map[string]any
	if err := json.Unmarshal([]byte(task.ParamsJSON), &params); err != nil {
		t.Fatal(err)
	}
	if params["uid"] != "uid-original" || params["resource_version"] != "17" {
		t.Fatalf("submitted identity=%v, want uid and resource_version pinned", params)
	}
}

func TestDeleteMissingNetworkPolicyDoesNotSubmitTask(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "missing-network-policy.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	engine := tasks.NewEngine(store)
	engine.Register("k8s_delete_np", apiNoopTaskHandler{})
	handlers := &k8sHandlers{eng: engine, store: store, client: fake.NewSimpleClientset()}
	gin.SetMode(gin.TestMode)
	router := gin.New()
	router.DELETE("/network-policies/:name", handlers.deleteNetworkPolicy)

	req := httptest.NewRequest(http.MethodDelete, "/network-policies/missing?namespace=ns1", nil)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, req)
	if response.Code != http.StatusNotFound {
		t.Fatalf("code=%d body=%s, want 404", response.Code, response.Body.String())
	}
	tasks, err := store.ListTasks(context.Background(), 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(tasks) != 0 {
		t.Fatalf("submitted %d task(s) for a missing NetworkPolicy", len(tasks))
	}
}
