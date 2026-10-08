package k8s

import (
	"context"
	"fmt"
	"strings"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// NodeAcceleratorAllocation reports Kubernetes device allocations, rather than
// hardware utilization. Total is the sum of count-based allocatable resources;
// Used is the effective device request of all non-terminal pods bound to the node.
// Device plugins may advertise logical devices, so these are not necessarily
// physical card counts. Used is not clamped to Total.
type NodeAcceleratorAllocation struct {
	Name  string `json:"name"`
	Host  string `json:"host"`
	Total int64  `json:"total"`
	Used  int64  `json:"used"`
}

// ListNodeAcceleratorAllocations includes every node, including nodes without
// accelerators. Host is its first InternalIP (empty if absent). All namespaces
// and workloads are included, not only notebooks. Bound Pending/Unknown and
// terminating non-terminal pods still reserve resources; Succeeded/Failed and
// unbound pods do not. A pod referencing a node absent from the node list is
// ignored, since it cannot be matched to a current worker.
func ListNodeAcceleratorAllocations(ctx context.Context, client kubernetes.Interface) ([]NodeAcceleratorAllocation, error) {
	nodes, err := client.CoreV1().Nodes().List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		return nil, fmt.Errorf("list nodes for accelerator allocations: %w", err)
	}
	pods, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		return nil, fmt.Errorf("list pods for accelerator allocations: %w", err)
	}
	out := make([]NodeAcceleratorAllocation, 0, len(nodes.Items))
	byName := make(map[string]int, len(nodes.Items))
	for _, node := range nodes.Items {
		host := ""
		for _, address := range node.Status.Addresses {
			if address.Type == corev1.NodeInternalIP {
				host = address.Address
				break
			}
		}
		byName[node.Name] = len(out)
		out = append(out, NodeAcceleratorAllocation{
			Name:  node.Name,
			Host:  host,
			Total: acceleratorResourceCount(acceleratorResourceCounts(node.Status.Allocatable)),
		})
	}
	for _, pod := range pods.Items {
		if pod.Spec.NodeName == "" || pod.Status.Phase == corev1.PodSucceeded || pod.Status.Phase == corev1.PodFailed {
			continue
		}
		if index, ok := byName[pod.Spec.NodeName]; ok {
			out[index].Used += acceleratorResourceCount(podAcceleratorRequests(pod))
		}
	}
	return out, nil
}

// isAcceleratorCountResource deliberately recognizes device-count names, not
// arbitrary resources containing "gpu" or "npu". Ascend device models vary, so
// their suffix is flexible, but memory/core/share/percentage units are excluded.
func isAcceleratorCountResource(name corev1.ResourceName) bool {
	lower := strings.ToLower(string(name))
	switch lower {
	case "nvidia.com/gpu", "amd.com/gpu", "hygon.com/dcu", "cambricon.com/mlu":
		return true
	}
	if !strings.HasPrefix(lower, "huawei.com/ascend") {
		return false
	}
	for _, unit := range []string{"memory", "mem", "core", "share", "percent", "ratio", "utilization"} {
		if strings.Contains(lower, unit) {
			return false
		}
	}
	return true
}

func acceleratorResourceCounts(resources corev1.ResourceList) map[string]int64 {
	out := map[string]int64{}
	for name, quantity := range resources {
		if !isAcceleratorCountResource(name) {
			continue
		}
		// Accept exact whole quantities even when represented as "2.0" or
		// "2000m". Value rounds, so the fallback must verify exact equality
		// to avoid treating a fractional device request as a whole card.
		count, exact := quantity.AsInt64()
		if !exact {
			count = quantity.Value()
			exact = quantity.Cmp(*resource.NewQuantity(count, resource.DecimalSI)) == 0
		}
		if exact && count > 0 {
			out[string(name)] = count
		}
	}
	return out
}

// containerAcceleratorRequests applies request precedence per resource. Limits
// are a fallback only when the resource key is missing from Requests; an explicit
// zero request also overrides its limit. The two values are never added together.
func containerAcceleratorRequests(container corev1.Container) map[string]int64 {
	out := acceleratorResourceCounts(container.Resources.Requests)
	for name, count := range acceleratorResourceCounts(container.Resources.Limits) {
		if _, requested := container.Resources.Requests[corev1.ResourceName(name)]; !requested {
			out[name] = count
		}
	}
	return out
}

// podAcceleratorRequests follows Kubernetes effective request accounting per
// resource: sum application containers and restartable init containers, then take
// the maximum against each initialization stage. An ordinary init stage overlaps
// only the restartable init containers preceding it, not those started later.
// Pod overhead is added after this per-resource maximum. Ephemeral containers
// do not reserve additional scheduler resources and are intentionally excluded.
func podAcceleratorRequests(pod corev1.Pod) map[string]int64 {
	app := map[string]int64{}
	for _, container := range pod.Spec.Containers {
		addAcceleratorResources(app, containerAcceleratorRequests(container))
	}
	restartable := map[string]int64{}
	initPeak := map[string]int64{}
	for _, container := range pod.Spec.InitContainers {
		stage := containerAcceleratorRequests(container)
		if container.RestartPolicy != nil && *container.RestartPolicy == corev1.ContainerRestartPolicyAlways {
			addAcceleratorResources(app, stage)
			addAcceleratorResources(restartable, stage)
			// The restartable stage's effective request is the cumulative
			// restartable request, including this container exactly once.
			stage = restartable
		} else {
			addAcceleratorResources(stage, restartable)
		}
		maxAcceleratorResources(initPeak, stage)
	}
	maxAcceleratorResources(app, initPeak)
	addAcceleratorResources(app, acceleratorResourceCounts(pod.Spec.Overhead))
	return app
}

func addAcceleratorResources(dst, src map[string]int64) {
	for name, count := range src {
		dst[name] += count
	}
}

func maxAcceleratorResources(dst, src map[string]int64) {
	for name, count := range src {
		if count > dst[name] {
			dst[name] = count
		}
	}
}

func acceleratorResourceCount(resources map[string]int64) int64 {
	var total int64
	for _, count := range resources {
		total += count
	}
	return total
}
