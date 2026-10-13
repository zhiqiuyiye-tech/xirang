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

func TestResizeLVHandlerRejectsUnknownActionBeforeSSH(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	runner := newScriptRunner()
	RegisterStorageHandlers(eng, runner, store)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root"})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_resize_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_data", "action": "shrik", "delta_gb": 10,
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(runner.calls) != 0 {
		t.Fatalf("invalid action must not run an SSH command: %v", runner.calls)
	}
}

type resizeSafetyTaskResult struct {
	status    string
	taskError string
	runner    *scriptRunner
}

func runResizeSafetyTask(t *testing.T, action string, safetyResults, identityResults []scriptResult, reserved []string, checker PodGuardChecker, filesystem ...string) resizeSafetyTaskResult {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	runner := newScriptRunner()
	fsType := "ext4"
	if len(filesystem) > 0 {
		fsType = filesystem[0]
	}
	runner.add("cp-storage-resize-filesystem", scriptResult{stdout: fsType})
	runner.add("device='/dev/vg_data/lv_data'", safetyResults...)
	if identityResults != nil {
		runner.add("cp-storage-namespace-inspect", identityResults...)
	}
	opts := make([]any, 0, 2)
	if len(reserved) > 0 {
		opts = append(opts, WithReservedMounts(reserved...))
	}
	if checker != nil {
		opts = append(opts, WithPodGuardChecker(checker))
	}
	RegisterStorageHandlers(eng, runner, store, opts...)
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_resize_lv", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "lv_name": "lv_data", "action": action, "delta_gb": 10,
	})
	if err != nil {
		t.Fatal(err)
	}
	deadline := time.Now().Add(2 * time.Second)
	var got *db.Task
	for time.Now().Before(deadline) {
		got, err = store.GetTask(context.Background(), id)
		if err == nil && (got.Status == "succeeded" || got.Status == "failed") {
			break
		}
		time.Sleep(10 * time.Millisecond)
	}
	if got == nil || (got.Status != "succeeded" && got.Status != "failed") {
		t.Fatalf("resize task %d never reached a terminal state", id)
	}
	taskError := ""
	if got.Error != nil {
		taskError = *got.Error
	}
	return resizeSafetyTaskResult{status: got.Status, taskError: taskError, runner: runner}
}

