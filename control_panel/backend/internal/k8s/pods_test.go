package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestListNotebookPods(t *testing.T) {
	cs := fake.NewSimpleClientset(
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-user1", Namespace: "ns1", UID: "u1", Labels: map[string]string{"app": "nb"}}, Spec: corev1.PodSpec{NodeName: "worker-1"}, Status: corev1.PodStatus{Phase: corev1.PodRunning, PodIP: "10.1.0.1"}},
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "NoteBook-2", Namespace: "ns2", UID: "u2"}, Status: corev1.PodStatus{Phase: corev1.PodPending}},
		&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "nginx-deploy", Namespace: "default", UID: "u3"}, Status: corev1.PodStatus{Phase: corev1.PodRunning}},
	)
	pods, err := ListNotebookPods(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	if len(pods) != 2 {
		t.Fatalf("expected 2 notebook pods, got %d: %+v", len(pods), pods)
	}
	byName := map[string]PodInfo{}
	for _, p := range pods {
		byName[p.Name] = p
	}
	if byName["notebook-user1"].Namespace != "ns1" || byName["notebook-user1"].UID != "u1" || byName["notebook-user1"].Node != "worker-1" {
		t.Fatalf("notebook-user1 wrong: %+v", byName["notebook-user1"])
	}
	if byName["notebook-user1"].Status != "Running" {
		t.Fatalf("status wrong: %s", byName["notebook-user1"].Status)
	}
	if byName["NoteBook-2"].Name != "NoteBook-2" {
		t.Fatalf("case-insensitive match failed: %+v", byName["NoteBook-2"])
	}
}

func TestStableKeyForPod(t *testing.T) {
	key, kind, ws, proj := StableKeyForPod("ns1", "uid-123", map[string]string{
		"workspace_id": "ws-abc",
		"project_id":   "proj-xyz",
	})
	if key != "v1:namespace:ns1:workspace:ws-abc:project:proj-xyz" || kind != "business_labels" || ws != "ws-abc" || proj != "proj-xyz" {
		t.Fatalf("business labels stable key wrong: key=%s kind=%s ws=%s proj=%s", key, kind, ws, proj)
	}

	fallbackKey, fallbackKind, _, _ := StableKeyForPod("ns1", "uid-123", map[string]string{
		"workspace_id": "ws-abc",
	})
	if fallbackKey != "v1:pod_uid:uid-123" || fallbackKind != "pod_uid" {
		t.Fatalf("missing project_id fallback wrong: key=%s kind=%s", fallbackKey, fallbackKind)
	}
}
