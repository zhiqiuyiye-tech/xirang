package k8s

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

// errNoK8sClient is the failure recorded when a k8s task runs while the panel
// has no in-cluster client (non-cluster / local dev mode). The HTTP layer
// returns 503 up front in that case, so reaching a task handler with a nil
// client should be impossible - this guard turns the would-be nil-deref
// panic into a clean failed task.
var errNoK8sClient = errors.New("k8s client unavailable (non-cluster mode)")

// RegisterK8sHandlers registers the five K8s task handlers (k8s_create_svc,
// k8s_update_svc, k8s_delete_svc, k8s_create_np, k8s_delete_np) on the engine.
// Each handler parses task.ParamsJSON, invokes the corresponding k8s operation,
// and records a step via the reporter before succeeding or failing.
func RegisterK8sHandlers(eng *tasks.Engine, client kubernetes.Interface) {
	eng.Register("k8s_create_svc", &createSvcHandler{client: client})
	eng.Register("k8s_update_svc", &updateSvcHandler{client: client})
	eng.Register("k8s_delete_svc", &deleteSvcHandler{client: client})
	eng.Register("k8s_create_np", &createNPHandler{client: client})
	eng.Register("k8s_delete_np", &deleteNPHandler{client: client})
}

func parsePortSpecs(mappings, ports []map[string]any) ([]PortSpec, error) {
	if len(mappings) > 0 {
		seenPodPorts := make(map[int32]bool)
		seenNodePorts := make(map[int32]bool)
		specs := make([]PortSpec, 0, len(mappings))
		for _, m := range mappings {
			podPort, err := numField(m, "pod_port")
			if err != nil || podPort == 0 {
				podPort, err = numField(m, "target_port")
			}
			if err != nil || podPort < 1 || podPort > 65535 {
				return nil, fmt.Errorf("pod_port must be between 1 and 65535")
			}
			nodePort, _ := numField(m, "node_port")
			if nodePort != 0 && (nodePort < 30000 || nodePort > 32767) {
				return nil, fmt.Errorf("node_port must be between 30000 and 32767 (or 0 for automatic)")
			}
			p32 := int32(podPort)
			n32 := int32(nodePort)
			if seenPodPorts[p32] {
				return nil, fmt.Errorf("duplicate pod_port %d", p32)
			}
			seenPodPorts[p32] = true
			if n32 > 0 {
				if seenNodePorts[n32] {
					return nil, fmt.Errorf("duplicate node_port %d", n32)
				}
				seenNodePorts[n32] = true
			}
			specs = append(specs, PortSpec{
				Port:       p32,
				TargetPort: p32,
				NodePort:   n32,
				Protocol:   corev1.ProtocolTCP,
			})
		}
		return specs, nil
	}

	specs := make([]PortSpec, 0, len(ports))
	for _, pp := range ports {
		port, err := numField(pp, "port")
		if err != nil {
			return nil, err
		}
		targetPort, err := numField(pp, "target_port")
		if err != nil {
			return nil, err
		}
		nodePort, err := numField(pp, "node_port")
		if err != nil {
			return nil, err
		}
		protocol, err := strField(pp, "protocol")
		if err != nil {
			return nil, err
		}
		specs = append(specs, PortSpec{
			Port:       int32(port),
			TargetPort: int32(targetPort),
			NodePort:   int32(nodePort),
			Protocol:   corev1.Protocol(protocol),
		})
	}
	return specs, nil
}

// --- createSvcHandler ---

type createSvcHandler struct{ client kubernetes.Interface }

