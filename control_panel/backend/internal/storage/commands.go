package storage

import (
	"fmt"
	"path"
	"regexp"
	"strings"
)

var nameRe = regexp.MustCompile(`^[a-zA-Z0-9_/-]+$`)

// reinitializableFilesystemTypes are ordinary filesystem signatures that may be
// cleared after the read-only device preflight confirms the target is unused.
// Partition-table, LVM, RAID, encrypted, swap, multi-device Btrfs, and unknown
// signatures stay blocked; a single-device mount check cannot prove all Btrfs
// members unused.
var reinitializableFilesystemTypes = []string{"ext2", "ext3", "ext4", "xfs", "vfat", "exfat", "ntfs"}

func isReinitializableFilesystem(fstype string) bool {
	fstype = strings.ToLower(strings.TrimSpace(fstype))
	if fstype == "" {
		return true
	}
	for _, allowed := range reinitializableFilesystemTypes {
		if fstype == allowed {
			return true
		}
	}
	return false
}

// diskRe limits disk paths to /dev/ + safe characters.
var diskRe = regexp.MustCompile(`^/dev/[a-zA-Z0-9/_-]+$`)

// exportOptsRe limits NFS export option strings (e.g. "*(rw,sync)" or
// "10.0.0.0/24(rw) host.example.com(ro)") to the punctuation that
// legitimately appears in client specs and options. Everything that could
// break out of the single-quoted echo in the exports step - quotes,
// semicolons, backticks, dollars, backslashes - is outside this set.
var exportOptsRe = regexp.MustCompile(`^[0-9a-zA-Z*_,()\-.\[\]:=@/ ]*$`)

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
// injection. Both whole-device and partition paths are accepted; destructive
// handlers must run PreflightDeviceCmd immediately before use.
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

// ValidateMountPoint ensures mountPoint is an absolute, clean path, does not contain
// directory traversal or shell metacharacters, and is not a system-critical path
// (/, /boot, /etc, /usr, /var, /run, /root, /bin, /sbin, /lib, /sys, /proc, /dev)
// or within configured reserved mounts (e.g. /data01).
func ValidateMountPoint(mountPoint string, reservedMounts []string) error {
	if mountPoint == "" {
		return fmt.Errorf("mount point cannot be empty")
	}
	if !strings.HasPrefix(mountPoint, "/") {
		return fmt.Errorf("mount point must be an absolute path: %q", mountPoint)
	}
	if err := ValidateName(mountPoint); err != nil {
		return err
	}
	cleaned := path.Clean(mountPoint)
	if cleaned == "/" {
		return fmt.Errorf("mount point cannot be root directory: %q", mountPoint)
	}
	systemRoots := []string{
		"/bin", "/boot", "/dev", "/etc", "/home", "/lib", "/lib64",
		"/proc", "/root", "/run", "/sbin", "/sys", "/usr", "/var",
	}
	for _, sys := range systemRoots {
		if cleaned == sys || strings.HasPrefix(cleaned, sys+"/") {
			return fmt.Errorf("mount point %q is within protected system path %q", mountPoint, sys)
		}
	}
	for _, res := range reservedMounts {
		res = path.Clean(strings.TrimRight(res, "/"))
		if res != "" && (cleaned == res || strings.HasPrefix(cleaned, res+"/")) {
			return fmt.Errorf("mount point %q is within reserved mount %q", mountPoint, res)
		}
	}
	return nil
}

// ValidateLVComponent accepts a single LVM basename, not a path or CLI option.
func ValidateLVComponent(value string) error {
	if !regexp.MustCompile(`^[A-Za-z0-9_+][A-Za-z0-9_+.\-]*$`).MatchString(value) || len(value) > 127 || value == "." || value == ".." {
		return fmt.Errorf("invalid LVM basename: %q", value)
	}
	return nil
}

func shellLiteral(value string) string {
	return "'" + strings.ReplaceAll(value, "'", `'"'"'`) + "'"
}

