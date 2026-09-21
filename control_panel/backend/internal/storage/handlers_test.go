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
	if len(mr.calls) != 8 {
		t.Fatalf("expected 8 calls, got %d: %v", len(mr.calls), mr.calls)
	}
}

func TestProvisionHandlerFailureTriggersRollback(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	mr := &mockRunner{failAt: 4} // mount fails
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
	RegisterStorageHandlers(eng, sr, store)
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
	RegisterStorageHandlers(eng, sr, store)
	wid, _ := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	id, err := eng.Submit(context.Background(), "install_deps", "worker", wid, map[string]any{"worker_id": wid})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	// 6 commands: detect_pm, check_deps, install, verify, configure_nfs_v4, enable_nfs_service
	if len(sr.calls) != 6 {
		t.Fatalf("expected 6 calls, got %d: %v", len(sr.calls), sr.calls)
	}
}

func TestInstallDeps_UnsupportedDistro(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	// detect_pm returns empty -> ParsePM error -> fail
	sr.add("echo yum", scriptResult{stdout: ""})
	RegisterStorageHandlers(eng, sr, store)
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
	RegisterStorageHandlers(eng, sr, store)
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
	RegisterStorageHandlers(eng, sr, store)
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
	// Each disk: detect_vg + pvcreate + vgcreate = 3 calls x 2 disks = 6.
	if len(sr.calls) != 6 {
		t.Fatalf("expected 6 calls, got %d: %v", len(sr.calls), sr.calls)
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

// TestCreateVGHandler_SkipsExistingVG verifies idempotency: a disk whose
// derived VG already exists is skipped (no pvcreate/vgcreate for it), while a
// disk whose VG is absent is still created.
func TestCreateVGHandler_SkipsExistingVG(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	// sdb's VG already exists -> skip; sdc's is absent -> create.
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "exists"})
	sr.add("vgs vg_data_sdc", scriptResult{stdout: "absent"})
	RegisterStorageHandlers(eng, sr, store)
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
	// sdb: detect only (exists -> skip). sdc: detect + pvcreate + vgcreate.
	// Total = 1 + 3 = 4.
	if len(sr.calls) != 4 {
		t.Fatalf("expected 4 calls (skip existing), got %d: %v", len(sr.calls), sr.calls)
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
