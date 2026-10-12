package api

import (
	"context"
	"encoding/json"
	"errors"
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
	store               *db.Store
	eng                 *tasks.Engine
	tk                  *auth.Tokens
	cookieName          string
	authRecheckInterval time.Duration
}

func taskSubmitStatus(err error, fallbackStatus int) int {
	var queueFull *tasks.QueueFullError
	if errors.As(err, &queueFull) {
		return http.StatusServiceUnavailable
	}
	return fallbackStatus
}

type taskRegistrationDetails struct {
	VGName     string `json:"vg_name"`
	LVName     string `json:"lv_name"`
	SizeGB     int    `json:"size_gb"`
	FSType     string `json:"fs_type"`
	MountPoint string `json:"mount_point"`
}

func registrationDetailsForTask(task *db.Task) *taskRegistrationDetails {
	if task == nil || task.Type != "storage_provision_nfs" || task.Status != "succeeded" {
		return nil
	}
	var params struct {
		VGName     string  `json:"vg_name"`
		LVName     string  `json:"lv_name"`
		SizeGB     float64 `json:"size_gb"`
		FSType     string  `json:"fs_type"`
		MountPoint string  `json:"mount_point"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &params); err != nil || params.VGName == "" || params.LVName == "" || params.SizeGB <= 0 || params.FSType == "" || params.MountPoint == "" {
		return nil
	}
	return &taskRegistrationDetails{
		VGName: params.VGName, LVName: params.LVName, SizeGB: int(params.SizeGB),
		FSType: params.FSType, MountPoint: params.MountPoint,
	}
}

func (h *taskHandlers) authSessionValid(ctx context.Context, token string) bool {
	claims, err := h.tk.Parse(token)
	if err != nil {
		return false
	}
	if h.store == nil {
		return true
	}
	version, err := h.store.GetAdminAuthVersion(ctx, claims.AdminID)
	return err == nil && version == claims.AuthVersion
}

func (h *taskHandlers) authRecheckEvery() time.Duration {
	if h.authRecheckInterval > 0 {
		return h.authRecheckInterval
	}
	return 30 * time.Second
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
	response := gin.H{"id": t.ID, "task": t, "steps": steps}
	if registration := registrationDetailsForTask(t); registration != nil {
		response["registration"] = registration
	}
	c.JSON(http.StatusOK, response)
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
	authTicker := time.NewTicker(h.authRecheckEvery())
	defer authTicker.Stop()
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
		case <-authTicker.C:
			if !h.authSessionValid(c.Request.Context(), tok) {
				return
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
