package storage

import (
	"context"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func noPodUsers(context.Context, string, string) (bool, []string, error) { return false, nil, nil }

func submitDeleteTask(t *testing.T, sr *scriptRunner, kind string, opts ...StorageOption) (*db.Store, int64) {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "delete.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	eng := tasks.NewEngine(store)
	all := make([]any, 0, len(opts))
	for _, opt := range opts {
		all = append(all, opt)
	}
	RegisterStorageHandlers(eng, sr, store, all...)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), kind, "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	return store, id
}

func TestDeleteLVHandlerRejectsTargetWorkerMismatch(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	RegisterStorageHandlers(eng, sr, store)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid+1, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(sr.calls) != 0 {
		t.Fatalf("worker lock mismatch allowed SSH: %v", sr.calls)
	}
}

func TestReclaimHandlerStillReclaimsUnmountedVolumeSafely(t *testing.T) {
	sr := residualBeforeRemoveRunner(t)
	guardCalls, allowlistCalls := 0, 0
	store, id := submitDeleteTask(t, sr, "storage_reclaim_nfs",
		WithPodGuardChecker(func(context.Context, string, string) (bool, []string, error) {
			guardCalls++
			return true, []string{"default/business"}, nil
		}),
		WithNamespaceCleanup(func(context.Context, string, string, []NamespaceHolder) error {
			allowlistCalls++
			return context.Canceled
		}, time.Minute, time.Second),
	)
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if guardCalls != 0 || allowlistCalls != 0 {
		t.Fatalf("reclaim invoked optional Kubernetes/workload callbacks: pod=%d allowlist=%d", guardCalls, allowlistCalls)
	}

	commands := strings.Join(sr.calls, "\n")
	ordered := []int{
		strings.Index(commands, "sed -i '\\#^/data02/share #d' /etc/exports"),
		strings.Index(commands, "exportfs -arv"),
		strings.Index(commands, "umount /data02/share"),
		strings.Index(commands, "logical volume is still mounted at:"),
		strings.Index(commands, "# cp-storage-namespace-scan_delete"),
		strings.Index(commands, "# cp-storage-namespace-cleanup_delete"),
		strings.Index(commands, "# cp-storage-namespace-verify_delete"),
		strings.LastIndex(commands, "# cp-storage-namespace-inspect_lv"),
		strings.Index(commands, "lvremove -f /dev/vg_data/lv_1"),
		strings.Index(commands, "sed -i '\\#^/dev/vg_data/lv_1 #d' /etc/fstab"),
	}
	for i, position := range ordered {
		if position < 0 || (i > 0 && position <= ordered[i-1]) {
			t.Fatalf("reclaim did not follow the handbook deletion order: %v", sr.calls)
		}
	}
	if sr.counts["cp-storage-namespace-inspect_lv"] != 2 {
		t.Fatalf("expected initial and pre-remove LV identity checks, got %d", sr.counts["cp-storage-namespace-inspect_lv"])
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}

func TestDeleteAndReclaimRejectProtectedMountTargets(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		t.Run(kind, func(t *testing.T) {
			sr := newScriptRunner()
			sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data01/private\n"})
			store, id := submitDeleteTask(t, sr, kind)
			waitFor(t, store, id, "failed", 2*time.Second)
			for _, command := range sr.calls {
				if strings.Contains(command, "sed -i") || strings.Contains(command, "exportfs -arv") || strings.Contains(command, "umount ") || strings.Contains(command, "lvremove ") {
					t.Fatalf("protected mount target was mutated: %v", sr.calls)
				}
			}
		})
	}
}

func TestDeleteLVHandlerRejectsNonBasenameNames(t *testing.T) {
	for _, name := range []string{"../vg", "vg/other", "-option", "."} {
		t.Run(name, func(t *testing.T) {
			store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
			defer store.Close()
			eng := tasks.NewEngine(store)
			sr := newScriptRunner()
			RegisterStorageHandlers(eng, sr, store)
			id, _ := eng.Submit(context.Background(), "storage_delete_lv", "storage", 1, map[string]any{"worker_id": 1, "vg_name": name, "lv_name": "lv_1"})
			waitFor(t, store, id, "failed", 2*time.Second)
			if len(sr.calls) != 0 {
				t.Fatalf("unsafe name permitted SSH: %v", sr.calls)
			}
		})
	}
}
