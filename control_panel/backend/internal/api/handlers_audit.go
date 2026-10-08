package api

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

// Only explicitly supported, non-secret fields enter the audit trail or API.
// Filtering on both write and read also protects older rows with raw params.
func safeAuditDetails(raw map[string]any) map[string]any {
	out := map[string]any{}
	// The browser submits mappings rather than the lower-level ports schema.
	// Normalize only documented mapping fields, never copy arbitrary payloads.
	if mappings, ok := raw["mappings"].([]any); ok {
		ports := []any{}
		for _, item := range mappings {
			if mapping, ok := item.(map[string]any); ok {
				target := mapping["pod_port"]
				if target == nil {
					target = mapping["target_port"]
				}
				ports = append(ports, map[string]any{"port": target, "target_port": target, "node_port": mapping["node_port"], "protocol": "TCP"})
			}
		}
		// Use a copy so audit serialization never mutates task parameters.
		normalized := make(map[string]any, len(raw))
		for key, value := range raw {
			if key != "mappings" {
				normalized[key] = value
			}
		}
		normalized["ports"] = ports
		return safeAuditDetails(normalized)
	}
	for key, value := range raw {
		switch key {
		case "worker_id", "worker_name", "name", "host", "port", "username", "namespace", "pod_name", "pod_uid", "type", "resource_version", "task_id", "vg_name", "lv_name", "size_gb", "fs_type", "mount_point", "action", "delta_gb", "owner_name", "note", "target_port", "node_port", "protocol", "auth_mode":
			switch value.(type) {
			case string, float64, bool:
				out[key] = value
			}
		case "before", "after":
			if nested, ok := value.(map[string]any); ok {
				out[key] = safeAuditDetails(nested)
			}
		case "ports":
			if ports, ok := value.([]any); ok {
				safePorts := []map[string]any{}
				for _, item := range ports {
					if port, ok := item.(map[string]any); ok {
						safe := map[string]any{}
						for _, field := range []string{"port", "target_port", "node_port", "protocol"} {
							switch v := port[field].(type) {
							case string, float64:
								safe[field] = v
							}
						}
						safePorts = append(safePorts, safe)
					}
				}
				out[key] = safePorts
			}
		case "disks":
			if disks, ok := value.([]any); ok {
				safeDisks := []string{}
				for _, disk := range disks {
					if path, ok := disk.(string); ok {
						safeDisks = append(safeDisks, path)
					}
				}
				out[key] = safeDisks
			}
		}
	}
	return out
}

func recordAudit(c *gin.Context, store *db.Store, action, target, result string, params ...map[string]any) {
	actor := "admin"
	if claims, ok := auth.ClaimsFrom(c); ok {
		actor = claims.Username
	}
	merged := map[string]any{}
	for _, fields := range params {
		for key, value := range fields {
			merged[key] = value
		}
	}
	var paramsJSON *string
	if encoded, err := json.Marshal(merged); err == nil {
		var decoded map[string]any
		if json.Unmarshal(encoded, &decoded) == nil {
			if safe, err := json.Marshal(safeAuditDetails(decoded)); err == nil {
				text := string(safe)
				paramsJSON = &text
			}
		}
	}
	_ = store.InsertAudit(c, db.AuditLog{Actor: actor, Action: action, Target: &target, Result: result, ParamsJSON: paramsJSON})
}

func workerAuditDetails(c *gin.Context, store *db.Store, target string) map[string]any {
	id, err := strconv.ParseInt(target, 10, 64)
	if err != nil {
		return nil
	}
	worker, err := store.GetWorker(c, id)
	if err != nil {
		return map[string]any{"worker_id": id}
	}
	return map[string]any{"worker_id": id, "worker_name": worker.Name, "host": worker.Host, "port": worker.Port, "username": worker.Username, "auth_mode": worker.AuthMode}
}

func auditHandler(store *db.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		logs, err := store.ListAudit(c, 200)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		type auditResponse struct {
			db.AuditLog
			Details map[string]any `json:"details"`
		}
		response := make([]auditResponse, 0, len(logs))
		for _, log := range logs {
			details := map[string]any{}
			if log.ParamsJSON != nil {
				var raw map[string]any
				if json.Unmarshal([]byte(*log.ParamsJSON), &raw) == nil {
					details = safeAuditDetails(raw)
				}
			}
			response = append(response, auditResponse{AuditLog: log, Details: details})
		}
		c.JSON(http.StatusOK, response)
	}
}
