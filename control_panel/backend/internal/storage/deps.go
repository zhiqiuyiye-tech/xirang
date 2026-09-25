package storage

import (
	"fmt"
	"strings"
)

// DetectPMOutput returns one available package manager and exits zero as soon
// as it finds one. A single conditional chain is important: independent
// semicolon-separated probes would inherit the exit code of the final missing
// command and falsely fail on RHEL hosts without apt.
func DetectPMOutput() string {
	return "if command -v dnf >/dev/null 2>&1; then echo dnf; exit 0; elif command -v yum >/dev/null 2>&1; then echo yum; exit 0; elif command -v apt-get >/dev/null 2>&1; then echo apt; exit 0; else exit 1; fi"
}

// ParsePM parses the output of DetectPMOutput and returns the package manager
// to use. Priority follows the detection chain: dnf > yum > apt.
func ParsePM(stdout string) (string, error) {
	if strings.Contains(stdout, "dnf") {
		return "dnf", nil
	}
	if strings.Contains(stdout, "yum") {
		return "yum", nil
	}
	if strings.Contains(stdout, "apt") {
		return "apt", nil
	}
	return "", fmt.Errorf("unsupported distro (no yum/dnf/apt found): %q", stdout)
}

// DetectPrivilegeCmd determines whether commands can run directly as root or
// through non-interactive sudo. Interactive sudo is intentionally unsupported.
func DetectPrivilegeCmd() string {
	return `if [ "$(id -u)" = "0" ]; then echo root; exit 0; elif command -v sudo >/dev/null 2>&1 && sudo -n true >/dev/null 2>&1; then echo sudo; exit 0; else echo none; exit 1; fi`
}

func ParsePrivilege(stdout string) (string, error) {
	for _, line := range strings.Fields(stdout) {
		if line == "root" || line == "sudo" {
			return line, nil
		}
	}
	return "", fmt.Errorf("root or passwordless sudo is required")
}

// PrivilegedCmd wraps a fixed command for execution via passwordless sudo.
// The caller only supplies commands assembled by this package, never raw user
// input. Single quotes are escaped using the standard POSIX shell sequence.
func PrivilegedCmd(mode, command string) string {
	if mode == "root" {
		return command
	}
	escaped := strings.ReplaceAll(command, "'", `'"'"'`)
	return "sudo -n sh -c '" + escaped + "'"
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
