package storage

import (
	"context"
	"io"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

type mockRunner struct {
	failAt int // 1-based step index to fail; 0 = never
	calls  []string
}

func (m *mockRunner) Run(_ context.Context, _ db.WorkerNode, cmd string) (string, string, int, error) {
	m.calls = append(m.calls, cmd)
	if m.failAt > 0 && len(m.calls) == m.failAt {
		return "", "boom", 1, nil
	}
	if strings.Contains(cmd, "lvs --noheadings -o lv_name") {
		return "", "", 0, nil
	}
	return "ok", "", 0, nil
}

func (m *mockRunner) RunWithStdin(_ context.Context, _ db.WorkerNode, cmd string, _ io.Reader) (string, string, int, error) {
	return m.Run(context.Background(), db.WorkerNode{}, cmd)
}

func TestProvisionHandlerSuccess(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	mr := &mockRunner{}
	RegisterStorageHandlers(eng, mr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	params := map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "size_gb": 100.0,
		"fs_type": "xfs", "mount_point": "/data02/nb",
	}
	id, err := eng.Submit(context.Background(), "storage_provision_nfs", "storage", wid, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if len(mr.calls) != 9 {
		t.Fatalf("expected 9 calls, got %d: %v", len(mr.calls), mr.calls)
	}
}

func TestProvisionHandlerRejectsDuplicateLVName(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("lvs --noheadings -o lv_name '/dev/vg_data/lv_1'", scriptResult{stdout: " lv_1\n"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_provision_nfs", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "size_gb": 100.0,
		"fs_type": "ext4", "mount_point": "/data02/nfs_lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	got, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Error == nil || !contains(*got.Error, "already exists") {
		t.Fatalf("error=%v, want duplicate LV name rejection", got.Error)
	}
	for _, call := range sr.calls {
		if strings.Contains(call, "lvcreate") || strings.Contains(call, "mkfs.") {
			t.Fatalf("no destructive command should run for an existing LV: %v", sr.calls)
		}
	}
}

func TestProvisionHandlerFailureTriggersRollback(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	mr := &mockRunner{failAt: 5} // mount fails after the LV-name check
	RegisterStorageHandlers(eng, mr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, _ := eng.Submit(context.Background(), "storage_provision_nfs", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "size_gb": 100.0,
		"fs_type": "xfs", "mount_point": "/data02/nb",
	})
	waitFor(t, store, id, "failed", 2*time.Second)
	// 7 provision steps (4th fails) + rollback: done=[lvcreate,mkfs,mkdir]
	// rollback undoes lvcreate -> lvremove. Verify lvremove was called.
	found := false
	for _, c := range mr.calls {
		if contains(c, "lvremove") {
			found = true
		}
	}
	if !found {
		t.Fatalf("rollback did not call lvremove; calls=%v", mr.calls)
	}
}

// TestProvisionHandlerRejectsExportOptsInjection verifies the export_opts
// command-injection fix: a payload containing a single quote (which would
// break out of the single-quoted echo in the exports step) fails the task
// BEFORE any command is run on the worker.
func TestProvisionHandlerRejectsExportOptsInjection(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	mr := &mockRunner{}
	RegisterStorageHandlers(eng, mr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, _ := eng.Submit(context.Background(), "storage_provision_nfs", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "size_gb": 100.0,
		"fs_type": "xfs", "mount_point": "/data02/nb",
		"export_opts": "'; touch /tmp/PWNED; '",
	})
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(mr.calls) != 0 {
		t.Fatalf("no command should run for a rejected task, got: %v", mr.calls)
	}
	got, _ := store.GetTask(context.Background(), id)
	if got.Error == nil || !contains(*got.Error, "export_opts") {
		t.Fatalf("error=%v, want export_opts rejection", got.Error)
	}
}

// TestProvisionHandlerRejectsBadSize verifies size_gb <= 0 is rejected before
// any command runs (previously it relied on lvcreate failing downstream).
func TestProvisionHandlerRejectsBadSize(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	mr := &mockRunner{}
	RegisterStorageHandlers(eng, mr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, _ := eng.Submit(context.Background(), "storage_provision_nfs", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1", "size_gb": 0,
		"fs_type": "xfs", "mount_point": "/data02/nb",
	})
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(mr.calls) != 0 {
		t.Fatalf("no command should run for a rejected task, got: %v", mr.calls)
	}
}

func waitFor(t *testing.T, store *db.Store, id int64, want string, timeout time.Duration) {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		got, err := store.GetTask(context.Background(), id)
		if err == nil && got.Status == want {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("task %d never reached %s", id, want)
}

// --- scriptRunner: per-command-substring mock returning ordered results ---

type scriptResult struct {
	stdout   string
	stderr   string
	exitCode int
}

// scriptRunner implements ssh.Runner by matching command substrings to a list
// of ordered results. Each call to a matching substring consumes the next
// result (or repeats the last if exhausted). This lets tests return different
// outputs for the same command on successive calls (e.g. check_deps returns
// "not installed" first, then "installed" on verify).
type scriptRunner struct {
	scripts map[string][]scriptResult
	counts  map[string]int
	calls   []string
}

func newScriptRunner() *scriptRunner {
	return &scriptRunner{scripts: map[string][]scriptResult{}, counts: map[string]int{}}
}

func (s *scriptRunner) add(sub string, results ...scriptResult) {
	s.scripts[sub] = results
}

func (s *scriptRunner) Run(_ context.Context, _ db.WorkerNode, cmd string) (string, string, int, error) {
	s.calls = append(s.calls, cmd)
	for sub, results := range s.scripts {
		if strings.Contains(cmd, sub) {
			idx := s.counts[sub]
			if idx >= len(results) {
				idx = len(results) - 1
			}
			s.counts[sub]++
			r := results[idx]
			return r.stdout, r.stderr, r.exitCode, nil
		}
	}
	if strings.Contains(cmd, "$(id -u)") {
		return "root\n", "", 0, nil
	}
	if strings.Contains(cmd, "cp-storage-namespace-scan") {
		return `{"ok":true,"result":{"device":{"uuid":"u","major_minor":"253:0"},"holders":[]}}`, "", 0, nil
	}
	if strings.Contains(cmd, "cp-storage-namespace-inspect") {
		return `{"ok":true,"result":{"uuid":"u","major_minor":"253:0"}}`, "", 0, nil
	}
	if strings.Contains(cmd, "cp-storage-preflight") {
		return "SAFE\n", "", 0, nil
	}
	return "", "", 0, nil
}

func (s *scriptRunner) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, _ io.Reader) (string, string, int, error) {
	return s.Run(ctx, w, cmd)
}

// --- install_deps handler tests (4 paths) ---

func TestInstallDeps_AllAlreadyInstalled(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("echo yum", scriptResult{stdout: "yum\n"})
	sr.add("echo lvm2_ok", scriptResult{stdout: "lvm2_ok\nnfs_ok\n"})
	sr.add("nfs.conf", scriptResult{stdout: ""})
	sr.add("systemctl enable", scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "install_deps", "worker", wid, map[string]any{"worker_id": wid})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	// Idempotent: install command must NOT be called (already installed -> skip)
	for _, c := range sr.calls {
		if strings.Contains(c, "install") && !strings.Contains(c, "systemctl") {
			t.Fatalf("package install command should not be called; calls=%v", sr.calls)
		}
	}
	// Verify NFSv4 config and systemctl enable steps were executed
	hasConf, hasEnable := false, false
	for _, c := range sr.calls {
		if strings.Contains(c, "nfs.conf") {
			hasConf = true
		}
		if strings.Contains(c, "systemctl enable") {
			hasEnable = true
		}
	}
	if !hasConf || !hasEnable {
		t.Fatalf("expected nfs.conf and systemctl enable steps, calls=%v", sr.calls)
	}
}

func TestInstallDeps_InstallSuccess(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("echo yum", scriptResult{stdout: "yum\n"})
	// check_deps: first call returns empty (not installed), verify: second call returns installed
	sr.add("echo lvm2_ok",
		scriptResult{stdout: ""},
		scriptResult{stdout: "lvm2_ok\nnfs_ok\n"},
	)
	sr.add("yum install", scriptResult{stdout: ""})
	sr.add("nfs.conf", scriptResult{stdout: ""})
	sr.add("systemctl enable", scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "install_deps", "worker", wid, map[string]any{"worker_id": wid})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	// 7 commands: privilege, detect_pm, check_deps, install, verify, configure_nfs_v4, enable_nfs_service
	if len(sr.calls) != 7 {
		t.Fatalf("expected 7 calls, got %d: %v", len(sr.calls), sr.calls)
	}
}

func TestInstallDeps_UnsupportedDistro(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	// detect_pm returns empty -> ParsePM error -> fail
	sr.add("echo yum", scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "install_deps", "worker", wid, map[string]any{"worker_id": wid})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
}

func TestInstallDeps_VerifyStillMissing(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("echo yum", scriptResult{stdout: "yum\n"})
	// check_deps: empty (not installed), verify: still empty (install didn't work)
	sr.add("echo lvm2_ok",
		scriptResult{stdout: ""},
		scriptResult{stdout: ""},
	)
	sr.add("yum install", scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "install_deps", "worker", wid, map[string]any{"worker_id": wid})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
}

// --- create_vg handler tests (per-disk VG) ---

// TestCreateVGHandler_CreatesOneVGPerDisk verifies each selected disk gets its
// own vgcreate (named <prefix>_<basename>) and the task succeeds.
func TestCreateVGHandler_CreatesOneVGPerDisk(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	// vgs <name> -> absent for both disks (neither VG exists yet).
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "absent"})
	sr.add("vgs vg_data_sdc", scriptResult{stdout: "absent"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb", "/dev/sdc"},
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	// Each disk: preflight + detect_vg + pvcreate + vgcreate = 4 calls x 2 disks = 8.
	if len(sr.calls) != 8 {
		t.Fatalf("expected 8 calls, got %d: %v", len(sr.calls), sr.calls)
	}
	// vgcreate uses a per-disk name, one disk each.
	var creates []string
	for _, c := range sr.calls {
		if strings.Contains(c, "vgcreate ") {
			creates = append(creates, c)
		}
	}
	if len(creates) != 2 {
		t.Fatalf("expected 2 vgcreate calls, got %v", creates)
	}
	if !contains(creates[0], "vg_data_sdb /dev/sdb") || !contains(creates[1], "vg_data_sdc /dev/sdc") {
		t.Fatalf("per-disk vgcreate wrong: %v", creates)
	}
}

func TestCreateVGHandler_StopsWhenPreflightRejectsReservedDisk(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("cp-storage-preflight", scriptResult{stderr: "device belongs to reserved mount /data01", exitCode: 1})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, _ := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb"},
	})
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, call := range sr.calls {
		if strings.Contains(call, "pvcreate") || strings.Contains(call, "vgcreate") {
			t.Fatalf("destructive command ran after failed preflight: %v", sr.calls)
		}
	}
}

// TestCreateVGHandler_SkipsExistingVG verifies idempotency: a disk whose
// derived VG already exists is skipped (no pvcreate/vgcreate for it), while a
// disk whose VG is absent is still created.
func TestCreateVGHandler_SkipsExistingVG(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	// sdb's VG already exists and its PV membership matches; sdc's VG is absent.
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "exists"})
	sr.add("pvs --noheadings -o vg_name '/dev/sdb'", scriptResult{stdout: " vg_data_sdb\n"})
	// If preflight runs for the already-initialized sdb, it must reject the active VG.
	sr.add("device='/dev/sdb'", scriptResult{stderr: "device belongs to active volume group: vg_data_sdb", exitCode: 1})
	sr.add("vgs vg_data_sdc", scriptResult{stdout: "absent"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb", "/dev/sdc"},
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	// Two preflights; sdb: detect only (exists -> skip); sdc: detect + pvcreate + vgcreate.
	// Total = 2 + 1 + 3 = 6.
	if len(sr.calls) != 6 {
		t.Fatalf("expected 6 calls (preflight + skip existing), got %d: %v", len(sr.calls), sr.calls)
	}
	// No pvcreate/vgcreate touching sdb.
	for _, c := range sr.calls {
		if strings.Contains(c, "/dev/sdb") && (strings.Contains(c, "pvcreate") || strings.Contains(c, "vgcreate")) {
			t.Fatalf("existing-VG disk sdb should be skipped, got call: %s", c)
		}
	}
	// sdc vgcreate present.
	found := false
	for _, c := range sr.calls {
		if strings.Contains(c, "vgcreate vg_data_sdc /dev/sdc") {
			found = true
		}
	}
	if !found {
		t.Fatalf("sdc vgcreate missing; calls=%v", sr.calls)
	}
}

func TestCreateVGHandler_RejectsVGNameCollisionOnDifferentPV(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "exists"})
	sr.add("pvs --noheadings -o vg_name '/dev/sdb'", scriptResult{stdout: "vg_other\n"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb"},
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	got, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Error == nil || !strings.Contains(*got.Error, "belongs to vg_other") {
		t.Fatalf("error=%v, want existing VG membership conflict", got.Error)
	}
	for _, call := range sr.calls {
		if strings.Contains(call, "cp-storage-preflight") || strings.Contains(call, "pvcreate") || strings.Contains(call, "vgcreate") {
			t.Fatalf("device must not be initialized when VG name belongs to another PV: %v", sr.calls)
		}
	}
}

func TestDeleteLVHandlerUnmountsAllMountTargets(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1",
		scriptResult{stdout: "/data02/share\n/data02/share/sub\n"},
		scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	commands := strings.Join(sr.calls, "\n")
	subMount := strings.Index(commands, "umount /data02/share/sub")
	parentMount := strings.Index(commands, "umount /data02/share\n")
	userCheck := strings.Index(commands, "fuser -vm /data02/share/sub")
	verifyUnmounted := strings.LastIndex(commands, "findmnt -rn -o TARGET --source /dev/vg_data/lv_1")
	lvremove := strings.Index(commands, "lvremove -f /dev/vg_data/lv_1")
	if subMount < 0 || parentMount < 0 || subMount > parentMount {
		t.Fatalf("all mount targets must be unmounted deepest-first: %v", sr.calls)
	}
	if userCheck < 0 || userCheck > subMount {
		t.Fatalf("mount users should be diagnosed before unmount: %v", sr.calls)
	}
	if verifyUnmounted <= parentMount || lvremove <= verifyUnmounted {
		t.Fatalf("LV removal must follow unmount verification: %v", sr.calls)
	}
}

func TestDeleteLVHandlerDoesNotRemoveStillMountedLV(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1",
		scriptResult{stdout: "/data02/share\n"},
		scriptResult{stderr: "logical volume is still mounted at: /data02/share", exitCode: 1})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	for _, call := range sr.calls {
		if strings.Contains(call, "lvremove -f /dev/vg_data/lv_1") {
			t.Fatalf("lvremove ran while the LV was still mounted: %v", sr.calls)
		}
	}
	got, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Error == nil || !strings.Contains(*got.Error, "still mounted") {
		t.Fatalf("error=%v, want a remaining-mount diagnostic", got.Error)
	}
}

