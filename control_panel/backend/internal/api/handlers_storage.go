package api

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

// storageHandlers exposes the three storage API endpoints (provision, reclaim,
// list) backed by the task engine. Provision and reclaim are asynchronous: they
// submit a task (storage_provision_nfs / storage_reclaim_nfs) to the engine
// and respond 202 + task_id. The actual SSH work runs in the registered task
// handler (see storage.RegisterStorageHandlers, called from main.go). List is
// synchronous and returns recent tasks whose target_kind is 'storage'.
type storageHandlers struct {
	eng   *tasks.Engine
	store *db.Store
}

// provision: POST /api/v1/storage/provision
// Body: {worker_id, vg_name, lv_name, size_gb, fs_type, mount_point, export_opts?}
// Responds 202 + {task_id} on submit. target_kind='storage', target_id=worker_id.
func (h *storageHandlers) provision(c *gin.Context) {
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	wid, _ := parseWorkerID(req["worker_id"])
	taskID, err := h.eng.Submit(c, "storage_provision_nfs", "storage", wid, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "storage.provision_nfs", strconv.FormatInt(wid, 10), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// reclaim: POST /api/v1/storage/reclaim
// Body: {worker_id, vg_name, lv_name, mount_point}
// Responds 202 + {task_id} on submit. target_kind='storage', target_id=worker_id.
func (h *storageHandlers) reclaim(c *gin.Context) {
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	wid, _ := parseWorkerID(req["worker_id"])
	taskID, err := h.eng.Submit(c, "storage_reclaim_nfs", "storage", wid, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "storage.reclaim_nfs", strconv.FormatInt(wid, 10), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// list: GET /api/v1/storage
// Synchronous: returns recent tasks whose target_kind is 'storage'. Reuses
// store.ListTasks and filters in the handler.
func (h *storageHandlers) list(c *gin.Context) {
	tasks, err := h.store.ListTasks(c, 100)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	var out []db.Task
	for _, t := range tasks {
		if t.TargetKind == "storage" {
			out = append(out, t)
		}
	}
	c.JSON(http.StatusOK, out)
}

// parseWorkerID extracts the worker_id from a JSON-decoded map value (which
// arrives as float64 from encoding/json). Returns 0 if missing or unparseable;
// the task handler will surface a clear error for an invalid worker_id.
func parseWorkerID(v any) (int64, error) {
	switch w := v.(type) {
	case float64:
		return int64(w), nil
	case int64:
		return w, nil
	case int:
		return int64(w), nil
	case string:
		return strconv.ParseInt(w, 10, 64)
	}
	return 0, nil
}

// audit records an audit log entry. The actor is read from the JWT claims
// (defaulting to "admin"). Mirrors the helper on workerHandlers / k8sHandlers.
func (h *storageHandlers) audit(c *gin.Context, action, target, result string) {
	actor := "admin"
	if cl, ok := auth.ClaimsFrom(c); ok {
		actor = cl.Username
	}
	t := target
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: actor, Action: action, Target: &t, Result: result})
}
