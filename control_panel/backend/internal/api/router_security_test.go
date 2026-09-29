package api

import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
)

func TestConfigureTrustedProxiesUsesRemoteAddrByDefault(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	if err := configureTrustedProxies(r, nil); err != nil {
		t.Fatalf("configureTrustedProxies(nil) error = %v", err)
	}
	r.GET("/client-ip", func(c *gin.Context) { c.String(http.StatusOK, c.ClientIP()) })

	req := httptest.NewRequest(http.MethodGet, "/client-ip", nil)
	req.RemoteAddr = "192.0.2.10:1234"
	req.Header.Set("X-Forwarded-For", "203.0.113.77")
	response := httptest.NewRecorder()
	r.ServeHTTP(response, req)
	if response.Body.String() != "192.0.2.10" {
		t.Fatalf("client IP = %q, want RemoteAddr 192.0.2.10", response.Body.String())
	}
}

func TestConfigureTrustedProxiesAcceptsForwardedIPOnlyFromConfiguredCIDR(t *testing.T) {
	gin.SetMode(gin.TestMode)
	r := gin.New()
	if err := configureTrustedProxies(r, []string{"10.0.0.0/8"}); err != nil {
		t.Fatalf("configureTrustedProxies() error = %v", err)
	}
	r.GET("/client-ip", func(c *gin.Context) { c.String(http.StatusOK, c.ClientIP()) })

	req := httptest.NewRequest(http.MethodGet, "/client-ip", nil)
	req.RemoteAddr = "10.1.2.3:8080"
	req.Header.Set("X-Forwarded-For", "192.0.2.20")
	response := httptest.NewRecorder()
	r.ServeHTTP(response, req)
	if response.Body.String() != "192.0.2.20" {
		t.Fatalf("client IP = %q, want trusted proxy's forwarded IP", response.Body.String())
	}
}

func TestStaticKeyLoginHasStrictCSPAndNoStore(t *testing.T) {
	router, _, _, _ := newRouter(t)
	pageRequest := httptest.NewRequest(http.MethodGet, "/", nil)
	pageResponse := httptest.NewRecorder()
	router.ServeHTTP(pageResponse, pageRequest)
	if pageResponse.Code != http.StatusOK {
		t.Fatalf("GET / status=%d", pageResponse.Code)
	}
	page := pageResponse.Body.String()
	p256Script := strings.Index(page, "/static/p256.bundle.js")
	keyLoginScript := strings.Index(page, "/static/key_login.js")
	appScript := strings.Index(page, "/static/app.js")
	if p256Script < 0 || keyLoginScript <= p256Script || appScript <= keyLoginScript {
		t.Fatal("P-256 bundle and key login controller must load locally before the app script")
	}
	if strings.Contains(page, "onsubmit=") || strings.Contains(page, "javascript:") || strings.Contains(page, "login-password") {
		t.Fatal("legacy password form or inline script hook remains in login HTML")
	}
	if pageResponse.Header().Get("Cache-Control") != "no-store" {
		t.Fatal("login HTML must be no-store")
	}
	csp := pageResponse.Header().Get("Content-Security-Policy")
	for _, required := range []string{"script-src 'self'", "object-src 'none'", "base-uri 'none'", "frame-ancestors 'none'", "form-action 'self'"} {
		if !strings.Contains(csp, required) {
			t.Fatalf("CSP missing %q: %s", required, csp)
		}
	}
	if strings.Contains(csp, "unsafe-eval") || strings.Contains(csp, "script-src 'self' 'unsafe-inline'") {
		t.Fatalf("CSP allows inline/eval script: %s", csp)
	}
	if pageResponse.Header().Get("Referrer-Policy") != "no-referrer" {
		t.Fatal("Referrer-Policy must be no-referrer")
	}

	for _, asset := range []string{"/static/p256.bundle.js", "/static/key_login.js"} {
		assetRequest := httptest.NewRequest(http.MethodGet, asset, nil)
		assetResponse := httptest.NewRecorder()
		router.ServeHTTP(assetResponse, assetRequest)
		if assetResponse.Code != http.StatusOK || assetResponse.Header().Get("Cache-Control") != "no-store" {
			t.Fatalf("asset %s status=%d cache-control=%q", asset, assetResponse.Code, assetResponse.Header().Get("Cache-Control"))
		}
	}
}
