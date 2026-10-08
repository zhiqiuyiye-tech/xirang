package workers

import (
	"context"
	"errors"
	"fmt"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
	"time"
	"unicode/utf8"

	"xirang/control_panel/internal/db"
)

const npuSample = `+----------------------------------------------------------------------------------+
| npu-smi 24.1.0                    Version: 24.1.0                                |
| NPU     Name                     | Health                | Power(W)              |
| Chip    Device                   | Bus-Id                | AICore(%)             |
| 0       910B4                    | OK                    | 90.1                  |
| 0       0                        | 0000:81:00.0          | 0                     |
| 1       910B4                    | OK                    | 90.2                  |
| 0       1                        | 0000:82:00.0          | 0                     |
+----------------------------------------------------------------------------------+
| NPU     Chip       Process id    | Process name          | Process memory(MB)    |
| 0       0          12345         | python                | 1000                  |
| 1       0          67890         | python                | 1000                  |
+----------------------------------------------------------------------------------+`

type acceleratorSSHStub struct {
	workerSSHStub
	output string
	stderr string
	code   int
	err    error
	calls  int
}

func (s *acceleratorSSHStub) Run(ctx context.Context, w db.WorkerNode, cmd string) (string, string, int, error) {
	s.calls++
	if !strings.Contains(cmd, "npu-smi info") || !strings.Contains(cmd, "nvidia-smi") {
		return "", "", 1, errors.New("missing device discovery commands")
	}
	return s.output, s.stderr, s.code, s.err
}

type waitingAcceleratorSSH struct{ workerSSHStub }

func (s *waitingAcceleratorSSH) Run(ctx context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	<-ctx.Done()
	return "", "", -1, ctx.Err()
}

func TestAcceleratorTimeoutOptionIsEnforced(t *testing.T) {
	svc := setup(t)
	if svc.acceleratorTimeout != 45*time.Second {
		t.Fatalf("default budget=%s", svc.acceleratorTimeout)
	}
	svc = NewService(svc.store, svc.c, &waitingAcceleratorSSH{}, svc.eng, WithAcceleratorTimeout(20*time.Millisecond))
	info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
	if !strings.Contains(info.Error, "20ms") || !strings.Contains(info.Error, "WORKER_ACCELERATOR_TIMEOUT") || info.Total != nil {
		t.Fatalf("got %+v", info)
	}
}

func TestAcceleratorFailureDiagnostics(t *testing.T) {
	for _, tc := range []struct {
		name string
		stub acceleratorSSHStub
		want []string
	}{
		{name: "ssh stage", stub: acceleratorSSHStub{err: fmt.Errorf("ssh wait for command completion: %w", context.DeadlineExceeded)}, want: []string{"45s", "ssh wait for command completion", "context deadline exceeded"}},
		{name: "ssh authentication", stub: acceleratorSSHStub{err: errors.New("ssh handshake/authentication: unable to authenticate")}, want: []string{"handshake/authentication", "unable to authenticate"}},
		{name: "driver stderr", stub: acceleratorSSHStub{code: 3, stderr: "npu-smi: error while loading shared libraries: libdrvdsmi.so"}, want: []string{"exit=3", "libdrvdsmi.so"}},
		{name: "driver stdout", stub: acceleratorSSHStub{code: 1, output: "__NPU__\nFailed to initialize driver"}, want: []string{"exit=1", "Failed to initialize driver"}},
		{name: "both streams", stub: acceleratorSSHStub{code: 1, output: "Failed to initialize driver", stderr: "npu-smi info failed (exit=3)"}, want: []string{"exit=3", "Failed to initialize driver"}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			svc := setup(t)
			svc.sshm = &tc.stub
			info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			for _, want := range tc.want {
				if !strings.Contains(info.Error, want) {
					t.Fatalf("missing %q in diagnostic %q", want, info.Error)
				}
			}
			if info.Total != nil || info.Status != "unknown" {
				t.Fatalf("failure incorrectly has a known total: %+v", info)
			}
		})
	}
}

