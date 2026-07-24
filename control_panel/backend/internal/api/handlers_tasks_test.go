package api

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"testing"
	"time"

	"xirang/control_panel/internal/workers"
)

func TestGetTaskByID(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	id, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), id, "x")
	time.Sleep(100 * time.Millisecond)
	req := httptest.NewRequest("GET", "/api/v1/tasks/"+strconv.Itoa(int(taskID)), nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var resp map[string]any
	json.Unmarshal(w.Body.Bytes(), &resp)
	if resp["id"] == nil {
		t.Fatal("no id in response")
	}
}

func TestListTasks(t *testing.T) {
	r, _, _, tk := newRouter(t)
	req := httptest.NewRequest("GET", "/api/v1/tasks", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d", w.Code)
	}
}
