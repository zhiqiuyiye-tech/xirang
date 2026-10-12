package k8s

import (
	"context"
	"fmt"
	"strings"

	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/labels"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/kubernetes"
)

// IngressPortSpec describes a single ingress port allowed by a NetworkPolicy.
type IngressPortSpec struct {
	Protocol string // "TCP" | "UDP"
	Port     int32
}

// CreateNetworkPolicyReq is the input to CreateNetworkPolicy.
type CreateNetworkPolicyReq struct {
	Name         string
	Namespace    string
	ServiceName  string
	PodName      string
	PodUID       string
	PodSelector  map[string]string
	IngressPorts []IngressPortSpec
}

// CreateNetworkPolicy creates a NetworkPolicy owned by the given Pod that
// allows ingress traffic to the selected pods on the listed ports. The policy
// is labelled with managed-by=control-panel and pod-uid=<uid>, plus
// service-name=<serviceName> when provided so it can be cascade-deleted.
func CreateNetworkPolicy(ctx context.Context, client kubernetes.Interface, req CreateNetworkPolicyReq) (*networkingv1.NetworkPolicy, error) {
	if isProtectedNamespace(req.Namespace) {
		return nil, fmt.Errorf("cannot create network policy in protected namespace %q", req.Namespace)
	}
	if len(req.PodSelector) == 0 {
		return nil, fmt.Errorf("pod selector cannot be empty")
	}
	if req.Namespace == "" || req.PodName == "" {
		return nil, fmt.Errorf("namespace and target pod name required")
	}
	if req.PodUID == "" {
		return nil, fmt.Errorf("target pod UID required")
	}
	targetPod, err := client.CoreV1().Pods(req.Namespace).Get(ctx, req.PodName, metav1.GetOptions{})
	if err != nil {
		return nil, fmt.Errorf("get target Pod %s/%s: %w", req.Namespace, req.PodName, err)
	}
	if string(targetPod.UID) != req.PodUID {
		return nil, fmt.Errorf("target Pod %s/%s UID changed; refresh and retry", req.Namespace, req.PodName)
	}
	selector, err := metav1.LabelSelectorAsSelector(&metav1.LabelSelector{MatchLabels: req.PodSelector})
	if err != nil {
		return nil, fmt.Errorf("invalid pod selector: %w", err)
	}
	if !selector.Matches(labels.Set(targetPod.Labels)) {
		return nil, fmt.Errorf("pod selector does not match target Pod %s/%s", req.Namespace, req.PodName)
	}
	matchedPods, err := client.CoreV1().Pods(req.Namespace).List(ctx, metav1.ListOptions{LabelSelector: selector.String()})
	if err != nil {
		return nil, fmt.Errorf("list Pods matching selector in namespace %q: %w", req.Namespace, err)
	}
	if len(matchedPods.Items) != 1 {
		return nil, fmt.Errorf("pod selector matches %d Pods in namespace %q; adjust labels so it uniquely matches the target Pod", len(matchedPods.Items), req.Namespace)
	}
	if string(matchedPods.Items[0].UID) != req.PodUID {
		return nil, fmt.Errorf("pod selector no longer matches target Pod %s/%s; refresh and retry", req.Namespace, req.PodName)
	}
	ports := make([]networkingv1.NetworkPolicyPort, 0, len(req.IngressPorts))
	for _, p := range req.IngressPorts {
		portVal := intOrString(p.Port)
		ports = append(ports, networkingv1.NetworkPolicyPort{
			Protocol: protoPtr(p.Protocol),
			Port:     &portVal,
		})
	}
	labels := map[string]string{
		"managed-by": "control-panel",
		"pod-uid":    req.PodUID,
	}
	if req.ServiceName != "" {
		labels["service-name"] = req.ServiceName
	}
	npName := req.Name
	generateName := ""
	if npName == "" {
		generateName = "cp-np-"
	}
	np := &networkingv1.NetworkPolicy{
		ObjectMeta: metav1.ObjectMeta{
			Name:         npName,
			GenerateName: generateName,
			Namespace:    req.Namespace,
			Labels:       labels,
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

// DeleteNetworkPolicy deletes a NetworkPolicy by name after verifying it is managed by the control panel.
// This legacy wrapper preserves the original API for callers without identity tokens.
func DeleteNetworkPolicy(ctx context.Context, client kubernetes.Interface, namespace, name string) error {
	if isProtectedNamespace(namespace) {
		return fmt.Errorf("cannot delete network policy in protected namespace %q", namespace)
	}
	np, err := client.NetworkingV1().NetworkPolicies(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return err
	}
	if np.Labels["managed-by"] != "control-panel" {
		return fmt.Errorf("cannot delete externally managed network policy %s/%s", namespace, name)
	}
	return client.NetworkingV1().NetworkPolicies(namespace).Delete(ctx, name, metav1.DeleteOptions{})
}

// DeleteNetworkPolicyWithIdentity deletes a managed NetworkPolicy only when it
// still matches the UID and resourceVersion supplied by the caller.
func DeleteNetworkPolicyWithIdentity(ctx context.Context, client kubernetes.Interface, namespace, name, uid, resourceVersion string) error {
	if isProtectedNamespace(namespace) {
		return fmt.Errorf("cannot delete network policy in protected namespace %q", namespace)
	}
	if namespace == "" || name == "" {
		return fmt.Errorf("namespace and name required")
	}
	if uid == "" || resourceVersion == "" {
		return fmt.Errorf("network policy UID and resourceVersion required")
	}
	np, err := client.NetworkingV1().NetworkPolicies(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return err
	}
	if np.Labels["managed-by"] != "control-panel" {
		return fmt.Errorf("cannot delete externally managed network policy %s/%s", namespace, name)
	}
	if string(np.UID) != uid || np.ResourceVersion != resourceVersion {
		return fmt.Errorf("conflict: network policy %s/%s was replaced or modified, please refresh", namespace, name)
	}
	uidValue := types.UID(uid)
	return client.NetworkingV1().NetworkPolicies(namespace).Delete(ctx, name, metav1.DeleteOptions{
		Preconditions: &metav1.Preconditions{UID: &uidValue, ResourceVersion: &resourceVersion},
	})
}

// DeleteNetworkPoliciesByService deletes any NetworkPolicy in the given namespace
// managed by the control panel that is labelled with service-name=<serviceName>.
func DeleteNetworkPoliciesByService(ctx context.Context, client kubernetes.Interface, namespace, serviceName string) error {
	list, err := client.NetworkingV1().NetworkPolicies(namespace).List(ctx, metav1.ListOptions{
		LabelSelector: fmt.Sprintf("managed-by=control-panel,service-name=%s", serviceName),
	})
	if err != nil {
		return err
	}
	for _, np := range list.Items {
		if err := client.NetworkingV1().NetworkPolicies(namespace).Delete(ctx, np.Name, metav1.DeleteOptions{}); err != nil {
			return err
		}
	}
	return nil
}

// policyUpdateChange records the exact policy state before the transaction and
// the identity returned by the successful update used for safe compensation.
type policyUpdateChange struct {
	before     *networkingv1.NetworkPolicy
	updatedUID string
	updatedRV  string
}

// UpdateNetworkPoliciesByService updates matching policies and compensates any
// earlier updates if a later policy update fails.
func UpdateNetworkPoliciesByService(ctx context.Context, client kubernetes.Interface, namespace, serviceName string, ingressPorts []IngressPortSpec) error {
	changes, err := updateNetworkPoliciesByService(ctx, client, namespace, serviceName, ingressPorts)
	if err == nil {
		return nil
	}
	if rollbackErr := restoreNetworkPolicyChanges(ctx, client, changes); rollbackErr != nil {
		return fmt.Errorf("%v; rollback incomplete: %w", err, rollbackErr)
	}
	return err
}

func updateNetworkPoliciesByService(ctx context.Context, client kubernetes.Interface, namespace, serviceName string, ingressPorts []IngressPortSpec) ([]policyUpdateChange, error) {
	list, err := client.NetworkingV1().NetworkPolicies(namespace).List(ctx, metav1.ListOptions{
		LabelSelector: fmt.Sprintf("managed-by=control-panel,service-name=%s", serviceName),
	})
	if err != nil {
		return nil, err
	}
	ports := make([]networkingv1.NetworkPolicyPort, 0, len(ingressPorts))
	for _, p := range ingressPorts {
		portVal := intOrString(p.Port)
		ports = append(ports, networkingv1.NetworkPolicyPort{
			Protocol: protoPtr(p.Protocol),
			Port:     &portVal,
		})
	}

	changes := make([]policyUpdateChange, 0, len(list.Items))
	for i := range list.Items {
		before := list.Items[i].DeepCopy()
		if before.Labels["managed-by"] != "control-panel" || before.Labels["service-name"] != serviceName {
			continue
		}
		current, err := client.NetworkingV1().NetworkPolicies(namespace).Get(ctx, before.Name, metav1.GetOptions{})
		if err != nil {
			return changes, fmt.Errorf("get network policy %s/%s before update: %w", namespace, before.Name, err)
		}
		if current.UID != before.UID || current.ResourceVersion != before.ResourceVersion {
			return changes, fmt.Errorf("conflict: network policy %s/%s changed before update", namespace, before.Name)
		}
		if current.Labels["managed-by"] != "control-panel" || current.Labels["service-name"] != serviceName {
			return changes, fmt.Errorf("network policy %s/%s is no longer managed for service %s", namespace, before.Name, serviceName)
		}
		current.Spec.Ingress = []networkingv1.NetworkPolicyIngressRule{{
			From:  []networkingv1.NetworkPolicyPeer{},
			Ports: append([]networkingv1.NetworkPolicyPort(nil), ports...),
		}}
		updated, err := client.NetworkingV1().NetworkPolicies(namespace).Update(ctx, current, metav1.UpdateOptions{})
		if err != nil {
			return changes, fmt.Errorf("update network policy %s/%s: %w", namespace, before.Name, err)
		}
		changes = append(changes, policyUpdateChange{
			before:     before,
			updatedUID: string(updated.UID),
			updatedRV:  updated.ResourceVersion,
		})
	}
	return changes, nil
}

// restoreNetworkPolicyChanges reverts policies in reverse order only when
// they still match the UID and resourceVersion produced by this transaction.
func restoreNetworkPolicyChanges(_ context.Context, client kubernetes.Interface, changes []policyUpdateChange) error {
	cleanupCtx, cancel := newK8sCleanupContext()
	defer cancel()
	var failures []string
	for i := len(changes) - 1; i >= 0; i-- {
		change := changes[i]
		before := change.before
		current, err := client.NetworkingV1().NetworkPolicies(before.Namespace).Get(cleanupCtx, before.Name, metav1.GetOptions{})
		if err != nil {
			failures = append(failures, fmt.Sprintf("%s/%s: get before rollback: %v", before.Namespace, before.Name, err))
			continue
		}
		if string(current.UID) != change.updatedUID || current.ResourceVersion != change.updatedRV {
			failures = append(failures, fmt.Sprintf("%s/%s: identity changed before rollback (UID/resourceVersion mismatch)", before.Namespace, before.Name))
			continue
		}
		if current.Labels["managed-by"] != "control-panel" || current.Labels["service-name"] != before.Labels["service-name"] {
			failures = append(failures, fmt.Sprintf("%s/%s: ownership changed before rollback", before.Namespace, before.Name))
			continue
		}
		current.Spec = *before.Spec.DeepCopy()
		if _, err := client.NetworkingV1().NetworkPolicies(before.Namespace).Update(cleanupCtx, current, metav1.UpdateOptions{}); err != nil {
			failures = append(failures, fmt.Sprintf("%s/%s: restore failed: %v", before.Namespace, before.Name, err))
		}
	}
	if len(failures) != 0 {
		return fmt.Errorf("%s", strings.Join(failures, "; "))
	}
	return nil
}

// ListNetworkPolicies returns the NetworkPolicies in the namespace that are
// managed by the control panel (filtered by managed-by=control-panel).
func ListNetworkPolicies(ctx context.Context, client kubernetes.Interface, namespace string) ([]networkingv1.NetworkPolicy, error) {
	list, err := client.NetworkingV1().NetworkPolicies(namespace).List(ctx, metav1.ListOptions{
		LabelSelector:   "managed-by=control-panel",
		ResourceVersion: "0",
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
