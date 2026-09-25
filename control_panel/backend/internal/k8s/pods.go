package k8s

import (
	"context"
	"fmt"
	"strings"
	"time"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// PodInfo is a discovered cluster pod (filtered to notebook pods), used by the
// UI to drive port-mapping (SVC) creation: selecting a pod auto-fills its
// namespace/name/uid/selector so the admin only enters ports.
type PodInfo struct {
	Name              string            `json:"name"`
	Namespace         string            `json:"namespace"`
	UID               string            `json:"uid"`
	Node              string            `json:"node"`
	Status            string            `json:"status"`
	IPs               []string          `json:"ips"`
	Labels            map[string]string `json:"labels"`
	StableKey         string            `json:"stable_key"`
	KeyKind           string            `json:"key_kind"`
	WorkspaceID       string            `json:"workspace_id,omitempty"`
	ProjectID         string            `json:"project_id,omitempty"`
	OwnerName         string            `json:"owner_name,omitempty"`
	Note              string            `json:"note,omitempty"`
	UpdatedBy         string            `json:"updated_by,omitempty"`
	MetadataUpdatedAt *time.Time        `json:"metadata_updated_at,omitempty"`
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
	list, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{
		ResourceVersion: "0",
	})
	if err != nil {
		return nil, err
	}
	out := make([]PodInfo, 0, len(list.Items))
	for _, p := range list.Items {
		if !strings.Contains(strings.ToLower(p.Name), "notebook") {
			continue
		}
		ips := []string{}
		if p.Status.PodIP != "" {
			ips = append(ips, p.Status.PodIP)
		}
		for _, ip := range p.Status.PodIPs {
			if ip.IP != "" && ip.IP != p.Status.PodIP {
				ips = append(ips, ip.IP)
			}
		}
		stableKey, kind, ws, proj := StableKeyForPod(p.Namespace, string(p.UID), p.Labels)
		out = append(out, PodInfo{
			Name:        p.Name,
			Namespace:   p.Namespace,
			UID:         string(p.UID),
			Node:        p.Spec.NodeName,
			Status:      string(p.Status.Phase),
			IPs:         ips,
			Labels:      p.Labels,
			StableKey:   stableKey,
			KeyKind:     kind,
			WorkspaceID: ws,
			ProjectID:   proj,
		})
	}
	return out, nil
}
