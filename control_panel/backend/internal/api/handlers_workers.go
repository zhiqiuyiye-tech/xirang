package api

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

type workerHandlers struct {
	ws    *workers.Service
	store *db.Store
	eng   *tasks.Engine
}

func (h *workerHandlers) list(c *gin.Context) {
	ws, err := h.ws.List(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, ws)
}

func (h *workerHandlers) create(c *gin.Context) {
	var r workers.CreateReq
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	id, err := h.ws.Create(c, r)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.create", strconv.FormatInt(id, 10), "success")
	c.JSON(http.StatusCreated, gin.H{"id": id})
}

func (h *workerHandlers) get(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	w, err := h.ws.Get(c, id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, w)
}

func (h *workerHandlers) update(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	var r workers.UpdateReq
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := h.ws.Update(c, id, r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.update", c.Param("id"), "success")
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *workerHandlers) delete(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	if err := h.ws.Delete(c, id); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.delete", c.Param("id"), "success")
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *workerHandlers) test(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	if err := h.ws.TestConnection(c, id); err != nil {
		h.audit(c, "worker.test", c.Param("id"), "fail")
		c.JSON(http.StatusOK, gin.H{"ok": false, "error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *workerHandlers) setPrivateKey(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	var r struct {
		PrivateKey string `json:"private_key"`
	}
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := h.ws.SetPrivateKey(c, id, r.PrivateKey); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.set_private_key", c.Param("id"), "success")
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *workerHandlers) setPanelPassword(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	var r struct {
		Password string `json:"password"`
	}
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	if err := h.ws.SetPanelPassword(c, id, r.Password); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.set_panel_password", c.Param("id"), "success")
	c.JSON(http.StatusOK, gin.H{"ok": true})
}

func (h *workerHandlers) changeRootPassword(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	var r struct {
		Password string `json:"password"`
	}
	if err := c.ShouldBindJSON(&r); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	taskID, err := h.ws.ChangeRootPassword(c, id, r.Password)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.change_root_password", c.Param("id"), "success")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// installDeps: POST /api/v1/workers/:id/install-deps
// Submits an async "install_deps" task that SSHes to the worker and installs
// lvm2 + nfs-utils. Responds 202 + {task_id}. No request body needed.
func (h *workerHandlers) installDeps(c *gin.Context) {
	id, _ := strconv.ParseInt(c.Param("id"), 10, 64)
	taskID, err := h.eng.Submit(c, "install_deps", "worker", id, map[string]any{"worker_id": id})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "worker.install_deps", c.Param("id"), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// audit records an audit log entry. The actor is read from the JWT claims
// (defaulting to "admin"); credential plaintext is never logged - only the
// action name, target id, and result are recorded.
func (h *workerHandlers) audit(c *gin.Context, action, target, result string) {
	actor := "admin"
	if cl, ok := auth.ClaimsFrom(c); ok {
		actor = cl.Username
	}
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: actor, Action: action, Target: &target, Result: result})
}
