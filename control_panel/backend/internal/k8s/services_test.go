package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
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

func TestDeleteService(t *testing.T) {
	cs := fake.NewSimpleClientset(&corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "s1", Namespace: "ns1"}})
	if err := DeleteService(context.Background(), cs, "ns1", "s1"); err != nil {
		t.Fatal(err)
	}
	if _, err := cs.CoreV1().Services("ns1").Get(context.Background(), "s1", metav1.GetOptions{}); err == nil {
		t.Fatal("expected not found after delete")
	}
}
