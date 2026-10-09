package api

import (
	"bytes"
	"context"
	"encoding/json"
	"math"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/workers"
)

func TestStorageIDsRejectFractionalOrOverflowedNumbers(t *testing.T) {
	for _, value := range []float64{1.5, -1, math.NaN(), math.Inf(1), float64(1 << 63)} {
		if _, err := parseWorkerID(value); err == nil {
			t.Fatalf("accepted noninteger/out-of-range ID %v", value)
		}
	}
	for _, value := range []any{float64(1), int64(1), "1"} {
		if id, err := parseWorkerID(value); err != nil || id != 1 {
			t.Fatalf("valid id=%v err=%v", id, err)
		}
	}
	if id, err := parseWorkerID(strconv.FormatInt(1<<63-1, 10)); err != nil || id != 1<<63-1 {
		t.Fatalf("valid decimal string ID rejected: %v %v", id, err)
	}
}

func TestReclaimByProvisionTaskUsesActualWorkerLock(t *testing.T) {
	r, ws, store, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "real-worker", Host: "127.0.0.1", Port: 22, Username: "root"})
	params, _ := json.Marshal(map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "mount_point": "/data02/share"})
	provisionID, err := store.CreateTask(context.Background(), db.Task{Type: "storage_provision_nfs", TargetKind: "storage", TargetID: wid, Status: "succeeded", ParamsJSON: string(params)})
	if err != nil {
		t.Fatal(err)
	}
	body, _ := json.Marshal(map[string]any{"task_id": provisionID, "worker_id": wid + 10})
	req := httptest.NewRequest("POST", "/api/v1/storage/reclaim", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	response := httptest.NewRecorder()
	r.ServeHTTP(response, req)
	if response.Code != http.StatusAccepted {
		t.Fatalf("code=%d %s", response.Code, response.Body.String())
	}
	var result struct {
		TaskID int64 `json:"task_id"`
	}
	if err := json.Unmarshal(response.Body.Bytes(), &result); err != nil {
		t.Fatal(err)
	}
	task, err := store.GetTask(context.Background(), result.TaskID)
	if err != nil {
		t.Fatal(err)
	}
	if task.TargetID != wid {
		t.Fatalf("locked worker %d instead of actual %d", task.TargetID, wid)
	}
	var actual struct {
		WorkerID int64 `json:"worker_id"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &actual); err != nil {
		t.Fatal(err)
	}
	if actual.WorkerID != wid {
		t.Fatalf("params worker=%d want %d", actual.WorkerID, wid)
	}
}

func TestReclaimRejectsMissingProvisionTaskBeforeSubmission(t *testing.T) {
	r, _, _, tk := newRouter(t)
	req := httptest.NewRequest("POST", "/api/v1/storage/reclaim", bytes.NewBufferString(`{"task_id":999999}`))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	response := httptest.NewRecorder()
	r.ServeHTTP(response, req)
	if response.Code != http.StatusBadRequest {
		t.Fatalf("code=%d %s", response.Code, response.Body.String())
	}
}
