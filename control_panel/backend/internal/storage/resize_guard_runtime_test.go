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
		name, mounts, fstab, swaps, opens, fs, identity, mountTarget, pinnedFS string
		grow, shrink                                                           bool
	}{
		{name: "unused ext4", opens: "0", fs: "ext4", identity: "stable-uuid 253 0", grow: true, shrink: true},
		{name: "mounted ext4 online grow", mounts: "/data02/live\n", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true},
		{name: "mounted xfs online grow", mounts: "/data02/live\n", opens: "1", fs: "xfs", identity: "stable-uuid 253 0", mountTarget: "/data02/live", grow: true},
		{name: "unmounted xfs grow relies on -r", opens: "0", fs: "xfs", identity: "stable-uuid 253 0", grow: true},
		{name: "xfs mount target moved before resize", mounts: "/data02/moved\n", opens: "1", fs: "xfs", identity: "stable-uuid 253 0", mountTarget: "/data02/live"},
		{name: "mounted ext4 shrink", mounts: "/data02/live\n", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true},
		{name: "device held open after server probe", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true},
		{name: "swap after server probe", swaps: "Filename\tType\tSize\tUsed\tPriority\n/dev/mapper/target\tpartition\t1024\t0\t-2\n", opens: "0", fs: "ext4", identity: "stable-uuid 253 0"},
		{name: "identity replacement after server probe", opens: "0", fs: "ext4", identity: "replacement-uuid 253 1"},
		{name: "filesystem changed after server probe", opens: "0", fs: "xfs", identity: "stable-uuid 253 0", pinnedFS: "ext4"},
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
				pinnedFS := tc.pinnedFS
				if pinnedFS == "" {
					pinnedFS = tc.fs
				}
				wantMutation := tc.shrink
				if grow {
					wantMutation = tc.grow
				}
				req := ResizeLVReq{VGName: "vg_data", LVName: "lv_data", Grow: grow, DeltaGB: 10, FSType: pinnedFS}
				if grow && tc.mountTarget != "" {
					req.MountPoint = tc.mountTarget
				}
				if !resizeFilesystemSupported(grow, pinnedFS) {
					// An action the handbook does not cover (XFS shrink) must not
					// produce a mutating command at all.
					if _, err := buildGuardedResizeCommand(req, DeviceIdentity{UUID: "stable-uuid", MajorMinor: "253:0"}, []string{"/custom/protected"}); err == nil {
						t.Fatalf("unsupported %s resize built a guarded command", pinnedFS)
					}
					return
				}
				cmd, err := buildGuardedResizeCommand(req, DeviceIdentity{UUID: "stable-uuid", MajorMinor: "253:0"}, []string{"/custom/protected"})
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
					"lvextend() { printf '%s\\n' 'MUTATION-RAN'; }; lvreduce() { printf '%s\\n' 'MUTATION-RAN'; }\n" +
					"resize2fs() { printf '%s\\n' 'FS-MUTATION-RAN'; }; xfs_growfs() { printf '%s\\n' 'FS-MUTATION-RAN'; }\n" + cmd
				command := exec.Command(shell)
				// The generated script is delivered on stdin. Passing it as a -c
				// argument mangles its quoting on Windows shells, which would test
				// the transport instead of the script text.
				command.Stdin = strings.NewReader(script)
				output, runErr := command.CombinedOutput()
				mutated := strings.Contains(string(output), "MUTATION-RAN")
				if mutated != wantMutation || (wantMutation && runErr != nil) || (!wantMutation && runErr == nil) {
					t.Fatalf("mutation=%v want=%v err=%v output=%s", mutated, wantMutation, runErr, output)
				}
				if wantMutation {
					// Grow completes the filesystem explicitly: resize2fs for ext
					// and xfs_growfs for a mounted XFS; an unmounted XFS has no
					// completion command of its own.
					wantFS := grow && (strings.HasPrefix(tc.fs, "ext") || (tc.fs == "xfs" && tc.mountTarget != ""))
					if got := strings.Contains(string(output), "FS-MUTATION-RAN"); got != wantFS {
						t.Fatalf("filesystem completion=%v want=%v output=%s", got, wantFS, output)
					}
				}
			})
		}
	}
}
