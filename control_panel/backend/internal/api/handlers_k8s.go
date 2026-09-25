package api

import (
	"fmt"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/tasks"
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

// listServices: GET /api/v1/k8s/services
// Synchronous: returns ServiceInfo for every Service in namespaces that contain
// notebook pods - including Services NOT created by the control panel (e.g. the
// platform's notebook-multi-port-svc). Each entry carries a Managed flag so the
// UI can mark ours (deletable) vs external (read-only).
func (h *k8sHandlers) listServices(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	svcs, err := k8s.ListServicesForNotebooks(c, h.client)
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

// updateService: PUT /api/v1/k8s/services/:name?namespace=
// Async: submits k8s_update_svc and responds 202 + {task_id}.
func (h *k8sHandlers) updateService(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	var req map[string]any
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	req["name"] = c.Param("name")
	if req["namespace"] == nil || req["namespace"] == "" {
		req["namespace"] = c.Query("namespace")
	}
	taskID, err := h.eng.Submit(c, "k8s_update_svc", "k8s", 0, req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.update_service", c.Param("name"), "submitted")
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

// listNodes: GET /api/v1/k8s/nodes
// Returns discovered cluster nodes (name/internal IP/role). Used by the worker
// form to prefill host/name so the admin only needs to supply SSH credentials.
func (h *k8sHandlers) listNodes(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	nodes, err := k8s.ListNodes(c, h.client)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, nodes)
}

// listPods: GET /api/v1/k8s/pods
// Returns notebook pods across all namespaces, batch-joining owner_name and
// note from notebook_metadata by their stable key.
func (h *k8sHandlers) listPods(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	pods, err := k8s.ListNotebookPods(c, h.client)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	keys := make([]string, 0, len(pods))
	for _, p := range pods {
		if p.StableKey != "" {
			keys = append(keys, p.StableKey)
		}
	}
	if h.store != nil && len(keys) > 0 {
		metaMap, _ := h.store.GetNotebookMetadataByKeys(c, keys)
		for i := range pods {
			if meta, ok := metaMap[pods[i].StableKey]; ok {
				pods[i].OwnerName = meta.OwnerName
				pods[i].Note = meta.Note
				pods[i].UpdatedBy = meta.UpdatedBy
				pods[i].MetadataUpdatedAt = &meta.UpdatedAt
			}
		}
	}
	c.JSON(http.StatusOK, pods)
}

// updateNotebookMetadata: PUT /api/v1/k8s/notebooks/:namespace/:name/metadata
// Body: { "owner_name": string, "note": string }
// Resolves the current Pod from Kubernetes, computes its stable key, and updates
// or cleans up metadata in SQLite.
func (h *k8sHandlers) updateNotebookMetadata(c *gin.Context) {
	if h.client == nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{"error": "k8s client unavailable (non-cluster mode)"})
		return
	}
	namespace := c.Param("namespace")
	name := c.Param("name")
	if namespace == "" || name == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "namespace and name required"})
		return
	}

	var req struct {
		OwnerName string `json:"owner_name"`
		Note      string `json:"note"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	ownerName := strings.TrimSpace(req.OwnerName)
	note := strings.TrimSpace(req.Note)
	if len([]rune(ownerName)) > 100 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "owner_name cannot exceed 100 characters"})
		return
	}
	if len([]rune(note)) > 1000 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "note cannot exceed 1000 characters"})
		return
	}

	pod, err := h.client.CoreV1().Pods(namespace).Get(c, name, metav1.GetOptions{})
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": fmt.Sprintf("pod not found: %v", err)})
		return
	}

	stableKey, kind, ws, proj := k8s.StableKeyForPod(namespace, string(pod.UID), pod.Labels)
	actor := "admin"
	if cl, ok := auth.ClaimsFrom(c); ok {
		actor = cl.Username
	}

	if ownerName == "" && note == "" {
		_ = h.store.DeleteNotebookMetadata(c, stableKey)
		h.audit(c, "k8s.delete_notebook_metadata", namespace+"/"+name, "deleted")
		c.JSON(http.StatusOK, gin.H{"deleted": true, "stable_key": stableKey})
		return
	}

	m := db.NotebookMetadata{
		StableKey:   stableKey,
		KeyKind:     kind,
		Namespace:   namespace,
		WorkspaceID: ws,
		ProjectID:   proj,
		LastPodUID:  string(pod.UID),
		OwnerName:   ownerName,
		Note:        note,
		UpdatedBy:   actor,
	}
	if err := h.store.UpsertNotebookMetadata(c, m); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	h.audit(c, "k8s.update_notebook_metadata", namespace+"/"+name, "success")
	c.JSON(http.StatusOK, m)
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
