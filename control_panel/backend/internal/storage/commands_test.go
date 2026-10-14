package storage

import (
	"strings"
	"testing"
)

func TestValidateName_OK(t *testing.T) {
	for _, n := range []string{"lv_notebook_200g", "vg_data", "data02"} {
		if err := ValidateName(n); err != nil {
			t.Fatalf("unexpected err for %q: %v", n, err)
		}
	}
}

func TestValidateName_Bad(t *testing.T) {
	for _, n := range []string{"lv;rm -rf", "a|b", "c&d", "x$y", "with space", ""} {
		if err := ValidateName(n); err == nil {
			t.Fatalf("expected err for %q", n)
		}
	}
}

func TestValidateMountPoint(t *testing.T) {
	reserved := []string{"/data01"}
	// Valid mounts
	for _, m := range []string{"/data02/nb", "/data02", "/mnt/storage", "/opt/data"} {
		if err := ValidateMountPoint(m, reserved); err != nil {
			t.Fatalf("unexpected err for %q: %v", m, err)
		}
	}
	// Invalid mounts: relative, root, protected system, reserved
	for _, m := range []string{"", "relative/path", "/", "/boot", "/boot/efi", "/etc", "/etc/exports", "/var/log", "/run", "/run/containerd", "/run/containerd/io.containerd", "/data01", "/data01/sub"} {
		if err := ValidateMountPoint(m, reserved); err == nil {
			t.Fatalf("expected err for mount point %q", m)
		}
	}
}

func TestValidateMountPointRejectsRunFstabFixture(t *testing.T) {
	_, err := parseLVResizeSafetyState(`{"mount_targets":[],"fstab_targets":["/run/containerd"],"swap_active":false,"device_open_count":0}`)
	if err == nil || !strings.Contains(err.Error(), `fstab_targets target "/run/containerd"`) {
		t.Fatalf("protected fstab target was not rejected: %v", err)
	}
}

func TestProvisionSteps(t *testing.T) {
	steps := ProvisionSteps(ProvisionReq{
		VGName: "vg_data", LVName: "lv_200g", SizeGB: 200, FSType: "xfs",
		MountPoint: "/data02/nb", ExportOpts: "*(rw,sync,no_root_squash,no_subtree_check)",
	})
	if len(steps) != 8 {
		t.Fatalf("expected 8 steps, got %d", len(steps))
	}
	if steps[0].Name != "lvcreate" || steps[0].Cmd != "lvcreate -y -L 200G -n lv_200g vg_data" {
		t.Fatalf("step0 wrong: %+v", steps[0])
	}
	if steps[1].Cmd != "mkfs.xfs /dev/vg_data/lv_200g" {
		t.Fatalf("step1 wrong: %s", steps[1].Cmd)
	}
	// step4 fstab: idempotent sed dedupe then append
	if !contains(steps[4].Cmd, "/dev/vg_data/lv_200g /data02/nb xfs defaults 0 0") {
		t.Fatalf("fstab step wrong: %s", steps[4].Cmd)
	}
	if !contains(steps[4].Cmd, "sed -i") {
		t.Fatalf("fstab not idempotent: %s", steps[4].Cmd)
	}
	// step5 exports
	if !contains(steps[5].Cmd, "/data02/nb") || !contains(steps[5].Cmd, "no_root_squash") {
		t.Fatalf("exports step wrong: %s", steps[5].Cmd)
	}
	wantExportsNewlineGuard := `if [ -s /etc/exports ] && [ -n "$(tail -c 1 /etc/exports)" ]; then printf '\n' >> /etc/exports; fi`
	if !strings.Contains(steps[5].Cmd, wantExportsNewlineGuard) {
		t.Fatalf("exports step must terminate an existing unterminated line before appending: %s", steps[5].Cmd)
	}
	if strings.Index(steps[5].Cmd, wantExportsNewlineGuard) > strings.LastIndex(steps[5].Cmd, `echo '/data02/nb `) {
		t.Fatalf("exports newline guard must run before appending the export: %s", steps[5].Cmd)
	}
	// step6 ensure_nfs
	if steps[6].Name != "ensure_nfs" || !contains(steps[6].Cmd, "systemctl") {
		t.Fatalf("ensure_nfs step wrong: %+v", steps[6])
	}
	// step7 exportfs
	if steps[7].Name != "exportfs" || steps[7].Cmd != "exportfs -arv" {
		t.Fatalf("exportfs step wrong: %+v", steps[7])
	}
}

