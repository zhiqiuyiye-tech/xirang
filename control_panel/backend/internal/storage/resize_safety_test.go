package storage

import (
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"regexp"
	"runtime"
	"strings"
	"testing"
)

const unusedLVResizeState = `{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":0}`

func TestBuildLVResizeSafetySwapProbeShell(t *testing.T) {
	header := "Filename\tType\tSize\tUsed\tPriority\n"
	cases := []struct {
		name    string
		swaps   string
		want    string
		wantErr bool
	}{
		{name: "standard tab header with no swap", swaps: header, want: "false"},
		{
			name:  "tab-delimited active swap",
			swaps: header + "/dev/vg_data/lv_1\tpartition\t1024\t0\t-2\n",
			want:  "true",
		},
		{
			name:  "space-delimited active swap",
			swaps: "Filename Type Size Used Priority\n/dev/vg_data/lv_1 partition 1024 0 -2\n",
			want:  "true",
		},
		{name: "malformed header", swaps: "Name\tType\tSize\tUsed\tPriority\n", wantErr: true},
		{
			name:    "malformed row",
			swaps:   header + "/dev/vg_data/lv_1\tpartition\t1024\n",
			wantErr: true,
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			got, err := runLVResizeSwapProbe(t, tc.swaps)
			if tc.wantErr {
				if err == nil {
					t.Fatalf("swap probe unexpectedly succeeded with output %q", got)
				}
				return
			}
			if err != nil {
				t.Fatalf("swap probe failed: %v; output: %s", err, got)
			}
			if got != tc.want {
				t.Fatalf("swap_active = %q, want %q", got, tc.want)
			}
		})
	}
}

func runLVResizeSwapProbe(t *testing.T, swaps string) (string, error) {
	t.Helper()
	shell := findPOSIXShell(t)
	command := buildLVResizeSafetyCommand("/dev/vg_data/lv_1")
	const startMarker = "swap_active=false\n{"
	const inputMarker = "} < /proc/swaps"
	start := strings.Index(command, startMarker)
	if start < 0 {
		t.Fatal("command is missing the swap probe block")
	}
	end := strings.Index(command[start:], inputMarker)
	if end < 0 {
		t.Fatal("command is missing the /proc/swaps input redirection")
	}
	block := command[start : start+end+len(inputMarker)]
	block = strings.Replace(block, inputMarker, `} <<'SWAP_FIXTURE'`, 1)
	fixture := strings.TrimSuffix(swaps, "\n")
	script := "fail() { printf '%s\\n' \"$1\" >&2; exit 1; }\n" +
		"readlink() { [ \"$1\" = -f ] && shift; [ \"$1\" = -- ] && shift; printf '%s\\n' \"$1\"; }\n" +
		"resolved='/dev/vg_data/lv_1'\n" + block + "\n" + fixture +
		"\nSWAP_FIXTURE\nprintf '%s\\n' \"$swap_active\"\n"
	output, err := exec.Command(shell, "-c", script).CombinedOutput()
	return strings.TrimSpace(string(output)), err
}

func findPOSIXShell(t *testing.T) string {
	t.Helper()
	if shell, err := exec.LookPath("sh"); err == nil {
		return shell
	}
	if shell, err := exec.LookPath("bash"); err == nil {
		return shell
	}
	if runtime.GOOS == "windows" {
		if git, err := exec.LookPath("git"); err == nil {
			candidate := filepath.Clean(filepath.Join(filepath.Dir(git), "..", "usr", "bin", "sh.exe"))
			if _, err := os.Stat(candidate); err == nil {
				return candidate
			}
		}
	}
	t.Skip("POSIX shell unavailable; this regression runs on Linux or with Git Bash")
	return ""
}

func TestBuildLVResizeSafetyCommand(t *testing.T) {
	cmd := buildLVResizeSafetyCommand("/dev/vg_data/lv_1")
	if !strings.Contains(cmd, `device='/dev/vg_data/lv_1'`) {
		t.Fatalf("LV device must be shell-quoted as one literal, command:\n%s", cmd)
	}
	for _, want := range []string{
		"readlink -f",
		"findmnt",
		"--fstab",
		"--evaluate",
		"--output SOURCE,TARGET",
		"/proc/swaps",
		"dmsetup",
		`"mount_targets"`,
		`"fstab_targets"`,
		`"swap_active"`,
		`"device_open_count"`,
	} {
		if !strings.Contains(cmd, want) {
			t.Errorf("safety command missing %q", want)
		}
	}
	mutatingCommand := regexp.MustCompile(`(?m)^[[:space:]]*(lvextend|lvreduce|lvremove|lvresize|umount|mount|sed|exportfs|tee|rm|mv)([[:space:]]|$)`)
	if match := mutatingCommand.FindString(cmd); match != "" {
		t.Errorf("read-only safety probe must not invoke mutating command token %q", strings.TrimSpace(match))
	}

	unsafeDevice := "/dev/vg_data/lv'; touch /tmp/pwned; #"
	unsafeCmd := buildLVResizeSafetyCommand(unsafeDevice)
	if strings.Contains(unsafeCmd, unsafeDevice) || strings.Contains(unsafeCmd, "touch /tmp/pwned") {
		t.Fatalf("invalid device path was interpolated into command:\n%s", unsafeCmd)
	}
	if !strings.Contains(unsafeCmd, "invalid logical volume device path") {
		t.Fatalf("invalid device path must produce a failing command, got:\n%s", unsafeCmd)
	}
}

