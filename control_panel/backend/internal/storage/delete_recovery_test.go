package storage

import (
	"context"
	"encoding/json"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

func recoverySnapshotJSON(t *testing.T, snapshot NamespaceSnapshot) string {
	t.Helper()
	data, err := json.Marshal(map[string]any{"ok": true, "result": snapshot})
	if err != nil {
		t.Fatal(err)
	}
	return string(data)
}

func recoveryScriptRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	empty := namespaceTestSnapshot()
	empty.Device.UUID = "stable-uuid"
	empty.Holders = []NamespaceHolder{}
	holder := namespaceTestSnapshot()
	holder.Device.UUID = "stable-uuid"
	holder.Holders[0].Mounts[0].Path = "/data02/share"
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	sr.add("lvremove -f /dev/vg_data/lv_1",
		scriptResult{stderr: "Logical volume vg_data/lv_1 contains a filesystem in use.", exitCode: 5},
		scriptResult{stdout: "removed"},
	)
	// The ordinary path confirms no holders before the first lvremove. A later
	// actual filesystem-in-use result represents a new namespace holder race.
	sr.add("cp-storage-namespace-scan_delete",
		scriptResult{stdout: recoverySnapshotJSON(t, empty)},
		scriptResult{stdout: recoverySnapshotJSON(t, holder)},
	)
	sr.add("cp-storage-namespace-cleanup_delete", scriptResult{stdout: `{"ok":true,"result":{"cleaned":true}}`})
	sr.add("cp-storage-namespace-verify_delete", scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"stable-uuid","major_minor":"253:0"}}}`})
	sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity, stableIdentity)
	return sr
}

func submitRecoveryDelete(t *testing.T, sr *scriptRunner, opts ...StorageOption) (*db.Store, int64) {
	t.Helper()
	return submitDeleteTask(t, sr, "storage_delete_lv", opts...)
}

func TestDeleteLVRecoveryStopsOnPhysicalSafetyFailures(t *testing.T) {
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	empty := namespaceTestSnapshot()
	empty.Device.UUID = "stable-uuid"
	empty.Holders = []NamespaceHolder{}
	holder := namespaceTestSnapshot()
	holder.Device.UUID = "stable-uuid"
	holder.Holders[0].Mounts[0].Path = "/data02/share"
	replacement := namespaceTestSnapshot()
	replacement.Device.UUID = "replacement-uuid"
	replacement.Holders[0].Mounts[0].Path = "/data02/share"
	cleaned := scriptResult{stdout: `{"ok":true,"result":{"cleaned":true}}`}
	verified := scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"stable-uuid","major_minor":"253:0"}}}`}

	for _, tc := range []struct {
		name  string
		setup func(*scriptRunner)
		want  string
	}{
		{
			name: "fallback scan failure",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: `{"ok":false,"error":"permission denied","state_unknown":false}`, exitCode: 1},
				)
			},
			want: "namespace scan failed",
		},
		{
			name: "fallback scan transport error",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{runErr: context.DeadlineExceeded},
				)
			},
			want: "namespace scan failed",
		},
		{
			name: "fallback scan identity changed",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, replacement)},
				)
			},
			want: "identity changed",
		},
		{
			name: "ordinary cleanup busy",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, holder)},
				)
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{stdout: `{"ok":false,"error":"ordinary unmount busy","state_unknown":false}`, exitCode: 1})
			},
			want: "namespace cleanup failed",
		},
		{
			name: "cleanup timeout",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, holder)},
				)
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{exitCode: 124})
			},
			want: "namespace cleanup failed",
		},
		{
			name: "cleanup transport error",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, holder)},
				)
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{runErr: context.Canceled})
			},
			want: "namespace cleanup failed",
		},
		{
			name: "nonzero device open count",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, holder)},
				)
				sr.add("cp-storage-namespace-verify_delete", verified,
					scriptResult{stdout: `{"ok":false,"error":"Open Count=1","state_unknown":false}`, exitCode: 1},
				)
			},
			want: "device release verification failed",
		},
		{
			name: "LV UUID changed before retry",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: recoverySnapshotJSON(t, empty)},
					scriptResult{stdout: recoverySnapshotJSON(t, holder)},
				)
				sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity,
					scriptResult{stdout: `{"ok":true,"result":{"uuid":"replacement-uuid","major_minor":"253:0"}}`},
				)
				sr.add("cp-storage-namespace-cleanup_delete", cleaned)
				sr.add("cp-storage-namespace-verify_delete", verified)
			},
			want: "identity changed",
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			sr := recoveryScriptRunner(t)
			tc.setup(sr)
			store, id := submitRecoveryDelete(t, sr)
			waitFor(t, store, id, "failed", 2*time.Second)
			task, err := store.GetTask(context.Background(), id)
			if err != nil {
				t.Fatal(err)
			}
			if task.Error == nil || !strings.Contains(*task.Error, tc.want) {
				t.Fatalf("error=%v want %q", task.Error, tc.want)
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatalf("safety failure must retain the LV without retry: %v", sr.counts)
			}
			assertNoUnsafeDeleteEscalation(t, sr)
		})
	}
}

func TestDeleteLVDoesNotRetryLVMTransportFailure(t *testing.T) {
	sr := recoveryScriptRunner(t)
	sr.add("lvremove -f /dev/vg_data/lv_1", scriptResult{runErr: context.DeadlineExceeded})
	store, id := submitRecoveryDelete(t, sr)
	waitFor(t, store, id, "failed", 2*time.Second)
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
		t.Fatalf("LVM transport failure must not trigger a second remove: %v", sr.counts)
	}
	if sr.counts["cp-storage-namespace-scan_delete"] != 1 || sr.counts["cp-storage-namespace-cleanup_delete"] != 0 {
		t.Fatalf("transport failure must not enter namespace recovery: %v", sr.counts)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}

func TestDeleteLVRecoveryReportsLatestRetryError(t *testing.T) {
	sr := recoveryScriptRunner(t)
	sr.add("lvremove -f /dev/vg_data/lv_1",
		scriptResult{stderr: "contains a filesystem in use", exitCode: 5},
		scriptResult{stderr: "latest LVM error", exitCode: 7},
	)
	store, id := submitRecoveryDelete(t, sr)
	waitFor(t, store, id, "failed", 2*time.Second)
	task, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if task.Error == nil || !strings.Contains(*task.Error, "latest LVM error") {
		t.Fatalf("lost latest error: %v", task.Error)
	}
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 2 {
		t.Fatalf("filesystem-in-use fallback must make exactly one additional attempt: %v", sr.counts)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}
