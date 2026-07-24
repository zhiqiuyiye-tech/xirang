package api

import (
	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

func NewRouter(tk *auth.Tokens, ws *workers.Service, store *db.Store, eng *tasks.Engine) *gin.Engine {
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
		h := &workerHandlers{ws: ws, store: store}
		authed.GET("/workers", h.list)
		authed.POST("/workers", h.create)
		authed.GET("/workers/:id", h.get)
		authed.PUT("/workers/:id", h.update)
		authed.DELETE("/workers/:id", h.delete)
		authed.POST("/workers/:id/test", h.test)
		authed.POST("/workers/:id/credentials/private-key", h.setPrivateKey)
		authed.POST("/workers/:id/credentials/password", h.setPanelPassword)
		authed.POST("/workers/:id/root-password", h.changeRootPassword)

		authed.GET("/tasks", th.list)
		authed.GET("/tasks/:id", th.get)

		authed.GET("/audit-log", auditHandler(store))
	}
	return r
}