func TestParseLVResizeSafetyState(t *testing.T) {
	t.Run("empty unused state", func(t *testing.T) {
		got, err := parseLVResizeSafetyState(unusedLVResizeState)
		if err != nil {
			t.Fatalf("parse unused state: %v", err)
		}
		want := lvResizeSafetyState{
			MountTargets: []string{}, FstabTargets: []string{},
			SwapActive: false, DeviceOpenCount: 0,
		}
		if !reflect.DeepEqual(got, want) {
			t.Fatalf("state = %#v, want %#v", got, want)
		}
	})

	t.Run("multiple targets are sorted and deduplicated", func(t *testing.T) {
		input := `{"mount_targets":["/data03/archive","/data02/lv_1/","/data02/lv_1"],"fstab_targets":["/data04/backup","/data02/lv_1","/data04/backup/"],"swap_active":false,"device_open_count":0}`
		got, err := parseLVResizeSafetyState(input)
		if err != nil {
			t.Fatalf("parse multiple targets: %v", err)
		}
		want := lvResizeSafetyState{
			MountTargets: []string{"/data02/lv_1", "/data03/archive"},
			FstabTargets: []string{"/data02/lv_1", "/data04/backup"},
			SwapActive:   false, DeviceOpenCount: 0,
		}
		if !reflect.DeepEqual(got, want) {
			t.Fatalf("state = %#v, want %#v", got, want)
		}
	})

	t.Run("active swap is retained", func(t *testing.T) {
		input := `{"mount_targets":[],"fstab_targets":[],"swap_active":true,"device_open_count":0}`
		got, err := parseLVResizeSafetyState(input)
		if err != nil {
			t.Fatalf("parse active swap state: %v", err)
		}
		if !got.SwapActive {
			t.Fatalf("swap_active = false, want true")
		}
	})

	t.Run("nonzero open count is retained", func(t *testing.T) {
		input := `{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":7}`
		got, err := parseLVResizeSafetyState(input)
		if err != nil {
			t.Fatalf("parse open-device state: %v", err)
		}
		if got.DeviceOpenCount != 7 {
			t.Fatalf("device_open_count = %d, want 7", got.DeviceOpenCount)
		}
	})

	t.Run("rejects malformed or trailing JSON", func(t *testing.T) {
		for _, input := range []string{
			`{"mount_targets":`,
			unusedLVResizeState + ` trailing`,
			unusedLVResizeState + ` {}`,
			`null`,
			`[]`,
		} {
			if _, err := parseLVResizeSafetyState(input); err == nil {
				t.Errorf("parseLVResizeSafetyState(%q) unexpectedly succeeded", input)
			}
		}
	})

	t.Run("rejects missing fields", func(t *testing.T) {
		missingFieldInputs := map[string]string{
			"mount_targets":     `{"fstab_targets":[],"swap_active":false,"device_open_count":0}`,
			"fstab_targets":     `{"mount_targets":[],"swap_active":false,"device_open_count":0}`,
			"swap_active":       `{"mount_targets":[],"fstab_targets":[],"device_open_count":0}`,
			"device_open_count": `{"mount_targets":[],"fstab_targets":[],"swap_active":false}`,
		}
		for field, input := range missingFieldInputs {
			if _, err := parseLVResizeSafetyState(input); err == nil {
				t.Errorf("missing %q unexpectedly succeeded: %s", field, input)
			}
		}
	})

	t.Run("rejects null or malformed safety values", func(t *testing.T) {
		for _, input := range []string{
			`{"mount_targets":null,"fstab_targets":[],"swap_active":false,"device_open_count":0}`,
			`{"mount_targets":[],"fstab_targets":null,"swap_active":false,"device_open_count":0}`,
			`{"mount_targets":[],"fstab_targets":[],"swap_active":null,"device_open_count":0}`,
			`{"mount_targets":[],"fstab_targets":[],"swap_active":"false","device_open_count":0}`,
			`{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":null}`,
			`{"mount_targets":"/data02/lv_1","fstab_targets":[],"swap_active":false,"device_open_count":0}`,
		} {
			if _, err := parseLVResizeSafetyState(input); err == nil {
				t.Errorf("malformed evidence unexpectedly succeeded: %s", input)
			}
		}
	})

	t.Run("rejects negative open count", func(t *testing.T) {
		input := `{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":-1}`
		if _, err := parseLVResizeSafetyState(input); err == nil {
			t.Fatal("negative device_open_count unexpectedly succeeded")
		}
	})

	t.Run("rejects invalid targets in both lists", func(t *testing.T) {
		for _, field := range []string{"mount_targets", "fstab_targets"} {
			for _, target := range []string{"", "relative/path", "/", "/etc", "/data02/../etc", "/data02/a b"} {
				var input string
				if field == "mount_targets" {
					input = `{"mount_targets":[` + `"` + target + `"` + `],"fstab_targets":[],"swap_active":false,"device_open_count":0}`
				} else {
					input = `{"mount_targets":[],"fstab_targets":[` + `"` + target + `"` + `],"swap_active":false,"device_open_count":0}`
				}
				if _, err := parseLVResizeSafetyState(input); err == nil {
					t.Errorf("invalid %s target %q unexpectedly succeeded", field, target)
				}
			}
		}
	})

	t.Run("rejects duplicate keys and unknown fields", func(t *testing.T) {
		for _, input := range []string{
			`{"mount_targets":[],"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":0}`,
			`{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":0,"extra":true}`,
		} {
			if _, err := parseLVResizeSafetyState(input); err == nil {
				t.Errorf("ambiguous or unknown JSON field unexpectedly succeeded: %s", input)
			}
		}
	})
}
