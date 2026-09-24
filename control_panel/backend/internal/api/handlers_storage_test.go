package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
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

// TestCreateVGViaAPI verifies POST /api/v1/storage/vg submits the
// storage_create_vg task and returns 202 + task_id.
func TestCreateVGViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb", "/dev/sdc"},
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/vg", bytes.NewReader(body))
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
		t.Fatalf("no task_id: %s", w.Body.String())
	}
}

// TestResizeLVViaAPI verifies POST /api/v1/storage/lv/resize submits the
// storage_resize_lv task and returns 202 + task_id.
func TestResizeLVViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
		"action": "grow", "delta_gb": 50,
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/lv/resize", bytes.NewReader(body))
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
		t.Fatalf("no task_id: %s", w.Body.String())
	}
}

// TestDeleteLVViaAPI verifies POST /api/v1/storage/lv/delete submits the
// storage_delete_lv task and returns 202 + task_id.
func TestDeleteLVViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	body, _ := json.Marshal(map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	req := httptest.NewRequest("POST", "/api/v1/storage/lv/delete", bytes.NewReader(body))
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
		t.Fatalf("no task_id: %s", w.Body.String())
	}
}

// TestListInventoryValidation verifies the sync inventory endpoint's input
// validation: missing worker_id -> 400, unknown worker -> 404. (The 200 path
// requires a live SSH connection and is not exercised here, matching the
// existing listVgs coverage.)
func TestListInventoryValidation(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	// Missing worker_id.
	req := httptest.NewRequest("GET", "/api/v1/storage/inventory", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusBadRequest {
		t.Fatalf("missing worker_id: code=%d want 400", w.Code)
	}
	// Unknown worker.
	req2 := httptest.NewRequest("GET", "/api/v1/storage/inventory?worker_id=99999", nil)
	req2.Header.Set("Authorization", authHeader(t, tk))
	w2 := httptest.NewRecorder()
	r.ServeHTTP(w2, req2)
	if w2.Code != http.StatusNotFound {
		t.Fatalf("unknown worker: code=%d want 404", w2.Code)
	}
	// Valid worker_id but SSH unreachable -> 500 (not a 202; sync endpoint).
	req3 := httptest.NewRequest("GET", "/api/v1/storage/inventory?worker_id="+itoa(wid), nil)
	req3.Header.Set("Authorization", authHeader(t, tk))
	w3 := httptest.NewRecorder()
	r.ServeHTTP(w3, req3)
	if w3.Code != http.StatusInternalServerError {
		t.Fatalf("valid worker unreachable: code=%d want 500", w3.Code)
	}
}

// itoa is a tiny strconv.Itoa alias to keep imports lean in this test file.
func itoa(n int64) string {
	return strconv.FormatInt(n, 10)
}

// TestListNFSHostsViaAPI verifies GET /api/v1/storage/nfs-hosts returns 200
// with an array of NFS host summaries.
func TestListNFSHostsViaAPI(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	// Empty case
	req := httptest.NewRequest("GET", "/api/v1/storage/nfs-hosts", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var hosts []map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &hosts); err != nil {
		t.Fatal(err)
	}
	if len(hosts) != 0 {
		t.Fatalf("expected 0 hosts, got %d", len(hosts))
	}

	// With a worker and all=true
	_, _ = ws.Create(context.Background(), workers.CreateReq{
		Name: "w-test", Host: "127.0.0.1", Port: 22, Username: "root",
	})
	req2 := httptest.NewRequest("GET", "/api/v1/storage/nfs-hosts?all=true", nil)
	req2.Header.Set("Authorization", authHeader(t, tk))
	w2 := httptest.NewRecorder()
	r.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w2.Code, w2.Body.String())
	}
	var hosts2 []map[string]any
	if err := json.Unmarshal(w2.Body.Bytes(), &hosts2); err != nil {
		t.Fatal(err)
	}
	if len(hosts2) != 1 {
		t.Fatalf("expected 1 host with all=true, got %d", len(hosts2))
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

// TestStorageEndpointsRequireAuth verifies the storage endpoints are behind
// BearerMiddleware (authed group): no Authorization header -> 401.
func TestStorageEndpointsRequireAuth(t *testing.T) {
	r, _, _, _ := newRouter(t)
	endpoints := []struct {
		method, path string
	}{
		{"POST", "/api/v1/storage/provision"},
		{"POST", "/api/v1/storage/reclaim"},
		{"GET", "/api/v1/storage"},
		{"GET", "/api/v1/storage/inventory"},
		{"POST", "/api/v1/storage/vg"},
		{"POST", "/api/v1/storage/lv/resize"},
		{"POST", "/api/v1/storage/lv/delete"},
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
