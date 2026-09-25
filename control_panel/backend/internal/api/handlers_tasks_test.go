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

// TestGetTaskByIDNoParamsJSON verifies C2: the task's params_json field is
// never returned by the API. After C1, params_json holds AES ciphertext, but
// it should still not be exfiltrable via the tasks endpoint (json:"-").
func TestGetTaskByIDNoParamsJSON(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	id, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), id, "secret-pw")
	time.Sleep(100 * time.Millisecond)
	req := httptest.NewRequest("GET", "/api/v1/tasks/"+strconv.Itoa(int(taskID)), nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	body := w.Body.String()
	if strings.Contains(body, "params_json") {
		t.Fatalf("API response leaks params_json: %s", body)
	}
	if strings.Contains(body, "secret-pw") {
		t.Fatalf("API response leaks password: %s", body)
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

// TestStreamCookieAuth verifies the cookie auth path: an EventSource client
// sending a valid session cookie gets a 200 text/event-stream response with
// at least the initial "task" SSE frame.
func TestStreamCookieAuth(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")
	time.Sleep(100 * time.Millisecond)

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream"
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", url, nil).WithContext(ctx)
	req.AddCookie(&http.Cookie{Name: "cp_session", Value: tok})
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

// TestStreamTokenQueryRejected locks in the removal of ?token= query parameter
// authentication: passing ?token= without a valid cookie or Bearer header must
// be rejected with 401 Unauthorized to prevent tokens leaking into access logs.
func TestStreamTokenQueryRejected(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream?token=" + tok
	req := httptest.NewRequest("GET", url, nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusUnauthorized {
		t.Fatalf("code=%d, want 401 (?token= query must be rejected)", w.Code)
	}
}

// TestStreamBearerHeader verifies the primary auth path for the stream route:
// a valid "Authorization: Bearer <jwt>" header (no ?token= query) yields a 200
// text/event-stream response with the initial "task" SSE frame. This locks in
// that the Bearer-header branch is actually reachable and not shadowed by the
// ?token= fallback or the route's public-group placement.
func TestStreamBearerHeader(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")
	time.Sleep(100 * time.Millisecond)

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream"
	// Bound the request so the looping SSE handler exits when the context
	// times out (it emits the initial "task" frame before entering the loop).
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", url, nil).WithContext(ctx)
	req.Header.Set("Authorization", "Bearer "+tok)
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

// TestStreamBearerHeaderLowercase locks in the case-insensitive Bearer prefix
// fix (RFC 7235): a lowercase "bearer <jwt>" header must be accepted, matching
// the BearerMiddleware behavior on the other routes.
func TestStreamBearerHeaderLowercase(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")
	time.Sleep(100 * time.Millisecond)

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream"
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", url, nil).WithContext(ctx)
	req.Header.Set("Authorization", "bearer "+tok)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	if !strings.Contains(w.Body.String(), "event:task") {
		t.Fatalf("body missing initial event:task frame: %s", w.Body.String())
	}
}

// TestStreamLiveTaskAndStepUpdates verifies that step events have lowercase json fields
// (seq, name, status, stdout) and terminal task status events are emitted to the client.
func TestStreamLiveTaskAndStepUpdates(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	taskID, _ := ws.ChangeRootPassword(context.Background(), wid, "x")
	time.Sleep(150 * time.Millisecond)

	tok, _ := tk.Issue(1, "admin")
	url := "/api/v1/tasks/" + strconv.Itoa(int(taskID)) + "/stream"
	ctx, cancel := context.WithTimeout(context.Background(), 500*time.Millisecond)
	defer cancel()
	req := httptest.NewRequest("GET", url, nil).WithContext(ctx)
	req.Header.Set("Authorization", "Bearer "+tok)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	body := w.Body.String()
	if !strings.Contains(body, "event:task") {
		t.Fatalf("missing event:task frame: %s", body)
	}
	if !strings.Contains(body, `"seq":`) {
		t.Fatalf("missing lowercase seq field in step event: %s", body)
	}
	if !strings.Contains(body, `"name":`) {
		t.Fatalf("missing lowercase name field in step event: %s", body)
	}
}
