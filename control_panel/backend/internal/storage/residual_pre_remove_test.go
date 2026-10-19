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
	stableIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	sr.add("cp-storage-namespace-inspect_lv", stableIdentity, stableIdentity)
	sr.add("cp-storage-namespace-scan_delete",
		scriptResult{stdout: holdersJSON(t, "stable-uuid", NamespaceHolderRef{PID: 123, Paths: []string{"/host-data/share"}})},
	)
	sr.add("nsenter -t 123 -m umount '/host-data/share'", scriptResult{})
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
				// Handbook 8.2: the holder's own copy is unmounted inside its
				// mount namespace before the final host unmount check.
				"cp-storage-namespace-scan_delete",
				"nsenter -t 123 -m umount '/host-data/share'",
				"logical volume is still mounted at:",
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

	for _, stage := range []string{"identity", "unmount_busy", "unmount_transport", "revalidate_identity"} {
		t.Run(stage, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			want := ""
			switch stage {
			case "identity":
				sr.add("cp-storage-namespace-scan_delete", scriptResult{stdout: holdersJSON(t, "replacement-uuid",
					NamespaceHolderRef{PID: 123, Paths: []string{"/host-data/share"}})})
				want = "identity changed"
			case "unmount_busy":
				sr.add("nsenter -t 123 -m umount '/host-data/share'", scriptResult{stderr: "target is busy", exitCode: 1})
				want = "namespace unmount failed"
			case "unmount_transport":
				sr.add("nsenter -t 123 -m umount '/host-data/share'", scriptResult{runErr: context.Canceled})
				want = "namespace unmount failed"
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

// The holder lookup only supplies the PID and mount path that the handbook
// unmount needs. A host whose evidence cannot be read must not block the
// handbook order, because lvremove itself refuses an in-use volume.
func TestHolderLookupFailureDoesNotBlockLvremove(t *testing.T) {
	for _, tc := range []struct {
		name  string
		stage scriptResult
	}{
		{
			name:  "evidence rejected",
			stage: scriptResult{stdout: `{"ok":false,"error":"permission denied reading namespace evidence","state_unknown":false}`, exitCode: 1},
		},
		{
			name:  "transport failure",
			stage: scriptResult{runErr: context.DeadlineExceeded},
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			sr := residualBeforeRemoveRunner(t)
			sr.add("cp-storage-namespace-scan_delete", tc.stage)
			store, id := submitDeleteTask(t, sr, "storage_delete_lv")
			waitFor(t, store, id, "succeeded", 2*time.Second)

			if sr.counts["nsenter -t 123 -m umount '/host-data/share'"] != 0 {
				t.Fatalf("a failed holder lookup must skip the handbook unmount: %v", sr.calls)
			}
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
				t.Fatalf("a failed holder lookup must not block lvremove: %v", sr.calls)
			}
			steps, err := store.ListSteps(context.Background(), id)
			if err != nil {
				t.Fatal(err)
			}
			lookup := -1
			for i, step := range steps {
				if step.Name == "scan_namespace_holders_before_remove" {
					lookup = i
				}
			}
			if lookup < 0 {
				t.Fatalf("holder lookup step was not recorded: %+v", steps)
			}
			recorded := steps[lookup]
			if recorded.Status != "failed" || recorded.Error == nil ||
				!strings.Contains(*recorded.Error, "namespace holder lookup failed") {
				t.Fatalf("lookup step must record the skipped unmount: %+v", recorded)
			}
			assertNoUnsafeDeleteEscalation(t, sr)
		})
	}
}

// Handbook 8.2: when the host unmount reports the target busy, a holder still
// has its own copy, so that copy is ordinarily unmounted inside its mount
// namespace and the host unmount is retried before the final check.
func TestBusyHostUnmountFallsBackToNamespaceUnmount(t *testing.T) {
	sr := residualBeforeRemoveRunner(t)
	sr.add("umount /data02/share",
		scriptResult{stderr: "umount: /data02/share: target is busy.", exitCode: 32},
		scriptResult{},
	)
	store, id := submitDeleteTask(t, sr, "storage_delete_lv")
	waitFor(t, store, id, "succeeded", 2*time.Second)

	if sr.counts["umount /data02/share"] != 2 {
		t.Fatalf("a busy host unmount must be retried after the holder release: %v", sr.calls)
	}
	if sr.counts["nsenter -t 123 -m umount '/host-data/share'"] != 1 {
		t.Fatalf("the holder's own copy must be released before the retry: %v", sr.calls)
	}
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
		t.Fatalf("deletion must still reach lvremove: %v", sr.calls)
	}
	commands := strings.Join(sr.calls, "\n")
	first := strings.Index(commands, "umount /data02/share")
	release := strings.Index(commands, "nsenter -t 123 -m umount '/host-data/share'")
	retry := strings.LastIndex(commands, "umount /data02/share")
	verify := strings.Index(commands, "logical volume is still mounted at:")
	if first < 0 || release <= first || retry <= release || verify <= retry {
		t.Fatalf("order must be host unmount, holder release, retry, final check: %v", sr.calls)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}

// A host mount that stays busy after the holder was released has a local user
// that is not the holder, so the volume is retained and that reason is reported
// instead of the holder.
func TestStillBusyHostUnmountRetainsVolume(t *testing.T) {
	sr := residualBeforeRemoveRunner(t)
	sr.add("umount /data02/share",
		scriptResult{stderr: "umount: /data02/share: target is busy.", exitCode: 32},
	)
	store, id := submitDeleteTask(t, sr, "storage_delete_lv")
	waitFor(t, store, id, "failed", 2*time.Second)
	task, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if task.Error == nil || !strings.Contains(*task.Error, "host unmount still failing after releasing holders") {
		t.Fatalf("error=%v", task.Error)
	}
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 0 {
		t.Fatalf("a still-busy host mount must retain the volume: %v", sr.calls)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}

// A mount that an actor already released between the lookup and the unmount is
// the state this step exists to produce, so it is not a deletion failure.
func TestAlreadyReleasedMountsAreNotDeletionFailures(t *testing.T) {
	sr := residualBeforeRemoveRunner(t)
	sr.add("umount /data02/share", scriptResult{stderr: "umount: /data02/share: not mounted.", exitCode: 32})
	sr.add("nsenter -t 123 -m umount '/host-data/share'", scriptResult{stderr: "umount: /host-data/share: not mounted.", exitCode: 32})
	store, id := submitDeleteTask(t, sr, "storage_delete_lv")
	waitFor(t, store, id, "succeeded", 2*time.Second)

	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 1 {
		t.Fatalf("an already-released mount must not block lvremove: %v", sr.calls)
	}
	if sr.counts["umount /data02/share"] != 1 {
		t.Fatalf("an already-released host mount needs no retry: %v", sr.calls)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}
