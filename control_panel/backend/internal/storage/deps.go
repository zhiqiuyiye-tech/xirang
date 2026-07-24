package storage

import (
	"fmt"
	"strings"
)

// DetectPMOutput returns the shell command that probes for the available
// package manager. It echoes "yum", "dnf", or "apt" for whichever exists on
// the target host. The command is a fixed string (no user input) to prevent
// command injection.
func DetectPMOutput() string {
	return "command -v yum >/dev/null 2>&1 && echo yum; command -v dnf >/dev/null 2>&1 && echo dnf; command -v apt >/dev/null 2>&1 && echo apt"
}

// ParsePM parses the output of DetectPMOutput and returns the package manager
// to use. Priority: yum > dnf > apt (yum wins on RHEL8 where yum is a dnf
// symlink and both echo). Uses substring containment so output order does not
// matter - yum is always checked first regardless of which line appears first.
func ParsePM(stdout string) (string, error) {
	if strings.Contains(stdout, "yum") {
		return "yum", nil
	}
	if strings.Contains(stdout, "dnf") {
		return "dnf", nil
	}
	if strings.Contains(stdout, "apt") {
		return "apt", nil
	}
	return "", fmt.Errorf("unsupported distro (no yum/dnf/apt found): %q", stdout)
}

// CheckDepsCmd returns the shell command that checks whether lvm2 and nfs
// are already installed by probing for their key binaries (lvcreate, exportfs).
// Fixed string, no user input.
func CheckDepsCmd() string {
	return "command -v lvcreate >/dev/null 2>&1 && echo lvm2_ok; command -v exportfs >/dev/null 2>&1 && echo nfs_ok"
}

// ParseDepsCheck parses the output of CheckDepsCmd and returns whether lvm2
// and nfs are installed.
func ParseDepsCheck(stdout string) (lvm2, nfs bool) {
	return strings.Contains(stdout, "lvm2_ok"), strings.Contains(stdout, "nfs_ok")
}

// InstallDepsCmd returns the install command for the given package manager.
// Packages are hardcoded (lvm2 + nfs-utils for yum/dnf, lvm2 +
// nfs-kernel-server for apt) to prevent command injection. Returns an error
// for unsupported package managers.
func InstallDepsCmd(pm string) (string, error) {
	switch pm {
	case "yum":
		return "yum install -y lvm2 nfs-utils", nil
	case "dnf":
		return "dnf install -y lvm2 nfs-utils", nil
	case "apt":
		return "apt-get update -qq && apt-get install -y lvm2 nfs-kernel-server", nil
	default:
		return "", fmt.Errorf("unsupported package manager: %q", pm)
	}
}
