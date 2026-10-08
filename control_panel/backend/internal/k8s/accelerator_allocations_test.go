package k8s

import (
	"context"
	"errors"
	"reflect"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/fake"
	k8stesting "k8s.io/client-go/testing"
)

func acceleratorTestPod(name, namespace, node string, phase corev1.PodPhase, containers ...corev1.Container) *corev1.Pod {
	return &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: name, Namespace: namespace},
		Spec:       corev1.PodSpec{NodeName: node, Containers: containers},
		Status:     corev1.PodStatus{Phase: phase},
	}
}

func TestListNodeAcceleratorAllocations(t *testing.T) {
	always := corev1.ContainerRestartPolicyAlways
	sidecar := acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2"}, nil)
	sidecar.RestartPolicy = &always
	initPod := acceleratorTestPod("batch-init", "batch", "gpu-node", corev1.PodRunning,
		acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "3"}, nil))
	initPod.Spec.InitContainers = []corev1.Container{sidecar, acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "6"}, nil)}
	terminating := acceleratorTestPod("terminating", "other", "gpu-node", corev1.PodRunning,
		acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "1"}, nil))
	now := metav1.Now()
	terminating.DeletionTimestamp = &now
	cs := fake.NewSimpleClientset(
		&corev1.Node{
			ObjectMeta: metav1.ObjectMeta{Name: "gpu-node"},
			Status: corev1.NodeStatus{
				Addresses: []corev1.NodeAddress{
					{Type: corev1.NodeExternalIP, Address: "203.0.113.1"},
					{Type: corev1.NodeInternalIP, Address: "10.0.0.1"},
					{Type: corev1.NodeInternalIP, Address: "10.0.0.9"},
				},
				Allocatable: acceleratorTestResources(map[string]string{
					"nvidia.com/gpu": "8", "huawei.com/Ascend910B": "4", "amd.com/gpu": "1", "hygon.com/dcu": "2",
					"huawei.com/Ascend910B-memory": "64000", "huawei.com/Ascend910B-cores": "100", "huawei.com/Ascend910B-share": "100", "huawei.com/Ascend910B-percentage": "100",
					"nvidia.com/gpu.shared": "20", "cpu": "64", "memory": "128Gi",
				}),
				Capacity: acceleratorTestResources(map[string]string{"nvidia.com/gpu": "80"}),
			},
		},
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "npu-node"}, Status: corev1.NodeStatus{
			Addresses:   []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.2"}},
			Allocatable: acceleratorTestResources(map[string]string{"huawei.com/Ascend310P": "4"}),
		}},
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "cpu-node"}, Status: corev1.NodeStatus{
			Allocatable: acceleratorTestResources(map[string]string{"cpu": "8", "memory": "16Gi"}),
		}},
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "no-allocatable"}, Status: corev1.NodeStatus{
			Addresses: []corev1.NodeAddress{{Type: corev1.NodeHostName, Address: "host.example"}},
			Capacity:  acceleratorTestResources(map[string]string{"nvidia.com/gpu": "8"}),
		}},
		acceleratorTestPod("training", "other", "gpu-node", corev1.PodRunning,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2"}, map[string]string{"nvidia.com/gpu": "2"}),
			acceleratorTestContainer(nil, map[string]string{"nvidia.com/gpu": "1"})),
		acceleratorTestPod("scheduled-pending", "default", "gpu-node", corev1.PodPending,
			acceleratorTestContainer(map[string]string{"huawei.com/Ascend910B": "3"}, nil)),
		initPod, terminating,
		acceleratorTestPod("unknown-phase", "other", "gpu-node", corev1.PodUnknown,
			acceleratorTestContainer(map[string]string{"amd.com/gpu": "1"}, nil)),
		acceleratorTestPod("npu-training", "other", "npu-node", corev1.PodRunning,
			acceleratorTestContainer(nil, map[string]string{"huawei.com/Ascend310P": "1"})),
		acceleratorTestPod("no-resource", "default", "cpu-node", corev1.PodRunning,
			acceleratorTestContainer(map[string]string{"cpu": "2"}, nil)),
		acceleratorTestPod("allocation-without-total", "default", "no-allocatable", corev1.PodRunning,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2"}, nil)),
		acceleratorTestPod("succeeded", "default", "gpu-node", corev1.PodSucceeded,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "100"}, nil)),
		acceleratorTestPod("failed", "default", "gpu-node", corev1.PodFailed,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "100"}, nil)),
		acceleratorTestPod("unbound-pending", "default", "", corev1.PodPending,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "100"}, nil)),
		acceleratorTestPod("deleted-node", "default", "missing", corev1.PodRunning,
			acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "100"}, nil)),
	)
	got, err := ListNodeAcceleratorAllocations(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	byName := map[string]NodeAcceleratorAllocation{}
	for _, allocation := range got {
		byName[allocation.Name] = allocation
	}
	want := map[string]NodeAcceleratorAllocation{
		"gpu-node":       {Name: "gpu-node", Host: "10.0.0.1", Total: 15, Used: 16},
		"npu-node":       {Name: "npu-node", Host: "10.0.0.2", Total: 4, Used: 1},
		"cpu-node":       {Name: "cpu-node"},
		"no-allocatable": {Name: "no-allocatable", Used: 2},
	}
	if len(got) != len(want) || !reflect.DeepEqual(byName, want) {
		t.Fatalf("got %+v, want %+v", got, want)
	}
}

