package api

import (
	"testing"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
)

func TestResolvePodNFSMountMarksWorkerCandidatesWithoutGuessing(t *testing.T) {
	pod := k8s.PodInfo{Name: "notebook-a", Namespace: "ns1", UID: "uid-a", OwnerName: "Alice", Note: "job"}
	workers := []db.WorkerNode{
		{ID: 1, Name: "worker-a", Host: "WORKER-A.EXAMPLE."},
		{ID: 2, Name: "worker-b", Host: "worker-a.example"},
	}
	states := map[int64]*workerMountAssociation{
		1: {unmatchedMounts: []unmatchedNFSMountInfo{}, mountedPodsByLV: map[string][]mountedPodInfo{}},
		2: {unmatchedMounts: []unmatchedNFSMountInfo{}, mountedPodsByLV: map[string][]mountedPodInfo{}},
	}
	mount := podNFSMount{
		Status: "unmatched", NFSSourceConfirmed: true, PVCName: "claim", PVName: "pv",
		nfsServer: "worker-a.example", nfsPath: "/exports/share/user",
		ContainerMounts: []containerMountInfo{},
	}
	resolvePodNFSMount(&mount, pod, indexWorkersByServer(workers), nil, states, 0)
	if mount.Status != "ambiguous" || mount.Reason != "multiple_workers" || mount.WorkerID != nil || mount.Capacity != nil {
		t.Fatalf("multiple Worker records sharing an address must not be guessed: %+v", mount)
	}
	for _, workerID := range []int64{1, 2} {
		state := states[workerID]
		if summarizeWorkerMounts(state) != "partial" || len(state.unmatchedMounts) != 1 {
			t.Fatalf("candidate Worker %d should receive one partial warning: %+v", workerID, state)
		}
		warning := state.unmatchedMounts[0]
		if warning.Status != "ambiguous" || warning.Reason != "multiple_workers" || !warning.CandidateWorker || warning.PodUID != "uid-a" {
			t.Fatalf("candidate warning should identify the Pod without assigning it: %+v", warning)
		}
	}
}

func TestUnsupportedNFSSourceCreatesCandidateWorkerWarnings(t *testing.T) {
	pod := k8s.PodInfo{Name: "notebook-a", Namespace: "ns1", UID: "uid-a"}
	worker := db.WorkerNode{ID: 3, Name: "worker-a", Host: "worker-a"}
	state := &workerMountAssociation{unmatchedMounts: []unmatchedNFSMountInfo{}, mountedPodsByLV: map[string][]mountedPodInfo{}}
	mount := podNFSMount{
		Status: "unsupported", Reason: "missing_csi_share", NFSSourceConfirmed: true,
		PVCName: "claim", PVName: "pv", nfsServer: "worker-a", ContainerMounts: []containerMountInfo{},
	}
	resolvePodNFSMount(&mount, pod, indexWorkersByServer([]db.WorkerNode{worker}), nil, map[int64]*workerMountAssociation{worker.ID: state}, 0)
	if mount.Status != "unsupported" || mount.Reason != "missing_csi_share" {
		t.Fatalf("Pod-side source status should stay unsupported: %+v", mount)
	}
	if len(state.unmatchedMounts) != 1 {
		t.Fatalf("the unique Worker candidate should receive an unsupported warning: %+v", state)
	}
	warning := state.unmatchedMounts[0]
	if warning.Status != "unsupported" || warning.Reason != "missing_csi_share" || warning.SourceStatus != "unsupported" || warning.CandidateWorker {
		t.Fatalf("unsupported-source Worker warning has the wrong fields: %+v", warning)
	}
}

func TestNormalizeNFSServerAndPathIsLiteralAndPOSIX(t *testing.T) {
	serverCases := []struct {
		input string
		want  string
		ok    bool
	}{
		{input: " WORKER-A.EXAMPLE. ", want: "worker-a.example", ok: true},
		{input: "10.0.0.1", want: "10.0.0.1", ok: true},
		{input: "2001:db8::1", want: "2001:db8::1", ok: true},
		{input: "worker-a:2049", ok: false},
		{input: "", ok: false},
	}
	for _, test := range serverCases {
		got, ok := normalizeNFSServer(test.input)
		if got != test.want || ok != test.ok {
			t.Errorf("normalizeNFSServer(%q) = %q, %v; want %q, %v", test.input, got, ok, test.want, test.ok)
		}
	}

	pathCases := []struct {
		input string
		want  string
		ok    bool
	}{
		{input: "/exports//notebook/../data", want: "/exports/data", ok: true},
		{input: "/share", want: "/share", ok: true},
		{input: "share", ok: false},
		{input: "", ok: false},
	}
	for _, test := range pathCases {
		got, ok := normalizeNFSPath(test.input)
		if got != test.want || ok != test.ok {
			t.Errorf("normalizeNFSPath(%q) = %q, %v; want %q, %v", test.input, got, ok, test.want, test.ok)
		}
	}
}
