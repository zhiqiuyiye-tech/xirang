package storage

import (
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"runtime"
	"strconv"
	"strings"
	"testing"
)

// Exercise the complete generated shell program with fixture-only readlink,
// findmnt and dmsetup outputs. Only the block-device type check is replaced by
// a regular-file sentinel; no real device, /etc/fstab or /proc file is accessed.
func TestLVResizeFullProbeWithFixtures(t *testing.T) {
	shell := findPOSIXShell(t)
	awk, err := exec.LookPath("awk")
	if err != nil && runtime.GOOS == "windows" {
		candidate := filepath.Join(filepath.Dir(shell), "awk.exe")
		if _, statErr := os.Stat(candidate); statErr == nil {
			awk, err = candidate, nil
		}
	}
	if err != nil {
		t.Skip("awk unavailable for fixture-only full shell probe")
	}
	header := "Filename\tType\tSize\tUsed\tPriority\n"
	for _, tc := range []struct {
		name, mounts, fstab, swaps, opens string
		mountError, fstabError, openError int
		wantMounts, wantFstab             []string
		wantSwap                          bool
		wantOpen                          int
		wantErr                           bool
	}{
		{name: "unused LV with unrelated system fstab", fstab: "/dev/system\t/\n", opens: " 0 ", wantMounts: []string{}, wantFstab: []string{}},
		{name: "multiple mounts", mounts: "/data02/share\n/data03/bind\n", opens: "2", wantMounts: []string{"/data02/share", "/data03/bind"}, wantFstab: []string{}, wantOpen: 2},
		{name: "evaluated fstab alias", fstab: "/dev/mapper/target /data02/share\n", opens: "0", wantMounts: []string{}, wantFstab: []string{"/data02/share"}},
		{name: "active swap", swaps: header + "/dev/mapper/target\tpartition\t1024\t0\t-2\n", opens: "1", wantMounts: []string{}, wantFstab: []string{}, wantSwap: true, wantOpen: 1},
		{name: "protected target", fstab: "/dev/mapper/target /\n", opens: "0", wantErr: true},
		{name: "live query failure", mountError: 2, opens: "0", wantErr: true},
		{name: "fstab query failure", fstabError: 2, opens: "0", wantErr: true},
		{name: "unresolved fstab UUID", fstab: "UUID=unresolved /data02/share\n", opens: "0", wantErr: true},
		{name: "malformed mount target", mounts: "relative-target\n", opens: "0", wantErr: true},
		{name: "ambiguous open count", opens: "0\n1\n", wantErr: true},
		{name: "device query failure", openError: 1, opens: "0", wantErr: true},
		{name: "malformed swap row", swaps: header + "/dev/mapper/target\tpartition\n", opens: "0", wantErr: true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			dir := t.TempDir()
			device := filepath.ToSlash(filepath.Join(dir, "fixture-device"))
			fstab := filepath.ToSlash(filepath.Join(dir, "fixture-fstab"))
			swaps := filepath.ToSlash(filepath.Join(dir, "fixture-swaps"))
			if tc.swaps == "" {
				tc.swaps = header
			}
			for path, content := range map[string]string{device: "sentinel", fstab: tc.fstab, swaps: tc.swaps} {
				if err := os.WriteFile(path, []byte(content), 0600); err != nil {
					t.Fatal(err)
				}
			}
			command := buildLVResizeSafetyCommand("/dev/vg_data/lv_1")
			if !strings.Contains(command, `[ -b "$resolved" ]`) {
				t.Fatal("block-device check changed; update explicit fixture substitution")
			}
			command = strings.Replace(command, `[ -b "$resolved" ]`, `[ -f "$resolved" ]`, 1)
			command = strings.ReplaceAll(command, "/etc/fstab", shellLiteral(fstab))
			command = strings.ReplaceAll(command, "/proc/swaps", shellLiteral(swaps))
			mountStatus, fstabStatus := tc.mountError, tc.fstabError
			if mountStatus == 0 && tc.mounts == "" {
				mountStatus = 1
			}
			if fstabStatus == 0 && tc.fstab == "" {
				fstabStatus = 1
			}
			script := "awk() { " + shellLiteral(filepath.ToSlash(awk)) + " \"$@\"; }\n" +
				"readlink() { last=''; for arg in \"$@\"; do last=$arg; done; case \"$last\" in /dev/vg_data/lv_1|/dev/mapper/target) printf '%s\\n' " + shellLiteral(device) + ";; /dev/system) printf '%s\\n' '/fixture-other-device';; *) return 1;; esac; }\n" +
				"findmnt() { case \" $* \" in *' --fstab '*) printf '%s' " + shellLiteral(tc.fstab) + "; return " + strconv.Itoa(fstabStatus) + ";; *) printf '%s' " + shellLiteral(tc.mounts) + "; return " + strconv.Itoa(mountStatus) + ";; esac; }\n" +
				"dmsetup() { printf '%s' " + shellLiteral(tc.opens) + "; return " + strconv.Itoa(tc.openError) + "; }\n" + command
			output, runErr := exec.Command(shell, "-c", script).CombinedOutput()
			state, parseErr := parseLVResizeSafetyState(string(output))
			if tc.wantErr {
				if runErr == nil && parseErr == nil {
					t.Fatalf("unsafe/inconclusive fixture accepted: %+v", state)
				}
				return
			}
			if runErr != nil || parseErr != nil {
				t.Fatalf("full fixture probe failed: command=%v parser=%v output=%s", runErr, parseErr, output)
			}
			want := lvResizeSafetyState{MountTargets: tc.wantMounts, FstabTargets: tc.wantFstab, SwapActive: tc.wantSwap, DeviceOpenCount: tc.wantOpen}
			if !reflect.DeepEqual(state, want) {
				t.Fatalf("state=%+v want=%+v", state, want)
			}
		})
	}
}
