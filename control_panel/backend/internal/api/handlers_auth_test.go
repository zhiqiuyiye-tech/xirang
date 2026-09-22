package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

func setupAuthTestEnv(t *testing.T) (*db.Store, *auth.Tokens, *auth.RateLimiter, *gin.Engine) {
	t.Helper()
	gin.SetMode(gin.TestMode)

	store, err := db.Open(filepath.Join(t.TempDir(), "auth_test.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })

	// Seed admin with password "correct-horse-battery-staple"
	hash, err := auth.HashPassword("correct-horse-battery-staple")
	if err != nil {
		t.Fatal(err)
	}
	if err := store.UpsertAdminPassword(context.Background(), "admin", hash); err != nil {
		t.Fatal(err)
	}

	tk := auth.NewTokens("test-jwt-secret-key-32bytes-long", time.Hour)
	limiter := auth.NewRateLimiter(3, 100*time.Millisecond, 200*time.Millisecond)
	t.Cleanup(func() { limiter.Close() })

	authH := newAuthHandlers(AuthHandlerConfig{
		Store:          store,
		Tokens:         tk,
		Limiter:        limiter,
		CookieName:     "cp_session",
		CookieSecure:   false,
		CookieSameSite: "Lax",
		CSRFCookieName: "cp_csrf",
		TokenTTL:       time.Hour,
	})

	r := gin.New()
	r.POST("/api/v1/auth/login", authH.login)

	authed := r.Group("/api/v1")
	authed.Use(auth.AuthMiddleware(auth.MiddlewareConfig{
		Tokens:       tk,
		VersionStore: store,
		CookieName:   "cp_session",
	}))
	{
		authed.GET("/auth/me", authH.me)
		authed.PUT("/auth/password", authH.changePassword)
		authed.POST("/auth/logout", authH.logout)
	}

	return store, tk, limiter, r
}

func TestAuth_LoginSuccess(t *testing.T) {
	store, _, _, r := setupAuthTestEnv(t)

	body, _ := json.Marshal(map[string]string{
		"username": "admin",
		"password": "correct-horse-battery-staple",
	})
	req := httptest.NewRequest("POST", "/api/v1/auth/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Fatalf("expected 200, got %d: %s", w.Code, w.Body.String())
	}

	var res map[string]string
	if err := json.Unmarshal(w.Body.Bytes(), &res); err != nil {
		t.Fatal(err)
	}
	if res["token"] == "" {
		t.Fatal("expected token in response")
	}
	if res["csrf_token"] == "" {
		t.Fatal("expected csrf_token in response")
	}

	// Verify session cookie was set
	cookies := w.Result().Cookies()
	var foundSession, foundCSRF bool
	for _, c := range cookies {
		if c.Name == "cp_session" {
			foundSession = true
			if !c.HttpOnly {
				t.Fatal("session cookie must be HttpOnly")
			}
		}
		if c.Name == "cp_csrf" {
			foundCSRF = true
			if c.HttpOnly {
				t.Fatal("csrf cookie must not be HttpOnly so script can read it")
			}
		}
	}
	if !foundSession || !foundCSRF {
		t.Fatalf("missing cookies: foundSession=%v, foundCSRF=%v", foundSession, foundCSRF)
	}

	// Verify audit log
	audits, err := store.ListAudit(context.Background(), 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(audits) == 0 || audits[0].Action != "auth.login" || audits[0].Result != "success" {
		t.Fatalf("unexpected audit log: %+v", audits)
	}
}

func TestAuth_LoginInvalidAndRateLimiting(t *testing.T) {
	_, _, _, r := setupAuthTestEnv(t)

	body, _ := json.Marshal(map[string]string{
		"username": "admin",
		"password": "wrong-password",
	})

	// Failures 1 and 2: 401 Unauthorized
	for i := 1; i <= 2; i++ {
		req := httptest.NewRequest("POST", "/api/v1/auth/login", bytes.NewReader(body))
		req.Header.Set("Content-Type", "application/json")
		w := httptest.NewRecorder()
		r.ServeHTTP(w, req)
		if w.Code != http.StatusUnauthorized {
			t.Fatalf("attempt %d: expected 401, got %d", i, w.Code)
		}
	}

	// Failure 3: reaches maxFailures (3) -> returns 429
	req := httptest.NewRequest("POST", "/api/v1/auth/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusTooManyRequests {
		t.Fatalf("attempt 3: expected 429, got %d", w.Code)
	}

	// Attempt 4 while locked -> 429 with Retry-After header
	req = httptest.NewRequest("POST", "/api/v1/auth/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w = httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusTooManyRequests {
		t.Fatalf("attempt 4: expected 429, got %d", w.Code)
	}
	if w.Header().Get("Retry-After") == "" {
		t.Fatal("expected Retry-After header on 429 response")
	}

	// Wait for lockout to pass
	time.Sleep(120 * time.Millisecond)

	// Valid login should now work and reset failures
	goodBody, _ := json.Marshal(map[string]string{
		"username": "admin",
		"password": "correct-horse-battery-staple",
	})
	req = httptest.NewRequest("POST", "/api/v1/auth/login", bytes.NewReader(goodBody))
	req.Header.Set("Content-Type", "application/json")
	w = httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("expected 200 after lockout expiration, got %d", w.Code)
	}
}

func TestAuth_ChangePasswordAndSessionRevocation(t *testing.T) {
	_, tk, _, r := setupAuthTestEnv(t)

	// Issue token for admin at auth_version 1
	tokV1, err := tk.Issue(1, "admin", 1)
	if err != nil {
		t.Fatal(err)
	}

	// 1. Check GET /auth/me with tokV1 -> 200, auth_version 1
	reqMe := httptest.NewRequest("GET", "/api/v1/auth/me", nil)
	reqMe.Header.Set("Authorization", "Bearer "+tokV1)
	wMe := httptest.NewRecorder()
	r.ServeHTTP(wMe, reqMe)
	if wMe.Code != http.StatusOK {
		t.Fatalf("expected 200 from /auth/me, got %d", wMe.Code)
	}

	// 2. Change password with too short password (< 12 chars) -> 400
	shortBody, _ := json.Marshal(map[string]string{
		"old_password": "correct-horse-battery-staple",
		"new_password": "short",
	})
	reqShort := httptest.NewRequest("PUT", "/api/v1/auth/password", bytes.NewReader(shortBody))
	reqShort.Header.Set("Authorization", "Bearer "+tokV1)
	reqShort.Header.Set("Content-Type", "application/json")
	wShort := httptest.NewRecorder()
	r.ServeHTTP(wShort, reqShort)
	if wShort.Code != http.StatusBadRequest {
		t.Fatalf("expected 400 for short password, got %d", wShort.Code)
	}

	// 3. Change password with wrong old password -> 401
	wrongOldBody, _ := json.Marshal(map[string]string{
		"old_password": "wrong-old-password",
		"new_password": "new-strong-password-1234",
	})
	reqWrongOld := httptest.NewRequest("PUT", "/api/v1/auth/password", bytes.NewReader(wrongOldBody))
	reqWrongOld.Header.Set("Authorization", "Bearer "+tokV1)
	reqWrongOld.Header.Set("Content-Type", "application/json")
	wWrongOld := httptest.NewRecorder()
	r.ServeHTTP(wWrongOld, reqWrongOld)
	if wWrongOld.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401 for wrong old password, got %d", wWrongOld.Code)
	}

	// 4. Change password successfully -> 200, returns new token
	changeBody, _ := json.Marshal(map[string]string{
		"old_password": "correct-horse-battery-staple",
		"new_password": "new-strong-password-1234",
	})
	reqChange := httptest.NewRequest("PUT", "/api/v1/auth/password", bytes.NewReader(changeBody))
	reqChange.Header.Set("Authorization", "Bearer "+tokV1)
	reqChange.Header.Set("Content-Type", "application/json")
	wChange := httptest.NewRecorder()
	r.ServeHTTP(wChange, reqChange)
	if wChange.Code != http.StatusOK {
		t.Fatalf("expected 200 for change password, got %d: %s", wChange.Code, wChange.Body.String())
	}

	var changeRes map[string]string
	_ = json.Unmarshal(wChange.Body.Bytes(), &changeRes)
	newTok := changeRes["token"]
	if newTok == "" || newTok == tokV1 {
		t.Fatalf("expected new distinct token, got %q", newTok)
	}

	// 5. Old token (tokV1) must now be rejected with 401 because auth_version was bumped!
	reqOldMe := httptest.NewRequest("GET", "/api/v1/auth/me", nil)
	reqOldMe.Header.Set("Authorization", "Bearer "+tokV1)
	wOldMe := httptest.NewRecorder()
	r.ServeHTTP(wOldMe, reqOldMe)
	if wOldMe.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401 for old token after password change, got %d", wOldMe.Code)
	}

	// 6. New token works and reflects auth_version 2
	reqNewMe := httptest.NewRequest("GET", "/api/v1/auth/me", nil)
	reqNewMe.Header.Set("Authorization", "Bearer "+newTok)
	wNewMe := httptest.NewRecorder()
	r.ServeHTTP(wNewMe, reqNewMe)
	if wNewMe.Code != http.StatusOK {
		t.Fatalf("expected 200 for new token, got %d", wNewMe.Code)
	}
	var meRes map[string]any
	_ = json.Unmarshal(wNewMe.Body.Bytes(), &meRes)
	if meRes["auth_version"] != float64(2) {
		t.Fatalf("expected auth_version 2, got %v", meRes["auth_version"])
	}
}

func TestAuth_LogoutRevokesSessions(t *testing.T) {
	_, tk, _, r := setupAuthTestEnv(t)

	tok, _ := tk.Issue(1, "admin", 1)

	// Call logout
	reqLogout := httptest.NewRequest("POST", "/api/v1/auth/logout", nil)
	reqLogout.Header.Set("Authorization", "Bearer "+tok)
	wLogout := httptest.NewRecorder()
	r.ServeHTTP(wLogout, reqLogout)
	if wLogout.Code != http.StatusOK {
		t.Fatalf("expected 200 from logout, got %d", wLogout.Code)
	}

	// Subsequent request with tok must be rejected with 401
	reqMe := httptest.NewRequest("GET", "/api/v1/auth/me", nil)
	reqMe.Header.Set("Authorization", "Bearer "+tok)
	wMe := httptest.NewRecorder()
	r.ServeHTTP(wMe, reqMe)
	if wMe.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401 after logout, got %d", wMe.Code)
	}
}
