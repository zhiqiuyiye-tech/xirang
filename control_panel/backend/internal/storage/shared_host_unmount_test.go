package storage

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
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

func sharedDeleteRunner(t *testing.T) *scriptRunner {
	t.Helper()
	sr := newScriptRunner()
	sr.add("findmnt -rn -o TARGET --source /dev/vg_data/lv_1", scriptResult{stdout: "/data02/share\n"}, scriptResult{})
	sr.add("cp-storage-namespace-delete_inspect", scriptResult{stdout: `{"ok":true,"result":{"device":{"uuid":"u","major_minor":"253:0"},"requires_host_authorization":true}}`})
	sr.add("cp-storage-namespace-host_plan", scriptResult{stdout: sharedPlanJSON(t, sharedHostTestPlan())})
	sr.add("cp-storage-namespace-host_unmount", scriptResult{stdout: `{"ok":true,"result":{"unmounted":true,"device":{"uuid":"u","major_minor":"253:0"}}}`})
	sr.add("cp-storage-namespace-host_verify", scriptResult{stdout: `{"ok":true,"result":{"released":true,"device":{"uuid":"u","major_minor":"253:0"}}}`})
	return sr
}

func TestSharedHostDeleteAuthorizesBeforeMutationAndRechecksBeforeUnmount(t *testing.T) {
	sr := sharedDeleteRunner(t)
	calls := 0
	authorize := func(_ context.Context, _, export string, holders []NamespaceHolder) error {
		calls++
		if export != "/data02/share" || len(holders) != 1 || holders[0].PID == 1 {
			return fmt.Errorf("incorrect foreign holder authorization scope")
		}
		if calls == 1 && sr.counts["cp-storage-namespace-host_unmount"] != 0 {
			return fmt.Errorf("mutated before authorization")
		}
		return nil
	}
	store, id := submitRecoveryDelete(t, sr, WithHostUnmountAuthorizer(authorize))
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if calls != 3 || sr.counts["cp-storage-namespace-host_unmount"] != 1 {
		t.Fatalf("authorization=%d unmount=%d", calls, sr.counts["cp-storage-namespace-host_unmount"])
	}
	for _, cmd := range sr.calls {
		if strings.Contains(cmd, "umount /data02/share") || strings.Contains(cmd, "--make-private") || strings.Contains(cmd, "--make-rprivate") {
			t.Fatal("shared deletion bypassed the verified RPC or changed propagation")
		}
	}
}

func TestSharedHostDeleteStopsBeforeMutationOnUnknownHolders(t *testing.T) {
	for _, authorize := range []NamespaceCleanupAuthorizer{nil, func(context.Context, string, string, []NamespaceHolder) error { return fmt.Errorf("unknown holder") }} {
		sr := sharedDeleteRunner(t)
		store, id := submitRecoveryDelete(t, sr, WithHostUnmountAuthorizer(authorize))
		waitFor(t, store, id, "failed", 2*time.Second)
		for _, cmd := range sr.calls {
			if strings.Contains(cmd, "sed -i") || strings.Contains(cmd, "exportfs -arv") || strings.Contains(cmd, "lvremove -f /dev/vg_data/lv_1") {
				t.Fatal("unknown holders must stop before exports, unmount, and lvremove")
			}
		}
		if sr.counts["cp-storage-namespace-host_unmount"] != 0 {
			t.Fatal("unknown holder was unmounted")
		}
	}
}

func TestSharedHostDeleteStopsWhenPlanOrAuthorizationChanges(t *testing.T) {
	for _, change := range []string{"proof", "authorization", "pod", "timeout", "open_count"} {
		t.Run(change, func(t *testing.T) {
			sr := sharedDeleteRunner(t)
			original := sharedHostTestPlan()
			changed := sharedHostTestPlan()
			changed.Proof = strings.Repeat("b", 64)
			if change == "proof" {
				sr.add("cp-storage-namespace-host_plan", scriptResult{stdout: sharedPlanJSON(t, original)}, scriptResult{stdout: sharedPlanJSON(t, changed)})
			}
			if change == "open_count" {
				sr.add("cp-storage-namespace-host_verify", scriptResult{stdout: `{"ok":false,"error":"Open Count remains nonzero","state_unknown":false}`, exitCode: 1})
			}
			if change == "timeout" {
				sr.add("cp-storage-namespace-host_unmount", scriptResult{exitCode: 124})
			}
			calls := 0
			authorize := func(context.Context, string, string, []NamespaceHolder) error {
				calls++
				if change == "authorization" && calls > 1 {
					return fmt.Errorf("authorization changed")
				}
				return nil
			}
			guards := 0
			guard := func(context.Context, string, string) (bool, []string, error) {
				guards++
				return change == "pod" && guards > 1, []string{"new/business"}, nil
			}
			store, id := submitRecoveryDelete(t, sr, WithHostUnmountAuthorizer(authorize), WithPodGuardChecker(guard))
			waitFor(t, store, id, "failed", 2*time.Second)
			if sr.counts["lvremove -f /dev/vg_data/lv_1"] != 0 {
				t.Fatal("unsafe lvremove after changed evidence")
			}
			if change != "timeout" && change != "open_count" && sr.counts["cp-storage-namespace-host_unmount"] != 0 {
				t.Fatal("unmounted after changed evidence")
			}
		})
	}
}
