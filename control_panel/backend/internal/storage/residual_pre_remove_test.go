package storage

import (
	"context"
	"strings"
	"testing"
	"time"
)

func residualBeforeRemoveRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	snapshot := namespaceTestSnapshot()
	snapshot.Device.UUID = "stable-uuid"
	snapshot.Holders[0].Mounts[0].Path = "/host-data/share"
	snapshot.Holders[0].Mounts[0].Optional = []string{"shared:578"}
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity)
	sr.add("cp-storage-namespace-scan_delete", scriptResult{stdout: recoverySnapshotJSON(t, snapshot)})
	sr.add("cp-storage-namespace-cleanup_delete", scriptResult{stdout: `{"ok":true,"result":{"cleaned":true}}`})
	sr.add("cp-storage-namespace-verify_delete", scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"stable-uuid","major_minor":"253:0"}}}`})
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

func lastCommand(calls []string, needle string) int {
	for i := len(calls) - 1; i >= 0; i-- {
		if strings.Contains(calls[i], needle) {
			return i
		}
	}
	return -1
}

func TestResidualMountsAreClearedBeforeFirstLvremove(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		t.Run(kind, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			store, id := submitDeleteTask(t, sr, kind)
			waitFor(t, store, id, "succeeded", 2*time.Second)

			previous := -1
			orderedBeforeIdentity := []string{
				"sed -i '\\#^/data02/share #d' /etc/exports",
				"exportfs -arv",
				"umount /data02/share",
				"logical volume is still mounted at:",
				"cp-storage-namespace-scan_delete",
				"cp-storage-namespace-cleanup_delete",
				"cp-storage-namespace-verify_delete",
			}
			for _, command := range orderedBeforeIdentity {
				index := firstCommand(sr.calls, command)
				if index <= previous {
					t.Fatalf("missing or misordered pre-removal step %s: index=%d previous=%d calls=%v", command, index, previous, sr.calls)
				}
				previous = index
			}
			identity := lastCommand(sr.calls, "cp-storage-namespace-inspect_lv")
			if identity <= previous {
				t.Fatalf("LV identity was not revalidated after release verification: %v", sr.calls)
			}
			previous = identity
			for _, command := range []string{"lvremove -f /dev/vg_data/lv_1", "sed -i '\\#^/dev/vg_data/lv_1 #d' /etc/fstab"} {
				index := firstCommand(sr.calls, command)
				if index <= previous {
					t.Fatalf("missing or misordered pre-removal step %s: index=%d previous=%d calls=%v", command, index, previous, sr.calls)
				}
				previous = index
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatal("known residual holder must be released before the first lvremove")
			}
			assertNoUnsafeDeleteEscalation(t, sr)
		})
	}
}

func TestResidualFailuresRetainLVBeforeFirstLvremove(t *testing.T) {
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	changedIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"replacement-uuid","major_minor":"253:0"}}`}

	for _, stage := range []string{"scan", "scan_transport", "identity", "cleanup_busy", "cleanup_timeout", "cleanup_transport", "open_count", "verify_transport", "revalidate_identity"} {
		t.Run(stage, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			want := ""
			switch stage {
			case "scan":
				sr.add("cp-storage-namespace-scan_delete", scriptResult{stdout: `{"ok":false,"error":"permission denied","state_unknown":false}`, exitCode: 1})
				want = "namespace scan failed"
			case "scan_transport":
				sr.add("cp-storage-namespace-scan_delete", scriptResult{runErr: context.DeadlineExceeded})
				want = "namespace scan failed"
			case "identity":
				changedSnapshot := namespaceTestSnapshot()
				changedSnapshot.Device.UUID = "replacement-uuid"
				changedSnapshot.Holders[0].Mounts[0].Path = "/host-data/share"
				sr.add("cp-storage-namespace-scan_delete", scriptResult{stdout: recoverySnapshotJSON(t, changedSnapshot)})
				want = "identity changed"
			case "cleanup_busy":
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{stdout: `{"ok":false,"error":"ordinary unmount busy","state_unknown":false}`, exitCode: 1})
				want = "namespace cleanup failed"
			case "cleanup_timeout":
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{exitCode: 124})
				want = "namespace cleanup failed"
			case "cleanup_transport":
				sr.add("cp-storage-namespace-cleanup_delete", scriptResult{runErr: context.Canceled})
				want = "namespace cleanup failed"
			case "open_count":
				sr.add("cp-storage-namespace-verify_delete", scriptResult{stdout: `{"ok":false,"error":"Open Count=1","state_unknown":false}`, exitCode: 1})
				want = "device release verification failed"
			case "verify_transport":
				sr.add("cp-storage-namespace-verify_delete", scriptResult{runErr: context.DeadlineExceeded})
				want = "device release verification failed"
			case "revalidate_identity":
				sr.add("cp-storage-namespace-inspect_lv", stableIdentity, changedIdentity)
				want = "identity changed"
			}
			store, id := submitDeleteTask(t, sr, "storage_delete_lv")
			waitFor(t, store, id, "failed", 2*time.Second)
			task, err := store.GetTask(context.Background(), id)
			if err != nil {
				t.Fatal(err)
			}
			if task.Error == nil || !strings.Contains(*task.Error, want) {
				t.Fatalf("error=%v, want %q", task.Error, want)
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 0 {
				t.Fatalf("physical safety failure allowed lvremove: %v", sr.calls)
			}
			assertNoUnsafeDeleteEscalation(t, sr)
		})
	}
}
