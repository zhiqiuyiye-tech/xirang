package api

import (
	"fmt"
	"net"
	"net/http"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

type RouterOptions struct {
	RateLimiter                 *auth.RateLimiter
	CookieName                  string
	CookieSecure                bool
	CookieSameSite              string
	CSRFCookieName              string
	CSRFHeaderName              string
	RequireK8s                  bool
	TrustedProxies              []string
	ChallengeRateLimitPerMinute int
	ChallengeMaxPendingPerIP    int
	ChallengeMaxPendingGlobal   int
	Collector                   storageCollector
	StaleAfter                  time.Duration
}

type RouterOption func(*RouterOptions)

func WithCollector(c storageCollector) RouterOption {
	return func(o *RouterOptions) { o.Collector = c }
}

func WithStaleAfter(d time.Duration) RouterOption {
	return func(o *RouterOptions) { o.StaleAfter = d }
}

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

func WithChallengeLimits(perMinute, pendingPerIP, pendingGlobal int) RouterOption {
	return func(o *RouterOptions) {
		o.ChallengeRateLimitPerMinute = perMinute
		o.ChallengeMaxPendingPerIP = pendingPerIP
		o.ChallengeMaxPendingGlobal = pendingGlobal
	}
}

func configureTrustedProxies(r *gin.Engine, proxies []string) error {
	for _, proxy := range proxies {
		if _, _, err := net.ParseCIDR(proxy); err != nil {
			return fmt.Errorf("trusted proxy %q must be a CIDR: %w", proxy, err)
		}
	}
	return r.SetTrustedProxies(proxies)
}

func securityHeadersMiddleware(isHTTPS bool) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("X-Content-Type-Options", "nosniff")
		c.Header("X-Frame-Options", "DENY")
		c.Header("Referrer-Policy", "no-referrer")
		c.Header("Permissions-Policy", "geolocation=(), camera=(), microphone=()")
		c.Header("Content-Security-Policy", "default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'; connect-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'")
		path := c.Request.URL.Path
		if path == "/" || strings.HasPrefix(path, "/static/") || strings.HasPrefix(path, "/api/v1/auth/") {
			c.Header("Cache-Control", "no-store")
		}
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
func NewRouter(tk *auth.Tokens, ws *workers.Service, store *db.Store, eng *tasks.Engine, k8sClient kubernetes.Interface, sshRunner ssh.Runner, opts ...RouterOption) (*gin.Engine, error) {
	options := RouterOptions{
		CookieName:     "cp_session",
		CookieSecure:   false,
		CookieSameSite: "Strict",
		CSRFCookieName: "cp_csrf",
		CSRFHeaderName: "X-CSRF-Token",
	}
	for _, opt := range opts {
		opt(&options)
	}

	r := gin.New()
	r.Use(gin.Recovery())

	if err := configureTrustedProxies(r, options.TrustedProxies); err != nil {
		return nil, fmt.Errorf("configure trusted proxies: %w", err)
	}

	r.Use(securityHeadersMiddleware(options.CookieSecure))

	// Health probes
	r.GET("/health/live", liveHandler)
	r.GET("/health/ready", readyHandler(store, k8sClient, options.RequireK8s))

	api := r.Group("/api/v1")

	authH := newAuthHandlers(AuthHandlerConfig{
		Store:                       store,
		Tokens:                      tk,
		Limiter:                     options.RateLimiter,
		CookieName:                  options.CookieName,
		CookieSecure:                options.CookieSecure,
		CookieSameSite:              options.CookieSameSite,
		CSRFCookieName:              options.CSRFCookieName,
		TokenTTL:                    tk.TTL(),
		ChallengeRateLimitPerMinute: options.ChallengeRateLimitPerMinute,
		ChallengeMaxPendingPerIP:    options.ChallengeMaxPendingPerIP,
		ChallengeMaxPendingGlobal:   options.ChallengeMaxPendingGlobal,
	})

	api.GET("/auth/status", authH.status)
	api.POST("/auth/challenges/login", authH.loginChallenge)
	api.POST("/auth/challenges/bootstrap", authH.bootstrapChallenge)
	api.POST("/auth/bootstrap", authH.bootstrap)
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
		authed.POST("/auth/challenges/rotate", authH.rotateChallenge)
		authed.PUT("/auth/key", authH.rotateKey)
		authed.POST("/auth/logout", authH.logout)
		authed.POST("/auth/logout-all", authH.logoutAll)

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
		kh := &k8sHandlers{eng: eng, store: store, client: k8sClient, staleAfter: options.StaleAfter}
		authed.POST("/k8s/services", kh.createService)
		authed.GET("/k8s/services", kh.listServices)
		authed.PUT("/k8s/services/:name", kh.updateService)
		authed.DELETE("/k8s/services/:name", kh.deleteService)
		authed.POST("/k8s/network-policies", kh.createNetworkPolicy)
		authed.GET("/k8s/network-policies", kh.listNetworkPolicies)
		authed.DELETE("/k8s/network-policies/:name", kh.deleteNetworkPolicy)
		authed.GET("/k8s/nodes", kh.listNodes)
		authed.GET("/k8s/pods", kh.listPods)
		authed.PUT("/k8s/notebooks/:namespace/:name/metadata", kh.updateNotebookMetadata)

		// Storage endpoints: provision and reclaim are async.
		sh := &storageHandlers{
			eng:        eng,
			store:      store,
			runner:     sshRunner,
			collector:  options.Collector,
			staleAfter: options.StaleAfter,
			client:     k8sClient,
		}
		authed.POST("/storage/provision", sh.provision)
		authed.POST("/storage/reclaim", sh.reclaim)
		authed.GET("/storage", sh.list)
		authed.GET("/storage/vgs", sh.listVgs)
		authed.GET("/storage/inventory", sh.listInventory)
		authed.GET("/storage/nfs-hosts", sh.listNFSHosts)
		authed.POST("/storage/refresh", sh.refresh)
		authed.POST("/storage/vg", sh.createVG)
		authed.POST("/storage/lv/resize", sh.resizeLV)
		authed.POST("/storage/lv/delete", sh.deleteLV)
	}

	// Static frontend: embedded SPA served at GET / and GET /static/*.
	registerStaticRoutes(r)
	return r, nil
}
