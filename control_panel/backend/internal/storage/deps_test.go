package storage

import "testing"

func TestParsePM(t *testing.T) {
	cases := []struct{ in, want string }{
		{"yum\n", "yum"},
		{"dnf\n", "dnf"},
		{"apt\n", "apt"},
		{"yum\ndnf\napt\n", "dnf"}, // dnf 优先
		{"dnf\napt\n", "dnf"},      // dnf 次之
		{"", ""},
		{"\n\n", ""},
	}
	for _, c := range cases {
		got, err := ParsePM(c.in)
		if c.want == "" {
			if err == nil {
				t.Fatalf("expected error for %q", c.in)
			}
			continue
		}
		if err != nil {
			t.Fatalf("unexpected err for %q: %v", c.in, err)
		}
		if got != c.want {
			t.Fatalf("ParsePM(%q)=%q want %q", c.in, got, c.want)
		}
	}
}

func TestParseDepsCheck(t *testing.T) {
	lvm2, nfs := ParseDepsCheck("lvm2_ok\nnfs_ok\n")
	if !lvm2 || !nfs {
		t.Fatalf("expected both, got lvm2=%v nfs=%v", lvm2, nfs)
	}
	lvm2, nfs = ParseDepsCheck("lvm2_ok\n")
	if !lvm2 || nfs {
		t.Fatalf("expected lvm2 only, got lvm2=%v nfs=%v", lvm2, nfs)
	}
	lvm2, nfs = ParseDepsCheck("")
	if lvm2 || nfs {
		t.Fatalf("expected none, got lvm2=%v nfs=%v", lvm2, nfs)
	}
}

func TestInstallDepsCmd(t *testing.T) {
	cases := []struct{ pm, want string }{
		{"yum", "yum install -y lvm2 nfs-utils"},
		{"dnf", "dnf install -y lvm2 nfs-utils"},
		{"apt", "apt-get update -qq && apt-get install -y lvm2 nfs-kernel-server"},
	}
	for _, c := range cases {
		got, err := InstallDepsCmd(c.pm)
		if err != nil {
			t.Fatalf("err for %q: %v", c.pm, err)
		}
		if got != c.want {
			t.Fatalf("InstallDepsCmd(%q)=%q want %q", c.pm, got, c.want)
		}
	}
	if _, err := InstallDepsCmd("pacman"); err == nil {
		t.Fatal("expected error for unknown pm")
	}
}

func TestDetectPMOutput(t *testing.T) {
	if DetectPMOutput() == "" {
		t.Fatal("empty")
	}
	if !contains(DetectPMOutput(), "command -v yum") {
		t.Fatal("no yum probe")
	}
}

func TestCheckDepsCmd(t *testing.T) {
	if CheckDepsCmd() == "" {
		t.Fatal("empty")
	}
	if !contains(CheckDepsCmd(), "lvcreate") || !contains(CheckDepsCmd(), "exportfs") {
		t.Fatal("missing probes")
	}
}

func TestDetectPMOutputUsesSuccessfulConditionalChain(t *testing.T) {
	cmd := DetectPMOutput()
	if !contains(cmd, "if command -v dnf") || !contains(cmd, "elif command -v yum") || !contains(cmd, "elif command -v apt-get") {
		t.Fatalf("package manager detection is not a single conditional chain: %s", cmd)
	}
	if !contains(cmd, "exit 0") {
		t.Fatalf("successful detection must explicitly exit zero: %s", cmd)
	}
}

func TestPrivilegeDetectionAndWrapping(t *testing.T) {
	if !contains(DetectPrivilegeCmd(), "sudo -n true") || !contains(DetectPrivilegeCmd(), "id -u") {
		t.Fatalf("privilege probe missing checks: %s", DetectPrivilegeCmd())
	}
	for input, want := range map[string]string{"root\n": "root", "sudo\n": "sudo"} {
		got, err := ParsePrivilege(input)
		if err != nil || got != want {
			t.Fatalf("ParsePrivilege(%q)=%q,%v want %q", input, got, err, want)
		}
	}
	if _, err := ParsePrivilege("none\n"); err == nil {
		t.Fatal("expected unsupported privilege error")
	}
	if got := PrivilegedCmd("root", "dnf install -y lvm2"); got != "dnf install -y lvm2" {
		t.Fatalf("root wrapper=%q", got)
	}
	got := PrivilegedCmd("sudo", "touch /etc/nfs.conf && echo 'x'")
	if !contains(got, "sudo -n sh -c") || !contains(got, "'\"'\"'") {
		t.Fatalf("sudo wrapper does not safely quote command: %s", got)
	}
}

func TestNFSServiceAndCommands(t *testing.T) {
	if got := NFSServiceName("apt"); got != "nfs-kernel-server" {
		t.Fatalf("NFSServiceName(apt) = %s, want nfs-kernel-server", got)
	}
	if got := NFSServiceName("yum"); got != "nfs-server" {
		t.Fatalf("NFSServiceName(yum) = %s, want nfs-server", got)
	}
	if got := NFSServiceName("dnf"); got != "nfs-server" {
		t.Fatalf("NFSServiceName(dnf) = %s, want nfs-server", got)
	}

	confCmd := ConfigureNFSv4Cmd()
	if !contains(confCmd, "[nfsd]") || !contains(confCmd, "vers4=y") || !contains(confCmd, "vers2=n") {
		t.Fatalf("ConfigureNFSv4Cmd missing key elements: %s", confCmd)
	}

	enableCmd := EnableNFSServiceCmd("yum")
	if enableCmd != "systemctl enable --now nfs-server" {
		t.Fatalf("EnableNFSServiceCmd(yum) = %s", enableCmd)
	}

	ensureCmd := EnsureNFSServiceCmd("apt")
	if !contains(ensureCmd, "nfs-kernel-server") {
		t.Fatalf("EnsureNFSServiceCmd(apt) = %s", ensureCmd)
	}
}
