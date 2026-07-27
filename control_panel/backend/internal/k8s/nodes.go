package k8s

import (
	"context"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// NodeInfo is a discovered cluster node, used to prefill the worker form.
type NodeInfo struct {
	Name string `json:"name"`
	Host string `json:"host"`
	Role string `json:"role"`
}

// ListNodes returns all cluster nodes with the first internal IP and role
// (master/control-plane vs worker). Used by the UI to prefill worker records
// so the admin only needs to supply SSH credentials.
func ListNodes(ctx context.Context, client kubernetes.Interface) ([]NodeInfo, error) {
	list, err := client.CoreV1().Nodes().List(ctx, metav1.ListOptions{})
	if err != nil {
		return nil, err
	}
	out := make([]NodeInfo, 0, len(list.Items))
	for _, n := range list.Items {
		host := ""
		for _, a := range n.Status.Addresses {
			if a.Type == corev1.NodeInternalIP {
				host = a.Address
				break
			}
		}
		role := "worker"
		if _, ok := n.Labels["node-role.kubernetes.io/control-plane"]; ok {
			role = "master"
		} else if _, ok := n.Labels["node-role.kubernetes.io/master"]; ok {
			role = "master"
		}
		out = append(out, NodeInfo{
			Name: n.Name,
			Host: host,
			Role: role,
		})
	}
	return out, nil
}
