package k8s

import (
	"context"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestAcceleratorAllocationCacheTracksWorkloadChangesWithoutRequestLists(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	cs := fake.NewSimpleClientset(
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker"}, Status: corev1.NodeStatus{Allocatable: corev1.ResourceList{"nvidia.com/gpu": resource.MustParse("2")}}},
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns"}, Spec: corev1.PodSpec{NodeName: "worker", Containers: []corev1.Container{{Name: "notebook", Resources: corev1.ResourceRequirements{Limits: corev1.ResourceList{"nvidia.com/gpu": resource.MustParse("1")}}}}}, Status: corev1.PodStatus{Phase: corev1.PodRunning}},
	)
	cache := NewAcceleratorAllocationCache(ctx, cs)
	waitFor := func(used, total int64) {
		t.Helper()
		timeout, stop := context.WithTimeout(ctx, 5*time.Second)
		defer stop()
		for {
			rows, err := cache.Snapshot(timeout)
			if err == nil && len(rows) == 1 && rows[0].Used == used && rows[0].Total == total {
				return
			}
			select {
			case <-timeout.Done():
				t.Fatalf("allocation snapshot rows=%+v err=%v; want %d/%d", rows, err, used, total)
			case <-time.After(10 * time.Millisecond):
			}
		}
	}
	waitFor(1, 2)
	listCount := func() int {
		count := 0
		for _, action := range cs.Actions() {
			if action.GetVerb() == "list" {
				count++
			}
		}
		return count
	}
	initialLists := listCount()
	for range 5 {
		waitFor(1, 2)
	}
	if listCount() != initialLists {
		t.Fatalf("page visits made new list calls: before=%d after=%d", initialLists, listCount())
	}
	pod, err := cs.CoreV1().Pods("ns").Get(ctx, "notebook-a", metav1.GetOptions{})
	if err != nil {
		t.Fatal(err)
	}
	pod.Status.Phase = corev1.PodSucceeded
	if _, err := cs.CoreV1().Pods("ns").UpdateStatus(ctx, pod, metav1.UpdateOptions{}); err != nil {
		t.Fatal(err)
	}
	waitFor(0, 2)
	pod.Name = "ordinary-gpu-workload"
	pod.ResourceVersion = ""
	pod.Status.Phase = corev1.PodRunning
	if _, err := cs.CoreV1().Pods("ns").Create(ctx, pod, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	waitFor(1, 2)
	if err := cs.CoreV1().Pods("ns").Delete(ctx, pod.Name, metav1.DeleteOptions{}); err != nil {
		t.Fatal(err)
	}
	waitFor(0, 2)
	node, err := cs.CoreV1().Nodes().Get(ctx, "worker", metav1.GetOptions{})
	if err != nil {
		t.Fatal(err)
	}
	node.Status.Allocatable["nvidia.com/gpu"] = resource.MustParse("4")
	if _, err := cs.CoreV1().Nodes().UpdateStatus(ctx, node, metav1.UpdateOptions{}); err != nil {
		t.Fatal(err)
	}
	waitFor(0, 4)
	rows, err := cache.Snapshot(ctx)
	if err != nil {
		t.Fatal(err)
	}
	rows[0].Total = 99
	waitFor(0, 4)
	if listCount() != initialLists {
		t.Fatal("workload updates triggered request-time list calls")
	}
}

func TestAcceleratorAllocationCacheDoesNotReportZeroBeforeSync(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	cache := NewAcceleratorAllocationCache(ctx, fake.NewSimpleClientset())
	rows, err := cache.Snapshot(ctx)
	if err == nil || rows != nil {
		t.Fatalf("unsynced allocation cache rows=%+v err=%v", rows, err)
	}
}