func TestResizeLVHandlerRejectsUnsafeState(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	changedIdentity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"replacement-uuid","major_minor":"253:1"}}`}
	tests := []struct {
		name              string
		safety            []scriptResult
		identities        []scriptResult
		reserved          []string
		podMode           string
		wantProbeCount    int
		wantIdentityCount int
		wantPodCount      int
	}{
		{
			name:    "mounted data LV",
			safety:  []scriptResult{{stdout: `{"mount_targets":["/data02/live"],"fstab_targets":[],"swap_active":false,"device_open_count":0}`}},
			podMode: "unused",
		},
		{
			name:    "protected OS fstab target",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/etc/storage"],"swap_active":false,"device_open_count":0}`}},
			podMode: "unused",
		},
		{
			name:    "default reserved fstab target",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/data01/archive"],"swap_active":false,"device_open_count":0}`}},
			podMode: "unused",
		},
		{
			name:     "custom reserved fstab target",
			safety:   []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/custom/protected/archive"],"swap_active":false,"device_open_count":0}`}},
			reserved: []string{"/custom/protected"},
			podMode:  "unused",
		},
		{
			name:    "active swap",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":[],"swap_active":true,"device_open_count":0}`}},
			podMode: "unused",
		},
		{
			name:    "open device",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":1}`}},
			podMode: "unused",
		},
		{
			name:    "Pod in use",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`}},
			podMode: "in-use",
		},
		{
			name:    "Pod guard error",
			safety:  []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`}},
			podMode: "error",
		},
		{
			name:   "Pod guard unavailable for target path",
			safety: []scriptResult{{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`}},
		},
		{
			name:   "safety probe error",
			safety: []scriptResult{{stderr: "probe failed", exitCode: 1}},
		},
		{
			name:   "safety probe transport error",
			safety: []scriptResult{{runErr: context.Canceled}},
		},
		{
			name:   "malformed safety evidence",
			safety: []scriptResult{{stdout: `{not-json}`}},
		},
		{
			name:              "identity replaced during recheck probe",
			podMode:           "unused",
			safety:            []scriptResult{{stdout: unusedLVResizeState}, {stdout: unusedLVResizeState}},
			identities:        []scriptResult{identity, identity, identity, changedIdentity},
			wantIdentityCount: 4,
		},
		{
			name: "identity replaced during recheck Pod callback",
			safety: []scriptResult{
				{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`},
				{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`},
			},
			identities:        []scriptResult{identity, identity, identity, changedIdentity},
			podMode:           "unused",
			wantIdentityCount: 4,
			wantPodCount:      2,
		},
		{
			name:           "state becomes mounted during recheck",
			safety:         []scriptResult{{stdout: unusedLVResizeState}, {stdout: `{"mount_targets":["/data02/new"],"fstab_targets":[],"swap_active":false,"device_open_count":0}`}},
			identities:     []scriptResult{identity, identity},
			podMode:        "unused",
			wantProbeCount: 2,
		},
		{
			name: "Pod becomes in use during recheck",
			safety: []scriptResult{
				{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`},
				{stdout: `{"mount_targets":[],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":0}`},
			},
			identities:     []scriptResult{identity, identity},
			podMode:        "in-use-on-recheck",
			wantProbeCount: 2,
		},
	}
	for _, tc := range tests {
		for _, action := range []string{"grow", "shrink"} {
			t.Run(tc.name+"/"+action, func(t *testing.T) {
				var podPaths []string
				podCalls := 0
				var checker PodGuardChecker
				if tc.podMode != "" {
					checker = func(_ context.Context, _, exportPath string) (bool, []string, error) {
						podCalls++
						podPaths = append(podPaths, exportPath)
						switch tc.podMode {
						case "in-use":
							return true, []string{"default/business"}, nil
						case "in-use-on-recheck":
							return podCalls > 1, []string{"default/business"}, nil
						case "error":
							return false, nil, context.Canceled
						default:
							return false, nil, nil
						}
					}
				}
				result := runResizeSafetyTask(t, action, tc.safety, tc.identities, tc.reserved, checker)
				if result.status != "failed" {
					t.Fatalf("unsafe resize status=%q, want failed; commands=%v", result.status, result.runner.calls)
				}
				for _, command := range result.runner.calls {
					if strings.Contains(command, "lvextend -r -L ") || strings.Contains(command, "lvreduce -y -r -L ") {
						t.Fatalf("rejected resize issued mutation %q; commands=%v", command, result.runner.calls)
					}
				}
				if tc.wantProbeCount > 0 && result.runner.counts["device='/dev/vg_data/lv_data'"] != tc.wantProbeCount {
					t.Fatalf("safety probe count=%d, want %d", result.runner.counts["device='/dev/vg_data/lv_data'"], tc.wantProbeCount)
				}
				if tc.name == "mounted data LV" && (len(podPaths) != 1 || podPaths[0] != "/data02/live") {
					t.Fatalf("mounted path Pod guard calls=%v, want [/data02/live]", podPaths)
				}
				if tc.name == "protected OS fstab target" && (!strings.Contains(result.taskError, "protected system path") || !strings.Contains(result.taskError, `"/etc"`)) {
					t.Fatalf("protected fstab path failed for an unexpected reason: %q", result.taskError)
				}
				if tc.wantIdentityCount > 0 && result.runner.counts["cp-storage-namespace-inspect"] != tc.wantIdentityCount {
					t.Fatalf("identity inspections=%d, want %d", result.runner.counts["cp-storage-namespace-inspect"], tc.wantIdentityCount)
				}
				if tc.wantPodCount > 0 && len(podPaths) != tc.wantPodCount {
					t.Fatalf("Pod guard calls=%d, want %d (paths=%v)", len(podPaths), tc.wantPodCount, podPaths)
				}
			})
		}
	}
}