func TestValidateExportOpts(t *testing.T) {
	// Legitimate export option strings pass.
	for _, s := range []string{
		"",
		"*(rw,sync,no_root_squash,no_subtree_check)",
		"192.168.0.0/24(rw,async)",
		"host.example.com(ro) 10.0.0.0/8(rw,no_wdelay)",
		"*(ro,root_squash)",
	} {
		if err := ValidateExportOpts(s); err != nil {
			t.Fatalf("unexpected err for %q: %v", s, err)
		}
	}
	// Injection payloads are rejected: each of these would break out of the
	// single-quoted echo in the exports step.
	for _, s := range []string{
		"'; rm -rf /; '",
		"') && touch /tmp/pwned && echo '",
		"$(reboot)",
		"`reboot`",
		"rw;shutdown -h now",
		"rw & reboot",
		"rw | cat /etc/shadow",
		"rw\n10.0.0.1(rw)",
	} {
		if err := ValidateExportOpts(s); err == nil {
			t.Fatalf("expected err for %q", s)
		}
	}
}

func TestReclaimStepsReverse(t *testing.T) {
	steps := ReclaimSteps(ReclaimReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: "/data02/nb"})
	if len(steps) != 5 {
		t.Fatalf("expected 5 steps, got %d", len(steps))
	}
	if steps[0].Name != "remove_exports_line" || !contains(steps[0].Cmd, "sed -i") {
		t.Fatalf("step0 wrong: %+v", steps[0])
	}
	if steps[4].Cmd != "lvremove -f /dev/vg_data/lv_200g" {
		t.Fatalf("last step not lvremove: %s", steps[4].Cmd)
	}
}

func TestValidateDisk(t *testing.T) {
	for _, d := range []string{"/dev/sdb", "/dev/nvme0n1", "/dev/disk/by-id/wwn-0x5000c500a"} {
		if err := ValidateDisk(d); err != nil {
			t.Fatalf("unexpected err for %q: %v", d, err)
		}
	}
	for _, d := range []string{"/dev/sdb;rm -rf", "sdb", "/dev/sdb$(x)", "/dev/sdb && echo", "/dev/sdb x", ""} {
		if err := ValidateDisk(d); err == nil {
			t.Fatalf("expected err for %q", d)
		}
	}
}

func TestPreflightDeviceRequiresSignatureProbe(t *testing.T) {
	cmd := PreflightDeviceCmd("/dev/sdb", []string{"/data01"})
	for _, required := range []string{
		"command -v wipefs",
		"wipefs --noheadings --no-act -o TYPE",
		"device has unsafe or unsupported signature",
	} {
		if !strings.Contains(cmd, required) {
			t.Fatalf("preflight command missing fail-closed probe %q: %s", required, cmd)
		}
	}
}

func TestCreateVGSteps_New(t *testing.T) {
	// Each disk becomes its OWN VG: 2 disks -> wipe signatures, then pvcreate + vgcreate.
	// Signature removal is explicit and follows the separate read-only safety preflight.
	steps := CreateVGSteps(CreateVGReq{VGNamePrefix: "vg_data", Disks: []string{"/dev/sdb", "/dev/sdc"}})
	if len(steps) != 6 {
		t.Fatalf("expected 6 steps (2 disks x 3), got %d", len(steps))
	}
	if steps[0].Name != "wipefs:/dev/sdb" || steps[0].Cmd != "wipefs -a /dev/sdb" {
		t.Fatalf("wipefs sdb must be explicit and scoped to the selected device: %+v", steps[0])
	}
	if steps[1].Name != "pvcreate:/dev/sdb" || steps[1].Cmd != "pvcreate /dev/sdb" {
		t.Fatalf("pvcreate sdb must not bypass prompts: %+v", steps[1])
	}
	if steps[2].Name != "vgcreate:vg_data_sdb" || steps[2].Cmd != "vgcreate vg_data_sdb /dev/sdb" {
		t.Fatalf("vgcreate sdb wrong: %+v", steps[2])
	}
	if steps[3].Name != "wipefs:/dev/sdc" || steps[3].Cmd != "wipefs -a /dev/sdc" {
		t.Fatalf("wipefs sdc wrong: %+v", steps[3])
	}
	if steps[4].Name != "pvcreate:/dev/sdc" || steps[4].Cmd != "pvcreate /dev/sdc" {
		t.Fatalf("pvcreate sdc wrong: %+v", steps[4])
	}
	if steps[5].Name != "vgcreate:vg_data_sdc" || steps[5].Cmd != "vgcreate vg_data_sdc /dev/sdc" {
		t.Fatalf("vgcreate sdc wrong: %+v", steps[5])
	}
}

func TestCreateVGSteps_NvmeName(t *testing.T) {
	// NVMe disks (/dev/nvme0n1) keep their full basename in the VG name.
	steps := CreateVGSteps(CreateVGReq{VGNamePrefix: "vg_data", Disks: []string{"/dev/nvme0n1"}})
	if len(steps) != 3 {
		t.Fatalf("expected 3 steps, got %d", len(steps))
	}
	if steps[2].Name != "vgcreate:vg_data_nvme0n1" || steps[2].Cmd != "vgcreate vg_data_nvme0n1 /dev/nvme0n1" {
		t.Fatalf("nvme vgcreate wrong: %+v", steps[2])
	}
}

