package k8s

import (
	"context"
	"fmt"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/apimachinery/pkg/util/intstr"
	"k8s.io/client-go/kubernetes"
)

// PortSpec describes a single port on a Service.
type PortSpec struct {
	Port       int32
	TargetPort int32
	NodePort   int32
	Protocol   corev1.Protocol
}

// CreateServiceReq is the input to CreateService.
type CreateServiceReq struct {
	Namespace string
	PodName   string
	PodUID    string
	Selector  map[string]string
	Type      string // "NodePort" | "ClusterIP"
	Ports     []PortSpec
}

// CreateService creates a Service owned by the given Pod. The Service is
// labelled with managed-by=control-panel and pod-uid=<uid> so it can be
// discovered and garbage-collected by the control panel.
func CreateService(ctx context.Context, client kubernetes.Interface, req CreateServiceReq) (*corev1.Service, error) {
	svcType := corev1.ServiceTypeClusterIP
	if req.Type == "NodePort" {
		svcType = corev1.ServiceTypeNodePort
	}
	ports := make([]corev1.ServicePort, 0, len(req.Ports))
	for _, p := range req.Ports {
		ports = append(ports, corev1.ServicePort{
			Name:       fmt.Sprintf("port-%d", p.Port),
			Port:       p.Port,
			TargetPort: intOrString(p.TargetPort),
			NodePort:   p.NodePort,
			Protocol:   p.Protocol,
		})
	}
	svc := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			GenerateName: "cp-svc-",
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
		Spec: corev1.ServiceSpec{
			Type:     svcType,
			Selector: req.Selector,
			Ports:    ports,
		},
	}
	created, err := client.CoreV1().Services(req.Namespace).Create(ctx, svc, metav1.CreateOptions{})
	if err != nil {
		return nil, err
	}
	return created, nil
}

// DeleteService deletes a Service by name.
func DeleteService(ctx context.Context, client kubernetes.Interface, namespace, name string) error {
	return client.CoreV1().Services(namespace).Delete(ctx, name, metav1.DeleteOptions{})
}

// ListServices returns the Services in the namespace that are managed by the
// control panel (filtered by managed-by=control-panel).
func ListServices(ctx context.Context, client kubernetes.Interface, namespace string) ([]corev1.Service, error) {
	list, err := client.CoreV1().Services(namespace).List(ctx, metav1.ListOptions{
		LabelSelector: "managed-by=control-panel",
	})
	if err != nil {
		return nil, err
	}
	return list.Items, nil
}

// ServiceInfo is a compact, UI-facing view of a Service: its ports are
// flattened into PortRow and a Managed flag indicates whether the control panel
// created it (managed-by=control-panel label). Services created by other
// systems are included so the admin can see ALL existing port mappings for
// notebook pods, not just ours; the UI presents external ones read-only.
type ServiceInfo struct {
	Name      string            `json:"name"`
	Namespace string            `json:"namespace"`
	Type      string            `json:"type"` // ClusterIP | NodePort | LoadBalancer
	Selector  map[string]string `json:"selector"`
	Managed   bool              `json:"managed"`
	Ports     []PortRow         `json:"ports"`
}

// PortRow is a flattened Service port for the UI.
type PortRow struct {
	Port       int32  `json:"port"`
	TargetPort int32  `json:"target_port"`
	NodePort   int32  `json:"node_port"`
	Protocol   string `json:"protocol"`
}

// ListServicesForNotebooks returns every Service in namespaces that contain at
// least one notebook pod, as ServiceInfo with a Managed flag. Unlike ListServices
// (managed-by=control-panel only), this includes Services created by other
// systems (e.g. the platform's notebook-multi-port-svc) so the admin can see all
// existing port mappings. Scoping to notebook-pod namespaces avoids pulling in
// kube-system / default noise.
func ListServicesForNotebooks(ctx context.Context, client kubernetes.Interface) ([]ServiceInfo, error) {
	pods, err := ListNotebookPods(ctx, client)
	if err != nil {
		return nil, fmt.Errorf("list notebook pods: %w", err)
	}
	nsSet := make(map[string]struct{}, len(pods))
	for _, p := range pods {
		nsSet[p.Namespace] = struct{}{}
	}
	out := make([]ServiceInfo, 0)
	for ns := range nsSet {
		list, err := client.CoreV1().Services(ns).List(ctx, metav1.ListOptions{})
		if err != nil {
			return nil, err
		}
		for _, s := range list.Items {
			out = append(out, toServiceInfo(s))
		}
	}
	return out, nil
}

// toServiceInfo flattens a corev1.Service into the UI-facing ServiceInfo DTO.
func toServiceInfo(s corev1.Service) ServiceInfo {
	ports := make([]PortRow, 0, len(s.Spec.Ports))
	for _, p := range s.Spec.Ports {
		ports = append(ports, PortRow{
			Port:       p.Port,
			TargetPort: int32(p.TargetPort.IntValue()),
			NodePort:   p.NodePort,
			Protocol:   string(p.Protocol),
		})
	}
	return ServiceInfo{
		Name:      s.Name,
		Namespace: s.Namespace,
		Type:      string(s.Spec.Type),
		Selector:  s.Spec.Selector,
		Managed:   s.Labels["managed-by"] == "control-panel",
		Ports:     ports,
	}
}

// --- shared helpers (also used by networkpolicies.go) ---

func intOrString(port int32) intstr.IntOrString { return intstr.FromInt(int(port)) }
func boolPtr(b bool) *bool                      { return &b }
func typesUID(s string) types.UID              { return types.UID(s) }
