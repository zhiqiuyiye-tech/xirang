package storage

import "fmt"

// RollbackFor generates the reverse-order undo command sequence for a
// provision failure. done is the list of SUCCESSFULLY-executed step names
// (the failed step is NOT included). The undo order is the reverse of
// provision: mount->umount, exports->sed remove, fstab->sed remove,
// lvcreate->lvremove. mkfs and mkdir are irreversible and skipped.
//
// Each rollback step is best-effort: the handler records it as a task step
// even if the undo command itself fails, so the failure path is never blocked.
func RollbackFor(req ProvisionReq, done []string) []Step {
	has := map[string]bool{}
	for _, n := range done {
		has[n] = true
	}
	var rb []Step
	lvDev := fmt.Sprintf("/dev/%s/%s", req.VGName, req.LVName)
	// Reverse order: undo later steps first.
	// Exports must be undone and reloaded before umount, otherwise NFS holds the
	// mount point open and umount fails with EBUSY (device or resource busy).
	if has["exports"] {
		rb = append(rb,
			Step{"rollback:exports", fmt.Sprintf(`sed -i '\#^%s #d' /etc/exports`, req.MountPoint)},
			Step{"rollback:exportfs", "exportfs -arv"},
		)
	}
	if has["mount"] {
		rb = append(rb, Step{"rollback:mount", fmt.Sprintf("umount %s", req.MountPoint)})
	}
	if has["fstab"] {
		rb = append(rb, Step{"rollback:fstab", fmt.Sprintf(`sed -i '\#^%s #d' /etc/fstab`, lvDev)})
	}
	if has["lvcreate"] {
		rb = append(rb, Step{"rollback:lvcreate", fmt.Sprintf("lvremove -f %s", lvDev)})
	}
	// mkfs/mkdir are irreversible, skip
	return rb
}
