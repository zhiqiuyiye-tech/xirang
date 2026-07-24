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
