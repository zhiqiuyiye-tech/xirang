package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

type RouterOptions struct {
	RateLimiter    *auth.RateLimiter
	CookieName     string
	CookieSecure   bool
	CookieSameSite string
	CSRFCookieName string
	CSRFHeaderName string
	RequireK8s     bool
	TrustedProxies []string
}

type RouterOption func(*RouterOptions)

func WithRateLimiter(l *auth.RateLimiter) RouterOption {
	return func(o *RouterOptions) { o.RateLimiter = l }
}

func WithCookieName(name string) RouterOption {
	return func(o *RouterOptions) { o.CookieName = name }
}

func WithCookieSecure(secure bool) RouterOption {
	return func(o *RouterOptions) { o.CookieSecure = secure }
}

func WithCookieSameSite(sameSite string) RouterOption {
	return func(o *RouterOptions) { o.CookieSameSite = sameSite }
}

func WithCSRFCookieName(name string) RouterOption {
	return func(o *RouterOptions) { o.CSRFCookieName = name }
}

func WithCSRFHeaderName(name string) RouterOption {
	return func(o *RouterOptions) { o.CSRFHeaderName = name }
}

func WithRequireK8s(require bool) RouterOption {
	return func(o *RouterOptions) { o.RequireK8s = require }
}

func WithTrustedProxies(proxies []string) RouterOption {
	return func(o *RouterOptions) { o.TrustedProxies = proxies }
}

func securityHeadersMiddleware(isHTTPS bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("Referrer-Policy", "strict-origin-when-cross-origin")
		c.Header("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
		c.Header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'")
		if isHTTPS {
			c.Header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
		}
		c.Next()
	}
}

func liveHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"status": "alive"})
}

func readyHandler(store *db.Store, k8sClient kubernetes.Interface, requireK8s bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		if store != nil {
			if err := store.Ping(); err != nil {
				c.JSON(http.StatusServiceUnavailable, gin.H{
					"status": "not_ready",
					"error":  "db: " + err.Error(),
				})
				return
			}
		}
		if requireK8s && k8sClient == nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{
				"status": "not_ready",
				"error":  "k8s: client unavailable and REQUIRE_K8S=true",
			})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "ready"})
	}
}

// NewRouter wires every HTTP route for the control panel. k8sClient may be nil
// (non-cluster / local dev) - in that case the k8s endpoints return 503
// Service Unavailable instead of panicking.
func NewRouter(tk *auth.Tokens, ws *workers.Service, store *db.Store, eng *tasks.Engine, k8sClient kubernetes.Interface, sshRunner ssh.Runner, opts ...RouterOption) *gin.Engine {
	options := RouterOptions{
		CookieName:     "cp_session",
		CookieSecure:   false,
		CookieSameSite: "Lax",
		CSRFCookieName: "cp_csrf",
		CSRFHeaderName: "X-CSRF-Token",
	}
	for _, opt := range opts {
		opt(&options)
	}

	r := gin.New()
	r.Use(gin.Recovery())

	if len(options.TrustedProxies) > 0 {
		_ = r.SetTrustedProxies(options.TrustedProxies)
	}

	r.Use(securityHeadersMiddleware(options.CookieSecure))

	// Health probes
	r.GET("/health/live", liveHandler)
	r.GET("/health/ready", readyHandler(store, k8sClient, options.RequireK8s))

	api := r.Group("/api/v1")

	authH := newAuthHandlers(AuthHandlerConfig{
		Store:          store,
		Tokens:         tk,
		Limiter:        options.RateLimiter,
		CookieName:     options.CookieName,
		CookieSecure:   options.CookieSecure,
		CookieSameSite: options.CookieSameSite,
		CSRFCookieName: options.CSRFCookieName,
		TokenTTL:       tk.TTL(),
	})

	api.POST("/auth/login", authH.login)

	// SSE task stream (authenticated via session cookie or Bearer header)
	th := &taskHandlers{store: store, eng: eng, tk: tk, cookieName: options.CookieName}
	api.GET("/tasks/:id/stream", th.stream)

	authed := api.Group("")
	authed.Use(auth.AuthMiddleware(auth.MiddlewareConfig{
		Tokens:       tk,
		VersionStore: store,
		CookieName:   options.CookieName,
	}))
	authed.Use(auth.CSRFMiddleware(auth.CSRFConfig{
		CookieName: options.CSRFCookieName,
		HeaderName: options.CSRFHeaderName,
	}))
	{
		authed.GET("/auth/me", authH.me)
		authed.PUT("/auth/password", authH.changePassword)
		authed.POST("/auth/logout", authH.logout)

		h := &workerHandlers{ws: ws, store: store, eng: eng}
		authed.GET("/workers", h.list)
		authed.POST("/workers", h.create)
		authed.GET("/workers/:id", h.get)
		authed.PUT("/workers/:id", h.update)
		authed.DELETE("/workers/:id", h.delete)
		authed.POST("/workers/:id/test", h.test)
		authed.POST("/workers/:id/credentials/private-key", h.setPrivateKey)
		authed.POST("/workers/:id/credentials/password", h.setPanelPassword)
		authed.POST("/workers/:id/root-password", h.changeRootPassword)
		authed.POST("/workers/:id/install-deps", h.installDeps)

		authed.GET("/tasks", th.list)
		authed.GET("/tasks/:id", th.get)

		authed.GET("/audit-log", auditHandler(store))

		// K8s endpoints: all Bearer/Cookie protected.
		kh := &k8sHandlers{eng: eng, store: store, client: k8sClient}
		authed.POST("/k8s/services", kh.createService)
		authed.GET("/k8s/services", kh.listServices)
		authed.DELETE("/k8s/services/:name", kh.deleteService)
		authed.POST("/k8s/network-policies", kh.createNetworkPolicy)
		authed.GET("/k8s/network-policies", kh.listNetworkPolicies)
		authed.DELETE("/k8s/network-policies/:name", kh.deleteNetworkPolicy)
		authed.GET("/k8s/nodes", kh.listNodes)
		authed.GET("/k8s/pods", kh.listPods)

		// Storage endpoints: provision and reclaim are async.
		sh := &storageHandlers{eng: eng, store: store, runner: sshRunner}
		authed.POST("/storage/provision", sh.provision)
		authed.POST("/storage/reclaim", sh.reclaim)
		authed.GET("/storage", sh.list)
		authed.GET("/storage/vgs", sh.listVgs)
		authed.GET("/storage/inventory", sh.listInventory)
		authed.GET("/storage/nfs-hosts", sh.listNFSHosts)
		authed.POST("/storage/vg", sh.createVG)
		authed.POST("/storage/lv/resize", sh.resizeLV)
		authed.POST("/storage/lv/delete", sh.deleteLV)
	}

	// Static frontend: embedded SPA served at GET / and GET /static/*.
	registerStaticRoutes(r)
	return r
}