func TestAcceleratorProbeIdentifiesFailedTool(t *testing.T) {
	for _, want := range []string{"npu-smi info failed (exit=%s)", "nvidia-smi query failed (exit=%s)"} {
		if !strings.Contains(acceleratorProbeCommand, want) {
			t.Fatalf("probe does not identify failed tool %q", want)
		}
	}
}

func TestAcceleratorFailureDiagnosticIsBounded(t *testing.T) {
	svc := setup(t)
	svc.sshm = &acceleratorSSHStub{code: 1, stderr: strings.Repeat("驱动异常", 2000), output: strings.Repeat("输出", 2000)}
	info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
	if len([]rune(info.Error)) > 1200 {
		t.Fatalf("diagnostic is too long: %d", len([]rune(info.Error)))
	}
	if !utf8.ValidString(info.Error) {
		t.Fatal("diagnostic truncation broke UTF-8")
	}
}

func acceleratorTestBash(t *testing.T) string {
	t.Helper()
	bash, err := exec.LookPath("bash")
	if err != nil && runtime.GOOS == "windows" {
		if git, gitErr := exec.LookPath("git"); gitErr == nil {
			bash = filepath.Join(filepath.Dir(git), "..", "bin", "bash.exe")
			err = nil
		}
	}
	if err != nil {
		t.Skip("bash is not installed")
	}
	return bash
}

func TestProbeScriptSkipsNVIDIAAfterNPUSuccess(t *testing.T) {
	bash := acceleratorTestBash(t)
	script := "npu-smi() { printf '%s\\n' '" + npuSample + "'; }\n" +
		"nvidia-smi() { printf '/usr/bin/nvidia-smi: Permission denied\\n' >&2; return 126; }\n" + acceleratorProbeCommand
	output, runErr := exec.Command(bash, "-c", script).Output()
	if runErr != nil {
		t.Fatalf("irrelevant NVIDIA probe caused failure: err=%v output=%s", runErr, output)
	}
	if strings.Contains(string(output), "__NVIDIA__") || strings.Contains(string(output), "Permission denied") {
		t.Fatalf("NVIDIA was queried on an Ascend node: %s", output)
	}
	svc := setup(t)
	svc.sshm = &acceleratorSSHStub{output: string(output)}
	info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
	if info.Status != "available" || info.Total == nil || *info.Total != 2 || len(info.Devices) != 1 || info.Devices[0].Count != 2 || info.Error != "" || info.Source != "npu-smi" {
		t.Fatalf("unexpected single-vendor result: %+v", info)
	}
}

func TestProbeScriptUsesSingleVendorFallback(t *testing.T) {
	bash := acceleratorTestBash(t)
	for _, tc := range []struct {
		name, setup            string
		wantStatus, wantSource string
		wantTotal              int64
	}{
		{name: "NVIDIA only", setup: "command() { if [ \"$2\" = npu-smi ]; then return 1; fi; builtin command \"$@\"; }\n", wantStatus: "available", wantSource: "nvidia-smi", wantTotal: 1},
		{name: "failed Ascend tool on NVIDIA node", setup: "npu-smi() { printf 'Ascend driver unavailable\\n'; return 3; }\n", wantStatus: "available", wantSource: "nvidia-smi", wantTotal: 1},
		{name: "both tools fail", setup: "npu-smi() { printf 'Ascend driver unavailable\\n'; return 3; }\nnvidia-smi() { printf 'NVIDIA driver unavailable\\n'; return 126; }\n", wantStatus: "unknown"},
		{name: "neither tool available", setup: "command() { return 1; }\n", wantStatus: "unknown"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			script := "nvidia-smi() { printf 'GPU-a, NVIDIA A100\\n'; }\n" + tc.setup + acceleratorProbeCommand
			output, err := exec.Command(bash, "-c", script).Output()
			code := 0
			stderr := ""
			if err != nil {
				var exitErr *exec.ExitError
				if !errors.As(err, &exitErr) {
					t.Fatal(err)
				}
				code, stderr = exitErr.ExitCode(), string(exitErr.Stderr)
			}
			svc := setup(t)
			svc.sshm = &acceleratorSSHStub{output: string(output), stderr: stderr, code: code}
			info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			if info.Status != tc.wantStatus || info.Source != tc.wantSource {
				t.Fatalf("got %+v", info)
			}
			if tc.wantStatus == "available" {
				if code != 0 || info.Total == nil || *info.Total != tc.wantTotal || info.Error != "" {
					t.Fatalf("fallback contains irrelevant failure: code=%d info=%+v", code, info)
				}
			} else if info.Total != nil || info.Error == "" {
				t.Fatalf("failed detection should preserve diagnostics: %+v", info)
			}
		})
	}
}

