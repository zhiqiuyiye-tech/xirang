package storage

import (
	"context"
	"encoding/json"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

// holdersJSON builds one holder-lookup response. Every lookup result carries
// only the PID and paths the handbook unmount consumes.
func holdersJSON(t *testing.T, deviceUUID string, holders ...NamespaceHolderRef) string {
	t.Helper()
	if holders == nil {
		holders = []NamespaceHolderRef{}
	}
	data, err := json.Marshal(map[string]any{"ok": true, "result": NamespaceHolders{
		Device:  DeviceIdentity{UUID: deviceUUID, MajorMinor: "253:0"},
		Holders: holders,
	}})
	if err != nil {
		t.Fatal(err)
	}
	return string(data)
}

func recoveryScriptRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	empty := holdersJSON(t, "stable-uuid")
	holder := holdersJSON(t, "stable-uuid", NamespaceHolderRef{PID: 123, Paths: []string{"/data02/share"}})
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	sr.add("lvremove -f /dev/vg_data/lv_1",
		scriptResult{stderr: "Logical volume vg_data/lv_1 contains a filesystem in use.", exitCode: 5},
		scriptResult{stdout: "removed"},
	)
	// The ordinary path confirms no holders before the first lvremove. A later
	// actual filesystem-in-use result represents a new namespace holder race.
	sr.add("cp-storage-namespace-scan_delete",
		scriptResult{stdout: empty},
		scriptResult{stdout: holder},
	)
	sr.add("nsenter -t 123 -m umount '/data02/share'", scriptResult{})
	sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity, stableIdentity)
	return sr
}

func submitRecoveryDelete(t *testing.T, sr *scriptRunner, opts ...StorageOption) (*db.Store, int64) {
	t.Helper()
	return submitDeleteTask(t, sr, "storage_delete_lv", opts...)
}

func TestDeleteLVRecoveryStopsOnPhysicalSafetyFailures(t *testing.T) {
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	empty := holdersJSON(t, "stable-uuid")
	holder := holdersJSON(t, "stable-uuid", NamespaceHolderRef{PID: 123, Paths: []string{"/data02/share"}})
	replacement := holdersJSON(t, "replacement-uuid", NamespaceHolderRef{PID: 123, Paths: []string{"/data02/share"}})

	for _, tc := range []struct {
		name  string
		setup func(*scriptRunner)
		want  string
	}{
		{
			name: "fallback scan failure",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{stdout: `{"ok":false,"error":"permission denied","state_unknown":false}`, exitCode: 1},
				)
			},
			want: "namespace holder lookup failed",
		},
		{
			name: "fallback scan transport error",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{runErr: context.DeadlineExceeded},
				)
			},
			want: "namespace holder lookup failed",
		},
		{
			name: "fallback scan identity changed",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{stdout: replacement},
				)
			},
			want: "identity changed",
		},
		{
			name: "ordinary unmount busy",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{stdout: holder},
				)
				sr.add("nsenter -t 123 -m umount '/data02/share'",
					scriptResult{stderr: "target is busy", exitCode: 1},
				)
			},
			want: "namespace unmount failed",
		},
		{
			name: "unmount transport error",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{stdout: holder},
				)
				sr.add("nsenter -t 123 -m umount '/data02/share'", scriptResult{runErr: context.Canceled})
			},
			want: "namespace unmount failed",
		},
		{
			name: "LV UUID changed before retry",
			setup: func(sr *scriptRunner) {
				sr.add("cp-storage-namespace-scan_delete",
					scriptResult{stdout: empty},
					scriptResult{stdout: holder},
				)
				sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity,
					scriptResult{stdout: `{"ok":true,"result":{"uuid":"replacement-uuid","major_minor":"253:0"}}`},
				)
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

func TestUnmountFailureClassification(t *testing.T) {
	for _, tc := range []struct {
		out  string
		busy bool
		gone bool
	}{
		{"umount: /data02/x: target is busy.\n", true, false},
		{"umount: /data02/x: device is busy\n", true, false},
		{"umount: /data02/x: not mounted.\n", false, true},
		{"umount: /data02/x: mountpoint not found\n", false, true},
		{"umount: /data02/x: must be superuser\n", false, false},
		{"umount: /data02/x: invalid argument\n", false, false},
		{"", false, false},
	} {
		if got := isTargetBusy("", tc.out); got != tc.busy {
			t.Fatalf("%q isTargetBusy=%v want %v", tc.out, got, tc.busy)
		}
		if got := isNotMounted("", tc.out); got != tc.gone {
			t.Fatalf("%q isNotMounted=%v want %v", tc.out, got, tc.gone)
		}
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
	if sr.counts["cp-storage-namespace-scan_delete"] != 1 || sr.counts["nsenter -t 123 -m umount '/data02/share'"] != 0 {
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
