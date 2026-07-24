package k8s

import (
	"context"

	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// IngressPortSpec describes a single ingress port allowed by a NetworkPolicy.
type IngressPortSpec struct {
	Protocol string // "TCP" | "UDP"
	Port     int32
}

// CreateNetworkPolicyReq is the input to CreateNetworkPolicy.
type CreateNetworkPolicyReq struct {
	Namespace    string
	PodName      string
	PodUID       string
	PodSelector  map[string]string
	IngressPorts []IngressPortSpec
}

// CreateNetworkPolicy creates a NetworkPolicy owned by the given Pod that
// allows ingress traffic to the selected pods on the listed ports. The policy
// is labelled with managed-by=control-panel and pod-uid=<uid>.
func CreateNetworkPolicy(ctx context.Context, client kubernetes.Interface, req CreateNetworkPolicyReq) (*networkingv1.NetworkPolicy, error) {
	ports := make([]networkingv1.NetworkPolicyPort, 0, len(req.IngressPorts))
	for _, p := range req.IngressPorts {
		portVal := intOrString(p.Port)
		ports = append(ports, networkingv1.NetworkPolicyPort{
			Protocol: protoPtr(p.Protocol),
			Port:     &portVal,
		})
	}
	np := &networkingv1.NetworkPolicy{
		ObjectMeta: metav1.ObjectMeta{
			GenerateName: "cp-np-",
			Namespace:    req.Namespace,
			Labels: map[string]string{
				"managed-by": "control-panel",
				"pod-uid":    req.PodUID,
			},
			OwnerReferences: []metav1.OwnerReference{{
				APIVersion: "v1",
				Kind:       "Pod",
				Name:       req.PodName,
				UID:        typesUID(req.PodUID),
				Controller: boolPtr(true),
			}},
		},
		Spec: networkingv1.NetworkPolicySpec{
			PodSelector: metav1.LabelSelector{MatchLabels: req.PodSelector},
			Ingress: []networkingv1.NetworkPolicyIngressRule{{
				From:  []networkingv1.NetworkPolicyPeer{},
				Ports: ports,
			}},
			PolicyTypes: []networkingv1.PolicyType{networkingv1.PolicyTypeIngress},
		},
	}
	created, err := client.NetworkingV1().NetworkPolicies(req.Namespace).Create(ctx, np, metav1.CreateOptions{})
	if err != nil {
		return nil, err
	}
	return created, nil
}

// DeleteNetworkPolicy deletes a NetworkPolicy by name.
func DeleteNetworkPolicy(ctx context.Context, client kubernetes.Interface, namespace, name string) error {
	return client.NetworkingV1().NetworkPolicies(namespace).Delete(ctx, name, metav1.DeleteOptions{})
}

// ListNetworkPolicies returns the NetworkPolicies in the namespace that are
// managed by the control panel (filtered by managed-by=control-panel).
func ListNetworkPolicies(ctx context.Context, client kubernetes.Interface, namespace string) ([]networkingv1.NetworkPolicy, error) {
	list, err := client.NetworkingV1().NetworkPolicies(namespace).List(ctx, metav1.ListOptions{
		LabelSelector: "managed-by=control-panel",
	})
	if err != nil {
		return nil, err
	}
	return list.Items, nil
}

// protoPtr converts a protocol string ("TCP"/"UDP") into a *corev1.Protocol.
func protoPtr(s string) *corev1.Protocol {
	p := corev1.Protocol(s)
	return &p
}
