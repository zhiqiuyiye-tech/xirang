package storage

import "testing"

func TestParsePM(t *testing.T) {
	cases := []struct{ in, want string }{
		{"yum\n", "yum"},
		{"dnf\n", "dnf"},
		{"apt\n", "apt"},
		{"yum\ndnf\napt\n", "yum"},  // yum 优先
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
