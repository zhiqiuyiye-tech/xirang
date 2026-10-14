package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"testing"
	"time"
)

func residualBeforeRemoveRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	snapshot := namespaceTestSnapshot()
	snapshot.Holders[0].Mounts[0].Path = "/host-data/share"
	snapshot.Holders[0].Mounts[0].Optional = []string{"shared:578"}
	encoded, err := json.Marshal(map[string]any{"ok": true, "result": snapshot})
	if err != nil {
		t.Fatal(err)
	}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{})
	sr.add("cp-storage-namespace-scan", scriptResult{stdout: string(encoded)})
	sr.add("cp-storage-namespace-cleanup", scriptResult{stdout: `{"ok":true,"result":{"cleaned":true}}`})
	sr.add("cp-storage-namespace-verify", scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"u","major_minor":"253:0"}}}`})
	sr.add("lvremove -f /dev/vg_data/lv_1", scriptResult{stdout: "removed"})
	return sr
}

func firstCommand(calls []string, needle string) int {
	for i, command := range calls {
		if strings.Contains(command, needle) {
			return i
		}
	}
	return -1
}

func TestResidualMountsAreClearedBeforeFirstLvremove(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		t.Run(kind, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			store, id := submitMaintenanceTask(t, sr, kind, nil, WithNamespaceCleanup(allowTestHolders, time.Minute, time.Second))
			waitFor(t, store, id, "succeeded", 2*time.Second)
			previous := -1
			for _, command := range []string{"umount /data02/share", "cp-storage-namespace-scan", "cp-storage-namespace-cleanup", "cp-storage-namespace-verify", "lvremove -f /dev/vg_data/lv_1"} {
				index := firstCommand(sr.calls, command)
				if index <= previous {
					t.Fatalf("missing or misordered pre-removal step %s: index=%d previous=%d", command, index, previous)
				}
				previous = index
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatal("known residual mount must not require a failed lvremove first")
			}
		})
	}
}

func TestResidualFailuresBlockFirstLvremove(t *testing.T) {
	for _, stage := range []string{"disabled", "unauthorized", "scan", "identity", "cleanup", "timeout", "open_count"} {
		t.Run(stage, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			authorizer := NamespaceCleanupAuthorizer(allowTestHolders)
			switch stage {
			case "disabled":
				authorizer = nil
			case "unauthorized":
				authorizer = func(context.Context, string, string, []NamespaceHolder) error { return fmt.Errorf("unknown workload") }
			case "scan":
				sr.add("cp-storage-namespace-scan", scriptResult{stdout: `{"ok":false,"error":"permission denied","state_unknown":false}`, exitCode: 1})
			case "identity":
				sr.add("cp-storage-namespace-scan", scriptResult{stdout: `{"ok":true,"result":{"device":{"uuid":"changed","major_minor":"253:0"},"holders":[]}}`})
			case "cleanup":
				sr.add("cp-storage-namespace-cleanup", scriptResult{stdout: `{"ok":false,"error":"ordinary unmount busy","state_unknown":false}`, exitCode: 1})
			case "timeout":
				sr.add("cp-storage-namespace-cleanup", scriptResult{exitCode: 124})
			case "open_count":
				sr.add("cp-storage-namespace-verify", scriptResult{stdout: `{"ok":false,"error":"Open Count=1","state_unknown":false}`, exitCode: 1})
			}
			store, id := submitMaintenanceTask(t, sr, "storage_delete_lv", nil, WithNamespaceCleanup(authorizer, time.Minute, time.Second))
			waitFor(t, store, id, "failed", 2*time.Second)
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 0 {
				t.Fatal("attempted lvremove before residuals were safely released")
			}
			if (stage == "disabled" || stage == "unauthorized" || stage == "scan" || stage == "identity") && sr.counts["cp-storage-namespace-cleanup"] != 0 {
				t.Fatal("namespace unmount ran without authorized matching evidence")
			}
		})
	}
}

func TestResidualCleanupRechecksBusinessUsage(t *testing.T) {
	for _, blockAt := range []int{2, 3} {
		t.Run(fmt.Sprint(blockAt), func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			checks := 0
			guard := func(context.Context, string, string) (bool, []string, error) {
				checks++
				return checks >= blockAt, []string{"new/business"}, nil
			}
			store, id := submitMaintenanceTask(t, sr, "storage_delete_lv", nil, WithNamespaceCleanup(allowTestHolders, time.Minute, time.Second), WithPodGuardChecker(guard))
			waitFor(t, store, id, "failed", 2*time.Second)
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 0 {
				t.Fatal("business workload was ignored before deletion")
			}
			if blockAt == 2 && sr.counts["cp-storage-namespace-cleanup"] != 0 {
				t.Fatal("new business workload must prevent container unmount")
			}
		})
	}
}
