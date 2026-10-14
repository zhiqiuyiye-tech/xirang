package storage

import (
	"context"
	"encoding/json"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func submitMaintenanceTask(t *testing.T, sr *scriptRunner, kind string, confirmation any, opts ...StorageOption) (*db.Store, int64) {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "maintenance.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	eng := tasks.NewEngine(store)
	all := []any{WithPodGuardChecker(noPodUsers), WithHostUnmountAuthorizer(allowTestHolders)}
	for _, opt := range opts {
		all = append(all, opt)
	}
	RegisterStorageHandlers(eng, sr, store, all...)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	if err != nil {
		t.Fatal(err)
	}
	params := map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"}
	if confirmation != nil {
		params["maintenance_confirmed"] = confirmation
	}
	id, err := eng.Submit(context.Background(), kind, "storage", wid, params)
	if err != nil {
		t.Fatal(err)
	}
	return store, id
}

func TestMaintenanceRequiresServerEnablementAndPerTaskBoolean(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		for _, confirmation := range []any{true, "true"} {
			sr := sharedDeleteRunner(t)
			store, id := submitMaintenanceTask(t, sr, kind, confirmation)
			waitFor(t, store, id, "failed", 2*time.Second)
			if len(sr.calls) != 0 {
				t.Fatal("disabled or malformed maintenance reached worker transport")
			}
		}
	}
}

func TestMaintenanceEnabledAloneDoesNotDowngradeStrictMode(t *testing.T) {
	sr := sharedDeleteRunner(t)
	sr.add("cp-storage-namespace-host_plan", scriptResult{stdout: `{"ok":false,"error":"kernel NS_MNT_GET_INFO unavailable","state_unknown":false}`, exitCode: 1})
	store, id := submitMaintenanceTask(t, sr, "storage_delete_lv", nil, WithSharedHostMaintenance(true))
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, cmd := range sr.calls {
		if strings.Contains(cmd, "sed -i") || strings.Contains(cmd, "lvremove -f /dev/vg_data/lv_1") {
			t.Fatal("strict failure silently downgraded to maintenance")
		}
	}
}

func TestMaintenanceConfirmedDeleteAndReclaimRecordReducedGuarantee(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		t.Run(kind, func(t *testing.T) {
			sr := sharedDeleteRunner(t)
			plan := sharedHostTestPlan()
			plan.Mode = "maintenance"
			sr.add("cp-storage-namespace-host_plan", scriptResult{stdout: sharedPlanJSON(t, plan)})
			store, id := submitMaintenanceTask(t, sr, kind, true, WithSharedHostMaintenance(true))
			waitFor(t, store, id, "succeeded", 2*time.Second)
			steps, _ := store.ListSteps(context.Background(), id)
			confirmed := false
			for _, step := range steps {
				if step.Name == "confirm_host_maintenance" && step.Status == "succeeded" {
					confirmed = true
				}
			}
			if !confirmed || sr.counts["cp-storage-namespace-host_unmount"] != 1 || sr.counts["cp-storage-namespace-host_verify"] != 2 {
				t.Fatal("maintenance confirmation or release checks missing")
			}
		})
	}
}

func TestMaintenancePlanCannotBeReplayedAsStrictPlan(t *testing.T) {
	plan := sharedHostTestPlan()
	plan.Mode = "maintenance"
	runner := &namespaceTestRunner{}
	n := NewNamespaceRecovery(runner, nil, time.Second)
	if err := n.UnmountHost(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan); err == nil || runner.calls != 0 {
		t.Fatal("maintenance plan used without confirmed task context")
	}
	runner.out = sharedPlanJSON(t, plan)
	if _, err := n.PlanHostUnmount(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan.Device, []string{"/data02/share"}); err == nil {
		t.Fatal("remote response was allowed to select a weaker mode")
	}
	var request map[string]any
	if err := json.Unmarshal([]byte(runner.input), &request); err != nil {
		t.Fatal(err)
	}
	if request["payload"].(map[string]any)["mode"] != "strict" {
		t.Fatal("default request must preserve strict mode")
	}
}
