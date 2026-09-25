package api

import (
	"context"
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/storage"
	"xirang/control_panel/internal/tasks"
)

type storageCollector interface {
	EnqueueInventory(workerID int64) bool
	EnqueueAllInventory(ctx context.Context) (int, error)
	IsInventoryRefreshing(workerID int64) bool
}

// storageHandlers exposes the storage API endpoints backed by the task engine,
// SQLite snapshot storage, and background collector.
type storageHandlers struct {
	eng        *tasks.Engine
	store      *db.Store
	runner     ssh.Runner
	collector  storageCollector
	staleAfter time.Duration
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

// listVgs: GET /api/v1/storage/vgs?worker_id=X
// Synchronous: SSHes to the worker and returns its volume groups with free
// space, so the UI can show available capacity before creating an NFS share.
func (h *storageHandlers) listVgs(c *gin.Context) {
	wid, err := strconv.ParseInt(c.Query("worker_id"), 10, 64)
	if err != nil || wid <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "worker_id required"})
		return
	}
	w, err := h.store.GetWorker(c, wid)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "worker not found"})
		return
	}
	vgs, err := storage.ListVGs(c, h.runner, *w)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, vgs)
}

// listInventory: GET /api/v1/storage/inventory?worker_id=X
// Returns the cached storage inventory snapshot and freshness metadata for the
// worker. If no snapshot exists yet or it is stale, background collection is
// scheduled without blocking the HTTP response.
func (h *storageHandlers) listInventory(c *gin.Context) {
	wid, err := strconv.ParseInt(c.Query("worker_id"), 10, 64)
	if err != nil || wid <= 0 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "worker_id required"})
		return
	}
	if _, err := h.store.GetWorker(c, wid); err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "worker not found"})
		return
	}

	refreshing := h.collector != nil && h.collector.IsInventoryRefreshing(wid)
	snapshot, err := h.store.GetInventorySnapshot(c, wid)
	if err != nil {
		if h.collector != nil && !refreshing {
			h.collector.EnqueueInventory(wid)
			refreshing = true
		}
		c.JSON(http.StatusOK, gin.H{
			"vgs":               []storage.VGInfo{},
			"lvs":               []storage.LVInfo{},
			"physical_disks":    []storage.PhysicalDiskInfo{},
			"unused_disks":      []storage.DiskInfo{},
			"nfs":               storage.NFSStatusInfo{Active: false, Exports: []string{}},
			"data":              nil,
			"collected_at":      nil,
			"last_attempted_at": nil,
			"stale":             true,
			"refreshing":        refreshing,
			"last_error":        nil,
		})
		return
	}

	stale := snapshot.CollectedAt == nil || (h.staleAfter > 0 && time.Since(*snapshot.CollectedAt) > h.staleAfter)
	if stale && !refreshing && h.collector != nil {
		h.collector.EnqueueInventory(wid)
		refreshing = true
	}

	var inv storage.InventoryInfo
	if snapshot.PayloadJSON != "" {
		_ = json.Unmarshal([]byte(snapshot.PayloadJSON), &inv)
	}
	if inv.VGs == nil {
		inv.VGs = []storage.VGInfo{}
	}
	if inv.LVs == nil {
		inv.LVs = []storage.LVInfo{}
	}
	if inv.PhysicalDisks == nil {
		inv.PhysicalDisks = []storage.PhysicalDiskInfo{}
	}
	if inv.UnusedDisks == nil {
		inv.UnusedDisks = []storage.DiskInfo{}
	}
	if inv.NFS.Exports == nil {
		inv.NFS.Exports = []string{}
	}

	c.JSON(http.StatusOK, gin.H{
		"vgs":               inv.VGs,
		"lvs":               inv.LVs,
		"physical_disks":    inv.PhysicalDisks,
		"unused_disks":      inv.UnusedDisks,
		"nfs":               inv.NFS,
		"data":              inv,
		"collected_at":      snapshot.CollectedAt,
		"last_attempted_at": snapshot.LastAttemptedAt,
		"stale":             stale,
		"refreshing":        refreshing,
		"last_error":        snapshot.LastError,
	})
}

