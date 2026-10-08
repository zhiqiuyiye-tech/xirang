package api

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func TestDeleteServiceAPIKeepsSubmittedIdentity(t *testing.T) {
	router, store, tk, client := newRouterWithK8s(t)
	_, err := client.CoreV1().Services("ns1").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "mapping-a", Namespace: "ns1", UID: "service-original", ResourceVersion: "17", Labels: map[string]string{"managed-by": "control-panel"}},
	}, metav1.CreateOptions{})
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest("DELETE", "/api/v1/k8s/services/mapping-a?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	if rr.Code != http.StatusAccepted {
		t.Fatalf("code=%d %s", rr.Code, rr.Body.String())
	}
	var response struct {
		TaskID int64 `json:"task_id"`
	}
	_ = json.Unmarshal(rr.Body.Bytes(), &response)
	waitForAuditTask(t, store, response.TaskID)
	task, err := store.GetTask(context.Background(), response.TaskID)
	if err != nil {
		t.Fatal(err)
	}
	var params map[string]any
	_ = json.Unmarshal([]byte(task.ParamsJSON), &params)
	if params["uid"] != "service-original" || params["resource_version"] != "17" {
		t.Fatalf("task missing validated identity: %#v", params)
	}
}

func TestDeleteMissingServiceDoesNotSubmitUnpinnedTask(t *testing.T) {
	router, store, tk, _ := newRouterWithK8s(t)
	req := httptest.NewRequest("DELETE", "/api/v1/k8s/services/missing?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	if rr.Code != http.StatusNotFound {
		t.Fatalf("code=%d %s", rr.Code, rr.Body.String())
	}
	tasks, err := store.ListTasks(context.Background(), 100)
	if err != nil || len(tasks) != 0 {
		t.Fatalf("unexpected unpinned task: %#v %v", tasks, err)
	}
}

func TestAuditUIPortMappingsKeepPortDetails(t *testing.T) {
	raw := map[string]any{"mappings": []any{map[string]any{"pod_port": float64(8888), "node_port": float64(31555), "password": "not-for-audit"}}}
	details := safeAuditDetails(raw)
	encoded, _ := json.Marshal(details)
	var result map[string]any
	_ = json.Unmarshal(encoded, &result)
	ports, ok := result["ports"].([]any)
	if !ok || len(ports) != 1 {
		t.Fatalf("missing UI port mapping details: %s", encoded)
	}
	port := ports[0].(map[string]any)
	if port["target_port"] != float64(8888) || port["node_port"] != float64(31555) || port["password"] != nil {
		t.Fatalf("wrong details: %#v", port)
	}
}
