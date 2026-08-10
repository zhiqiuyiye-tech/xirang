package storage

import (
	"fmt"
	"regexp"
	"strings"
)

var nameRe = regexp.MustCompile(`^[a-zA-Z0-9_/-]+$`)
var diskRe = regexp.MustCompile(`^/dev/[a-zA-Z0-9/_-]+$`)

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

// ValidateDisk rejects anything that is not a /dev/ path of safe characters.
// Applied to disk paths interpolated into pvcreate/wipefs to prevent command
// injection. Only whole-device paths (/dev/sdb, /dev/nvme0n1) pass; partitions
// (/dev/sdb1) also pass the charset but the inventory only offers whole disks.
func ValidateDisk(s string) error {
	if s == "" {
		return fmt.Errorf("empty")
	}
	if strings.ContainsAny(s, ";|&$`\\\"' ") {
		return fmt.Errorf("contains shell metacharacters: %q", s)
	}
	if !diskRe.MatchString(s) {
		return fmt.Errorf("invalid disk path: %q", s)
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

// --- VG pool creation ---

// CreateVGReq holds parameters for building a create-VG command sequence.
// Exists controls whether the VG already exists (vgextend) or not (vgcreate).
type CreateVGReq struct {
	VGName string
	Disks  []string
	Exists bool
}

// CreateVGSteps builds the sequence: wipefs+pvcreate each disk, then vgcreate
// (new VG) or vgextend (existing VG). Each disk is its own step so a single
// disk failure aborts before the VG change and the failure names which disk.
// wipefs first ensures pvcreate does not prompt on stale filesystem signatures
// (which would hang the non-interactive SSH session).
func CreateVGSteps(r CreateVGReq) []Step {
	steps := make([]Step, 0, len(r.Disks)*2+1)
	for _, d := range r.Disks {
		steps = append(steps, Step{
			Name: "pvcreate:" + d,
			Cmd:  fmt.Sprintf("wipefs -a %s && pvcreate %s", d, d),
		})
	}
	joined := strings.Join(r.Disks, " ")
	if r.Exists {
		steps = append(steps, Step{
			Name: "vgextend",
			Cmd:  fmt.Sprintf("vgextend %s %s", r.VGName, joined),
		})
	} else {
		steps = append(steps, Step{
			Name: "vgcreate",
			Cmd:  fmt.Sprintf("vgcreate %s %s", r.VGName, joined),
		})
	}
	return steps
}

// --- LV resize ---

// ResizeLVReq holds parameters for an lvextend (Grow) or lvreduce (!Grow).
type ResizeLVReq struct {
	VGName  string
	LVName  string
	Grow    bool // true=extend, false=reduce
	DeltaGB int
}

// ResizeLVSteps builds a single step using -r (--resizefs) so the filesystem
// is resized in the same operation: resize2fs for ext, xfs_growfs for xfs. For
// shrink, -r shrinks the filesystem first and aborts the LV reduce if the fs
// resize fails (e.g. shrinking below used space, or xfs which cannot shrink),
// so data is not lost. DeltaGB must be > 0 (validated by the handler).
func ResizeLVSteps(r ResizeLVReq) []Step {
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	sign := "+"
	verb := "lvextend"
	if !r.Grow {
		sign = "-"
		verb = "lvreduce"
	}
	return []Step{
		{Name: verb, Cmd: fmt.Sprintf("%s -r -L %s%dG %s", verb, sign, r.DeltaGB, lvDev)},
	}
}

// --- LV delete (generalized reclaim for any LV) ---

// DeleteLVReq holds parameters for deleting an arbitrary LV and releasing its
// space back to the VG. MountPoint is detected by the handler (findmnt); when
// empty (unmounted) the exports/umount steps are skipped.
type DeleteLVReq struct {
	VGName     string
	LVName     string
	MountPoint string
}

// DeleteLVSteps builds the teardown sequence. If the LV is mounted, it first
// removes any /etc/exports line for the mount point, refreshes exports,
// and unmounts. It always cleans any stale /etc/fstab line referencing the LV
// device, then lvremoves. This is the generalized form of ReclaimSteps that
// works for LVs not created by the control panel (no provision task).
func DeleteLVSteps(r DeleteLVReq) []Step {
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	steps := make([]Step, 0, 5)
	if r.MountPoint != "" {
		steps = append(steps,
			Step{"remove_exports_line", fmt.Sprintf(`sed -i '\#^%s #d' /etc/exports`, r.MountPoint)},
			Step{"exportfs", "exportfs -arv"},
			Step{"umount", fmt.Sprintf("umount %s", r.MountPoint)},
		)
	}
	steps = append(steps,
		Step{"remove_fstab_line", fmt.Sprintf(`sed -i '\#^%s #d' /etc/fstab`, lvDev)},
		Step{"lvremove", fmt.Sprintf("lvremove -f %s", lvDev)},
	)
	return steps
}
