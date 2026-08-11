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

func TestProvisionSteps(t *testing.T) {
	steps := ProvisionSteps(ProvisionReq{
		VGName: "vg_data", LVName: "lv_200g", SizeGB: 200, FSType: "xfs",
		MountPoint: "/data02/nb", ExportOpts: "*(rw,sync,no_root_squash,no_subtree_check)",
	})
	if len(steps) != 7 {
		t.Fatalf("expected 7 steps, got %d", len(steps))
	}
	if steps[0].Name != "lvcreate" || steps[0].Cmd != "lvcreate -L 200G -n lv_200g vg_data" {
		t.Fatalf("step0 wrong: %+v", steps[0])
	}
	if steps[1].Cmd != "mkfs.xfs /dev/vg_data/lv_200g" {
		t.Fatalf("step1 wrong: %s", steps[1].Cmd)
	}
	// step4 fstab: idempotent grep dedup then append
	if !contains(steps[4].Cmd, "/dev/vg_data/lv_200g /data02/nb xfs defaults 0 0") {
		t.Fatalf("fstab step wrong: %s", steps[4].Cmd)
	}
	if !contains(steps[4].Cmd, "grep -v") || !contains(steps[4].Cmd, "mv") {
		t.Fatalf("fstab not idempotent: %s", steps[4].Cmd)
	}
	// step5 exports
	if !contains(steps[5].Cmd, "/data02/nb") || !contains(steps[5].Cmd, "no_root_squash") {
		t.Fatalf("exports step wrong: %s", steps[5].Cmd)
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

func TestCreateVGSteps_New(t *testing.T) {
	// Each disk becomes its OWN VG: 2 disks -> 2x (pvcreate + vgcreate) = 4 steps.
	// The VG name is derived from the prefix + disk basename (vg_data + sdb -> vg_data_sdb).
	steps := CreateVGSteps(CreateVGReq{VGNamePrefix: "vg_data", Disks: []string{"/dev/sdb", "/dev/sdc"}})
	if len(steps) != 4 {
		t.Fatalf("expected 4 steps (2 disks x 2), got %d", len(steps))
	}
	if steps[0].Name != "pvcreate:/dev/sdb" || steps[0].Cmd != "wipefs -a /dev/sdb && pvcreate /dev/sdb" {
		t.Fatalf("pvcreate sdb wrong: %+v", steps[0])
	}
	if steps[1].Name != "vgcreate:vg_data_sdb" || steps[1].Cmd != "vgcreate vg_data_sdb /dev/sdb" {
		t.Fatalf("vgcreate sdb wrong: %+v", steps[1])
	}
	if steps[2].Name != "pvcreate:/dev/sdc" {
		t.Fatalf("pvcreate sdc wrong: %+v", steps[2])
	}
	if steps[3].Name != "vgcreate:vg_data_sdc" || steps[3].Cmd != "vgcreate vg_data_sdc /dev/sdc" {
		t.Fatalf("vgcreate sdc wrong: %+v", steps[3])
	}
}

func TestCreateVGSteps_NvmeName(t *testing.T) {
	// NVMe disks (/dev/nvme0n1) keep their full basename in the VG name.
	steps := CreateVGSteps(CreateVGReq{VGNamePrefix: "vg_data", Disks: []string{"/dev/nvme0n1"}})
	if len(steps) != 2 {
		t.Fatalf("expected 2 steps, got %d", len(steps))
	}
	if steps[1].Name != "vgcreate:vg_data_nvme0n1" || steps[1].Cmd != "vgcreate vg_data_nvme0n1 /dev/nvme0n1" {
		t.Fatalf("nvme vgcreate wrong: %+v", steps[1])
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
	if steps[0].Name != "lvreduce" || steps[0].Cmd != "lvreduce -r -L -10G /dev/vg_data/lv_200g" {
		t.Fatalf("shrink wrong: %+v", steps[0])
	}
}

func TestDeleteLVSteps_Mounted(t *testing.T) {
	steps := DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: "/data02/nb"})
	// exports + exportfs + umount + fstab + lvremove
	if len(steps) != 5 {
		t.Fatalf("expected 5 steps for mounted LV, got %d", len(steps))
	}
	if steps[0].Name != "remove_exports_line" || !contains(steps[0].Cmd, "/data02/nb") {
		t.Fatalf("exports step wrong: %+v", steps[0])
	}
	if steps[2].Name != "umount" || steps[2].Cmd != "umount /data02/nb" {
		t.Fatalf("umount step wrong: %+v", steps[2])
	}
	if steps[4].Cmd != "lvremove -f /dev/vg_data/lv_200g" {
		t.Fatalf("lvremove wrong: %s", steps[4].Cmd)
	}
}

func TestDeleteLVSteps_Unmounted(t *testing.T) {
	steps := DeleteLVSteps(DeleteLVReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: ""})
	// fstab + lvremove only (no exports/exportfs/umount)
	if len(steps) != 2 {
		t.Fatalf("expected 2 steps for unmounted LV, got %d", len(steps))
	}
	if steps[0].Name != "remove_fstab_line" {
		t.Fatalf("first step should be remove_fstab_line: %+v", steps[0])
	}
	if steps[1].Cmd != "lvremove -f /dev/vg_data/lv_200g" {
		t.Fatalf("lvremove wrong: %s", steps[1].Cmd)
	}
}

func contains(s, sub string) bool { return strings.Contains(s, sub) }
