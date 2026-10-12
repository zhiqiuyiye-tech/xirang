package storage

import (
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"testing"
)

func TestGuardedResizeRechecksLateWorkerStateBeforeMutation(t *testing.T) {
	shell := findPOSIXShell(t)
	python, err := exec.LookPath("python3")
	if runtime.GOOS == "windows" || err != nil {
		python, err = exec.LookPath("python")
	}
	if err != nil {
		t.Skip("Python unavailable for guarded command fixture")
	}
	awk, err := exec.LookPath("awk")
	if err != nil && runtime.GOOS == "windows" {
		awk = filepath.Join(filepath.Dir(shell), "awk.exe")
		_, err = os.Stat(awk)
	}
	if err != nil {
		t.Skip("awk unavailable for guarded command fixture")
	}
	for _, tc := range []struct {
		name, mounts, fstab, swaps, opens, fs, identity string
		wantMutation                                    bool
	}{
		{name: "unchanged safe ext4", opens: "0", fs: "ext4", identity: "stable-uuid 253 0", wantMutation: true},
		{name: "mounted after server probe", mounts: "/data02/new\n", opens: "0", fs: "ext4", identity: "stable-uuid 253 0"},
		{name: "opened after server probe", opens: "1", fs: "ext4", identity: "stable-uuid 253 0"},
		{name: "swap after server probe", swaps: "Filename\tType\tSize\tUsed\tPriority\n/dev/mapper/target\tpartition\t1024\t0\t-2\n", opens: "0", fs: "ext4", identity: "stable-uuid 253 0"},
		{name: "identity replacement after server probe", opens: "0", fs: "ext4", identity: "replacement-uuid 253 1"},
		{name: "unsupported xfs", opens: "0", fs: "xfs", identity: "stable-uuid 253 0"},
		{name: "reserved fstab after server probe", fstab: "/dev/mapper/target /custom/protected/volume\n", opens: "0", fs: "ext4", identity: "stable-uuid 253 0"},
		{name: "ambiguous identity", opens: "0", fs: "ext4", identity: "stable-uuid 253 0\nother-uuid 253 1"},
	} {
		for _, grow := range []bool{true, false} {
			t.Run(tc.name+"/grow="+strconv.FormatBool(grow), func(t *testing.T) {
				dir := t.TempDir()
				device := filepath.ToSlash(filepath.Join(dir, "device"))
				fstab := filepath.ToSlash(filepath.Join(dir, "fstab"))
				swaps := filepath.ToSlash(filepath.Join(dir, "swaps"))
				if tc.swaps == "" {
					tc.swaps = "Filename\tType\tSize\tUsed\tPriority\n"
				}
				for path, content := range map[string]string{device: "sentinel", fstab: tc.fstab, swaps: tc.swaps} {
					if err := os.WriteFile(path, []byte(content), 0600); err != nil {
						t.Fatal(err)
					}
				}
				cmd, err := buildGuardedResizeCommand(ResizeLVReq{VGName: "vg_data", LVName: "lv_data", Grow: grow, DeltaGB: 10}, DeviceIdentity{UUID: "stable-uuid", MajorMinor: "253:0"}, []string{"/custom/protected"})
				if err != nil {
					t.Fatal(err)
				}
				cmd = strings.Replace(cmd, `[ -b "$resolved" ]`, `[ -f "$resolved" ]`, 1)
				cmd = strings.ReplaceAll(cmd, "/etc/fstab", shellLiteral(fstab))
				cmd = strings.ReplaceAll(cmd, "/proc/swaps", shellLiteral(swaps))
				mountStatus, fstabStatus := 0, 0
				if tc.mounts == "" {
					mountStatus = 1
				}
				if tc.fstab == "" {
					fstabStatus = 1
				}
				script := "python3() { " + shellLiteral(filepath.ToSlash(python)) + " \"$@\"; }\n" +
					"awk() { " + shellLiteral(filepath.ToSlash(awk)) + " \"$@\"; }\n" +
					"readlink() { last=''; for arg in \"$@\"; do last=$arg; done; case \"$last\" in /dev/vg_data/lv_data|/dev/mapper/target) printf '%s\\n' " + shellLiteral(device) + ";; *) return 1;; esac; }\n" +
					"findmnt() { case \" $* \" in *' --fstab '*) printf '%s' " + shellLiteral(tc.fstab) + "; return " + strconv.Itoa(fstabStatus) + ";; *) printf '%s' " + shellLiteral(tc.mounts) + "; return " + strconv.Itoa(mountStatus) + ";; esac; }\n" +
					"dmsetup() { printf '%s' " + shellLiteral(tc.opens) + "; }\n" +
					"blkid() { printf '%s' " + shellLiteral(tc.fs) + "; }\n" +
					"lvs() { printf '%s' " + shellLiteral(tc.identity) + "; }\n" +
					"lvextend() { printf '%s\\n' 'MUTATION-RAN'; }; lvreduce() { printf '%s\\n' 'MUTATION-RAN'; }\n" + cmd
				output, runErr := exec.Command(shell, "-c", script).CombinedOutput()
				mutated := strings.Contains(string(output), "MUTATION-RAN")
				if mutated != tc.wantMutation || (tc.wantMutation && runErr != nil) || (!tc.wantMutation && runErr == nil) {
					t.Fatalf("mutation=%v want=%v err=%v output=%s", mutated, tc.wantMutation, runErr, output)
				}
			})
		}
	}
}