func TestVGNameForDisk(t *testing.T) {
	cases := []struct{ prefix, disk, want string }{
		{"vg_data", "/dev/sdb", "vg_data_sdb"},
		{"vg_data", "/dev/nvme0n1", "vg_data_nvme0n1"},
		{"vg", "/dev/disk/by-id/wwn-0x5000c500a", "vg_wwn-0x5000c500a"},
	}
	for _, c := range cases {
		if got := VGNameForDisk(c.prefix, c.disk); got != c.want {
			t.Fatalf("VGNameForDisk(%q,%q)=%q want %q", c.prefix, c.disk, got, c.want)
		}
		// The derived name must pass ValidateName (no shell metacharacters).
		if err := ValidateName(VGNameForDisk(c.prefix, c.disk)); err != nil {
			t.Fatalf("derived VG name %q fails ValidateName: %v", c.disk, err)
		}
	}
}

func TestResizeLVSteps_Grow(t *testing.T) {
	steps := ResizeLVSteps(ResizeLVReq{VGName: "vg_data", LVName: "lv_200g", Grow: true, DeltaGB: 50})
	if len(steps) != 1 {
		t.Fatalf("expected 1 step, got %d", len(steps))
	}
	if steps[0].Name != "lvextend" || steps[0].Cmd != "lvextend -r -L +50G /dev/vg_data/lv_200g" {
		t.Fatalf("grow wrong: %+v", steps[0])
	}
}

func TestResizeLVSteps_Shrink(t *testing.T) {
	steps := ResizeLVSteps(ResizeLVReq{VGName: "vg_data", LVName: "lv_200g", Grow: false, DeltaGB: 10})
	if steps[0].Name != "lvreduce" || steps[0].Cmd != "lvreduce -y -r -L -10G /dev/vg_data/lv_200g" {
		t.Fatalf("shrink wrong: %+v", steps[0])
	}
}

func TestDeleteLVSteps_Mounted(t *testing.T) {
	steps := DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: "/data02/nb"})
	// exports + exportfs + user check + umount + verification + lvremove + fstab
	if len(steps) != 7 {
		t.Fatalf("expected 7 steps for mounted LV, got %d", len(steps))
	}
	if steps[0].Name != "remove_exports_line" || !contains(steps[0].Cmd, "/data02/nb") {
		t.Fatalf("exports step wrong: %+v", steps[0])
	}
	if steps[2].Name != "check_mount_users" || !contains(steps[2].Cmd, "fuser -vm /data02/nb") {
		t.Fatalf("mount-user diagnostic step wrong: %+v", steps[2])
	}
	if steps[3].Name != "umount" || steps[3].Cmd != "umount /data02/nb" {
		t.Fatalf("umount step wrong: %+v", steps[3])
	}
	if steps[4].Name != "verify_unmounted" || !contains(steps[4].Cmd, "findmnt") {
		t.Fatalf("unmount verification step wrong: %+v", steps[4])
	}
	if steps[5].Cmd != "lvremove -f /dev/vg_data/lv_200g" || steps[6].Name != "remove_fstab_line" {
		t.Fatalf("LV removal must precede fstab cleanup: %+v", steps[5:])
	}
}

func TestDeleteLVSteps_Unmounted(t *testing.T) {
	steps := DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: ""})
	// verification + lvremove + fstab (no exports/exportfs/umount)
	if len(steps) != 3 {
		t.Fatalf("expected 3 steps for unmounted LV, got %d", len(steps))
	}
	if steps[0].Name != "verify_unmounted" || steps[1].Cmd != "lvremove -f /dev/vg_data/lv_200g" || steps[2].Name != "remove_fstab_line" {
		t.Fatalf("unmounted handbook order must verify, remove, then clean fstab: %+v", steps)
	}
}

func TestFindDeviceHoldersCmd(t *testing.T) {
	cmd := FindDeviceHoldersCmd("/dev/vg_data/lv_200g")
	if !contains(cmd, "mountinfo") {
		t.Fatalf("expected command to inspect /proc/*/mountinfo: %s", cmd)
	}
	if !contains(cmd, "/dev/vg_data/lv_200g") {
		t.Fatalf("expected command to search for target device: %s", cmd)
	}
}

func TestDeleteStepsNeverForceOrLazyUnmount(t *testing.T) {
	for _, step := range DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: "/data02/share"}) {
		if contains(step.Cmd, "umount -f") || contains(step.Cmd, "umount -l") {
			t.Fatalf("unsafe unmount command: %s", step.Cmd)
		}
	}
}

func TestUnmountVerificationChecksFindmntExitCode(t *testing.T) {
	steps := DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_1"})
	if !contains(steps[0].Cmd, `status=$?`) || !contains(steps[0].Cmd, `"$status" -ne 1`) {
		t.Fatalf("findmnt failure is not checked: %s", steps[0].Cmd)
	}
}

func contains(s, sub string) bool { return strings.Contains(s, sub) }