func TestEmptyFallbackDoesNotHidePrimaryDriverFailure(t *testing.T) {
	svc := setup(t)
	svc.sshm = &acceleratorSSHStub{output: "__NPU__\nAscend driver unavailable\n__NPU_EXIT__=3\n__NVIDIA__\n__NVIDIA_EXIT__=0\n__SELECTED__=nvidia-smi\n"}
	info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
	if info.Total != nil || info.Error == "" || !strings.Contains(info.Error, "npu-smi") {
		t.Fatalf("empty fallback hid the real driver failure: %+v", info)
	}
}

func TestSuccessfulNPUIsPreservedWhenNVIDIAFails(t *testing.T) {
	for _, exit := range []int{126, 127} {
		t.Run(fmt.Sprint(exit), func(t *testing.T) {
			svc := setup(t)
			svc.sshm = &acceleratorSSHStub{output: "__NPU__\n" + npuSample + "\n__NPU_EXIT__=0\n__NVIDIA__\n/usr/bin/nvidia-smi: Permission denied\n" + fmt.Sprintf("__NVIDIA_EXIT__=%d\n", exit)}
			info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			if info.Status != "partial" || len(info.Devices) != 1 || info.Devices[0].Count != 2 || info.Source != "npu-smi" {
				t.Fatalf("valid NPU results discarded: %+v", info)
			}
			if info.Total != nil {
				t.Fatal("partial probe must not claim a complete physical total")
			}
			if !strings.Contains(info.Error, "nvidia-smi") || !strings.Contains(info.Error, fmt.Sprintf("exit=%d", exit)) || !strings.Contains(info.Error, "Permission denied") {
				t.Fatalf("missing per-tool error: %q", info.Error)
			}
		})
	}
}

func TestIndependentDeviceProbeResults(t *testing.T) {
	for _, tc := range []struct {
		name, output, status string
		count                int
		total                int64
	}{
		{"both succeed", "__NPU__\n" + npuSample + "\n__NPU_EXIT__=0\n__NVIDIA__\nGPU-a, NVIDIA A100\n__NVIDIA_EXIT__=0\n", "available", 2, 3},
		{"both fail", "__NPU__\ndriver failure\n__NPU_EXIT__=3\n__NVIDIA__\nPermission denied\n__NVIDIA_EXIT__=126\n", "unknown", 0, 0},
		{"nvidia survives npu failure", "__NPU__\ndriver failure\n__NPU_EXIT__=3\n__NVIDIA__\nGPU-a, NVIDIA A100\n__NVIDIA_EXIT__=0\n", "partial", 1, 0},
		{"npu survives unsupported nvidia output", "__NPU__\n" + npuSample + "\n__NPU_EXIT__=0\n__NVIDIA__\nunrecognized output\n__NVIDIA_EXIT__=0\n", "partial", 1, 0},
	} {
		t.Run(tc.name, func(t *testing.T) {
			svc := setup(t)
			svc.sshm = &acceleratorSSHStub{output: tc.output}
			info := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			if info.Status != tc.status || len(info.Devices) != tc.count {
				t.Fatalf("info=%+v", info)
			}
			if tc.status == "available" && (info.Total == nil || *info.Total != tc.total) {
				t.Fatalf("total=%v", info.Total)
			}
			if tc.status != "available" && info.Total != nil {
				t.Fatal("incomplete physical count should be unknown")
			}
		})
	}
}

