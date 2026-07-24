package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"xirang/control_panel/internal/workers"
)

// TestProvisionStorageViaAPI verifies POST /api/v1/storage/provision returns
// 202 + task_id. The async task will fail (the test's ssh.Manager points at an
// unreachable host), but the API contract is to submit and return the task_id
// synchronously - same pattern as ChangeRootPassword.
func TestProvisionStorageViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
		"size_gb": 100, "fs_type": "xfs", "mount_point": "/data02/nb",
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/provision", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if resp["task_id"] == nil {
		t.Fatalf("no task_id in response: %s", w.Body.String())
	}
}

// TestReclaimStorageViaAPI verifies POST /api/v1/storage/reclaim returns
// 202 + task_id. Like provision, the async task fails but the API only
// asserts the synchronous 202 submission.
func TestReclaimStorageViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
		"mount_point": "/data02/nb",
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/reclaim", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if resp["task_id"] == nil {
		t.Fatalf("no task_id in response: %s", w.Body.String())
	}
}

// TestListStorageTasksViaAPI verifies GET /api/v1/storage returns 200 and the
// filtered list of tasks with target_kind='storage'. A provision task is
// submitted first so the list has at least one storage task; the async task
// fails (unreachable host) but the row persists.
func TestListStorageTasksViaAPI(t *testing.T) {
	r, ws, store, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	// Submit a storage task so the list has data.
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
		"size_gb": 100, "fs_type": "xfs", "mount_point": "/data02/nb",
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/provision", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("setup provision failed: code=%d body=%s", w.Code, w.Body.String())
	}
	// Give the async task a moment to be persisted (Submit is synchronous, so
	// the row exists before the 202 is returned; the brief sleep is just
	// defensive).
	time.Sleep(50 * time.Millisecond)

	req2 := httptest.NewRequest("GET", "/api/v1/storage", nil)
	req2.Header.Set("Authorization", authHeader(t, tk))
	w2 := httptest.NewRecorder()
	r.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w2.Code, w2.Body.String())
	}
	var list []map[string]any
	if err := json.Unmarshal(w2.Body.Bytes(), &list); err != nil {
		t.Fatal(err)
	}
	if len(list) < 1 {
		t.Fatalf("expected >=1 storage task, got %d", len(list))
	}
	for _, task := range list {
		if task["target_kind"] != "storage" {
			t.Fatalf("non-storage task leaked into list: %v", task)
		}
	}
	// Sanity: the store has the task too.
	all, _ := store.ListTasks(context.Background(), 100)
	if len(all) < 1 {
		t.Fatalf("store has no tasks")
	}
}

// TestStorageEndpointsRequireAuth verifies all three storage endpoints are
// behind BearerMiddleware (authed group): no Authorization header -> 401.
func TestStorageEndpointsRequireAuth(t *testing.T) {
	r, _, _, _ := newRouter(t)
	endpoints := []struct {
		method, path string
	}{
		{"POST", "/api/v1/storage/provision"},
		{"POST", "/api/v1/storage/reclaim"},
		{"GET", "/api/v1/storage"},
	}
	for _, e := range endpoints {
		req := httptest.NewRequest(e.method, e.path, nil)
		w := httptest.NewRecorder()
		r.ServeHTTP(w, req)
		if w.Code != http.StatusUnauthorized {
			t.Errorf("%s %s: code=%d, want 401", e.method, e.path, w.Code)
		}
	}
}
