package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/util/intstr"
	"k8s.io/client-go/kubernetes/fake"
)

func TestCreateServiceSetsOwnerRefAndLabels(t *testing.T) {
	cs := fake.NewSimpleClientset()
	// Build a target Pod (fake clientset needs it to exist; CreateService does
// not strongly validate the owner, it only constructs the reference).
	pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "p1", Namespace: "ns1", UID: "uid-1"}}
	if _, err := cs.CoreV1().Pods("ns1").Create(context.Background(), pod, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}

	svc, err := CreateService(context.Background(), cs, CreateServiceReq{
		Namespace: "ns1", PodName: "p1", PodUID: "uid-1",
		Selector: map[string]string{"app": "p1"},
		Type:     "NodePort",
		Ports:    []PortSpec{{Port: 31555, TargetPort: 31555, NodePort: 31555, Protocol: "TCP"}},
	})
	if err != nil {
		t.Fatal(err)
	}
	if len(svc.OwnerReferences) != 1 || svc.OwnerReferences[0].UID != "uid-1" || svc.OwnerReferences[0].Kind != "Pod" {
		t.Fatalf("ownerRef wrong: %+v", svc.OwnerReferences)
	}
	if svc.OwnerReferences[0].APIVersion != "v1" {
		t.Fatalf("ownerRef APIVersion wrong: %s", svc.OwnerReferences[0].APIVersion)
	}
	if svc.OwnerReferences[0].Name != "p1" {
		t.Fatalf("ownerRef Name wrong: %s", svc.OwnerReferences[0].Name)
	}
	if svc.OwnerReferences[0].Controller == nil || !*svc.OwnerReferences[0].Controller {
		t.Fatalf("ownerRef Controller wrong: %+v", svc.OwnerReferences[0].Controller)
	}
	if svc.Labels["managed-by"] != "control-panel" || svc.Labels["pod-uid"] != "uid-1" {
		t.Fatalf("labels wrong: %+v", svc.Labels)
	}
	if svc.Spec.Type != corev1.ServiceTypeNodePort {
		t.Fatalf("type wrong: %v", svc.Spec.Type)
	}
	if len(svc.Spec.Ports) != 1 || svc.Spec.Ports[0].NodePort != 31555 {
		t.Fatalf("ports wrong: %+v", svc.Spec.Ports)
	}
	if svc.Spec.Selector["app"] != "p1" {
		t.Fatalf("selector wrong: %+v", svc.Spec.Selector)
	}
}

func TestListServicesFiltersByManagedBy(t *testing.T) {
	cs := fake.NewSimpleClientset()
	if _, err := cs.CoreV1().Services("ns1").Create(context.Background(), &corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "a", Namespace: "ns1", Labels: map[string]string{"managed-by": "control-panel"}}}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	if _, err := cs.CoreV1().Services("ns1").Create(context.Background(), &corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "b", Namespace: "ns1", Labels: map[string]string{}}}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	svcs, err := ListServices(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(svcs) != 1 || svcs[0].Name != "a" {
		t.Fatalf("list wrong: %+v", svcs)
	}
}

func TestListServicesForNotebooksIncludesExternal(t *testing.T) {
	// A managed Service and an external Service co-located with a notebook pod
	// in the same namespace must both be returned, with the Managed flag set
	// correctly. Services in a non-notebook namespace must be excluded.
	cs := fake.NewSimpleClientset()
	pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-abc", Namespace: "ns-notebook", UID: "uid-1"}}
	if _, err := cs.CoreV1().Pods("ns-notebook").Create(context.Background(), pod, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// Managed by the control panel.
	if _, err := cs.CoreV1().Services("ns-notebook").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "cp-svc-1", Namespace: "ns-notebook", Labels: map[string]string{"managed-by": "control-panel"}},
		Spec: corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Selector: map[string]string{"app": "notebook"},
			Ports: []corev1.ServicePort{{Port: 31555, TargetPort: intstr.FromInt(31555), NodePort: 31555, Protocol: corev1.ProtocolTCP}}},
	}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// External - created by the platform, NOT managed-by=control-panel.
	if _, err := cs.CoreV1().Services("ns-notebook").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-multi-port-svc", Namespace: "ns-notebook"},
		Spec: corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Selector: map[string]string{"app": "notebook"},
			Ports: []corev1.ServicePort{{Port: 32703, TargetPort: intstr.FromInt(32703), NodePort: 32703, Protocol: corev1.ProtocolTCP}}},
	}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// Noise: a service in a non-notebook namespace must NOT appear.
	if _, err := cs.CoreV1().Services("kube-system").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "kube-dns", Namespace: "kube-system"},
		Spec:       corev1.ServiceSpec{Type: corev1.ServiceTypeClusterIP},
	}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}

	svcs, err := ListServicesForNotebooks(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	if len(svcs) != 2 {
		t.Fatalf("expected 2 services (managed + external), got %d: %+v", len(svcs), svcs)
	}
	byName := map[string]ServiceInfo{}
	for _, s := range svcs {
		byName[s.Name] = s
	}
	if m, ok := byName["cp-svc-1"]; !ok || !m.Managed {
		t.Fatalf("cp-svc-1 should be managed: %+v", m)
	}
	if e, ok := byName["notebook-multi-port-svc"]; !ok || e.Managed {
		t.Fatalf("notebook-multi-port-svc should be present and NOT managed: %+v", e)
	}
	if _, ok := byName["kube-dns"]; ok {
		t.Fatal("kube-dns (non-notebook ns) should not be listed")
	}
	// Port flattening + target port resolution.
	if got := byName["cp-svc-1"].Ports[0]; got.Port != 31555 || got.TargetPort != 31555 || got.NodePort != 31555 || got.Protocol != "TCP" {
		t.Fatalf("port row wrong: %+v", got)
	}
}

func TestDeleteService(t *testing.T) {
	cs := fake.NewSimpleClientset(&corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "s1", Namespace: "ns1"}})
	if err := DeleteService(context.Background(), cs, "ns1", "s1"); err != nil {
		t.Fatal(err)
	}
	if _, err := cs.CoreV1().Services("ns1").Get(context.Background(), "s1", metav1.GetOptions{}); err == nil {
		t.Fatal("expected not found after delete")
	}
}
