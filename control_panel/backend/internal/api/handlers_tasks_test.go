package api

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strconv"
	"strings"
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

// TestStreamTokenQueryFallback verifies the ?token= query fallback is
// reachable: an EventSource client (no Authorization header) passing a valid
// JWT as ?token= gets a 200 text/event-stream response with at least the
// initial "task" SSE frame. The stream route is on the public group precisely
// so this fallback is not pre-empted by BearerMiddleware.
func TestStreamTokenQueryFallback(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")
	time.Sleep(100 * time.Millisecond)

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream?token=" + tok
	// Bound the request so the looping SSE handler exits when the context
	// times out (it emits the initial "task" frame before entering the loop).
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", url, nil).WithContext(ctx)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	if ct := w.Header().Get("Content-Type"); !strings.Contains(ct, "text/event-stream") {
		t.Fatalf("content-type=%q, want text/event-stream", ct)
	}
	if !strings.Contains(w.Body.String(), "event:task") {
		t.Fatalf("body missing initial event:task frame: %s", w.Body.String())
	}
}

// TestStreamTokenQueryBogus verifies that a bogus ?token= (with no
// Authorization header) is rejected with 401.
func TestStreamTokenQueryBogus(t *testing.T) {
	r, ws, _, _ := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")

	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream?token=bogus"
	req := httptest.NewRequest("GET", url, nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusUnauthorized {
		t.Fatalf("code=%d, want 401", w.Code)
	}
}
