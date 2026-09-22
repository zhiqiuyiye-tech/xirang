package api

import (
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"
	"time"

	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

func TestHealthLiveAndReady(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "health.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()

	tk := auth.NewTokens("secret", time.Hour)
	eng := tasks.NewEngine(store)
	sshm := ssh.NewManager(nil, 1, time.Minute)
	ws := workers.NewService(store, nil, sshm, eng)

	r := NewRouter(tk, ws, store, eng, nil, sshm)

	// 1. Live probe
	reqLive := httptest.NewRequest("GET", "/health/live", nil)
	wLive := httptest.NewRecorder()
	r.ServeHTTP(wLive, reqLive)
	if wLive.Code != http.StatusOK {
		t.Fatalf("live probe code = %d, want 200", wLive.Code)
	}

	// 2. Ready probe without k8s required
	reqReady := httptest.NewRequest("GET", "/health/ready", nil)
	wReady := httptest.NewRecorder()
	r.ServeHTTP(wReady, reqReady)
	if wReady.Code != http.StatusOK {
		t.Fatalf("ready probe code = %d, want 200", wReady.Code)
	}

	// 3. Ready probe with requireK8s = true and nil client -> 503
	rStrict := NewRouter(tk, ws, store, eng, nil, sshm, WithRequireK8s(true))
	wStrict := httptest.NewRecorder()
	rStrict.ServeHTTP(wStrict, reqReady)
	if wStrict.Code != http.StatusServiceUnavailable {
		t.Fatalf("strict ready probe code = %d, want 503", wStrict.Code)
	}

	// 4. Security headers verification
	if wLive.Header().Get("X-Content-Type-Options") != "nosniff" {
		t.Fatal("missing X-Content-Type-Options header")
	}
	if wLive.Header().Get("X-Frame-Options") != "DENY" {
		t.Fatal("missing X-Frame-Options header")
	}
	if wLive.Header().Get("Content-Security-Policy") == "" {
		t.Fatal("missing Content-Security-Policy header")
	}
}
