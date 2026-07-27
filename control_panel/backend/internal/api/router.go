package api

import (
	"github.com/gin-gonic/gin"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

// NewRouter wires every HTTP route for the control panel. k8sClient may be nil
// (non-cluster / local dev) - in that case the k8s endpoints return 503
// Service Unavailable instead of panicking. The k8s task handlers are
// registered separately by k8s.RegisterK8sHandlers (called from main.go).
func NewRouter(tk *auth.Tokens, ws *workers.Service, store *db.Store, eng *tasks.Engine, k8sClient kubernetes.Interface) *gin.Engine {
	r := gin.New()
	r.Use(gin.Recovery())

	api := r.Group("/api/v1")
	api.POST("/auth/login", loginHandler(store, tk))

	// SSE stream is registered on the public group (not behind
	// BearerMiddleware) because EventSource clients cannot set Authorization
	// headers - the entire reason the ?token= query fallback exists. Behind
	// the middleware the handler would get a 401 before it runs, making that
	// fallback unreachable. The handler performs its own auth (Bearer header
	// OR ?token= query).
	th := &taskHandlers{store: store, eng: eng, tk: tk}
	api.GET("/tasks/:id/stream", th.stream)

	authed := api.Group("")
	authed.Use(auth.BearerMiddleware(tk))
	{
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

		// K8s endpoints: all Bearer-protected. When k8sClient is nil the sync
		// list endpoints return 503; async create/delete also return 503 so a
		// misconfigured panel surfaces the error synchronously rather than
		// queueing a task that would fail.
		kh := &k8sHandlers{eng: eng, store: store, client: k8sClient}
		authed.POST("/k8s/services", kh.createService)
		authed.GET("/k8s/services", kh.listServices)
		authed.DELETE("/k8s/services/:name", kh.deleteService)
		authed.POST("/k8s/network-policies", kh.createNetworkPolicy)
		authed.GET("/k8s/network-policies", kh.listNetworkPolicies)
		authed.DELETE("/k8s/network-policies/:name", kh.deleteNetworkPolicy)
		authed.GET("/k8s/nodes", kh.listNodes)

		// Storage endpoints: provision and reclaim are async (submit a task
		// and respond 202 + task_id); list is synchronous. The task handlers
		// are registered separately by storage.RegisterStorageHandlers
		// (called from main.go).
		sh := &storageHandlers{eng: eng, store: store}
		authed.POST("/storage/provision", sh.provision)
		authed.POST("/storage/reclaim", sh.reclaim)
		authed.GET("/storage", sh.list)
	}

	// Static frontend: embedded SPA served at GET / and GET /static/*.
	registerStaticRoutes(r)
	return r
}
