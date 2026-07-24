package api

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

// TestStaticIndexServed verifies GET / serves the embedded index.html with
// the correct content type and a valid HTML body.
func TestStaticIndexServed(t *testing.T) {
	r, _, _, _ := newRouter(t)
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("GET / code=%d, want 200", w.Code)
	}
	if ct := w.Header().Get("Content-Type"); !strings.HasPrefix(ct, "text/html") {
		t.Fatalf("Content-Type=%q, want text/html", ct)
	}
	if !strings.Contains(w.Body.String(), "<html") {
		t.Fatalf("body does not contain <html: %s", w.Body.String()[:200])
	}
}

// TestStaticJSAsset verifies GET /static/app.js serves the embedded JS asset.
func TestStaticJSAsset(t *testing.T) {
	r, _, _, _ := newRouter(t)
	req := httptest.NewRequest("GET", "/static/app.js", nil)
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("GET /static/app.js code=%d, want 200", w.Code)
	}
	if !strings.Contains(w.Body.String(), "Control Panel") {
		t.Fatalf("body does not contain expected JS content")
	}
}
