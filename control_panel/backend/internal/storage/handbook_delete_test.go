package storage

import (
	"context"
	"fmt"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func TestHandbookDeletionHasNoKubernetesOrMaintenancePrerequisites(t *testing.T) {
	for _, kind := range []string{"storage_delete_lv", "storage_reclaim_nfs"} {
		t.Run(kind, func(t *testing.T) {
			store, err := db.Open(filepath.Join(t.TempDir(), "handbook.db"))
			if err != nil {
				t.Fatal(err)
			}
			defer store.Close()
			sr := residualBeforeRemoveRunner(t)
			eng := tasks.NewEngine(store)
			guardCalls, authCalls := 0, 0
			RegisterStorageHandlers(eng, sr, store,
				WithPodGuardChecker(func(context.Context, string, string) (bool, []string, error) {
					guardCalls++
					return true, []string{"calico(hostPath)", "notebook(pvc)"}, nil
				}),
				WithNamespaceCleanup(func(context.Context, string, string, []NamespaceHolder) error {
					authCalls++
					return fmt.Errorf("allowlist intentionally empty")
				}, time.Minute, time.Second),
			)
			wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
			id, err := eng.Submit(context.Background(), kind, "storage", wid, map[string]any{
				"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "maintenance_confirmed": true,
			})
			if err != nil {
				t.Fatal(err)
			}
			waitFor(t, store, id, "succeeded", 2*time.Second)
			if guardCalls != 0 || authCalls != 0 {
				t.Fatalf("handbook still invoked Kubernetes: guards=%d auth=%d", guardCalls, authCalls)
			}
			previous := -1
			for _, needle := range []string{"sed -i '\\#^/data02/share #d' /etc/exports", "exportfs -arv", "umount /data02/share", "cp-storage-namespace-scan_delete", "nsenter -t 123 -m umount", "lvremove -f /dev/vg_data/lv_1", "sed -i '\\#^/dev/vg_data/lv_1 #d' /etc/fstab"} {
				index := firstCommand(sr.calls, needle)
				if index <= previous {
					t.Fatalf("missing or unordered handbook operation %s: %d <= %d", needle, index, previous)
				}
				previous = index
			}
			for _, cmd := range sr.calls {
				if strings.HasPrefix(cmd, "# cp-storage-namespace-host_") || strings.Contains(cmd, "umount -f ") || strings.Contains(cmd, "umount -l ") {
					t.Fatal("not an ordinary handbook unmount")
				}
			}
		})
	}
}
