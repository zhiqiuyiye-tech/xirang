package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestCreateNetworkPolicySetsOwnerRefAndIngress(t *testing.T) {
	cs := fake.NewSimpleClientset()
	np, err := CreateNetworkPolicy(context.Background(), cs, CreateNetworkPolicyReq{
		Namespace:    "ns1",
		PodName:     "p1",
		PodUID:      "uid-1",
		PodSelector: map[string]string{"app": "p1"},
		IngressPorts: []IngressPortSpec{{Protocol: "TCP", Port: 31555}},
	})
	if err != nil {
		t.Fatal(err)
	}
	if len(np.OwnerReferences) != 1 || np.OwnerReferences[0].UID != "uid-1" {
		t.Fatalf("ownerRef wrong: %+v", np.OwnerReferences)
	}
	if np.OwnerReferences[0].Kind != "Pod" || np.OwnerReferences[0].Name != "p1" {
		t.Fatalf("ownerRef wrong: %+v", np.OwnerReferences)
	}
	if np.OwnerReferences[0].APIVersion != "v1" {
		t.Fatalf("ownerRef APIVersion wrong: %s", np.OwnerReferences[0].APIVersion)
	}
	if np.OwnerReferences[0].Controller == nil || !*np.OwnerReferences[0].Controller {
		t.Fatalf("ownerRef Controller wrong: %+v", np.OwnerReferences[0].Controller)
	}
	if np.Labels["managed-by"] != "control-panel" || np.Labels["pod-uid"] != "uid-1" {
		t.Fatalf("labels wrong: %+v", np.Labels)
	}
	if np.Spec.PodSelector.MatchLabels["app"] != "p1" {
		t.Fatalf("podSelector wrong: %+v", np.Spec.PodSelector)
	}
	if len(np.Spec.Ingress) != 1 || len(np.Spec.Ingress[0].Ports) != 1 {
		t.Fatalf("ingress wrong: %+v", np.Spec.Ingress)
	}
	port := np.Spec.Ingress[0].Ports[0]
	if port.Protocol == nil || *port.Protocol != corev1.ProtocolTCP {
		t.Fatalf("ingress port protocol wrong: %+v", port)
	}
	if port.Port.IntVal != 31555 {
		t.Fatalf("ingress port wrong: %+v", port.Port)
	}
	if len(np.Spec.PolicyTypes) != 1 || np.Spec.PolicyTypes[0] != networkingv1.PolicyTypeIngress {
		t.Fatalf("policyTypes wrong: %+v", np.Spec.PolicyTypes)
	}
}

func TestListNetworkPolicies(t *testing.T) {
	cs := fake.NewSimpleClientset(&networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{Name: "np1", Namespace: "ns1", Labels: map[string]string{"managed-by": "control-panel"}}})
	nps, err := ListNetworkPolicies(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(nps) != 1 || nps[0].Name != "np1" {
		t.Fatalf("list wrong: %+v", nps)
	}
}

func TestDeleteNetworkPolicy(t *testing.T) {
	cs := fake.NewSimpleClientset(&networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{Name: "np1", Namespace: "ns1"}})
	if err := DeleteNetworkPolicy(context.Background(), cs, "ns1", "np1"); err != nil {
		t.Fatal(err)
	}
	if _, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), "np1", metav1.GetOptions{}); err == nil {
		t.Fatal("expected not found after delete")
	}
}
