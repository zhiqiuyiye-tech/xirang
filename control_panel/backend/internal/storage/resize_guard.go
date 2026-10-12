package storage

import (
	"encoding/json"
	"fmt"
)

// blkid probes the filesystem signature rather than trusting a cached inventory.
func resizeFilesystemCommand(lvDev string) string {
	return "# cp-storage-resize-filesystem\nblkid -p -s TYPE -o value -- " + shellLiteral(lvDev)
}

// buildGuardedResizeCommand rechecks local safety, filesystem and the pinned LV
// identity inside the same SSH execution that issues the resize. Kubernetes
// references are checked by the handler immediately before this command; no
// distributed transaction with a concurrent Pod creator is implied.
func buildGuardedResizeCommand(req ResizeLVReq, expected DeviceIdentity, reserved []string) (string, error) {
	if ValidateLVComponent(req.VGName) != nil || ValidateLVComponent(req.LVName) != nil || req.DeltaGB <= 0 || !validRecoveryIdentity(expected) {
		return "", fmt.Errorf("invalid guarded resize target or identity")
	}
	reservedJSON, err := json.Marshal(reserved)
	if err != nil {
		return "", err
	}
	validator := `import json, posixpath, re, sys

def require(condition, message):
    if not condition:
        raise SystemExit(message)

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate resize safety field")
        result[key] = value
    return result

state = json.load(sys.stdin, object_pairs_hook=unique_object)
require(type(state) is dict and set(state) == {"mount_targets", "fstab_targets", "swap_active", "device_open_count"}, "invalid resize safety state")
require(type(state["mount_targets"]) is list and type(state["fstab_targets"]) is list, "invalid resize safety targets")
require(not state["mount_targets"], "logical volume became mounted before resize")
require(type(state["swap_active"]) is bool and not state["swap_active"], "logical volume became active as swap")
require(type(state["device_open_count"]) is int and state["device_open_count"] == 0, "logical volume became open before resize")
roots = ["/bin", "/boot", "/dev", "/etc", "/home", "/lib", "/lib64", "/proc", "/root", "/run", "/sbin", "/sys", "/usr", "/var"]
roots += json.loads(sys.argv[1]) or []
for target in state["fstab_targets"]:
    require(type(target) is str and re.fullmatch(r"/[A-Za-z0-9_/-]+", target), "invalid fstab target")
    target = posixpath.normpath(target)
    require(target != "/", "protected root fstab target")
    for root in roots:
        if not root:
            continue
        root = posixpath.normpath(root)
        require(target != root and not target.startswith(root.rstrip("/") + "/"), "protected or reserved fstab target")
`
	dev := fmt.Sprintf("/dev/%s/%s", req.VGName, req.LVName)
	probe := buildLVResizeSafetyCommand(dev)
	command := "# cp-storage-safe-resize\nLC_ALL=C\nexport LC_ALL\nlv_dev=" + shellLiteral(dev) +
		"\nexpected_uuid=" + shellLiteral(expected.UUID) + "\nexpected_major_minor=" + shellLiteral(expected.MajorMinor) +
		"\nstate=$(\n" + probe + "\n) || exit 1\n" +
		"printf '%s' \"$state\" | python3 -I -c " + shellLiteral(validator) + " " + shellLiteral(string(reservedJSON)) + " || exit 1\n" +
		`filesystem=$(blkid -p -s TYPE -o value -- "$lv_dev") || { echo "cannot confirm filesystem before resize" >&2; exit 1; }
case "$filesystem" in ext2|ext3|ext4) ;; *) echo "unsupported offline resize filesystem" >&2; exit 1;; esac
identity=$(lvs --noheadings --options lv_uuid,lv_kernel_major,lv_kernel_minor -- "$lv_dev") || { echo "cannot verify LV identity before resize" >&2; exit 1; }
set -f
IFS=' 	
'
set -- $identity
if [ "$#" -ne 3 ] || [ "$1" != "$expected_uuid" ] || [ "$2:$3" != "$expected_major_minor" ]; then
  echo "logical volume identity changed at resize boundary" >&2
  exit 1
fi
` + ResizeLVSteps(req)[0].Cmd
	return command, nil
}
