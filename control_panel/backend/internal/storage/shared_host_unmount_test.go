package storage

import (
	"context"
	"encoding/json"
	"errors"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

func sharedHostTestPlan() SharedHostUnmountPlan {
	holder := namespaceTestSnapshot().Holders[0]
	holder.Mounts[0].Path = "/host-data/share"
	holder.Mounts[0].Optional = []string{"master:578"}
	host := NamespaceHolder{
		PID: 1, Namespace: "mnt:[1]", StartTime: "100", Cgroup: "0::/init.scope",
		RootDev: 8, RootIno: 1,
		Mounts:  []NamespaceMount{{ID: 1091, ParentID: 97, Device: "253:0", Root: "/", Path: "/data02/share", Optional: []string{"shared:578"}}},
		Members: []NamespaceProcess{{PID: 1, StartTime: "100", Cgroup: "0::/init.scope"}},
	}
	return SharedHostUnmountPlan{Mode: "strict", Device: DeviceIdentity{UUID: "u", MajorMinor: "253:0"}, Host: host, Holders: []NamespaceHolder{holder}, Proof: strings.Repeat("a", 64)}
}

func sharedPlanJSON(t *testing.T, plan SharedHostUnmountPlan) string {
	t.Helper()
	data, err := json.Marshal(map[string]any{"ok": true, "result": plan})
	if err != nil {
		t.Fatal(err)
	}
	return string(data)
}

func TestSharedHostUnmountProtocol(t *testing.T) {
	plan := sharedHostTestPlan()
	runner := &namespaceTestRunner{out: sharedPlanJSON(t, plan)}
	n := NewNamespaceRecovery(runner, nil, time.Second)
	got, err := n.PlanHostUnmount(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan.Device, []string{"/data02/share"})
	if err != nil || got.Proof != plan.Proof {
		t.Fatal(got, err)
	}
	if !strings.Contains(runner.command, "cp-storage-namespace-host_plan") || !strings.Contains(runner.input, `"paths":["/data02/share"]`) {
		t.Fatal("missing structured host plan request")
	}
	runner.out = `{"ok":true,"result":{"unmounted":true,"device":{"uuid":"u","major_minor":"253:0"}}}`
	if err := n.UnmountHost(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan); err != nil {
		t.Fatal(err)
	}
	for _, code := range []int{124, 137} {
		runner.code = code
		if err := n.UnmountHost(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan); !errors.Is(err, ErrNamespaceStateUnknown) {
			t.Fatalf("host unmount timeout must quarantine worker: %v", err)
		}
	}
}

func TestSharedHostUnmountInvalidEvidenceNeverRuns(t *testing.T) {
	for _, mutate := range []func(*SharedHostUnmountPlan){
		func(p *SharedHostUnmountPlan) { p.Proof = "untrusted" },
		func(p *SharedHostUnmountPlan) { p.Host.PID = 999 },
		func(p *SharedHostUnmountPlan) { p.Holders[0].Namespace = p.Host.Namespace },
		func(p *SharedHostUnmountPlan) { p.Host.Mounts[0].Device = "8:3" },
	} {
		plan := sharedHostTestPlan()
		mutate(&plan)
		runner := &namespaceTestRunner{}
		err := NewNamespaceRecovery(runner, nil, time.Second).UnmountHost(context.Background(), db.WorkerNode{}, "/dev/vg/lv", plan)
		if err == nil || runner.calls != 0 {
			t.Fatal("invalid plan reached remote unmount", err)
		}
	}
}

func TestSharedMountMetadataUsesOrdinaryDeleteUnmount(t *testing.T) {
	sr := residualBeforeRemoveRunner(t)
	authorizerCalls := 0
	store, id := submitDeleteTask(t, sr, "storage_delete_lv", WithHostUnmountAuthorizer(func(context.Context, string, string, []NamespaceHolder) error {
		authorizerCalls++
		return errors.New("unexpected special host authorization")
	}))
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if authorizerCalls != 0 {
		t.Fatalf("shared mount metadata invoked special host authorization %d times", authorizerCalls)
	}
	commands := strings.Join(sr.calls, "\n")
	for _, marker := range []string{"cp-storage-namespace-host_plan", "cp-storage-namespace-host_unmount", "cp-storage-namespace-host_verify"} {
		if strings.Contains(commands, marker) {
			t.Fatalf("delete selected obsolete special host path %q: %v", marker, sr.calls)
		}
	}
	unmount := strings.Index(commands, "umount /data02/share")
	verify := strings.Index(commands, "logical volume is still mounted at:")
	scan := strings.Index(commands, "# cp-storage-namespace-scan_delete")
	if unmount < 0 || verify <= unmount || scan <= verify {
		t.Fatalf("shared mount metadata must still use ordinary host unmount and verification: %v", sr.calls)
	}
	assertNoUnsafeDeleteEscalation(t, sr)
}
