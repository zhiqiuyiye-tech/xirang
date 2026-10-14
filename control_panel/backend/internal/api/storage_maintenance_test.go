package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"xirang/control_panel/internal/workers"
)

func TestStorageMaintenanceConfirmationMustBeJSONBoolean(t *testing.T) {
	router, ws, _, token := newRouter(t)
	wid, _ := ws.Create(context.Background(), workers.CreateReq{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root"})
	for _, endpoint := range []string{"/api/v1/storage/lv/delete", "/api/v1/storage/reclaim"} {
		for _, value := range []any{"true", float64(1), nil, map[string]any{}} {
			body, _ := json.Marshal(map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "maintenance_confirmed": value})
			request := httptest.NewRequest(http.MethodPost, endpoint, bytes.NewReader(body))
			request.Header.Set("Authorization", authHeader(t, token))
			request.Header.Set("Content-Type", "application/json")
			response := httptest.NewRecorder()
			router.ServeHTTP(response, request)
			if response.Code != http.StatusBadRequest {
				t.Fatalf("%s accepted nonboolean confirmation %v: %d", endpoint, value, response.Code)
			}
		}
	}
}

func TestMaintenanceConfirmationSurvivesSafeAuditFiltering(t *testing.T) {
	for _, confirmed := range []bool{true, false} {
		safe := safeAuditDetails(map[string]any{"maintenance_confirmed": confirmed, "password": "must-not-log"})
		if value, ok := safe["maintenance_confirmed"].(bool); !ok || value != confirmed || safe["password"] != nil {
			t.Fatal("maintenance attestation must be auditable without secrets")
		}
	}
	if _, exists := safeAuditDetails(map[string]any{"maintenance_confirmed": "not-a-boolean"})["maintenance_confirmed"]; exists {
		t.Fatal("nonboolean maintenance attestation must not be audited")
	}
}
