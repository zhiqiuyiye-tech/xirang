package storage

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"strings"
	"testing"
	"time"
	"xirang/control_panel/internal/db"
)

type namespaceTestRunner struct {
	out            string
	code           int
	err            error
	command, input string
	calls          int
}

func (r *namespaceTestRunner) Run(context.Context, db.WorkerNode, string) (string, string, int, error) {
	panic("must use JSON stdin")
}
func (r *namespaceTestRunner) RunWithStdin(_ context.Context, _ db.WorkerNode, cmd string, in io.Reader) (string, string, int, error) {
	r.calls++
	r.command = cmd
	b, _ := io.ReadAll(in)
	r.input = string(b)
	return r.out, "", r.code, r.err
}

func TestNamespaceRecoveryInspectStrict(t *testing.T) {
	for _, out := range []string{"", `{}`, `{"ok":true,"result":{}}`, `{"ok":true,"result":{"uuid":"u","major_minor":"253:0","extra":1}}`, `{"ok":true,"result":{"uuid":"u","major_minor":"253:0"}} trailing`, `{"ok":true,"result":{"uuid":"u","uuid":"v","major_minor":"253:0"}}`} {
		r := &namespaceTestRunner{out: out}
		_, err := NewNamespaceRecovery(r, nil, time.Second).Inspect(context.Background(), db.WorkerNode{}, "/dev/vg/lv")
		if err == nil {
			t.Fatalf("accepted %q", out)
		}
	}
	r := &namespaceTestRunner{out: `{"ok":true,"result":{"uuid":"u","major_minor":"253:0"}}`}
	id, err := NewNamespaceRecovery(r, []string{"/data01"}, time.Second).Inspect(context.Background(), db.WorkerNode{}, "/dev/vg/lv")
	if err != nil || id.UUID != "u" {
		t.Fatalf("%+v %v", id, err)
	}
	for _, part := range []string{"cp-storage-namespace-inspect", "python3 -I", "timeout", "env -i"} {
		if !strings.Contains(r.command, part) {
			t.Fatalf("missing %s", part)
		}
	}
	var req map[string]any
	if json.Unmarshal([]byte(r.input), &req) != nil || req["lv_dev"] != "/dev/vg/lv" {
		t.Fatal(r.input)
	}
}
func TestNamespaceRecoveryScanAndVerifyStrict(t *testing.T) {
	r := &namespaceTestRunner{out: `{"ok":true,"result":{"device":{"uuid":"u","major_minor":"253:0"},"holders":[]}}`}
	n := NewNamespaceRecovery(r, nil, time.Second)
	s, err := n.Scan(context.Background(), db.WorkerNode{}, "/dev/vg/lv")
	if err != nil || s.Device.UUID != "u" {
		t.Fatal(s, err)
	}
	r.out = `{"ok":true,"result":{"released":true,"device":{"uuid":"u","major_minor":"253:0"}}}`
	if err = n.VerifyReleased(context.Background(), db.WorkerNode{}, "/dev/vg/lv", s.Device); err != nil {
		t.Fatal(err)
	}
	r.out = `{"ok":true,"result":{"released":true,"device":{"uuid":"other","major_minor":"253:0"}}}`
	if n.VerifyReleased(context.Background(), db.WorkerNode{}, "/dev/vg/lv", s.Device) == nil {
		t.Fatal("accepted identity change")
	}
}
func namespaceTestSnapshot() NamespaceSnapshot {
	return NamespaceSnapshot{Device: DeviceIdentity{UUID: "u", MajorMinor: "253:0"}, Holders: []NamespaceHolder{{PID: 123, Namespace: "mnt:[42]", StartTime: "100", Cgroup: "0::/kubepods/test\n", RootDev: 1, RootIno: 2, Mounts: []NamespaceMount{{ID: 10, ParentID: 1, Device: "253:0", Root: "/", Path: "/data02/volume", Optional: []string{}}}, Members: []NamespaceProcess{{PID: 123, StartTime: "100", Cgroup: "0::/kubepods/test\n"}}}}}
}
func TestNamespaceRecoveryCleanupUnknown(t *testing.T) {
	for _, r := range []*namespaceTestRunner{{err: io.ErrUnexpectedEOF}, {code: 124}, {out: ""}, {out: `{"ok":false,"error":"timeout","state_unknown":true}`, code: 1}} {
		err := NewNamespaceRecovery(r, nil, time.Second).Cleanup(context.Background(), db.WorkerNode{}, "/dev/vg/lv", namespaceTestSnapshot())
		if !errors.Is(err, ErrNamespaceStateUnknown) {
			t.Fatalf("want state unknown: %v", err)
		}
	}
	r := &namespaceTestRunner{out: `{"ok":true,"result":{"cleaned":true}}`}
	if err := NewNamespaceRecovery(r, nil, time.Second).Cleanup(context.Background(), db.WorkerNode{}, "/dev/vg/lv", namespaceTestSnapshot()); err != nil {
		t.Fatal(err)
	}
	if r.calls != 1 || !strings.Contains(r.command, "cp-storage-namespace-cleanup") {
		t.Fatal(r.command)
	}
	r.out = `{"ok":false,"error":"mount changed","state_unknown":false}`
	r.code = 1
	if err := NewNamespaceRecovery(r, nil, time.Second).Cleanup(context.Background(), db.WorkerNode{}, "/dev/vg/lv", namespaceTestSnapshot()); err == nil || errors.Is(err, ErrNamespaceStateUnknown) {
		t.Fatal(err)
	}
}
func TestNamespaceRecoveryRejectsInvalidInput(t *testing.T) {
	r := &namespaceTestRunner{}
	n := NewNamespaceRecovery(r, nil, time.Second)
	for _, dev := range []string{"/dev/vg/lv;touch /tmp/x", "/dev/../lv", "/dev/mapper/x", ""} {
		if _, err := n.Inspect(context.Background(), db.WorkerNode{}, dev); err == nil {
			t.Fatal(dev)
		}
	}
	if r.calls != 0 {
		t.Fatal("sent invalid input")
	}
}
