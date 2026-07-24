package auth

import (
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
)

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

// TestBearerMiddleware_LowercaseScheme locks in I2: the Bearer scheme is
// case-insensitive per RFC 7235. A lowercase "bearer <jwt>" header must be
// accepted, matching the stream handler's behavior.
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

// TestBearerMiddleware_MixedCaseScheme verifies that mixed-case "BeArEr" is
// also accepted (full RFC 7235 compliance).
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
