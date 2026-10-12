package api

import (
	"context"
	"database/sql"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"strconv"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/db"
)

func TestHistoryRetentionKeepsNFSRegistrationResponse(t *testing.T) {
	path := filepath.Join(t.TempDir(), "registration-history.db")
	store, err := db.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	ctx := context.Background()
	const params = `{"worker_id":7,"vg_name":"vg_data","lv_name":"share_1","size_gb":100,"fs_type":"ext4","mount_point":"/data02/share_1"}`
	id, err := store.CreateTask(ctx, db.Task{Type: "storage_provision_nfs", TargetKind: "storage", TargetID: 7, Status: "succeeded", ParamsJSON: params})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := store.CreateStep(ctx, id, 1, "provision"); err != nil {
		t.Fatal(err)
	}
	now := time.Now().UTC()
	raw, err := sql.Open("sqlite", path)
	if err != nil {
		t.Fatal(err)
	}
	_, err = raw.Exec(`UPDATE tasks SET finished_at=? WHERE id=?`, now.Add(-400*24*time.Hour), id)
	raw.Close()
	if err != nil {
		t.Fatal(err)
	}
	result, err := store.PruneHistory(ctx, now, db.HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 10})
	if err != nil || result.Tasks != 0 || result.Steps != 1 {
		t.Fatalf("prune result=%+v err=%v", result, err)
	}
	original, err := store.GetTask(ctx, id)
	if err != nil || original.ParamsJSON != params {
		t.Fatalf("reclaim snapshot lost: %+v err=%v", original, err)
	}
	gin.SetMode(gin.TestMode)
	router := gin.New()
	handler := &taskHandlers{store: store}
	router.GET("/tasks/:id", handler.get)
	response := httptest.NewRecorder()
	router.ServeHTTP(response, httptest.NewRequest(http.MethodGet, "/tasks/"+strconv.FormatInt(id, 10), nil))
	if response.Code != http.StatusOK {
		t.Fatalf("registration lookup after retention: %d %s", response.Code, response.Body.String())
	}
	var body struct {
		Registration taskRegistrationDetails    `json:"registration"`
		Steps        []json.RawMessage          `json:"steps"`
		Task         map[string]json.RawMessage `json:"task"`
	}
	if err := json.Unmarshal(response.Body.Bytes(), &body); err != nil {
		t.Fatal(err)
	}
	if body.Registration.VGName != "vg_data" || body.Registration.LVName != "share_1" || body.Registration.MountPoint != "/data02/share_1" || body.Registration.SizeGB != 100 || body.Registration.FSType != "ext4" || len(body.Steps) != 0 {
		t.Fatalf("registration snapshot incorrect after pruning: %+v", body)
	}
	if _, exposed := body.Task["params_json"]; exposed {
		t.Fatal("raw task params exposed")
	}
}