func (h *createSvcHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	if h.client == nil {
		r.Fail(errNoK8sClient.Error())
		return errNoK8sClient
	}
	var p struct {
		Name      string            `json:"name"`
		Namespace string            `json:"namespace"`
		PodName   string            `json:"pod_name"`
		PodUID    string            `json:"pod_uid"`
		Selector  map[string]string `json:"selector"`
		Type      string            `json:"type"`
		Ports     []map[string]any  `json:"ports"`
		Mappings  []map[string]any  `json:"mappings"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("k8s_create_svc: parse params: %v", err))
		return err
	}
	if p.Type == "" {
		p.Type = "NodePort"
	}
	ports, err := parsePortSpecs(p.Mappings, p.Ports)
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_create_svc: %v", err))
		return err
	}

	st, err := r.Step("create_service")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_create_svc: create step: %v", err))
		return err
	}
	svc, err := CreateService(ctx, h.client, CreateServiceReq{
		Name: p.Name, Namespace: p.Namespace, PodName: p.PodName, PodUID: p.PodUID,
		Selector: p.Selector, Type: p.Type, Ports: ports,
	})
	if err != nil {
		st.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_create_svc: %v", err))
		return err
	}
	st.Done("succeeded", svc.Name, "", "")

	// Auto-create a NetworkPolicy that allows ingress on the target ports of the
	// Service (the ports the pod containers are actually listening on).
	// The NP uses the pod selector + ownerReferences so it is GC'd
	// with the pod and stays in sync with the exposed ports - the admin only
	// picks ports once, the firewall rule follows automatically.
	// We also record the service-name so the NP can be cascade-deleted when the
	// service is deleted.
	ingressPorts := make([]IngressPortSpec, 0, len(ports))
	for _, pp := range ports {
		targetPort := pp.TargetPort
		if targetPort <= 0 {
			targetPort = pp.Port
		}
		ingressPorts = append(ingressPorts, IngressPortSpec{
			Protocol: string(pp.Protocol),
			Port:     targetPort,
		})
	}
	st2, err := r.Step("create_network_policy")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_create_svc: create np step: %v", err))
		return err
	}
	np, err := CreateNetworkPolicy(ctx, h.client, CreateNetworkPolicyReq{
		Namespace: p.Namespace, ServiceName: svc.Name, PodName: p.PodName, PodUID: p.PodUID,
		PodSelector: p.Selector, IngressPorts: ingressPorts,
	})
	if err != nil {
		st2.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_create_svc: create network policy: %v", err))
		return err
	}
	st2.Done("succeeded", np.Name, "", "")
	r.Succeed()
	return nil
}

// --- updateSvcHandler ---

type updateSvcHandler struct{ client kubernetes.Interface }

func (h *updateSvcHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	if h.client == nil {
		r.Fail(errNoK8sClient.Error())
		return errNoK8sClient
	}
	var p struct {
		Namespace       string           `json:"namespace"`
		Name            string           `json:"name"`
		ResourceVersion string           `json:"resource_version"`
		Ports           []map[string]any `json:"ports"`
		Mappings        []map[string]any `json:"mappings"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("k8s_update_svc: parse params: %v", err))
		return err
	}
	if p.Namespace == "" || p.Name == "" {
		r.Fail("k8s_update_svc: namespace and name required")
		return errors.New("namespace and name required")
	}

	// Deleting the last mapping cleanly deletes the Service and its associated NetworkPolicy.
	if len(p.Mappings) == 0 && len(p.Ports) == 0 {
		st, err := r.Step("delete_empty_service")
		if err != nil {
			r.Fail(fmt.Sprintf("k8s_update_svc: %v", err))
			return err
		}
		if err := DeleteService(ctx, h.client, p.Namespace, p.Name); err != nil {
			st.Done("failed", "", err.Error(), err.Error())
			r.Fail(fmt.Sprintf("k8s_update_svc: delete service: %v", err))
			return err
		}
		st.Done("succeeded", p.Name, "", "")

		stNP, _ := r.Step("delete_network_policy")
		if err := DeleteNetworkPoliciesByService(ctx, h.client, p.Namespace, p.Name); err != nil {
			if stNP != nil {
				stNP.Done("failed", "", err.Error(), err.Error())
			}
		} else if stNP != nil {
			stNP.Done("succeeded", p.Name, "", "")
		}
		r.Succeed()
		return nil
	}

	ports, err := parsePortSpecs(p.Mappings, p.Ports)
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_update_svc: %v", err))
		return err
	}

	ingressPorts := make([]IngressPortSpec, 0, len(ports))
	for _, pp := range ports {
		tp := pp.TargetPort
		if tp <= 0 {
			tp = pp.Port
		}
		ingressPorts = append(ingressPorts, IngressPortSpec{
			Protocol: string(pp.Protocol),
			Port:     tp,
		})
	}

	stNP, err := r.Step("update_network_policy")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_update_svc: %v", err))
		return err
	}
	if err := UpdateNetworkPoliciesByService(ctx, h.client, p.Namespace, p.Name, ingressPorts); err != nil {
		stNP.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_update_svc: update network policy: %v", err))
		return err
	}
	stNP.Done("succeeded", p.Name, "", "")

	stSvc, err := r.Step("update_service")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_update_svc: %v", err))
		return err
	}
	svc, err := UpdateServicePorts(ctx, h.client, UpdateServiceReq{
		Namespace:       p.Namespace,
		Name:            p.Name,
		ResourceVersion: p.ResourceVersion,
		Ports:           ports,
	})
	if err != nil {
		stSvc.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_update_svc: update service: %v", err))
		return err
	}
	stSvc.Done("succeeded", svc.Name, "", "")
	r.Succeed()
	return nil
}

// --- deleteSvcHandler ---

type deleteSvcHandler struct{ client kubernetes.Interface }

