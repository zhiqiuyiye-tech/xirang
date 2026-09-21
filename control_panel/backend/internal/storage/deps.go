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

// NFSServiceName returns the systemd service name for the NFS server.
// On Debian/Ubuntu (apt) it is nfs-kernel-server; on RHEL/CentOS/Rocky (yum/dnf)
// it is nfs-server.
func NFSServiceName(pm string) string {
	if pm == "apt" {
		return "nfs-kernel-server"
	}
	return "nfs-server"
}

// ConfigureNFSv4Cmd returns the shell command that enforces NFSv4 (vers4=y,
// vers2=n, vers3=n) in /etc/nfs.conf. Fixed string, no user input.
// Uses an idempotent awk script to safely add or update the [nfsd] section
// while preserving all comments and other sections.
func ConfigureNFSv4Cmd() string {
	return `touch /etc/nfs.conf && awk 'BEGIN { in_nfsd=0; done=0 } /^\[nfsd\]/ { print; print "vers2=n\nvers3=n\nvers4=y\nvers4.0=y\nvers4.1=y\nvers4.2=y"; in_nfsd=1; done=1; next } /^\[/ { in_nfsd=0 } in_nfsd && /^vers[234]/ { next } { print } END { if (!done) print "\n[nfsd]\nvers2=n\nvers3=n\nvers4=y\nvers4.0=y\nvers4.1=y\nvers4.2=y" }' /etc/nfs.conf > /etc/nfs.conf.tmp && mv -f /etc/nfs.conf.tmp /etc/nfs.conf`
}

// EnableNFSServiceCmd returns the shell command to enable and start the NFS service.
func EnableNFSServiceCmd(pm string) string {
	return fmt.Sprintf("systemctl enable --now %s", NFSServiceName(pm))
}

// EnsureNFSServiceCmd returns the shell command to ensure the NFS service is active.
func EnsureNFSServiceCmd(pm string) string {
	svc := NFSServiceName(pm)
	return fmt.Sprintf("systemctl is-active --quiet %s || systemctl start %s", svc, svc)
}
