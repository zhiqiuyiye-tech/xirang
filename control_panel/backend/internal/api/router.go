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

		th := &taskHandlers{store: store, eng: eng, tk: tk}
		authed.GET("/tasks", th.list)
		authed.GET("/tasks/:id", th.get)
		authed.GET("/tasks/:id/stream", th.stream) // 内部也接受 ?token=

		authed.GET("/audit-log", auditHandler(store))
	}
	return r
}
