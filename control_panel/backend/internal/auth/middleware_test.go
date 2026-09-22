package auth

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
)

type mockVersionStore struct {
	versions map[int64]int64
}

func (m *mockVersionStore) GetAdminAuthVersion(ctx context.Context, id int64) (int64, error) {
	if v, ok := m.versions[id]; ok {
		return v, nil
	}
	return 1, nil
}

func TestBearerMiddleware_OK(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	tok, _ := tk.Issue(3, "admin")
	r := gin.New()
	r.Use(BearerMiddleware(tk))
	r.GET("/x", func(c *gin.Context) {
		cl, ok := ClaimsFrom(c)
		if !ok {
			c.Status(500)
			return
		}
		c.JSON(200, gin.H{"id": cl.AdminID})
	})
	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/x", nil)
	req.Header.Set("Authorization", "Bearer "+tok)
	r.ServeHTTP(w, req)
	if w.Code != 200 {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
}

func TestBearerMiddleware_Missing(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	r := gin.New()
	r.Use(BearerMiddleware(tk))
	r.GET("/x", func(c *gin.Context) { c.Status(200) })
	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/x", nil)
	r.ServeHTTP(w, req)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("code=%d", w.Code)
	}
}

func TestBearerMiddleware_BadToken(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	r := gin.New()
	r.Use(BearerMiddleware(tk))
	r.GET("/x", func(c *gin.Context) { c.Status(200) })
	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/x", nil)
	req.Header.Set("Authorization", "Bearer not-a-token")
	r.ServeHTTP(w, req)
	if w.Code != http.StatusUnauthorized {
		t.Fatalf("code=%d", w.Code)
	}
}

func TestBearerMiddleware_LowercaseScheme(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	tok, _ := tk.Issue(5, "admin")
	r := gin.New()
	r.Use(BearerMiddleware(tk))
	r.GET("/x", func(c *gin.Context) {
		cl, ok := ClaimsFrom(c)
		if !ok {
			c.Status(500)
			return
		}
		c.JSON(200, gin.H{"id": cl.AdminID})
	})
	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/x", nil)
	req.Header.Set("Authorization", "bearer "+tok)
	r.ServeHTTP(w, req)
	if w.Code != 200 {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
}

func TestBearerMiddleware_MixedCaseScheme(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	tok, _ := tk.Issue(6, "admin")
	r := gin.New()
	r.Use(BearerMiddleware(tk))
	r.GET("/x", func(c *gin.Context) { c.JSON(200, gin.H{"ok": true}) })
	w := httptest.NewRecorder()
	req := httptest.NewRequest("GET", "/x", nil)
	req.Header.Set("Authorization", "BeArEr "+tok)
	r.ServeHTTP(w, req)
	if w.Code != 200 {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
}

func TestAuthMiddleware_CookieAndAuthVersion(t *testing.T) {
	gin.SetMode(gin.TestMode)
	tk := NewTokens("s", time.Hour)
	vs := &mockVersionStore{
		versions: map[int64]int64{
			1: 2, // Admin 1 is at auth_version 2 in DB
		},
	}

	r := gin.New()
	r.Use(AuthMiddleware(MiddlewareConfig{
		Tokens:       tk,
		VersionStore: vs,
		CookieName:   "cp_session",
	}))
	r.GET("/test", func(c *gin.Context) {
		cl, _ := ClaimsFrom(c)
		authType, _ := AuthTypeFrom(c)
		c.JSON(200, gin.H{"user": cl.Username, "type": authType})
	})

	// 1. Token with version 1 (outdated/revoked session) -> 401
	oldTok, _ := tk.Issue(1, "admin", 1)
	w1 := httptest.NewRecorder()
	req1 := httptest.NewRequest("GET", "/test", nil)
	req1.Header.Set("Authorization", "Bearer "+oldTok)
	r.ServeHTTP(w1, req1)
	if w1.Code != http.StatusUnauthorized {
		t.Fatalf("expected 401 for outdated token version, got %d", w1.Code)
	}

	// 2. Token with version 2 via Cookie -> 200
	validTok, _ := tk.Issue(1, "admin", 2)
	w2 := httptest.NewRecorder()
	req2 := httptest.NewRequest("GET", "/test", nil)
	req2.AddCookie(&http.Cookie{Name: "cp_session", Value: validTok})
	r.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Fatalf("expected 200 for valid cookie token, got %d: %s", w2.Code, w2.Body.String())
	}

	// 3. Token with version 2 via Bearer -> 200
	w3 := httptest.NewRecorder()
	req3 := httptest.NewRequest("GET", "/test", nil)
	req3.Header.Set("Authorization", "Bearer "+validTok)
	r.ServeHTTP(w3, req3)
	if w3.Code != http.StatusOK {
		t.Fatalf("expected 200 for valid bearer token, got %d: %s", w3.Code, w3.Body.String())
	}
}