// PreflightDeviceCmd returns a read-only safety check that must run before
// signature clearing. It permits only known filesystem signatures to be reset,
// while rejecting mounted devices, partition tables, PV and unknown signatures,
// incomplete ancestry, protected mounts, and whole disks with child devices.
func PreflightDeviceCmd(device string, reservedMounts []string) string {
	patterns := []string{"/", "/boot", "/boot/efi"}
	for _, mountPoint := range reservedMounts {
		mountPoint = strings.TrimRight(mountPoint, "/")
		if mountPoint != "" {
			patterns = append(patterns, mountPoint, mountPoint+"/*")
		}
	}
	quotedPatterns := make([]string, 0, len(patterns))
	for _, pattern := range patterns {
		if strings.HasSuffix(pattern, "/*") {
			quotedPatterns = append(quotedPatterns, shellLiteral(strings.TrimSuffix(pattern, "/*"))+"/*")
		} else {
			quotedPatterns = append(quotedPatterns, shellLiteral(pattern))
		}
	}
	d := shellLiteral(device)
	script := `# cp-storage-preflight
 device=@@DEVICE@@
fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

test -b "$device" || { echo "device is not a block device: $device" >&2; exit 1; }
command -v wipefs >/dev/null 2>&1 || fail 'wipefs is unavailable; cannot inspect device signatures'
signatures=$(wipefs --noheadings --no-act -o TYPE "$device" 2>/dev/null) || fail 'cannot inspect device signatures'
while IFS= read -r signature || [ -n "$signature" ]; do
  [ -n "$signature" ] || continue
  case "$signature" in
    @@REINITIALIZABLE_SIGNATURES@@) ;;
    *) fail "device has unsafe or unsupported signature: $signature" ;;
  esac
done <<EOF
$signatures
EOF

nl='
'
current="$device"
root="$device"
selected_type=
seen_ancestry='|'
depth=0
while :; do
  [ "$depth" -lt 32 ] || fail 'device ancestry exceeds the safety depth limit'
  case "$seen_ancestry" in *"|$current|"*) fail 'device ancestry contains a cycle' ;; esac
  seen_ancestry="${seen_ancestry}${current}|"

  type_probe=$(lsblk -dn -o TYPE "$current" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
  type_status=$?
  [ "$type_status" -eq 0 ] || fail 'cannot inspect device type'
  type_output=${type_probe%?}
  case "$type_output" in
    disk|disk"$nl") node_type=disk ;;
    part|part"$nl") node_type=part ;;
    *) fail 'device type probe returned empty, malformed, or ambiguous data' ;;
  esac
  if [ "$current" = "$device" ]; then selected_type=$node_type; fi

  parent_probe=$(lsblk -dn -o PKNAME "$current" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
  parent_status=$?
  [ "$parent_status" -eq 0 ] || fail 'cannot inspect device parent'
  parent_output=${parent_probe%?}
  case "$parent_output" in *"$nl") parent_output=${parent_output%"$nl"} ;; esac
  case "$parent_output" in *"$nl"*) fail 'device parent probe returned multiple rows' ;; esac
  case "$parent_output" in *[!A-Za-z0-9_-]*) fail 'device parent probe returned a malformed name' ;; esac
  parent="$parent_output"

  case "$node_type" in
    part) [ -n "$parent" ] || fail 'partition parent could not be proven' ;;
    disk) [ -z "$parent" ] || fail 'disk unexpectedly reports a parent' ;;
  esac
  if [ -z "$parent" ]; then
    [ "$node_type" = disk ] || fail 'device ancestry does not terminate at a disk'
    root="$current"
    break
  fi

  root="/dev/$parent"
  current="$root"
  depth=$((depth + 1))
done

mountpoint_probe=$(lsblk -nr -o MOUNTPOINT "$root" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
mountpoint_status=$?
[ "$mountpoint_status" -eq 0 ] || fail 'cannot inspect ancestor mountpoints'
mountpoints=${mountpoint_probe%?}
[ -n "$mountpoints" ] || fail 'ancestor mountpoint probe returned no data'
while IFS= read -r mp || [ -n "$mp" ]; do
  [ -n "$mp" ] || continue
  case "$mp" in
    /*) ;;
    *) fail 'ancestor mountpoint probe returned malformed data' ;;
  esac
  case "$mp" in
    *[!A-Za-z0-9_./-]*) fail 'ancestor mountpoint probe returned unrepresentable data' ;;
  esac
  case "$mp" in @@PROTECTED_PATTERNS@@) echo "device belongs to protected mount: $mp" >&2; exit 1 ;; esac
done <<EOF
$mountpoints
EOF

findmnt_probe=$(findmnt -rn -S "$device" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
findmnt_status=$?
findmnt_output=${findmnt_probe%?}
case "$findmnt_status" in
  0) [ -n "$findmnt_output" ] || fail 'device mount probe returned empty successful data'; fail 'device is mounted' ;;
  1) [ -z "$findmnt_output" ] || fail 'device mount probe returned data with no-match status' ;;
  *) fail 'device mount probe failed' ;;
esac

if [ "$selected_type" = disk ]; then
  children_probe=$(lsblk -nr -o NAME "$device" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
  children_status=$?
  [ "$children_status" -eq 0 ] || fail 'cannot inspect disk child devices'
  children=${children_probe%?}
  [ -n "$children" ] || fail 'disk child query returned no names'
  case "$children" in *"$nl") children=${children%"$nl"} ;; esac
  [ -n "$children" ] || fail 'disk child query returned no names'
  seen_children='|'
  selected_seen=false
  has_children=false
  while IFS= read -r child || [ -n "$child" ]; do
    [ -n "$child" ] || fail 'disk child query returned an empty name'
    case "$child" in *[!A-Za-z0-9_-]*) fail 'disk child query returned a malformed name' ;; esac
    case "$seen_children" in *"|$child|"*) fail 'disk child query returned duplicate names' ;; esac
    seen_children="${seen_children}${child}|"
    if [ "$selected_seen" = false ]; then
      selected_seen=true
      continue
    fi
    has_children=true

    child_probe=$(findmnt -rn -S "/dev/$child" 2>/dev/null; probe_status=$?; printf '\001'; exit "$probe_status")
    child_status=$?
    child_output=${child_probe%?}
    case "$child_status" in
      0) [ -n "$child_output" ] || fail 'child mount probe returned empty successful data'; echo "child partition is mounted: /dev/$child" >&2; exit 1 ;;
      1) [ -z "$child_output" ] || fail 'child mount probe returned data with no-match status' ;;
      *) fail 'child mount probe failed' ;;
    esac
  done <<EOF
$children
EOF
  [ "$selected_seen" = true ] || fail 'disk child query did not include the selected device'
  [ "$has_children" = false ] || fail 'disk has child devices; select an unused partition instead'
fi

echo SAFE`
	script = strings.Replace(script, "device=@@DEVICE@@", "device="+d, 1)
	script = strings.Replace(script, "@@PROTECTED_PATTERNS@@", strings.Join(quotedPatterns, "|"), 1)
	return strings.Replace(script, "@@REINITIALIZABLE_SIGNATURES@@", strings.Join(reinitializableFilesystemTypes, "|"), 1)
}

