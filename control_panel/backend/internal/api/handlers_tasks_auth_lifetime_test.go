package api

import (
	"context"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func runAuthBoundedSSE(t *testing.T, store *db.Store, tokenTTL time.Duration, revoke bool) (int, string, time.Duration) {
	t.Helper()
	ctx := context.Background()
	taskID, err := store.CreateTask(ctx, db.Task{Type: "pending-test", TargetKind: "worker", TargetID: 1, Status: "running", ParamsJSON: "{}"})
	if err != nil {
		t.Fatal(err)
	}
	tokens := auth.NewTokens("test-jwt-secret-key-32bytes-long", tokenTTL)
	admin, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	token, err := tokens.Issue(admin.ID, admin.Username, admin.AuthVersion)
	if err != nil {
		t.Fatal(err)
	}
	handler := &taskHandlers{
		store:               store,
		eng:                 tasks.NewEngine(store),
		tk:                  tokens,
		cookieName:          "cp_session",
		authRecheckInterval: 10 * time.Millisecond,
	}
	router := gin.New()
	router.GET("/tasks/:id/stream", handler.stream)
	requestCtx, cancel := context.WithCancel(context.Background())
	request := httptest.NewRequest(http.MethodGet, "/tasks/"+strconv.FormatInt(taskID, 10)+"/stream", nil).WithContext(requestCtx)
	request.AddCookie(&http.Cookie{Name: "cp_session", Value: token})
	response := httptest.NewRecorder()
	done := make(chan struct{})
	started := time.Now()
	go func() {
		router.ServeHTTP(response, request)
		close(done)
	}()
	time.Sleep(35 * time.Millisecond)
	if revoke {
		if _, err := store.RevokeAdminSessions(ctx, admin.Username); err != nil {
			cancel()
			<-done
			t.Fatal(err)
		}
	}
	timeout := 500 * time.Millisecond
	if !revoke {
		timeout += tokenTTL
	}
	select {
	case <-done:
		cancel()
		return response.Code, response.Body.String(), time.Since(started)
	case <-time.After(timeout):
		cancel()
		<-done
		t.Fatal("SSE stayed open after auth version revocation or JWT expiry")
		return 0, "", 0
	}
}

func TestSSEClosesWithinRecheckIntervalAfterGlobalRevocation(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "sse-revoke.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	code, body, elapsed := runAuthBoundedSSE(t, store, time.Minute, true)
	if code != http.StatusOK || !strings.Contains(body, "event:task") {
		t.Fatalf("SSE response code=%d body=%q", code, body)
	}
	if elapsed > 100*time.Millisecond {
		t.Fatalf("SSE revocation latency=%v, want at most 100ms with 10ms test ticker", elapsed)
	}
}

func TestSSEClosesWhenJWTExpiresDuringStream(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "sse-expire.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	code, body, elapsed := runAuthBoundedSSE(t, store, 2*time.Second, false)
	if code != http.StatusOK || !strings.Contains(body, "event:task") {
		t.Fatalf("SSE response code=%d body=%q", code, body)
	}
	if elapsed > 2500*time.Millisecond {
		t.Fatalf("SSE expiry latency=%v, want at most 2.5s with 10ms test ticker", elapsed)
	}
}