func TestResizeLVHandlerAllowsUnusedLV(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	for _, action := range []string{"grow", "shrink"} {
		t.Run(action, func(t *testing.T) {
			result := runResizeSafetyTask(t, action,
				[]scriptResult{{stdout: unusedLVResizeState}, {stdout: unusedLVResizeState}},
				[]scriptResult{identity, identity}, nil, noPodUsers)
			if result.status != "succeeded" {
				t.Fatalf("safe resize status=%q, want succeeded; commands=%v", result.status, result.runner.calls)
			}
			want := "lvextend -r -L +10G /dev/vg_data/lv_data"
			if action == "shrink" {
				want = "lvreduce -y -r -L -10G /dev/vg_data/lv_data"
			}
			if !strings.Contains(strings.Join(result.runner.calls, "\n"), want) || !strings.Contains(strings.Join(result.runner.calls, "\n"), "# cp-storage-safe-resize") {
				t.Fatalf("safe resize did not run guarded %q; commands=%v", want, result.runner.calls)
			}
			if result.runner.counts["device='/dev/vg_data/lv_data'"] != 3 {
				t.Fatalf("safe resize probe count=%d, want 3", result.runner.counts["device='/dev/vg_data/lv_data'"])
			}
			if result.runner.counts["cp-storage-namespace-inspect"] != 4 {
				t.Fatalf("safe resize probe identity inspection count=%d, want 4", result.runner.counts["cp-storage-namespace-inspect"])
			}
		})
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
	runErr   error
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
			return r.stdout, r.stderr, r.exitCode, r.runErr
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
	// Each disk: detect_vg + preflight + wipefs + pvcreate + vgcreate = 5 calls x 2 disks = 10.
	if len(sr.calls) != 10 {
		t.Fatalf("expected 10 calls, got %d: %v", len(sr.calls), sr.calls)
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
		if strings.Contains(call, "wipefs -a") || strings.Contains(call, "pvcreate") || strings.Contains(call, "vgcreate") {
			t.Fatalf("destructive command ran after failed preflight: %v", sr.calls)
		}
	}
}

func TestCreateVGHandlerReinitializesUnmountedFilesystemDiskAfterPreflight(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "absent"})
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb"},
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	if len(sr.calls) != 5 {
		t.Fatalf("expected VG detection, safety preflight, signature wipe, pvcreate, and vgcreate; calls=%v", sr.calls)
	}
	preflight := strings.Index(sr.calls[1], "cp-storage-preflight")
	freshPreflight := strings.Index(sr.calls[2], "cp-storage-preflight")
	wipe := strings.Index(sr.calls[2], "wipefs -a /dev/sdb")
	pvcreate := strings.Index(sr.calls[3], "pvcreate /dev/sdb")
	vgcreate := strings.Index(sr.calls[4], "vgcreate vg_data_sdb /dev/sdb")
	if preflight < 0 || freshPreflight < 0 || wipe < freshPreflight || pvcreate < 0 || vgcreate < 0 {
		t.Fatalf("expected safe signature clearing after a fresh preflight and before LVM initialization: %v", sr.calls)
	}
}

func TestCreateVGHandlerRevalidatesDiskBeforeClearingSignatures(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	sr := newScriptRunner()
	sr.add("vgs vg_data_sdb", scriptResult{stdout: "absent"})
	sr.add("cp-storage-preflight",
		scriptResult{stdout: "SAFE"},
		scriptResult{stderr: "device became mounted", exitCode: 1},
	)
	RegisterStorageHandlers(eng, sr, store, WithPodGuardChecker(noPodUsers))
	wid, err := store.CreateWorker(context.Background(), db.WorkerNode{
		Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password",
	})
	if err != nil {
		t.Fatal(err)
	}
	id, err := eng.Submit(context.Background(), "storage_create_vg", "storage", wid, map[string]any{
		"worker_id": wid, "vg_name": "vg_data", "disks": []string{"/dev/sdb"},
	})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	if len(sr.calls) != 3 || !strings.Contains(sr.calls[2], "cp-storage-preflight") || !strings.Contains(sr.calls[2], "wipefs -a /dev/sdb") {
		t.Fatalf("signature clearing must be guarded by a fresh preflight in the same remote command: %v", sr.calls)
	}
	for _, call := range sr.calls {
		if strings.Contains(call, "pvcreate /dev/sdb") || strings.Contains(call, "vgcreate vg_data_sdb /dev/sdb") {
			t.Fatalf("initialization continued after the fresh preflight rejected the disk: %v", sr.calls)
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
	// Two VG detections + PV membership check for sdb + preflight and three
	// initialization steps for sdc.
	if len(sr.calls) != 7 {
		t.Fatalf("expected 7 calls (existing VG check plus safe initialization), got %d: %v", len(sr.calls), sr.calls)
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