// ValidateExportOpts validates the NFS export options string (the part after
// the mount point on an /etc/exports line). It is NOT the same charset as
// ValidateName - legitimate export options contain asterisks, commas, and
// parentheses - but it still blocks every character that could escape the
// single-quoted shell command the value is interpolated into. Empty is valid
// (the caller substitutes a secure default).
func ValidateExportOpts(s string) error {
	if s == "" {
		return nil
	}
	if strings.ContainsAny(s, "'\"`;|&$\\<>#!\n\r\t") {
		return fmt.Errorf("contains shell metacharacters: %q", s)
	}
	if !exportOptsRe.MatchString(s) {
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
//
// The fstab/exports steps dedupe with `sed -i '\#^<key> #d'` before appending.
// sed -i (unlike grep > tmpfile && mv) preserves the original file's mode and
// owner, and per-worker task serialization in the engine guarantees two
// concurrent tasks never interleave these edits.
func ProvisionSteps(r ProvisionReq) []Step {
	if r.ExportOpts == "" {
		r.ExportOpts = "*(rw,sync,no_root_squash,no_subtree_check)"
	}
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	exportsStepCmd := fmt.Sprintf(`sed -i '\#^%s #d' /etc/exports &&
if [ -s /etc/exports ] && [ -n "$(tail -c 1 /etc/exports)" ]; then printf '\n' >> /etc/exports; fi &&
echo '%s %s' >> /etc/exports`, r.MountPoint, r.MountPoint, r.ExportOpts)
	return []Step{
		{"lvcreate", fmt.Sprintf("lvcreate -y -L %dG -n %s %s", r.SizeGB, r.LVName, r.VGName)},
		{"mkfs", fmt.Sprintf("mkfs.%s %s", r.FSType, lvDev)},
		{"mkdir", fmt.Sprintf("mkdir -p %s", r.MountPoint)},
		{"mount", fmt.Sprintf("mount %s %s", lvDev, r.MountPoint)},
		{"fstab", fmt.Sprintf(`sed -i '\#^%s #d' /etc/fstab && echo '%s %s %s defaults 0 0' >> /etc/fstab`, lvDev, lvDev, r.MountPoint, r.FSType)},
		{"exports", exportsStepCmd},
		{"ensure_nfs", "systemctl is-active --quiet nfs-server || systemctl is-active --quiet nfs-kernel-server || systemctl start nfs-server || systemctl start nfs-kernel-server"},
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
// Each disk becomes its OWN VG (vgcreate one disk per VG), which sidesteps
// LVM's same-physical-block-size constraint that blocks mixing disks of
// different sector sizes (512e vs 4Kn) into one VG. VGNamePrefix gives each
// disk a distinct VG name derived from the prefix + disk basename
// (e.g. prefix "vg_data" + "/dev/sdb" -> "vg_data_sdb").
type CreateVGReq struct {
	VGNamePrefix string
	Disks        []string
}

// VGNameForDisk derives a VG name for a single disk: prefix + "_" + the disk's
// basename (basename of "/dev/sdb" is "sdb"). The caller validates the prefix;
// the basename is alnum so the result passes ValidateName.
func VGNameForDisk(prefix, disk string) string {
	return prefix + "_" + BaseName(disk)
}

// BaseName returns the last path segment of disk (e.g. "/dev/sdb" -> "sdb").
// Exported for tests.
func BaseName(path string) string {
	if i := strings.LastIndex(path, "/"); i >= 0 {
		return path[i+1:]
	}
	return path
}

// CreateVGSteps builds a per-disk wipefs + pvcreate + vgcreate sequence. The
// caller runs the strict read-only preflight first. Wipefs is limited by that
// preflight to known unmounted filesystem signatures; pvcreate does not use
// force flags, so new or unexpected signatures still cause initialization to fail.
func CreateVGSteps(r CreateVGReq) []Step {
	steps := make([]Step, 0, len(r.Disks)*3)
	for _, d := range r.Disks {
		vg := VGNameForDisk(r.VGNamePrefix, d)
		steps = append(steps,
			Step{Name: "wipefs:" + d, Cmd: fmt.Sprintf("wipefs -a %s", d)},
			Step{Name: "pvcreate:" + d, Cmd: fmt.Sprintf("pvcreate %s", d)},
			Step{Name: "vgcreate:" + vg, Cmd: fmt.Sprintf("vgcreate %s %s", vg, d)},
		)
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
	// FSType is the probed filesystem type (ext2/ext3/ext4/xfs). It selects the
	// filesystem command that completes a grow.
	FSType string
	// MountPoint is the probed mount target of a mounted volume. xfs_growfs
	// resizes by mount point, so a mounted XFS needs it; a mounted ext volume
	// uses it to check whether the online grow that lvextend -r performed
	// already covers the enlarged device. It is empty for an unmounted volume.
	MountPoint string
}

// resizeFilesystemSupported reports whether the handbook resize flow covers
// this filesystem type: ext2/ext3/ext4 grow and shrink, XFS grow only, because
// XFS cannot shrink.
func resizeFilesystemSupported(grow bool, fsType string) bool {
	switch fsType {
	case "ext2", "ext3", "ext4":
		return true
	case "xfs":
		return grow
	}
	return false
}

// ResizeLVSteps builds the resize mutation step. Grow follows the operator
// handbook for a live NFS share: lvextend -r extends the LV and resizes the
// filesystem in the same operation, and a failed extend stops the step so a
// filesystem-only success cannot be reported as a completed resize.
//
// The handbook's follow-up filesystem command is the fallback for a resize that
// lvextend -r did not complete, not a second unconditional resize. On a mounted
// ext volume the kernel performs the online grow in lvextend -r and writes the
// updated superblock asynchronously, so a resize2fs issued immediately
// afterwards can read that superblock mid-update and refuse to open the
// filesystem ("Superblock checksum does not match superblock"), failing a task
// whose volume and filesystem both grew. The mounted ext path therefore
// verifies the size the kernel reports and only then runs resize2fs; an
// unmounted ext volume has no online grow in flight, so it runs the handbook
// command directly. A mounted XFS completes with xfs_growfs, which is
// idempotent; an unmounted XFS needs no completion command because -r resizes
// it through a temporary mount.
//
// Shrink keeps -r, which shrinks the filesystem first and aborts the LV reduce
// if the filesystem resize fails (e.g. shrinking below used space, or XFS,
// which cannot shrink), so data is not lost. -y (--yes) bypasses the interactive
// confirmation prompt required by lvreduce in non-interactive SSH sessions.
// DeltaGB must be > 0.
func ResizeLVSteps(r ResizeLVReq) []Step {
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	if !r.Grow {
		return []Step{
			{Name: "lvreduce", Cmd: fmt.Sprintf("lvreduce -y -r -L -%dG %s", r.DeltaGB, lvDev)},
		}
	}
	cmd := fmt.Sprintf("lvextend -r -L +%dG %s", r.DeltaGB, lvDev)
	switch r.FSType {
	case "ext2", "ext3", "ext4":
		if r.MountPoint != "" {
			cmd += " || exit 1" + mountedExtGrowCompletion(lvDev, r.MountPoint)
		} else {
			cmd += fmt.Sprintf(" || exit 1\nresize2fs %s", lvDev)
		}
	case "xfs":
		if r.MountPoint != "" {
			cmd += fmt.Sprintf(" || exit 1\nxfs_growfs %s", shellLiteral(r.MountPoint))
		}
	}
	return []Step{{Name: "lvextend", Cmd: cmd}}
}

// mountedExtGrowCompletion completes a grow of a mounted ext volume without
// racing the online resize lvextend -r just performed. The kernel's statvfs view
// is authoritative for the mounted filesystem; when it already covers the
// enlarged device there is nothing left to do, and resize2fs would only read a
// superblock the kernel is still writing. When the size cannot be read (the
// mount disappeared between the safety probe and this step) or it still lags the
// device, the handbook's resize2fs runs and its failure fails the step.
func mountedExtGrowCompletion(lvDev, mountPoint string) string {
	return fmt.Sprintf(`
mount_target=%s
if fs_blocks=$(stat -f -c '%%b' -- "$mount_target" 2>/dev/null) &&
   fs_unit=$(stat -f -c '%%S' -- "$mount_target" 2>/dev/null) &&
   device_bytes=$(blockdev --getsize64 -- %s 2>/dev/null) &&
   [ "$((fs_blocks * fs_unit))" -ge "$device_bytes" ]; then
  echo 'filesystem already covers the enlarged logical volume'
else
  resize2fs %s
fi`, shellLiteral(mountPoint), lvDev, lvDev)
}

// --- LV delete (generalized reclaim for any LV) ---

// DeleteLVReq holds parameters for deleting an arbitrary LV and releasing its
// space back to the VG. The handler fills MountPoints from findmnt; MountPoint
// remains available for callers that only have one known mount target.
type DeleteLVReq struct {
	VGName      string
	LVName      string
	MountPoint  string // legacy single-mount field
	MountPoints []string
}

// DeleteLVSteps builds the teardown sequence. If mounted, it removes exports
// for every mount target, refreshes exports, and unmounts deepest paths first.
// Verify the host has no remaining mount before lvremove. Fstab cleanup
// follows successful removal, matching the operator handbook sequence.
func DeleteLVSteps(r DeleteLVReq) []Step {
	lvDev := fmt.Sprintf("/dev/%s/%s", r.VGName, r.LVName)
	mountPoints := r.MountPoints
	if len(mountPoints) == 0 && r.MountPoint != "" {
		mountPoints = []string{r.MountPoint}
	}
	steps := make([]Step, 0, len(mountPoints)*3+4)
	if len(mountPoints) > 0 {
		for _, mountPoint := range mountPoints {
			// A worker without an exports file has nothing to revoke. A real sed
			// failure on an existing file is still fatal.
			steps = append(steps, Step{"remove_exports_line", fmt.Sprintf(`if [ -f /etc/exports ]; then sed -i '\#^%s #d' /etc/exports; fi`, mountPoint)})
		}
		// A worker without exportfs has no export to refresh, so the absent tool
		// is not a deletion failure.
		steps = append(steps, Step{"exportfs", `if command -v exportfs >/dev/null 2>&1; then exportfs -arv; else echo "exportfs is unavailable; no export was refreshed"; fi`})
		for _, mountPoint := range mountPoints {
			steps = append(steps,
				Step{"check_mount_users", fmt.Sprintf(`if command -v fuser >/dev/null 2>&1; then fuser -vm %s 2>&1 || true; else echo "fuser is unavailable"; fi`, mountPoint)},
				// LC_ALL=C keeps the busy/not-mounted wording this flow matches on
				// independent of the worker's locale.
				Step{"umount", fmt.Sprintf("LC_ALL=C umount %s", mountPoint)},
			)
		}
	}
	steps = append(steps,
		Step{"verify_unmounted", fmt.Sprintf(`remaining=$(findmnt -rn -o TARGET --source %s 2>/dev/null); status=$?; if [ "$status" -ne 0 ] && [ "$status" -ne 1 ]; then echo "could not verify logical volume mount state (findmnt status=$status)" >&2; exit 1; fi; if [ -n "$remaining" ]; then echo "logical volume is still mounted at: $remaining" >&2; exit 1; fi`, lvDev)},
		// LC_ALL=C keeps the filesystem-in-use wording the retry matches on
		// independent of the worker's locale.
		Step{"lvremove", fmt.Sprintf("LC_ALL=C lvremove -f %s", lvDev)},
		Step{"remove_fstab_line", fmt.Sprintf(`sed -i '\#^%s #d' /etc/fstab`, lvDev)},
	)
	return steps
}

// FindDeviceHoldersCmd inspects all process mountinfo files to locate any process (like Promtail
// running in an isolated mount namespace) that still holds a mount of the device or its dm target.
func FindDeviceHoldersCmd(devPath string) string {
	d := shellLiteral(devPath)
	return fmt.Sprintf(`# cp-storage-find-holders
dev=%s
realdev=$(readlink -f "$dev" 2>/dev/null || echo "$dev")
majmin=$(lsblk -dn -o MAJ:MIN "$realdev" 2>/dev/null | head -n1 | tr -d ' ')
echo "=== Searching mount namespaces holding $dev ($realdev $majmin) ==="
for mi in /proc/[0-9]*/mountinfo; do
  [ -f "$mi" ] || continue
  if grep -qs -e "$dev" -e "$realdev" ${majmin:+-e "$majmin"} "$mi"; then
    pid=$(echo "$mi" | cut -d/ -f3)
    cmd=$(tr '\0' ' ' < /proc/$pid/cmdline 2>/dev/null || cat /proc/$pid/comm 2>/dev/null)
    matched_mounts=$(grep -E "$dev|$realdev${majmin:+|$majmin}" "$mi" | awk '{print $5}')
    echo "PID $pid ($cmd): $matched_mounts"
  fi
done`, d)
}

// NamespaceUnmountCmd ordinarily unmounts one residual mount inside the mount
// namespace of the process that still holds it, which is the handbook step
// `nsenter -t <pid> -m umount <path>`. Only the mount namespace is entered, so
// the host root stays in effect and the reported mount path resolves inside
// that namespace. The command never forces or lazily unmounts, and it pins no
// process identity: the caller re-derives the holder from device evidence.
// LC_ALL=C keeps the busy/not-mounted wording the caller matches on independent
// of the worker's locale.
func NamespaceUnmountCmd(pid int, path string) string {
	return fmt.Sprintf("# cp-storage-namespace-unmount\nLC_ALL=C nsenter -t %d -m umount %s", pid, shellLiteral(path))
}
