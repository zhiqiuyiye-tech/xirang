package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestListNodes(t *testing.T) {
	cs := fake.NewSimpleClientset(
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "master-1", Labels: map[string]string{"node-role.kubernetes.io/control-plane": ""}}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.1"}}}},
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-1"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.2"}}}},
		&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-2", Labels: map[string]string{"node-role.kubernetes.io/master": ""}}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeHostName, Address: "worker-2"}}}},
	)
	nodes, err := ListNodes(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	if len(nodes) != 3 {
		t.Fatalf("expected 3 nodes, got %d", len(nodes))
	}
	byName := map[string]NodeInfo{}
	for _, n := range nodes {
		byName[n.Name] = n
	}
	if byName["master-1"].Role != "master" || byName["master-1"].Host != "10.0.0.1" {
		t.Fatalf("master-1 wrong: %+v", byName["master-1"])
	}
	if byName["worker-1"].Role != "worker" || byName["worker-1"].Host != "10.0.0.2" {
		t.Fatalf("worker-1 wrong: %+v", byName["worker-1"])
	}
	// worker-2 has only a hostname address, no internal IP -> Host empty
	if byName["worker-2"].Host != "" {
		t.Fatalf("worker-2 host should be empty, got %q", byName["worker-2"].Host)
	}
}
