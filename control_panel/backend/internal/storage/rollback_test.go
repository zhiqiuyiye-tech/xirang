package storage

import "testing"

func TestRollbackReverses(t *testing.T) {
	req := ProvisionReq{VGName: "vg_data", LVName: "lv_200g", MountPoint: "/data02/nb"}
	done := []string{"lvcreate", "mkfs", "mkdir", "mount"}
	rb := RollbackFor(req, done)
	// reverse: mount->umount, lvcreate->lvremove; mkfs/mkdir irreversible skip
	if len(rb) != 2 {
		t.Fatalf("expected 2 rollback steps, got %d: %+v", len(rb), rb)
	}
	if rb[0].Name != "rollback:mount" || !contains(rb[0].Cmd, "umount") {
		t.Fatalf("rb0 wrong: %+v", rb[0])
	}
	if rb[1].Name != "rollback:lvcreate" || !contains(rb[1].Cmd, "lvremove") {
		t.Fatalf("rb1 wrong: %+v", rb[1])
	}
}
