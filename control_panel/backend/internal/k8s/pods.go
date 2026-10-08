package k8s

import (
	"context"
	"fmt"
	"strings"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// PodInfo is a discovered cluster pod (filtered to notebook pods), used by the
// UI to drive port-mapping (SVC) creation: selecting a pod auto-fills its
// namespace/name/uid/selector so the admin only enters ports.
type PodInfo struct {
	Name                 string            `json:"name"`
	Namespace            string            `json:"namespace"`
	UID                  string            `json:"uid"`
	Node                 string            `json:"node"`
	Status               string            `json:"status"`
	IPs                  []string          `json:"ips"`
	Labels               map[string]string `json:"labels"`
	StableKey            string            `json:"stable_key"`
	KeyKind              string            `json:"key_kind"`
	WorkspaceID          string            `json:"workspace_id,omitempty"`
	ProjectID            string            `json:"project_id,omitempty"`
	OwnerName            string            `json:"owner_name,omitempty"`
	Note                 string            `json:"note,omitempty"`
	UpdatedBy            string            `json:"updated_by,omitempty"`
	MetadataUpdatedAt    *time.Time        `json:"metadata_updated_at,omitempty"`
	AcceleratorCount     int64             `json:"accelerator_count"`
	AcceleratorResources map[string]int64  `json:"accelerator_resources"`
}

// StableKeyForPod derives the persistence key for Notebook metadata.
// When business tags workspace_id and project_id are both present, the key
// stays consistent across Pod recreations. Otherwise it safely falls back to
// the current Pod UID.
func StableKeyForPod(namespace, uid string, labels map[string]string) (key string, kind string, workspaceID string, projectID string) {
	ws := ""
	proj := ""
	if labels != nil {
		ws = strings.TrimSpace(labels["workspace_id"])
		proj = strings.TrimSpace(labels["project_id"])
	}
	if ws != "" && proj != "" {
		return fmt.Sprintf("v1:namespace:%s:workspace:%s:project:%s", namespace, ws, proj), "business_labels", ws, proj
	}
	return fmt.Sprintf("v1:pod_uid:%s", uid), "pod_uid", ws, proj
}

// ListNotebookPods returns all pods whose name contains "notebook"
// (case-insensitive), across every namespace. Served from the API server
// watch cache (ResourceVersion=0) - the name filter is client-side so a
// server-side selector is not possible, but the cached read avoids an etcd
// quorum read on large clusters.
func ListNotebookPods(ctx context.Context, client kubernetes.Interface) ([]PodInfo, error) {
	objects, err := ListNotebookPodObjects(ctx, client)
	if err != nil {
		return nil, err
	}
	out := make([]PodInfo, 0, len(objects))
	for _, pod := range objects {
		out = append(out, NotebookPodInfo(pod))
	}
	return out, nil
}

// ListNotebookPodObjects returns the filtered Kubernetes Pod objects so the
// API layer can resolve PVC references from the same batch Pod list used to
// construct the public PodInfo response.
func ListNotebookPodObjects(ctx context.Context, client kubernetes.Interface) ([]corev1.Pod, error) {
	list, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		return nil, err
	}
	out := make([]corev1.Pod, 0, len(list.Items))
	for i := range list.Items {
		pod := list.Items[i]
		if strings.Contains(strings.ToLower(pod.Name), "notebook") {
			out = append(out, pod)
		}
	}
	return out, nil
}

// NotebookPodInfo converts a Kubernetes Pod object into the existing public
// Pod DTO while preserving the stable metadata key behavior.
func NotebookPodInfo(pod corev1.Pod) PodInfo {
	ips := []string{}
	if pod.Status.PodIP != "" {
		ips = append(ips, pod.Status.PodIP)
	}
	for _, ip := range pod.Status.PodIPs {
		if ip.IP != "" && ip.IP != pod.Status.PodIP {
			ips = append(ips, ip.IP)
		}
	}
	stableKey, kind, ws, proj := StableKeyForPod(pod.Namespace, string(pod.UID), pod.Labels)
	accelerators := podAcceleratorRequests(pod)
	return PodInfo{
		Name:                 pod.Name,
		Namespace:            pod.Namespace,
		UID:                  string(pod.UID),
		Node:                 pod.Spec.NodeName,
		Status:               string(pod.Status.Phase),
		IPs:                  ips,
		Labels:               pod.Labels,
		StableKey:            stableKey,
		KeyKind:              kind,
		WorkspaceID:          ws,
		ProjectID:            proj,
		AcceleratorCount:     acceleratorResourceCount(accelerators),
		AcceleratorResources: accelerators,
	}
}
