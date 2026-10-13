package storage

import (
	"strings"
	"testing"
)

func TestVGFilesystemReinitializationRejectsMultiDeviceAndSpecialSignatures(t *testing.T) {
	// A Btrfs member may be in use through a mount whose source names another
	// member. The current single-device preflight cannot prove this member free.
	for _, signature := range []string{"btrfs", "LVM2_member", "linux_raid_member", "crypto_LUKS", "swap", "gpt", "unknown"} {
		if isReinitializableFilesystem(signature) {
			t.Errorf("unsafe signature %q was offered for initialization", signature)
		}
	}
	for _, signature := range []string{"", "ext2", "ext3", "ext4", "xfs"} {
		if !isReinitializableFilesystem(signature) {
			t.Errorf("supported signature %q was excluded", signature)
		}
	}
	if strings.Contains(PreflightDeviceCmd("/dev/sdb", nil), "|btrfs|") {
		t.Fatal("remote preflight permits multi-device Btrfs signatures")
	}
}
