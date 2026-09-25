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

	// Full rollback when exports and fstab were completed: exports before umount
	doneFull := []string{"lvcreate", "mkfs", "mkdir", "mount", "fstab", "exports"}
	rbFull := RollbackFor(req, doneFull)
	if len(rbFull) != 5 {
		t.Fatalf("expected 5 rollback steps, got %d: %+v", len(rbFull), rbFull)
	}
	if rbFull[0].Name != "rollback:exports" || rbFull[1].Name != "rollback:exportfs" {
		t.Fatalf("exports/exportfs must be undone first, got %s, %s", rbFull[0].Name, rbFull[1].Name)
	}
	if rbFull[2].Name != "rollback:mount" {
		t.Fatalf("mount must be undone after exports, got %s", rbFull[2].Name)
	}
	if rbFull[3].Name != "rollback:fstab" || rbFull[4].Name != "rollback:lvcreate" {
		t.Fatalf("fstab/lvcreate wrong order: %+v", rbFull)
	}
}
