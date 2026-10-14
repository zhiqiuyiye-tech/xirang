package storage

import (
	"context"
	"encoding/json"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

// This is a direct protocol test: deletion handlers no longer select a host
// maintenance plan, but NewNamespaceRecovery must still reject a replayed
// weaker plan when called directly.
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
	if !strings.Contains(runner.command, "cp-storage-namespace-host_plan") {
		t.Fatal("direct host planning protocol marker is missing")
	}
}
