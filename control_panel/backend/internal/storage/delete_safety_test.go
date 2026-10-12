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

func TestReclaimHandlerStillReclaimsUnusedMountedNFS(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1",
		scriptResult{stdout: "/data02/share\n"}, scriptResult{stdout: ""})
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	sr.add("cp-storage-namespace-inspect", identity, identity)
	var podPaths []string
	checker := func(_ context.Context, _, exportPath string) (bool, []string, error) {
		podPaths = append(podPaths, exportPath)
		return false, nil, nil
	}
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(checker))
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_reclaim_nfs", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if len(podPaths) != 2 || podPaths[0] != "/data02/share" || podPaths[1] != "/data02/share" {
		t.Fatalf("Pod guard paths=%v, want two checks of /data02/share", podPaths)
	}
	if sr.counts["cp-storage-namespace-inspect"] != 2 {
		t.Fatalf("LV identity inspect count=%d, want initial and pre-removal inspections", sr.counts["cp-storage-namespace-inspect"])
	}
	if sr.counts["findmnt -rn -o TARGET --source /dev/vg_data/lv_1"] != 2 {
		t.Fatalf("live mount lookup count=%d, want detection and unmounted verification", sr.counts["findmnt -rn -o TARGET --source /dev/vg_data/lv_1"])
	}

	commands := strings.Join(sr.calls, "\n")
	findmnt := strings.Index(commands, "findmnt -rn -o TARGET --source /dev/vg_data/lv_1")
	firstIdentity := strings.Index(commands, "# cp-storage-namespace-inspect")
	removeExport := strings.Index(commands, "sed -i '\\#^/data02/share #d' /etc/exports")
	exportfs := strings.Index(commands, "exportfs -arv")
	unmount := strings.Index(commands, "umount /data02/share")
	removeFstab := strings.Index(commands, "sed -i '\\#^/dev/vg_data/lv_1 #d' /etc/fstab")
	verifyUnmounted := strings.LastIndex(commands, "findmnt -rn -o TARGET --source /dev/vg_data/lv_1")
	lastIdentity := strings.LastIndex(commands, "# cp-storage-namespace-inspect")
	lvremove := strings.Index(commands, "lvremove -f /dev/vg_data/lv_1")
	ordered := []int{findmnt, firstIdentity, removeExport, exportfs, unmount, removeFstab, verifyUnmounted, lastIdentity, lvremove}
	for i, position := range ordered {
		if position < 0 || (i > 0 && position <= ordered[i-1]) {
			t.Fatalf("reclaim steps are missing or out of order: %v", sr.calls)
		}
	}
	if strings.Count(commands, "sed -i '\\#^") != 2 || strings.Count(commands, "sed -i '\\#^/data02/share #d' /etc/exports") != 1 {
		t.Fatalf("reclaim must remove only the target export and its LV fstab entry: %v", sr.calls)
	}
	steps, err := store.ListSteps(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	succeeded := map[string]bool{}
	for _, step := range steps {
		if step.Status == "succeeded" {
			succeeded[step.Name] = true
		}
	}
	for _, name := range []string{"detect_mount", "check_pod_usage", "verify_lv_identity", "remove_exports_line", "exportfs", "umount", "remove_fstab_line", "verify_unmounted", "verify_pod_usage", "verify_lv_identity_before_remove", "lvremove"} {
		if !succeeded[name] {
			t.Errorf("reclaim step %q did not succeed: %+v", name, steps)
		}
	}
}

func TestReclaimHandlerStillBlocksProtectedOrPodUsedTargets(t *testing.T) {
	tests := []struct {
		name    string
		mount   string
		checker PodGuardChecker
	}{
		{name: "reserved mount", mount: "/data01/private", checker: noPodUsers},
		{
			name:  "Pod consumer",
			mount: "/data02/share",
			checker: func(context.Context, string, string) (bool, []string, error) {
				return true, []string{"default/business"}, nil
			},
		},
	}
	for _, tc := range tests {
		t.Run(tc.name, func(t *testing.T) {
			store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
			if err != nil {
				t.Fatal(err)
			}
			defer store.Close()
			eng := tasks.NewEngine(store)
			sr := newScriptRunner()
			sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: tc.mount + "\n"})
			RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(tc.checker))
			wid, err := store.CreateWorker(context.Background(), db.WorkerNode{
				Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
			})
			if err != nil {
				t.Fatal(err)
			}
			id, err := eng.Submit(context.Background(), "storage_reclaim_nfs", "storage", wid, map[string]any{
				"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
			})
			if err != nil {
				t.Fatal(err)
			}
			waitFor(t, store, id, "failed", 2*time.Second)
			for _, command := range sr.calls {
				if strings.Contains(command, "lvremove -f /dev/vg_data/lv_1") {
					t.Fatalf("unsafe reclaim issued lvremove: %v", sr.calls)
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
			RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
			id, _ := eng.Submit(context.Background(), "storage_delete_lv", "storage", 1, map[string]any{"worker_id": 1, "vg_name": name, "lv_name": "lv_1"})
			waitFor(t, store, id, "failed", 2*time.Second)
			if len(sr.calls) != 0 {
				t.Fatalf("unsafe name permitted SSH: %v", sr.calls)
			}
		})
	}
}
