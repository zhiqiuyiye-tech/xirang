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
	// A managed Service and an external Service that both route to a notebook
	// pod (selector matches the pod's labels) must be returned and attributed to
	// that pod via Pods[]. A Service whose selector matches NO notebook pod is
	// still listed but with empty Pods. A Service in a non-notebook namespace is
	// excluded entirely.
	cs := fake.NewSimpleClientset()
	// Notebook pod with labels that both Services select on.
	pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{
		Name: "notebook-abc", Namespace: "ns-notebook", UID: "uid-1",
		Labels: map[string]string{"app": "nb-1"},
	}}
	if _, err := cs.CoreV1().Pods("ns-notebook").Create(context.Background(), pod, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// Managed by the control panel; selector matches the pod.
	if _, err := cs.CoreV1().Services("ns-notebook").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "cp-svc-1", Namespace: "ns-notebook", Labels: map[string]string{"managed-by": "control-panel"}},
		Spec: corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Selector: map[string]string{"app": "nb-1"},
			Ports: []corev1.ServicePort{{Port: 31555, TargetPort: intstr.FromInt(31555), NodePort: 31555, Protocol: corev1.ProtocolTCP}}},
	}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// External - created by the platform, selector also matches the pod.
	if _, err := cs.CoreV1().Services("ns-notebook").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-multi-port-svc", Namespace: "ns-notebook"},
		Spec: corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Selector: map[string]string{"app": "nb-1"},
			Ports: []corev1.ServicePort{{Port: 32703, TargetPort: intstr.FromInt(32703), NodePort: 32703, Protocol: corev1.ProtocolTCP}}},
	}, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	// A Service in the notebook namespace whose selector matches NO notebook pod:
	// still listed (it's in a notebook namespace) but Pods must be empty, so the
	// per-notebook UI won't attribute it to any pod.
	if _, err := cs.CoreV1().Services("ns-notebook").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: "unmatched-svc", Namespace: "ns-notebook"},
		Spec:       corev1.ServiceSpec{Type: corev1.ServiceTypeClusterIP, Selector: map[string]string{"app": "other"}},
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
	if len(svcs) != 3 {
		t.Fatalf("expected 3 services, got %d: %+v", len(svcs), svcs)
	}
	byName := map[string]ServiceInfo{}
	for _, s := range svcs {
		byName[s.Name] = s
	}
	// Managed flag.
	if m, ok := byName["cp-svc-1"]; !ok || !m.Managed {
		t.Fatalf("cp-svc-1 should be managed: %+v", m)
	}
	if e, ok := byName["notebook-multi-port-svc"]; !ok || e.Managed {
		t.Fatalf("notebook-multi-port-svc should be present and NOT managed: %+v", e)
	}
	if _, ok := byName["kube-dns"]; ok {
		t.Fatal("kube-dns (non-notebook ns) should not be listed")
	}
	// Pod attribution: both pod-targeting Services route to notebook-abc.
	wantPod := PodRef{Name: "notebook-abc", UID: "uid-1"}
	for _, name := range []string{"cp-svc-1", "notebook-multi-port-svc"} {
		s := byName[name]
		if len(s.Pods) != 1 || s.Pods[0] != wantPod {
			t.Fatalf("%s should route to notebook-abc, got Pods=%+v", name, s.Pods)
		}
	}
	// The unmatched Service routes to no notebook pod.
	if u := byName["unmatched-svc"]; len(u.Pods) != 0 {
		t.Fatalf("unmatched-svc should have empty Pods, got %+v", u.Pods)
	}
	// Port flattening + target port resolution.
	if got := byName["cp-svc-1"].Ports[0]; got.Port != 31555 || got.TargetPort != 31555 || got.NodePort != 31555 || got.Protocol != "TCP" {
		t.Fatalf("port row wrong: %+v", got)
	}
}

func TestSelectorMatches(t *testing.T) {
	podLabels := map[string]string{"app": "nb-1", "tier": "web"}
	cases := []struct {
		name     string
		selector map[string]string
		want     bool
	}{
		{"exact match", map[string]string{"app": "nb-1", "tier": "web"}, true},
		{"subset match", map[string]string{"app": "nb-1"}, true},
		{"wrong value", map[string]string{"app": "nb-2"}, false},
		{"missing key", map[string]string{"env": "prod"}, false},
		{"empty selector matches nothing", map[string]string{}, false},
		{"nil selector matches nothing", nil, false},
	}
	for _, c := range cases {
		if got := selectorMatches(c.selector, podLabels); got != c.want {
			t.Fatalf("%s: selectorMatches=%v want %v", c.name, got, c.want)
		}
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
