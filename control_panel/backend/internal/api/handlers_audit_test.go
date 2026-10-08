package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"strings"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/workers"
)

func waitForAuditTask(t *testing.T, store *db.Store, id int64) {
	t.Helper()
	deadline := time.Now().Add(3 * time.Second)
	for time.Now().Before(deadline) {
		task, err := store.GetTask(context.Background(), id)
		if err == nil && (task.Status == "succeeded" || task.Status == "failed") {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatal("task did not finish")
}

func TestAuditWorkerDetailsAndCredentialRedaction(t *testing.T) {
	router, _, store, tk := newRouter(t)
	request := func(method, path, body string) *httptest.ResponseRecorder {
		req := httptest.NewRequest(method, path, strings.NewReader(body))
		req.Header.Set("Authorization", authHeader(t, tk))
		req.Header.Set("Content-Type", "application/json")
		rr := httptest.NewRecorder()
		router.ServeHTTP(rr, req)
		return rr
	}
	rr := request("POST", "/api/v1/workers", `{"name":"worker-a","host":"10.0.0.8"}`)
	if rr.Code != http.StatusCreated {
		t.Fatal(rr.Body.String())
	}
	var created struct {
		ID int64 `json:"id"`
	}
	_ = json.Unmarshal(rr.Body.Bytes(), &created)
	path := "/api/v1/workers/" + strconv.FormatInt(created.ID, 10)
	if rr = request("PUT", path, `{"name":"worker-b","host":"10.0.0.9"}`); rr.Code != http.StatusOK {
		t.Fatal(rr.Body.String())
	}
	if rr = request("POST", path+"/credentials/password", `{"password":"super-secret"}`); rr.Code != http.StatusOK {
		t.Fatal(rr.Body.String())
	}
	rr = request("GET", "/api/v1/audit-log", "")
	if rr.Code != http.StatusOK {
		t.Fatal(rr.Body.String())
	}
	var logs []struct {
		Action  string         `json:"action"`
		Details map[string]any `json:"details"`
	}
	if err := json.Unmarshal(rr.Body.Bytes(), &logs); err != nil {
		t.Fatal(err)
	}
	byAction := map[string]map[string]any{}
	for _, log := range logs {
		byAction[log.Action] = log.Details
	}
	if d := byAction["worker.create"]; d["worker_name"] != "worker-a" || d["host"] != "10.0.0.8" || d["port"] != float64(22) {
		t.Fatalf("create details: %#v", d)
	}
	if d := byAction["worker.update"]; d["before"] == nil || d["after"] == nil {
		t.Fatalf("update details: %#v", d)
	}
	if d := byAction["worker.set_panel_password"]; d["worker_name"] != "worker-b" {
		t.Fatalf("credential target missing: %#v", d)
	}
	if bytes.Contains(rr.Body.Bytes(), []byte("super-secret")) || bytes.Contains(rr.Body.Bytes(), []byte("params_json")) {
		t.Fatal("audit API leaked credentials or raw params")
	}
	persisted, _ := store.ListAudit(context.Background(), 100)
	for _, log := range persisted {
		if log.ParamsJSON != nil && strings.Contains(*log.ParamsJSON, "super-secret") {
			t.Fatal("audit persisted password")
		}
	}
}

func TestAuditStorageTaskDetails(t *testing.T) {
	router, ws, store, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "storage-worker", Host: "127.0.0.1"})
	payload, _ := json.Marshal(map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "abcdef12", "size_gb": 200, "mount_point": "/data02/nfs_abcdef12", "password": "must-not-log"})
	req := httptest.NewRequest("POST", "/api/v1/storage/provision", bytes.NewReader(payload))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	if rr.Code != http.StatusAccepted {
		t.Fatal(rr.Body.String())
	}
	var submitted struct {
		TaskID int64 `json:"task_id"`
	}
	_ = json.Unmarshal(rr.Body.Bytes(), &submitted)
	logs, _ := store.ListAudit(context.Background(), 100)
	if len(logs) != 1 || logs[0].ParamsJSON == nil {
		t.Fatalf("missing audit parameters: %#v", logs)
	}
	var details map[string]any
	_ = json.Unmarshal([]byte(*logs[0].ParamsJSON), &details)
	if details["lv_name"] != "abcdef12" || details["size_gb"] != float64(200) || details["task_id"] != float64(submitted.TaskID) || details["worker_name"] != "storage-worker" {
		t.Fatalf("details: %#v", details)
	}
	if strings.Contains(*logs[0].ParamsJSON, "must-not-log") {
		t.Fatal("unexpected request credentials persisted")
	}
	waitForAuditTask(t, store, submitted.TaskID)
}

func TestAuditDeletedPortMappingKeepsPortDetails(t *testing.T) {
	router, store, tk, client := newRouterWithK8s(t)
	_, err := client.CoreV1().Services("notebook-a").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "mapping-a", Namespace: "notebook-a", Labels: map[string]string{"managed-by": "control-panel"}},
		Spec:       corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Ports: []corev1.ServicePort{{Port: 8888, NodePort: 31555, Protocol: corev1.ProtocolTCP}}},
	}, metav1.CreateOptions{})
	if err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest("DELETE", "/api/v1/k8s/services/mapping-a?namespace=notebook-a", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	if rr.Code != http.StatusAccepted {
		t.Fatal(rr.Body.String())
	}
	var response struct {
		TaskID int64 `json:"task_id"`
	}
	_ = json.Unmarshal(rr.Body.Bytes(), &response)
	waitForAuditTask(t, store, response.TaskID)
	logs, _ := store.ListAudit(context.Background(), 100)
	if len(logs) != 1 || logs[0].ParamsJSON == nil {
		t.Fatal("missing delete audit")
	}
	if logs[0].Target == nil || *logs[0].Target != "notebook-a/mapping-a" || !strings.Contains(*logs[0].ParamsJSON, "31555") {
		t.Fatalf("port mapping details missing: %+v %s", logs[0], *logs[0].ParamsJSON)
	}
}

func TestAuditHistoricalParamsAreFiltered(t *testing.T) {
	router, _, store, tk := newRouter(t)
	raw := `{"namespace":"notebook-a","password":"old-secret","private_key":"old-key","unknown":"old-unknown","ports":[{"node_port":31555,"target_port":8888,"password":"nested-secret"}],"host":{"password":"nested-host-secret"}}`
	if err := store.InsertAudit(context.Background(), db.AuditLog{Action: "k8s.create_service", ParamsJSON: &raw, Result: "submitted"}); err != nil {
		t.Fatal(err)
	}
	req := httptest.NewRequest("GET", "/api/v1/audit-log", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	rr := httptest.NewRecorder()
	router.ServeHTTP(rr, req)
	body := rr.Body.String()
	for _, secret := range []string{"old-secret", "old-key", "old-unknown", "nested-secret", "nested-host-secret", "params_json"} {
		if strings.Contains(body, secret) {
			t.Fatalf("leaked %s: %s", secret, body)
		}
	}
	if !strings.Contains(body, `"details"`) || !strings.Contains(body, "31555") || !strings.Contains(body, "notebook-a") {
		t.Fatalf("safe details missing: %s", body)
	}
}
