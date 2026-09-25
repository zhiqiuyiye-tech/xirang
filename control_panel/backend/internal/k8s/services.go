package k8s

import (
	"context"
	"fmt"
	"sync"

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
	Name      string
	Namespace string
	PodName   string
	PodUID    string
	Selector  map[string]string
	Type      string // "NodePort" | "ClusterIP"
	Ports     []PortSpec
}

func isProtectedNamespace(ns string) bool {
	switch ns {
	case "kube-system", "kube-public", "kube-node-lease":
		return true
	default:
		return false
	}
}

// CreateService creates a Service owned by the given Pod. The Service is
// labelled with managed-by=control-panel and pod-uid=<uid> so it can be
// discovered and garbage-collected by the control panel.
func CreateService(ctx context.Context, client kubernetes.Interface, req CreateServiceReq) (*corev1.Service, error) {
	if isProtectedNamespace(req.Namespace) {
		return nil, fmt.Errorf("cannot create service in protected namespace %q", req.Namespace)
	}
	if len(req.Selector) == 0 {
		return nil, fmt.Errorf("selector cannot be empty")
	}
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
	svcName := req.Name
	generateName := ""
	if svcName == "" {
		generateName = "cp-svc-"
	}
	svc := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name:         svcName,
			GenerateName: generateName,
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

// DeleteService deletes a Service by name after verifying it is managed by the control panel.
func DeleteService(ctx context.Context, client kubernetes.Interface, namespace, name string) error {
	if isProtectedNamespace(namespace) {
		return fmt.Errorf("cannot delete service in protected namespace %q", namespace)
	}
	svc, err := client.CoreV1().Services(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return err
	}
	if svc.Labels["managed-by"] != "control-panel" {
		return fmt.Errorf("cannot delete externally managed service %s/%s", namespace, name)
	}
	return client.CoreV1().Services(namespace).Delete(ctx, name, metav1.DeleteOptions{})
}

// UpdateServiceReq describes the desired ports and concurrency token for updating a Service.
type UpdateServiceReq struct {
	Namespace       string
	Name            string
	ResourceVersion string
	Ports           []PortSpec
}

// UpdateServicePorts replaces the port spec of a control-panel managed Service in-place,
// maintaining optimistic concurrency control via ResourceVersion.
func UpdateServicePorts(ctx context.Context, client kubernetes.Interface, req UpdateServiceReq) (*corev1.Service, error) {
	svc, err := client.CoreV1().Services(req.Namespace).Get(ctx, req.Name, metav1.GetOptions{})
	if err != nil {
		return nil, err
	}
	if svc.Labels["managed-by"] != "control-panel" {
		return nil, fmt.Errorf("cannot edit externally managed service %s/%s", req.Namespace, req.Name)
	}
	if req.ResourceVersion != "" && svc.ResourceVersion != req.ResourceVersion {
		return nil, fmt.Errorf("conflict: service %s/%s was modified, please refresh", req.Namespace, req.Name)
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
	svc.Spec.Ports = ports
	return client.CoreV1().Services(req.Namespace).Update(ctx, svc, metav1.UpdateOptions{})
}

// ListServices returns the Services in the namespace that are managed by the
// control panel (filtered by managed-by=control-panel).
func ListServices(ctx context.Context, client kubernetes.Interface, namespace string) ([]corev1.Service, error) {
	list, err := client.CoreV1().Services(namespace).List(ctx, metav1.ListOptions{
		LabelSelector:   "managed-by=control-panel",
		ResourceVersion: "0",
	})
	if err != nil {
		return nil, err
	}
	return list.Items, nil
}

// ServiceInfo is a compact, UI-facing view of a Service: its ports are
// flattened into PortRow, a Managed flag indicates whether the control panel
// created it (managed-by=control-panel label), and Pods lists the notebook pods
// the Service routes to (selector match). Pods lets the UI show existing port
// mappings grouped PER notebook pod instead of a flat cluster-wide list;
// Services created by other systems are included (read-only) when they target
// the same pod.
type ServiceInfo struct {
	Name            string            `json:"name"`
	Namespace       string            `json:"namespace"`
	Type            string            `json:"type"` // ClusterIP | NodePort | LoadBalancer
	Selector        map[string]string `json:"selector"`
	Managed         bool              `json:"managed"`
	Ports           []PortRow         `json:"ports"`
	Pods            []PodRef          `json:"pods"` // notebook pods this Service routes to (selector match); empty if none
	ResourceVersion string            `json:"resource_version"`
}

// PodRef is a minimal reference to a notebook pod a Service routes to.
type PodRef struct {
	Name string `json:"name"`
	UID  string `json:"uid"`
}

// PortRow is a flattened Service port for the UI.
type PortRow struct {
	Port       int32  `json:"port"`
	TargetPort int32  `json:"target_port"`
	NodePort   int32  `json:"node_port"`
	Protocol   string `json:"protocol"`
}

// ListServicesForNotebooks returns every Service in namespaces that contain at
// least one notebook pod, as ServiceInfo. Each Service's Pods field is
// populated with the notebook pods it routes to (by selector match), so the UI
// can display existing mappings grouped per notebook pod. Unlike ListServices
// (managed-by=control-panel only), this includes Services created by other
// systems (e.g. the platform's notebook-multi-port-svc) when they target a
// notebook pod. Scoping to notebook-pod namespaces avoids pulling in
// kube-system / default noise.
//
// The per-namespace Service lists run concurrently (bounded fan-out) - the
// sequential N+1 added up to (n x RTT) latency on this synchronous HTTP
// endpoint. Lists are served from the API server watch cache
// (ResourceVersion=0), skipping the etcd quorum read.
func ListServicesForNotebooks(ctx context.Context, client kubernetes.Interface) ([]ServiceInfo, error) {
	pods, err := ListNotebookPods(ctx, client)
	if err != nil {
		return nil, fmt.Errorf("list notebook pods: %w", err)
	}
	nsSet := make(map[string]struct{}, len(pods))
	podsByNs := make(map[string][]PodInfo, len(pods))
	for _, p := range pods {
		nsSet[p.Namespace] = struct{}{}
		podsByNs[p.Namespace] = append(podsByNs[p.Namespace], p)
	}
	out := make([]ServiceInfo, 0)
	var (
		mu       sync.Mutex
		wg       sync.WaitGroup
		firstErr error
	)
	sem := make(chan struct{}, 8) // bound the fan-out
	for ns := range nsSet {
		wg.Add(1)
		go func(ns string) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()
			list, err := client.CoreV1().Services(ns).List(ctx, metav1.ListOptions{
				ResourceVersion: "0",
			})
			if err != nil {
				mu.Lock()
				if firstErr == nil {
					firstErr = fmt.Errorf("list services in %s: %w", ns, err)
				}
				mu.Unlock()
				return
			}
			mu.Lock()
			defer mu.Unlock()
			for _, s := range list.Items {
				si := toServiceInfo(s)
				for _, p := range podsByNs[ns] {
					if selectorMatches(s.Spec.Selector, p.Labels) {
						si.Pods = append(si.Pods, PodRef{Name: p.Name, UID: p.UID})
					}
				}
				out = append(out, si)
			}
		}(ns)
	}
	wg.Wait()
	if firstErr != nil {
		return nil, firstErr
	}
	return out, nil
}

// selectorMatches reports whether a Service selector routes to a pod with the
// given labels: every selector key must be present on the pod with the same
// value. An empty selector (manual-endpoint Services like kube-dns) matches no
// pod. This is the K8s Service->Pod routing semantics, used to attribute each
// existing port mapping to the notebook pod(s) it serves.
func selectorMatches(selector, podLabels map[string]string) bool {
	if len(selector) == 0 {
		return false
	}
	for k, v := range selector {
		if podLabels[k] != v {
			return false
		}
	}
	return true
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
		Name:            s.Name,
		Namespace:       s.Namespace,
		Type:            string(s.Spec.Type),
		Selector:        s.Spec.Selector,
		Managed:         s.Labels["managed-by"] == "control-panel",
		Ports:           ports,
		ResourceVersion: s.ResourceVersion,
	}
}

// --- shared helpers (also used by networkpolicies.go) ---

func intOrString(port int32) intstr.IntOrString { return intstr.FromInt(int(port)) }
func boolPtr(b bool) *bool                      { return &b }
func typesUID(s string) types.UID               { return types.UID(s) }
