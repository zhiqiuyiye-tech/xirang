package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func allowTestHolders(context.Context, string, string, []NamespaceHolder) error { return nil }
func recoveryScriptRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	snapshot := namespaceTestSnapshot()
	snapshot.Holders[0].Mounts[0].Path = "/data02/share"
	data, err := json.Marshal(map[string]any{"ok": true, "result": snapshot})
	if err != nil {
		t.Fatal(err)
	}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	sr.add("lvremove -f /dev/vg_data/lv_1", scriptResult{stderr: "Logical volume vg_data/lv_1 contains a filesystem in use.", exitCode: 5}, scriptResult{stdout: "removed"})
	sr.add("cp-storage-namespace-scan", scriptResult{stdout: string(data)})
	sr.add("cp-storage-namespace-cleanup", scriptResult{stdout: `{"ok":true,"result":{"cleaned":true}}`})
	sr.add("cp-storage-namespace-verify", scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"u","major_minor":"253:0"}}` + `}`})
	return sr
}
func submitRecoveryDelete(t *testing.T, sr *scriptRunner, opts ...StorageOption) (*db.Store, int64) {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	eng := tasks.NewEngine(store)
	all := []any{WithPodGuardChecker(noPodUsers)}
	for _, opt := range opts {
		all = append(all, opt)
	}
	RegisterStorageHandlers(eng, sr, store, all...)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"})
	if err != nil {
		t.Fatal(err)
	}
	return store, id
}
func TestDeleteLVRecoveryStopsOnFailedSafetyChecks(t *testing.T) {
	for _, tc := range []struct {
		name, command, out string
		code               int
		authorizer         NamespaceCleanupAuthorizer
		want               string
	}{
		{name: "disabled", want: "disabled"},
		{name: "unauthorized", authorizer: func(context.Context, string, string, []NamespaceHolder) error { return fmt.Errorf("not authorized") }, want: "not authorized"},
		{name: "scan_failure", command: "cp-storage-namespace-scan", out: `{"ok":false,"error":"permission denied","state_unknown":false}`, code: 1, authorizer: allowTestHolders, want: "namespace scan failed"},
		{name: "identity_changed", command: "cp-storage-namespace-scan", out: `{"ok":true,"result":{"device":{"uuid":"different","major_minor":"253:0"},"holders":[]}}`, authorizer: allowTestHolders, want: "identity changed"},
		{name: "unmount_failure", command: "cp-storage-namespace-cleanup", out: `{"ok":false,"error":"busy","state_unknown":false}`, code: 1, authorizer: allowTestHolders, want: "namespace cleanup failed"},
		{name: "unmount_timeout", command: "cp-storage-namespace-cleanup", code: 124, authorizer: allowTestHolders, want: "namespace cleanup failed"},
		{name: "device_busy", command: "cp-storage-namespace-verify", out: `{"ok":false,"error":"Open Count=1","state_unknown":false}`, code: 1, authorizer: allowTestHolders, want: "device release verification failed"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			sr := recoveryScriptRunner(t)
			if tc.command != "" {
				sr.add(tc.command, scriptResult{stdout: tc.out, exitCode: tc.code})
			}
			store, id := submitRecoveryDelete(t, sr, WithNamespaceCleanup(tc.authorizer, time.Minute, time.Second))
			waitFor(t, store, id, "failed", 2*time.Second)
			task, err := store.GetTask(context.Background(), id)
			if err != nil {
				t.Fatal(err)
			}
			if task.Error == nil || !strings.Contains(*task.Error, tc.want) {
				t.Fatalf("error=%v want %s", task.Error, tc.want)
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatalf("unsafe retry: %v", sr.counts)
			}
			steps, _ := store.ListSteps(context.Background(), id)
			for _, step := range steps {
				if step.Name == "cleanup_namespace_mounts" && (tc.name == "unmount_failure" || tc.name == "unmount_timeout") && step.Status != "failed" {
					t.Fatalf("falsely successful cleanup: %+v", step)
				}
			}
		})
	}
}
func TestDeleteLVRecoveryRechecksPodsBeforeCleanupAndRetry(t *testing.T) {
	for _, blockAt := range []int{3, 4} {
		t.Run(fmt.Sprint(blockAt), func(t *testing.T) {
			sr := recoveryScriptRunner(t)
			count := 0
			guard := func(context.Context, string, string) (bool, []string, error) {
				count++
				return count >= blockAt, []string{"new/business"}, nil
			}
			store, id := submitRecoveryDelete(t, sr, WithNamespaceCleanup(allowTestHolders, time.Minute, time.Second), WithPodGuardChecker(guard))
			waitFor(t, store, id, "failed", 2*time.Second)
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatalf("unsafe removal retry: %v", sr.counts)
			}
			if blockAt == 3 && sr.counts["cp-storage-namespace-cleanup"] != 0 {
				t.Fatal("cleaned despite new pod")
			}
		})
	}
}
func TestDeleteLVRecoveryReportsLatestRetryError(t *testing.T) {
	sr := recoveryScriptRunner(t)
	sr.add("lvremove -f /dev/vg_data/lv_1", scriptResult{stderr: "contains a filesystem in use", exitCode: 5}, scriptResult{stderr: "latest LVM error", exitCode: 7})
	store, id := submitRecoveryDelete(t, sr, WithNamespaceCleanup(allowTestHolders, time.Minute, time.Second))
	waitFor(t, store, id, "failed", 2*time.Second)
	task, _ := store.GetTask(context.Background(), id)
	if task.Error == nil || !strings.Contains(*task.Error, "latest LVM error") {
		t.Fatalf("lost latest error: %v", task.Error)
	}
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 2 {
		t.Fatal(sr.counts)
	}
}