func TestDeleteLVHandlerExplainsInUseLVAfterUnmount(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1",
		scriptResult{stdout: "/data02/share\n"},
		scriptResult{stdout: ""})
	sr.add("lvremove -f /dev/vg_data/lv_1", scriptResult{
		stderr: "Logical volume vg_data/lv_1 contains a filesystem in use.", exitCode: 5,
	})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	got, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Error == nil || !strings.Contains(*got.Error, "check open file handles and other mount namespaces") {
		t.Fatalf("error=%v, want safe in-use guidance", got.Error)
	}
}

func TestDeleteLVHandler_BlockedByActivePod(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"})

	podChecker := func(ctx context.Context, workerHost, exportPath string) (bool, []string, error) {
		return true, []string{"default/promtail-f8vmv (hostPath)", "prod/notebook-1 (pvc: nb-data)"}, nil
	}

	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(podChecker))
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "storage_delete_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_1",
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	got, err := store.GetTask(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Error == nil || !strings.Contains(*got.Error, "cannot delete: volume is in use by pods") {
		t.Fatalf("error=%v, want blocked by pods message", got.Error)
	}
	// Verify no umount or lvremove ran
	for _, call := range sr.calls {
		if strings.Contains(call, "umount") || strings.Contains(call, "lvremove") {
			t.Fatalf("destructive command ran despite active pod blocker: %v", sr.calls)
		}
	}
}

func TestDeleteLVHandler_CleansNamespaceMountsAndRetriesLvremove(t *testing.T) {
	sr := recoveryScriptRunner(t)
	store, id := submitRecoveryDelete(t, sr, WithNamespaceCleanup(allowTestHolders, time.Minute, time.Second))
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 2 || sr.counts["cp-storage-namespace-cleanup"] != 1 || sr.counts["cp-storage-namespace-verify"] != 1 {
		t.Fatalf("unexpected recovery attempts: %v", sr.counts)
	}
	steps, err := store.ListSteps(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	var firstFailed, retrySucceeded bool
	for _, step := range steps {
		if step.Name == "lvremove" && step.Status == "failed" {
			firstFailed = true
		}
		if step.Name == "lvremove_retry" && step.Status == "succeeded" {
			retrySucceeded = true
		}
	}
	if !firstFailed || !retrySucceeded {
		t.Fatalf("original failure or successful retry lost: %+v", steps)
	}
}
