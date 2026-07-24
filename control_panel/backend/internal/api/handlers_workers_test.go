package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

func newRouter(t *testing.T) (*gin.Engine, *workers.Service, *db.Store, *auth.Tokens) {
	t.Helper()
	gin.SetMode(gin.TestMode)
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	t.Cleanup(func() { s.Close() })
	c, _ := crypto.New(make([]byte, 32))
	sshm := ssh.NewManager(c, 2, time.Minute)
	eng := tasks.NewEngine(s)
	ws := workers.NewService(s, c, sshm, eng)
	tk := auth.NewTokens("secret", time.Hour)
	return NewRouter(tk, ws, s, eng), ws, s, tk
}

func authHeader(t *testing.T, tk *auth.Tokens) string {
	tok, _ := tk.Issue(1, "admin")
	return "Bearer " + tok
}

func TestCreateWorkerViaAPI(t *testing.T) {
	r, _, store, tk := newRouter(t)
	body, _ := json.Marshal(map[string]any{"name": "w1", "host": "10.0.0.1", "port": 22, "username": "root"})
	req := httptest.NewRequest("POST", "/api/v1/workers", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusCreated {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	all, _ := store.ListWorkers(context.Background())
	if len(all) != 1 {
		t.Fatalf("workers=%d", len(all))
	}
}

func TestCreateWorkerUnauthorized(t *testing.T) {
	r, _, _, _ := newRouter(t)
	req := httptest.NewRequest("POST", "/api/v1/workers", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("code=%d", w.Code)
	}
}

func TestSetPanelPasswordViaAPI(t *testing.T) {
	r, ws, store, tk := newRouter(t)
	id, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	body, _ := json.Marshal(map[string]any{"password": "pw"})
	req := httptest.NewRequest("POST", "/api/v1/workers/"+strconv.Itoa(int(id))+"/credentials/password", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	got, _ := store.GetWorker(context.Background(), id)
	if got.EncPassword == nil {
		t.Fatal("password not set")
	}
}

// TestGetWorkerNoCredentials verifies I1: the workers API must not return
// encrypted credential ciphertext (enc_password, enc_private_key). These
// fields have json:"-" so even though they're in the DB row, they never
// appear in the HTTP response.
func TestGetWorkerNoCredentials(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	id, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	ws.SetPanelPassword(context.Background(), id, "secret-pw")
	ws.SetPrivateKey(context.Background(), id, "-----BEGIN RSA PRIVATE KEY-----\nx\n-----END RSA PRIVATE KEY-----")

	req := httptest.NewRequest("GET", "/api/v1/workers/"+strconv.Itoa(int(id)), nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	body := w.Body.String()
	if strings.Contains(body, "enc_password") {
		t.Fatalf("API response leaks enc_password: %s", body)
	}
	if strings.Contains(body, "enc_private_key") {
		t.Fatalf("API response leaks enc_private_key: %s", body)
	}
	if strings.Contains(body, "secret-pw") {
		t.Fatalf("API response leaks password value: %s", body)
	}
}

// TestListWorkersNoCredentials verifies I1 on the list endpoint.
func TestListWorkersNoCredentials(t *testing.T) {
	r, ws, _, tk := newRouter(t)
	id, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	ws.SetPanelPassword(context.Background(), id, "secret-pw")

	req := httptest.NewRequest("GET", "/api/v1/workers", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	body := w.Body.String()
	if strings.Contains(body, "enc_password") {
		t.Fatalf("API response leaks enc_password: %s", body)
	}
	if strings.Contains(body, "enc_private_key") {
		t.Fatalf("API response leaks enc_private_key: %s", body)
	}
}
