package api

import (
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

type taskHandlers struct {
	store      *db.Store
	eng        *tasks.Engine
	tk         *auth.Tokens
	cookieName string
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
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid task id"})
		return
	}
	t, err := h.store.GetTask(c, id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}
	steps, _ := h.store.ListSteps(c, id)
	c.JSON(http.StatusOK, gin.H{"id": t.ID, "task": t, "steps": steps})
}

// stream: SSE. Authenticated via HttpOnly Cookie (EventSource default) or
// Authorization: Bearer <jwt> header. Query-parameter tokens are prohibited
// to prevent tokens leaking into access logs or browser history.
func (h *taskHandlers) stream(c *gin.Context) {
	id, err := strconv.ParseInt(c.Param("id"), 10, 64)
	if err != nil || id <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid task id"})
		return
	}

	cookieName := h.cookieName
	if cookieName == "" {
		cookieName = "cp_session"
	}

	tok := ""
	if ah := c.GetHeader("Authorization"); strings.HasPrefix(strings.ToLower(ah), "bearer ") {
		tok = ah[7:]
	} else if cookieVal, err := c.Cookie(cookieName); err == nil && cookieVal != "" {
		tok = cookieVal
	}

	if tok == "" {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}

	cl, err := h.tk.Parse(tok)
	if err != nil {
		c.AbortWithStatus(http.StatusUnauthorized)
		return
	}

	if h.store != nil {
		curVer, err := h.store.GetAdminAuthVersion(c.Request.Context(), cl.AdminID)
		if err != nil || curVer != cl.AuthVersion {
			c.AbortWithStatus(http.StatusUnauthorized)
			return
		}
	}

	// 404 on an unknown task BEFORE subscribing: otherwise the subscription
	// would never receive events and the connection would hang until the
	// client gives up.
	t, err := h.store.GetTask(c, id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "task not found"})
		return
	}
	c.Header("Content-Type", "text/event-stream")
	c.Header("Cache-Control", "no-cache")
	c.Header("Connection", "keep-alive")
	// Disable proxy response buffering (nginx & co.); without it SSE frames
	// can sit in the proxy's buffer and the stream appears stalled.
	c.Header("X-Accel-Buffering", "no")
	flusher, _ := c.Writer.(http.Flusher)

	ch, cancel := h.eng.Subscribe(id)
	defer cancel()

	c.SSEvent("task", t)
	if flusher != nil {
		flusher.Flush()
	}
	if t.Status == "succeeded" || t.Status == "failed" {
		for {
			select {
			case ev, ok := <-ch:
				if ok && ev.Seq > 0 {
					c.SSEvent("step", ev)
					if flusher != nil {
						flusher.Flush()
					}
				}
			default:
				return
			}
		}
	}
	// Heartbeat: comment frames are ignored by EventSource but keep
	// intermediaries (proxies / load balancers) from reaping the idle
	// connection between step events.
	hb := time.NewTicker(30 * time.Second)
	defer hb.Stop()
	for {
		select {
		case ev, ok := <-ch:
			if !ok {
				return
			}
			if ev.Seq == 0 {
				curTask, err := h.store.GetTask(c, id)
				if err == nil {
					c.SSEvent("task", curTask)
					if flusher != nil {
						flusher.Flush()
					}
					if curTask.Status == "succeeded" || curTask.Status == "failed" {
						return
					}
				}
			} else {
				c.SSEvent("step", ev)
				if flusher != nil {
					flusher.Flush()
				}
			}
		case <-hb.C:
			if _, err := c.Writer.WriteString(": keepalive\n\n"); err != nil {
				return
			}
			if flusher != nil {
				flusher.Flush()
			}
		case <-c.Request.Context().Done():
			return
		}
	}
}
