package api

import (
	"net/http"
	"strconv"
	"strings"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

type taskHandlers struct {
	store *db.Store
	eng   *tasks.Engine
	tk    *auth.Tokens
}

func (h *taskHandlers) list(c *gin.Context) {
	limit := 100
	ts, err := h.store.ListTasks(c, limit)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, ts)
}

func (h *taskHandlers) get(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	t, err := h.store.GetTask(c, id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}
	steps, _ := h.store.ListSteps(c, id)
	c.JSON(http.StatusOK, gin.H{"id": t.ID, "task": t, "steps": steps})
}

// stream: SSE. EventSource cannot set headers, so in addition to a Bearer
// header it also accepts ?token=<jwt> as a fallback auth mechanism. This route
// is registered on the public group (not behind BearerMiddleware) so the
// ?token= fallback is reachable; auth is done here instead.
func (h *taskHandlers) stream(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	// Auth: prefer a Bearer header, fall back to ?token= query param, else 401.
	// The auth scheme is case-insensitive per RFC 7235 (and matches the
	// BearerMiddleware on other routes); slice the ORIGINAL header value to
	// preserve the token's exact casing.
	tok := ""
	if ah := c.GetHeader("Authorization"); strings.HasPrefix(strings.ToLower(ah), "bearer ") {
		tok = ah[7:]
	} else if q := c.Query("token"); q != "" {
		tok = q
	}
	if tok == "" {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}
	if _, err := h.tk.Parse(tok); err != nil {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}
	c.Header("Content-Type", "text/event-stream")
	c.Header("Cache-Control", "no-cache")
	c.Header("Connection", "keep-alive")
	flusher, _ := c.Writer.(http.Flusher)

	ch, cancel := h.eng.Subscribe(id)
	defer cancel()

	t, _ := h.store.GetTask(c, id)
	if t != nil {
		c.SSEvent("task", t)
		if flusher != nil {
			flusher.Flush()
		}
	}
	for {
		select {
		case ev, ok := <-ch:
			if !ok {
				return
			}
			c.SSEvent("step", ev)
			if flusher != nil {
				flusher.Flush()
			}
		case <-c.Request.Context().Done():
			return
		}
	}
}