func (h *deleteSvcHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	if h.client == nil {
		r.Fail(errNoK8sClient.Error())
		return errNoK8sClient
	}
	var p struct {
		Namespace string `json:"namespace"`
		Name      string `json:"name"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("k8s_delete_svc: parse params: %v", err))
		return err
	}

	st, err := r.Step("delete_service")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_delete_svc: create step: %v", err))
		return err
	}
	if err := DeleteService(ctx, h.client, p.Namespace, p.Name); err != nil {
		st.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_delete_svc: %v", err))
		return err
	}
	st.Done("succeeded", p.Name, "", "")

	// Cascade delete associated NetworkPolicy created by control-panel for this service
	st2, err := r.Step("delete_network_policy")
	if err == nil {
		if err := DeleteNetworkPoliciesByService(ctx, h.client, p.Namespace, p.Name); err != nil {
			st2.Done("failed", "", err.Error(), fmt.Sprintf("delete network policy for service %s: %v", p.Name, err))
		} else {
			st2.Done("succeeded", p.Name, "", "")
		}
	}
	r.Succeed()
	return nil
}

// --- createNPHandler ---

type createNPHandler struct{ client kubernetes.Interface }

func (h *createNPHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	if h.client == nil {
		r.Fail(errNoK8sClient.Error())
		return errNoK8sClient
	}
	var p struct {
		Namespace    string            `json:"namespace"`
		PodName      string            `json:"pod_name"`
		PodUID       string            `json:"pod_uid"`
		PodSelector  map[string]string `json:"pod_selector"`
		IngressPorts []map[string]any  `json:"ingress_ports"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("k8s_create_np: parse params: %v", err))
		return err
	}
	ingressPorts := make([]IngressPortSpec, 0, len(p.IngressPorts))
	for _, pp := range p.IngressPorts {
		protocol, err := strField(pp, "protocol")
		if err != nil {
			r.Fail(fmt.Sprintf("k8s_create_np: %v", err))
			return err
		}
		port, err := numField(pp, "port")
		if err != nil {
			r.Fail(fmt.Sprintf("k8s_create_np: %v", err))
			return err
		}
		ingressPorts = append(ingressPorts, IngressPortSpec{
			Protocol: protocol,
			Port:     int32(port),
		})
	}

	st, err := r.Step("create_network_policy")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_create_np: create step: %v", err))
		return err
	}
	np, err := CreateNetworkPolicy(ctx, h.client, CreateNetworkPolicyReq{
		Namespace:    p.Namespace,
		PodName:      p.PodName,
		PodUID:       p.PodUID,
		PodSelector:  p.PodSelector,
		IngressPorts: ingressPorts,
	})
	if err != nil {
		st.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_create_np: %v", err))
		return err
	}
	st.Done("succeeded", np.Name, "", "")
	r.Succeed()
	return nil
}

// --- deleteNPHandler ---

type deleteNPHandler struct{ client kubernetes.Interface }

func (h *deleteNPHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	if h.client == nil {
		r.Fail(errNoK8sClient.Error())
		return errNoK8sClient
	}
	var p struct {
		Namespace string `json:"namespace"`
		Name      string `json:"name"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("k8s_delete_np: parse params: %v", err))
		return err
	}

	st, err := r.Step("delete_network_policy")
	if err != nil {
		r.Fail(fmt.Sprintf("k8s_delete_np: create step: %v", err))
		return err
	}
	if err := DeleteNetworkPolicy(ctx, h.client, p.Namespace, p.Name); err != nil {
		st.Done("failed", "", err.Error(), err.Error())
		r.Fail(fmt.Sprintf("k8s_delete_np: %v", err))
		return err
	}
	st.Done("succeeded", p.Name, "", "")
	r.Succeed()
	return nil
}

// --- params helpers ---
//
// JSON unmarshals numeric values as float64. numField accepts float64 (and the
// occasional int/int64/json.Number) so the handlers do not panic when a field
// is missing or the wrong type. On a bad field the handler reports a clear
// error via r.Fail and returns, rather than panicking.

func numField(m map[string]any, key string) (float64, error) {
	v, ok := m[key]
	if !ok {
		return 0, fmt.Errorf("port spec missing field %q", key)
	}
	switch n := v.(type) {
	case float64:
		return n, nil
	case int:
		return float64(n), nil
	case int64:
		return float64(n), nil
	case int32:
		return float64(n), nil
	case json.Number:
		f, err := n.Float64()
		if err != nil {
			return 0, fmt.Errorf("field %q: %v", key, err)
		}
		return f, nil
	default:
		return 0, fmt.Errorf("field %q: expected number, got %T", key, v)
	}
}

func strField(m map[string]any, key string) (string, error) {
	v, ok := m[key]
	if !ok {
		return "", fmt.Errorf("port spec missing field %q", key)
	}
	s, ok := v.(string)
	if !ok {
		return "", fmt.Errorf("field %q: expected string, got %T", key, v)
	}
	return s, nil
}