// listNFSHosts: GET /api/v1/storage/nfs-hosts?all=true|false
// Returns the status of workers and their storage inventories from local
// SQLite snapshots without performing synchronous SSH round trips.
func (h *storageHandlers) listNFSHosts(c *gin.Context) {
	workers, err := h.store.ListWorkers(c)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	nfsOnly := c.Query("all") != "true"
	snapshots, _ := h.store.ListInventorySnapshots(c)
	snapMap := make(map[int64]db.InventorySnapshot, len(snapshots))
	for _, snap := range snapshots {
		snapMap[snap.WorkerID] = snap
	}

	results := make([]map[string]any, 0, len(workers))
	for _, w := range workers {
		refreshing := h.collector != nil && h.collector.IsInventoryRefreshing(w.ID)
		snap, hasSnap := snapMap[w.ID]
		var inv storage.InventoryInfo
		if hasSnap && snap.PayloadJSON != "" {
			_ = json.Unmarshal([]byte(snap.PayloadJSON), &inv)
		}
		if inv.PhysicalDisks == nil {
			inv.PhysicalDisks = []storage.PhysicalDiskInfo{}
		}
		if inv.LVs == nil {
			inv.LVs = []storage.LVInfo{}
		}
		if inv.NFS.Exports == nil {
			inv.NFS.Exports = []string{}
		}

		stale := !hasSnap || snap.CollectedAt == nil || (h.staleAfter > 0 && time.Since(*snap.CollectedAt) > h.staleAfter)
		var lastAttempted *time.Time
		if hasSnap {
			lastAttempted = &snap.LastAttemptedAt
		}
		var errMsg string
		if hasSnap && snap.LastError != nil {
			errMsg = *snap.LastError
		}

		hasExportedLV := false
		for _, lv := range inv.LVs {
			if lv.IsNFSExport {
				hasExportedLV = true
				break
			}
		}

		if nfsOnly && !inv.NFS.Active && len(inv.NFS.Exports) == 0 && !hasExportedLV {
			continue
		}

		hostItem := map[string]any{
			"worker_id":         w.ID,
			"worker_name":       w.Name,
			"host":              w.Host,
			"port":              w.Port,
			"status":            w.Status,
			"nfs_active":        inv.NFS.Active,
			"total_disks":       len(inv.PhysicalDisks),
			"physical_disks":    inv.PhysicalDisks,
			"virtual_disks":     inv.LVs,
			"nfs_exports":       inv.NFS.Exports,
			"collected_at":      snap.CollectedAt,
			"last_attempted_at": lastAttempted,
			"stale":             stale,
			"refreshing":        refreshing,
			"error_message":     errMsg,
		}
		results = append(results, hostItem)
	}

	c.JSON(http.StatusOK, results)
}

// refresh: POST /api/v1/storage/refresh
// Body: {worker_id?: int64}. Schedules an immediate background inventory probe
// for one worker or all workers and responds 202.
func (h *storageHandlers) refresh(c *gin.Context) {
	var req map[string]any
	_ = c.ShouldBindJSON(&req)
	var wid int64
	if req != nil {
		wid, _ = parseWorkerID(req["worker_id"])
	}
	if wid == 0 && c.Query("worker_id") != "" {
		wid, _ = strconv.ParseInt(c.Query("worker_id"), 10, 64)
	}

	if wid > 0 {
		if _, err := h.store.GetWorker(c, wid); err != nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "worker not found"})
			return
		}
		if h.collector != nil {
			h.collector.EnqueueInventory(wid)
		}
		c.JSON(http.StatusAccepted, gin.H{"refreshing": true, "worker_id": wid})
		return
	}

	count := 0
	if h.collector != nil {
		count, _ = h.collector.EnqueueAllInventory(c)
	}
	c.JSON(http.StatusAccepted, gin.H{"refreshing": true, "count": count})
}

// createVG: POST /api/v1/storage/vg
// Body: {worker_id, vg_name?, disks[]}. Submits storage_create_vg (pvcreate each
// disk + vgcreate/vgextend). Responds 202 + {task_id}.
func (h *storageHandlers) createVG(c *gin.Context) {
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	wid, _ := parseWorkerID(req["worker_id"])
	taskID, err := h.eng.Submit(c, "storage_create_vg", "storage", wid, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "storage.create_vg", strconv.FormatInt(wid, 10), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// resizeLV: POST /api/v1/storage/lv/resize
// Body: {worker_id, vg_name, lv_name, action: grow|shrink, delta_gb}. Submits
// storage_resize_lv (lvextend/lvreduce -r). Responds 202 + {task_id}.
func (h *storageHandlers) resizeLV(c *gin.Context) {
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	wid, _ := parseWorkerID(req["worker_id"])
	taskID, err := h.eng.Submit(c, "storage_resize_lv", "storage", wid, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "storage.resize_lv", strconv.FormatInt(wid, 10), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// deleteLV: POST /api/v1/storage/lv/delete
// Body: {worker_id, vg_name, lv_name}. Submits storage_delete_lv (teardown +
// lvremove, releasing space to the VG). Responds 202 + {task_id}.
func (h *storageHandlers) deleteLV(c *gin.Context) {
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	wid, _ := parseWorkerID(req["worker_id"])
	taskID, err := h.eng.Submit(c, "storage_delete_lv", "storage", wid, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "storage.delete_lv", strconv.FormatInt(wid, 10), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
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
