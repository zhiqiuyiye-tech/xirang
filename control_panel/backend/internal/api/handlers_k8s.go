package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/tasks"
	"k8s.io/client-go/kubernetes"
)

// k8sHandlers exposes the six K8s API endpoints (service + network-policy
// CRUD) backed by an injected kubernetes client. Create and delete operations
// are asynchronous: they submit a task (k8s_create_svc / k8s_delete_svc /
// k8s_create_np / k8s_delete_np) to the engine and respond 202 + task_id. List
// operations are synchronous.
//
// When client is nil (non-cluster / local dev) the sync list endpoints return
// 503 Service Unavailable rather than panicking. Async create/delete with a
// nil client also return 503 - the underlying task handler would fail anyway,
// and surfacing this synchronously gives the caller a clear signal.
type k8sHandlers struct {
	eng    *tasks.Engine
	store  *db.Store
	client kubernetes.Interface
}

// --- Services ---

// createService: POST /api/v1/k8s/services
// Body: CreateServiceReq as JSON (namespace, pod_name, pod_uid, selector, type, ports).
// Responds 202 + {task_id} on submit; the actual Service is created
// asynchronously by the k8s_create_svc task handler.
func (h *k8sHandlers) createService(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	taskID, err := h.eng.Submit(c, "k8s_create_svc", "k8s", 0, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.create_service", "", "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// listServices: GET /api/v1/k8s/services?namespace=
// Synchronous: returns the JSON array of Services managed by the control panel
// in the given namespace.
func (h *k8sHandlers) listServices(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	ns := c.Query("namespace")
	svcs, err := k8s.ListServices(c, h.client, ns)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, svcs)
}

// deleteService: DELETE /api/v1/k8s/services/:name?namespace=
// Async: submits k8s_delete_svc and responds 202 + {task_id}. The name and
// namespace come from the path / query so no JSON body is required.
func (h *k8sHandlers) deleteService(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	params := map[string]any{
		"namespace": c.Query("namespace"),
		"name":      c.Param("name"),
	}
	taskID, err := h.eng.Submit(c, "k8s_delete_svc", "k8s", 0, params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.delete_service", c.Param("name"), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// --- NetworkPolicies ---

// createNetworkPolicy: POST /api/v1/k8s/network-policies
// Body: CreateNetworkPolicyReq as JSON. Responds 202 + {task_id}.
func (h *k8sHandlers) createNetworkPolicy(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	taskID, err := h.eng.Submit(c, "k8s_create_np", "k8s", 0, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.create_network_policy", "", "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// listNetworkPolicies: GET /api/v1/k8s/network-policies?namespace=
// Synchronous: returns the JSON array of NetworkPolicies managed by the
// control panel in the given namespace.
func (h *k8sHandlers) listNetworkPolicies(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	ns := c.Query("namespace")
	nps, err := k8s.ListNetworkPolicies(c, h.client, ns)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, nps)
}

// deleteNetworkPolicy: DELETE /api/v1/k8s/network-policies/:name?namespace=
// Async: submits k8s_delete_np and responds 202 + {task_id}.
func (h *k8sHandlers) deleteNetworkPolicy(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	params := map[string]any{
		"namespace": c.Query("namespace"),
		"name":      c.Param("name"),
	}
	taskID, err := h.eng.Submit(c, "k8s_delete_np", "k8s", 0, params)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.delete_network_policy", c.Param("name"), "submitted")
	c.JSON(http.StatusAccepted, gin.H{"task_id": taskID})
}

// audit records an audit log entry. The actor is read from the JWT claims
// (defaulting to "admin"). Mirrors the helper on workerHandlers so the k8s
// endpoints record the same audit trail.
func (h *k8sHandlers) audit(c *gin.Context, action, target, result string) {
	actor := "admin"
	if cl, ok := auth.ClaimsFrom(c); ok {
		actor = cl.Username
	}
	t := target
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: actor, Action: action, Target: &t, Result: result})
}
