package k8s

import (
	"context"
	"strings"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// PodInfo is a discovered cluster pod (filtered to notebook pods), used by the
// UI to drive port-mapping (SVC) creation: selecting a pod auto-fills its
// namespace/name/uid/selector so the admin only enters ports.
type PodInfo struct {
	Name      string            `json:"name"`
	Namespace string            `json:"namespace"`
	UID       string            `json:"uid"`
	Node      string            `json:"node"`
	Status    string            `json:"status"`
	IPs       []string          `json:"ips"`
	Labels    map[string]string `json:"labels"`
}

// ListNotebookPods returns all pods whose name contains "notebook"
// (case-insensitive), across every namespace.
func ListNotebookPods(ctx context.Context, client kubernetes.Interface) ([]PodInfo, error) {
	list, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
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
		out = append(out, PodInfo{
			Name:      p.Name,
			Namespace: p.Namespace,
			UID:       string(p.UID),
			Node:      p.Spec.NodeName,
			Status:    string(p.Status.Phase),
			IPs:       ips,
			Labels:    p.Labels,
		})
	}
	return out, nil
}