func TestListNodeAcceleratorAllocationsEmpty(t *testing.T) {
	got, err := ListNodeAcceleratorAllocations(context.Background(), fake.NewSimpleClientset())
	if err != nil || got == nil || len(got) != 0 {
		t.Fatalf("got %+v, %v; want non-nil empty allocations", got, err)
	}
}

func TestListNodeAcceleratorAllocationsErrors(t *testing.T) {
	for _, resource := range []string{"nodes", "pods"} {
		t.Run(resource, func(t *testing.T) {
			cs := fake.NewSimpleClientset()
			wantErr := errors.New("list failed")
			cs.PrependReactor("list", resource, func(k8stesting.Action) (bool, runtime.Object, error) {
				return true, nil, wantErr
			})
			got, err := ListNodeAcceleratorAllocations(context.Background(), cs)
			if !errors.Is(err, wantErr) || got != nil {
				t.Fatalf("got %+v, %v; want nil and original list error", got, err)
			}
		})
	}
}

func TestListNotebookPodsAccelerators(t *testing.T) {
	cs := fake.NewSimpleClientset(
		acceleratorTestPod("notebook-gpu", "users", "gpu-node", corev1.PodRunning,
			acceleratorTestContainer(nil, map[string]string{"nvidia.com/gpu": "2"})),
		acceleratorTestPod("NoteBook-cpu", "users", "cpu-node", corev1.PodPending,
			acceleratorTestContainer(map[string]string{"cpu": "1"}, nil)),
		acceleratorTestPod("training-gpu", "users", "gpu-node", corev1.PodRunning,
			acceleratorTestContainer(nil, map[string]string{"nvidia.com/gpu": "8"})),
	)
	got, err := ListNotebookPods(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	if len(got) != 2 {
		t.Fatalf("got %d notebooks, want 2", len(got))
	}
	for _, pod := range got {
		wantCount := int64(0)
		wantResources := map[string]int64{}
		if pod.Name == "notebook-gpu" {
			wantCount = 2
			wantResources["nvidia.com/gpu"] = 2
		}
		if pod.AcceleratorCount != wantCount || !reflect.DeepEqual(pod.AcceleratorResources, wantResources) {
			t.Fatalf("pod %s got count=%d resources=%v, want count=%d resources=%v", pod.Name, pod.AcceleratorCount, pod.AcceleratorResources, wantCount, wantResources)
		}
	}
}
