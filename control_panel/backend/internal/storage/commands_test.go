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

func contains(s, sub string) bool { return strings.Contains(s, sub) }
