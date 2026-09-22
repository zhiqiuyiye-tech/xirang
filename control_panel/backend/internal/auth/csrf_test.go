package auth

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestCSRFMiddleware(t *testing.T) {
	gin.SetMode(gin.TestMode)

	setupRouter := func(authType string) *gin.Engine {
		r := gin.New()
		r.Use(func(c *gin.Context) {
			c.Set(authTypeKey, authType)
			c.Next()
		})
		r.Use(CSRFMiddleware(CSRFConfig{
			CookieName: "cp_csrf",
			HeaderName: "X-CSRF-Token",
		}))
		r.POST("/write", func(c *gin.Context) {
			c.JSON(200, gin.H{"ok": true})
		})
		r.GET("/read", func(c *gin.Context) {
			c.JSON(200, gin.H{"ok": true})
		})
		return r
	}

	// 1. Bearer auth skips CSRF check
	rBearer := setupRouter(AuthTypeBearer)
	w1 := httptest.NewRecorder()
	req1 := httptest.NewRequest("POST", "/write", nil)
	rBearer.ServeHTTP(w1, req1)
	if w1.Code != http.StatusOK {
		t.Fatalf("bearer auth should skip CSRF, got %d", w1.Code)
	}

	// 2. Cookie auth GET (safe method) passes without CSRF header
	rCookie := setupRouter(AuthTypeCookie)
	w2 := httptest.NewRecorder()
	req2 := httptest.NewRequest("GET", "/read", nil)
	rCookie.ServeHTTP(w2, req2)
	if w2.Code != http.StatusOK {
		t.Fatalf("GET should not require CSRF, got %d", w2.Code)
	}

	// 3. Cookie auth POST without CSRF header -> 403
	w3 := httptest.NewRecorder()
	req3 := httptest.NewRequest("POST", "/write", nil)
	req3.AddCookie(&http.Cookie{Name: "cp_csrf", Value: "token-123"})
	rCookie.ServeHTTP(w3, req3)
	if w3.Code != http.StatusForbidden {
		t.Fatalf("expected 403 for missing CSRF header, got %d", w3.Code)
	}

	// 4. Cookie auth POST with matching CSRF cookie and header -> 200
	w4 := httptest.NewRecorder()
	req4 := httptest.NewRequest("POST", "/write", nil)
	req4.Host = "localhost:8080"
	req4.Header.Set("Origin", "http://localhost:8080")
	req4.Header.Set("X-CSRF-Token", "token-123")
	req4.AddCookie(&http.Cookie{Name: "cp_csrf", Value: "token-123"})
	rCookie.ServeHTTP(w4, req4)
	if w4.Code != http.StatusOK {
		t.Fatalf("expected 200 with valid CSRF token, got %d: %s", w4.Code, w4.Body.String())
	}

	// 5. Cookie auth POST with mismatched Origin -> 403
	w5 := httptest.NewRecorder()
	req5 := httptest.NewRequest("POST", "/write", nil)
	req5.Host = "localhost:8080"
	req5.Header.Set("Origin", "http://attacker.com")
	req5.Header.Set("X-CSRF-Token", "token-123")
	req5.AddCookie(&http.Cookie{Name: "cp_csrf", Value: "token-123"})
	rCookie.ServeHTTP(w5, req5)
	if w5.Code != http.StatusForbidden {
		t.Fatalf("expected 403 for cross-origin Origin, got %d", w5.Code)
	}
}
