package api

import (
	"context"
	"errors"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kruntime "k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/fake"
	k8stesting "k8s.io/client-go/testing"

	"xirang/control_panel/internal/db"
)

func TestQueryNFSAssociationsBatchesPodPVCAndPVLists(t *testing.T) {
	client := fake.NewSimpleClientset(
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-1", Namespace: "ns1", UID: "uid-1"}},
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-2", Namespace: "ns2", UID: "uid-2"}},
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "worker-agent", Namespace: "ns1", UID: "uid-3"}},
	)
	result := queryNFSAssociations(context.Background(), client, nil, nil, nil, time.Minute, "")
	if result.errorCode != "" || len(result.pods) != 2 {
		t.Fatalf("unexpected association result: err=%q pods=%+v", result.errorCode, result.pods)
	}
	listCounts := map[string]int{}
	for _, action := range client.Actions() {
		if action.GetVerb() == "list" {
			listCounts[action.GetResource().Resource]++
		}
	}
	for resource, want := range map[string]int{"pods": 1, "persistentvolumeclaims": 1, "persistentvolumes": 1} {
		if listCounts[resource] != want {
			t.Errorf("%s list calls=%d, want %d (one cluster-wide batch)", resource, listCounts[resource], want)
		}
	}
}

func TestQueryNFSAssociationsReturnsSafeLookupFailures(t *testing.T) {
	worker := db.WorkerNode{ID: 7, Name: "worker-a", Host: "worker-a"}
	cases := []struct {
		name     string
		resource string
		wantCode string
	}{
		{name: "PVC list", resource: "persistentvolumeclaims", wantCode: "pvc_list_failed"},
		{name: "PV list", resource: "persistentvolumes", wantCode: "pv_list_failed"},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			client := fake.NewSimpleClientset(&corev1.Pod{
				ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns1", UID: "uid-a"},
			})
			client.PrependReactor("list", test.resource, func(k8stesting.Action) (bool, kruntime.Object, error) {
				return true, nil, errors.New("private API details must not escape")
			})
			result := queryNFSAssociations(context.Background(), client, nil, []db.WorkerNode{worker}, nil, time.Minute, "")
			if result.errorCode != test.wantCode || len(result.pods) != 1 || result.pods[0].NFSMountsStatus != "lookup_failed" ||
				result.pods[0].NFSMountsError != test.wantCode || len(result.pods[0].NFSMounts) != 0 {
				t.Fatalf("lookup failure was not represented with a safe code: %+v", result)
			}
			if state := result.workers[worker.ID]; state == nil || state.status != "lookup_failed" || state.errorCode != test.wantCode || len(state.unmatchedMounts) != 0 {
				t.Fatalf("worker lookup failure was not fail-closed: %+v", result.workers[worker.ID])
			}
		})
	}

	client := fake.NewSimpleClientset()
	client.PrependReactor("list", "pods", func(k8stesting.Action) (bool, kruntime.Object, error) {
		return true, nil, errors.New("private Pod list detail")
	})
	podFailure := queryNFSAssociations(context.Background(), client, nil, []db.WorkerNode{worker}, nil, time.Minute, "")
	if podFailure.errorCode != "pod_list_failed" || !podFailure.podListFailed || podFailure.workers[worker.ID].status != "lookup_failed" {
		t.Fatalf("Pod list error should be classified separately: %+v", podFailure)
	}

	noClient := queryNFSAssociations(context.Background(), nil, nil, []db.WorkerNode{worker}, nil, time.Minute, "")
	if noClient.errorCode != "k8s_client_unavailable" || noClient.workers[worker.ID].status != "lookup_failed" {
		t.Fatalf("unavailable client should be fail-closed: %+v", noClient)
	}
}

func TestQueryNFSAssociationsUsesPreflightFailureWithoutLosingPods(t *testing.T) {
	client := fake.NewSimpleClientset(&corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns1", UID: "uid-a"},
	})
	result := queryNFSAssociations(context.Background(), client, nil, nil, nil, time.Minute, "inventory_snapshot_list_failed")
	if len(result.pods) != 1 || result.pods[0].NFSMountsStatus != "lookup_failed" ||
		result.pods[0].NFSMountsError != "inventory_snapshot_list_failed" {
		t.Fatalf("preflight failure should retain base Pod data and mark associations unavailable: %+v", result)
	}
}
