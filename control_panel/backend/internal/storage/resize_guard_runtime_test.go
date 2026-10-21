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
		// fsUncovered reports a mounted ext filesystem that still lags the
		// enlarged device, so the completion command has to run. statUnavailable
		// simulates the mount disappearing between the safety probe and the
		// completion step.
		fsUncovered, statUnavailable bool
	}{
		{name: "unused ext4", opens: "0", fs: "ext4", identity: "stable-uuid 253 0", grow: true, shrink: true},
		{name: "mounted ext4 online grow already covers the device", mounts: "/data02/live\n", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true, mountTarget: "/data02/live"},
		{name: "mounted ext4 online grow still short", mounts: "/data02/live\n", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true, mountTarget: "/data02/live", fsUncovered: true},
		{name: "mounted ext4 grow whose mount vanished", mounts: "/data02/live\n", opens: "1", fs: "ext4", identity: "stable-uuid 253 0", grow: true, mountTarget: "/data02/live", statUnavailable: true},
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
				// The kernel's statvfs view of a mounted filesystem and the
				// device size decide whether the ext completion has work to do.
				fsBlocks, fsUnit, deviceBytes := "1000", "4096", "4096000"
				if tc.fsUncovered {
					deviceBytes = "8192000"
				}
				statFn := "stat() { case \"$3\" in %b) printf '%s\\n' " + fsBlocks + ";; %S) printf '%s\\n' " + fsUnit + ";; *) return 1;; esac; }\n"
				if tc.statUnavailable {
					statFn = "stat() { return 1; }\n"
				}
				script := "python3() { " + shellLiteral(filepath.ToSlash(python)) + " \"$@\"; }\n" +
					"awk() { " + shellLiteral(filepath.ToSlash(awk)) + " \"$@\"; }\n" +
					"readlink() { last=''; for arg in \"$@\"; do last=$arg; done; case \"$last\" in /dev/vg_data/lv_data|/dev/mapper/target) printf '%s\\n' " + shellLiteral(device) + ";; *) return 1;; esac; }\n" +
					"findmnt() { case \" $* \" in *' --fstab '*) printf '%s' " + shellLiteral(tc.fstab) + "; return " + strconv.Itoa(fstabStatus) + ";; *) printf '%s' " + shellLiteral(tc.mounts) + "; return " + strconv.Itoa(mountStatus) + ";; esac; }\n" +
					"dmsetup() { printf '%s' " + shellLiteral(tc.opens) + "; }\n" +
					"blkid() { printf '%s' " + shellLiteral(tc.fs) + "; }\n" +
					"lvs() { printf '%s' " + shellLiteral(tc.identity) + "; }\n" +
					statFn +
					"blockdev() { printf '%s\\n' " + deviceBytes + "; }\n" +
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
					// Grow completes the filesystem explicitly only when it has
					// work left: an unmounted ext volume always runs the handbook
					// resize2fs, a mounted ext volume runs it only when the kernel's
					// size still lags the device, and a mounted XFS completes with
					// xfs_growfs. An unmounted XFS has no completion command.
					wantFS := false
					switch {
					case grow && strings.HasPrefix(tc.fs, "ext") && tc.mountTarget == "":
						wantFS = true
					case grow && strings.HasPrefix(tc.fs, "ext"):
						wantFS = tc.fsUncovered || tc.statUnavailable
					case grow && tc.fs == "xfs" && tc.mountTarget != "":
						wantFS = true
					}
					if got := strings.Contains(string(output), "FS-MUTATION-RAN"); got != wantFS {
						t.Fatalf("filesystem completion=%v want=%v output=%s", got, wantFS, output)
					}
				}
			})
		}
	}
}
