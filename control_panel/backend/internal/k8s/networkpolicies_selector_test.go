package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestCreateNetworkPolicyRejectsStalePodIdentity(t *testing.T) {
	pod := k8sTestPod("notebook-a", "current-uid", map[string]string{"app": "notebook"})
	client := fake.NewSimpleClientset(pod)
	req := selectorTestPolicyRequest()
	req.PodUID = "stale-uid"

	if _, err := CreateNetworkPolicy(context.Background(), client, req); err == nil {
		t.Fatal("expected stale Pod UID to reject NetworkPolicy creation")
	}
	assertNoSelectorTestPolicies(t, client)
}

func TestCreateNetworkPolicyRejectsSelectorMatchingMultiplePods(t *testing.T) {
	client := fake.NewSimpleClientset(
		k8sTestPod("notebook-a", "pod-uid-a", map[string]string{"app": "notebook"}),
		k8sTestPod("notebook-b", "pod-uid-b", map[string]string{"app": "notebook"}),
	)

	if _, err := CreateNetworkPolicy(context.Background(), client, selectorTestPolicyRequest()); err == nil {
		t.Fatal("expected a selector matching multiple Pods to reject NetworkPolicy creation")
	}
	assertNoSelectorTestPolicies(t, client)
}

func TestCreateNetworkPolicyRejectsSelectorThatDoesNotMatchTargetPod(t *testing.T) {
	client := fake.NewSimpleClientset(
		k8sTestPod("notebook-a", "pod-uid-a", map[string]string{"app": "notebook"}),
	)
	req := selectorTestPolicyRequest()
	req.PodSelector = map[string]string{"app": "another-notebook"}

	if _, err := CreateNetworkPolicy(context.Background(), client, req); err == nil {
		t.Fatal("expected a selector that misses the target Pod to reject NetworkPolicy creation")
	}
	assertNoSelectorTestPolicies(t, client)
}

func selectorTestPolicyRequest() CreateNetworkPolicyReq {
	return CreateNetworkPolicyReq{
		Namespace:   "ns1",
		PodName:     "notebook-a",
		PodUID:      "pod-uid-a",
		PodSelector: map[string]string{"app": "notebook"},
	}
}

func k8sTestPod(name, uid string, labels map[string]string) *corev1.Pod {
	return &corev1.Pod{ObjectMeta: metav1.ObjectMeta{
		Name: name, Namespace: "ns1", UID: typesUID(uid), Labels: labels,
	}}
}

func assertNoSelectorTestPolicies(t *testing.T, client *fake.Clientset) {
	t.Helper()
	policies, err := client.NetworkingV1().NetworkPolicies("ns1").List(context.Background(), metav1.ListOptions{})
	if err != nil {
		t.Fatal(err)
	}
	if len(policies.Items) != 0 {
		t.Fatalf("expected no NetworkPolicy to be created, got %d", len(policies.Items))
	}
}