func TestAscend25DualChipLayout(t *testing.T) {
	var output strings.Builder
	output.WriteString("| NPU Name | Health | Power(W) |\n| Chip Phy-ID | Bus-Id | AICore(%) |\n")
	for card := 0; card < 8; card++ {
		for chip := 0; chip < 2; chip++ {
			fmt.Fprintf(&output, "| %d Ascend910 | OK | 164.3 |\n| %d %d | 0000:9D:00.0 | 0 |\n", card, chip, card*2+chip)
		}
	}
	output.WriteString("| NPU Chip | Process id | Process name |\n| No running processes found in NPU 0 |\n")
	devices, err := parseNPUCards(output.String())
	if err != nil || len(devices) != 1 || devices[0].Model != "Ascend910" || devices[0].Count != 8 || devices[0].DeviceCount != 16 {
		t.Fatalf("got %+v, err=%v; want 8 cards and 16 devices", devices, err)
	}
}

func TestParseNPUCards(t *testing.T) {
	devices, err := parseNPUCards(npuSample)
	if err != nil || len(devices) != 1 || devices[0].Model != "Ascend 910B4" || devices[0].Count != 2 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}
func TestNPUCountsPhysicalCardsOnceAcrossChips(t *testing.T) {
	devices, err := parseNPUCards(npuSample + "\n| 0 910B4 | OK | 90 |\n| 1 910B4 | OK | 90 |\n| 2 Ascend 310P | OK | 20 |")
	if err != nil || len(devices) != 2 || devices[0].Model != "Ascend 310P" || devices[0].Count != 1 || devices[1].Model != "Ascend 910B4" || devices[1].Count != 2 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}
func TestNPUNumericModelAndChipContinuation(t *testing.T) {
	devices, err := parseNPUCards("| 0 910 | OK | 90 |\n| 0 0 | 0000:81:00.0 | 0 |\n| 1 310 | Warning | 20 |\n| 0 1 | 0000:82:00.0 | 0 |")
	if err != nil || len(devices) != 2 || devices[0].Model != "Ascend 310" || devices[0].Count != 1 || devices[1].Model != "Ascend 910" || devices[1].Count != 1 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}

func TestNPUUnrecognizedOutputIsUnknown(t *testing.T) {
	for _, output := range []string{"", "npu-smi: driver unavailable", "| 0 0 123 | python | 1024 |"} {
		if _, err := parseNPUCards(output); err == nil {
			t.Fatalf("accepted invalid output %q", output)
		}
	}
}
func TestParseNVIDIACards(t *testing.T) {
	devices, err := parseNVIDIACards("GPU-a, NVIDIA A100-SXM4-80GB\nGPU-b, NVIDIA A100-SXM4-80GB\nGPU-c, NVIDIA H100 PCIe\n")
	if err != nil || len(devices) != 2 || devices[0].Count != 2 || devices[1].Count != 1 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
	if _, err := parseNVIDIACards("driver failed"); err == nil {
		t.Fatal("accepted invalid output")
	}
}
func TestDiscoverAccelerators(t *testing.T) {
	cases := []struct {
		name, output string
		code         int
		sshErr       error
		status       string
		total        int64
	}{
		{name: "npu", output: "__NPU__\n" + npuSample, status: "available", total: 2},
		{name: "nvidia", output: "__NVIDIA__\nGPU-a, NVIDIA A100\n", status: "available", total: 1},
		{name: "zero cards", output: "__NVIDIA__\n", status: "available", total: 0},
		{name: "both", output: "__NPU__\n" + npuSample + "\n__NVIDIA__\nGPU-a, NVIDIA A100\n", status: "available", total: 3},
		{name: "unsupported", output: "__UNSUPPORTED__\n", status: "unknown"},
		{name: "driver failure", output: "__NPU__\ndriver unavailable", code: 1, status: "unknown"},
		{name: "ssh failure", sshErr: errors.New("connection failed"), status: "unknown"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			svc := setup(t)
			stub := &acceleratorSSHStub{output: tc.output, code: tc.code, err: tc.sshErr}
			svc.sshm = stub
			got := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			if got.Status != tc.status {
				t.Fatalf("got %+v", got)
			}
			if tc.status == "available" && (got.Total == nil || *got.Total != tc.total) {
				t.Fatalf("got %+v", got)
			}
			if tc.status == "unknown" && (got.Total != nil || got.Error == "") {
				t.Fatalf("failure should have unknown count: %+v", got)
			}
		})
	}
}
