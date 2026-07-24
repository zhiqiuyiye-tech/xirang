package storage

import (
	"fmt"
	"regexp"
	"strings"
)

var nameRe = regexp.MustCompile(`^[a-zA-Z0-9_/-]+$`)

// ValidateName rejects empty strings, shell metacharacters, and characters
// outside [a-zA-Z0-9_/-]. It is applied to VGName, LVName, MountPoint, and
// FSType to prevent command injection through the SSH command string.
func ValidateName(s string) error {
	if s == "" {
		return fmt.Errorf("empty")
	}
	if strings.ContainsAny(s, ";|&$`\\\"' ") {
		return fmt.Errorf("contains shell metacharacters: %q", s)
	}
	if !nameRe.MatchString(s) {
		return fmt.Errorf("invalid characters: %q", s)
	}
	return nil
}

// Step represents a single named shell command in a provision/reclaim sequence.
type Step struct {
	Name string
	Cmd  string
}

// ProvisionReq holds the parameters for building an LVM+NFS provision
// command sequence.
type ProvisionReq struct {
	VGName     string
	LVName     string
	SizeGB     int
	FSType     string
	MountPoint string
	ExportOpts string
}

// ProvisionSteps builds the 7-step provision sequence:
// lvcreate, mkfs, mkdir, mount, fstab (idempotent), exports (idempotent),
// exportfs. If ExportOpts is empty, a secure default is used.
func ProvisionSteps(r ProvisionReq) []Step {
	if r.ExportOpts == "" {
		r.ExportOpts = "*(rw,sync,no_root_squash,no_subtree_check)"
	}
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	return []Step{
		{"lvcreate", fmt.Sprintf("lvcreate -L %dG -n %s %s", r.SizeGB, r.LVName, r.VGName)},
		{"mkfs", fmt.Sprintf("mkfs.%s %s", r.FSType, lvDev)},
		{"mkdir", fmt.Sprintf("mkdir -p %s", r.MountPoint)},
		{"mount", fmt.Sprintf("mount %s %s", lvDev, r.MountPoint)},
		{"fstab", fmt.Sprintf(`grep -v '^%s ' /etc/fstab > /tmp/fstab.cp && mv /tmp/fstab.cp /etc/fstab; echo '%s %s %s defaults 0 0' >> /etc/fstab`, lvDev, lvDev, r.MountPoint, r.FSType)},
		{"exports", fmt.Sprintf(`grep -v '^%s ' /etc/exports > /tmp/exports.cp && mv /tmp/exports.cp /etc/exports; echo '%s %s' >> /etc/exports`, r.MountPoint, r.MountPoint, r.ExportOpts)},
		{"exportfs", "exportfs -arv"},
	}
}

// ReclaimReq holds the parameters for building an LVM+NFS reclaim command
// sequence (the reverse of provision).
type ReclaimReq struct {
	VGName     string
	LVName     string
	MountPoint string
}

// ReclaimSteps builds the 5-step reclaim sequence (reverse order of
// provision): remove_exports_line, exportfs, umount, remove_fstab_line,
// lvremove.
func ReclaimSteps(r ReclaimReq) []Step {
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	return []Step{
		{"remove_exports_line", fmt.Sprintf(`sed -i '\#^%s #d' /etc/exports`, r.MountPoint)},
		{"exportfs", "exportfs -arv"},
		{"umount", fmt.Sprintf("umount %s", r.MountPoint)},
		{"remove_fstab_line", fmt.Sprintf(`sed -i '\#^%s #d' /etc/fstab`, lvDev)},
		{"lvremove", fmt.Sprintf("lvremove -f %s", lvDev)},
	}
}
