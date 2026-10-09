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

func TestDeleteLVHandlerFailsClosedWithoutPodChecker(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"})
	RegisterStorageHandlers(eng, sr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, c := range sr.calls {
		if strings.Contains(c, "sed -i") || strings.Contains(c, "umount ") || strings.Contains(c, "lvremove ") {
			t.Fatalf("mutation without pod checker: %s", c)
		}
	}
}

func TestReclaimHandlerCannotBypassPodGuard(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(func(context.Context, string, string) (bool, []string, error) {
		return true, []string{"default/business"}, nil
	}))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	id, _ := eng.Submit(context.Background(), "storage_reclaim_nfs", "storage", wid, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "mount_point": "/data02/share"})
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, c := range sr.calls {
		if strings.Contains(c, "sed -i") || strings.Contains(c, "umount ") || strings.Contains(c, "lvremove ") {
			t.Fatalf("legacy reclaim bypassed guard: %s", c)
		}
	}
}

func TestDeleteLVHandlerRejectsTargetWorkerMismatch(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	id, _ := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid+1, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"})
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(sr.calls) != 0 {
		t.Fatalf("worker lock mismatch allowed SSH: %v", sr.calls)
	}
}

func TestDeleteLVHandlerRechecksPodImmediatelyBeforeRemoval(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	calls := 0
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(func(context.Context, string, string) (bool, []string, error) {
		calls++
		return calls > 1, []string{"new/business"}, nil
	}))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	id, _ := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1"})
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, c := range sr.calls {
		if strings.Contains(c, "lvremove ") {
			t.Fatalf("removed despite new pod: %v", sr.calls)
		}
	}
}

func TestDeleteLVHandlerRejectsNonBasenameNames(t *testing.T) {
	for _, name := range []string{"../vg", "vg/other", "-option", "."} {
		t.Run(name, func(t *testing.T) {
			store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
			defer store.Close()
			eng := tasks.NewEngine(store)
			sr := newScriptRunner()
			RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
			id, _ := eng.Submit(context.Background(), "storage_delete_lv", "storage", 1, map[string]any{"worker_id": 1, "vg_name": name, "lv_name": "lv_1"})
			waitFor(t, store, id, "failed", 2*time.Second)
			if len(sr.calls) != 0 {
				t.Fatalf("unsafe name permitted SSH: %v", sr.calls)
			}
		})
	}
}
