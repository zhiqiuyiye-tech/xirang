package k8s

import (
	"context"
	"path/filepath"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

// TestCreateSvcHandlerCreatesService drives the full task pipeline: submit a
// k8s_create_svc task, wait for it to reach succeeded, and verify the Service
// was created in the fake clientset with the expected shape.
func TestCreateSvcHandlerCreatesService(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	cs := fake.NewSimpleClientset()
	RegisterK8sHandlers(eng, cs)

	params := map[string]any{
		"namespace": "ns1", "pod_name": "p1", "pod_uid": "uid-1",
		"selector": map[string]string{"app": "p1"}, "type": "NodePort",
		"ports": []map[string]any{{"port": 31555, "target_port": 31555, "node_port": 31555, "protocol": "TCP"}},
	}
	id, err := eng.Submit(context.Background(), "k8s_create_svc", "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	svcs, err := ListServices(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(svcs) != 1 {
		t.Fatalf("expected 1 svc, got %d", len(svcs))
	}
	svc := svcs[0]
	if svc.Spec.Type != corev1.ServiceTypeNodePort {
		t.Fatalf("type wrong: %v", svc.Spec.Type)
	}
	if len(svc.Spec.Ports) != 1 || svc.Spec.Ports[0].NodePort != 31555 || svc.Spec.Ports[0].Port != 31555 {
		t.Fatalf("ports wrong: %+v", svc.Spec.Ports)
	}
	if svc.Spec.Selector["app"] != "p1" {
		t.Fatalf("selector wrong: %+v", svc.Spec.Selector)
	}
	if len(svc.OwnerReferences) != 1 || svc.OwnerReferences[0].UID != "uid-1" {
		t.Fatalf("ownerRef wrong: %+v", svc.OwnerReferences)
	}
	steps, _ := store.ListSteps(context.Background(), id)
	if len(steps) != 2 || steps[0].Status != "succeeded" || steps[1].Status != "succeeded" {
		t.Fatalf("steps wrong: %+v", steps)
	}
	if steps[0].Name != "create_service" || steps[1].Name != "create_network_policy" {
		t.Fatalf("step names wrong: %+v", steps)
	}
	// The auto-created NetworkPolicy must exist and allow the same port.
	nps, _ := ListNetworkPolicies(context.Background(), cs, "ns1")
	if len(nps) != 1 {
		t.Fatalf("expected 1 network policy auto-created, got %d", len(nps))
	}
	if len(nps[0].Spec.Ingress) != 1 || len(nps[0].Spec.Ingress[0].Ports) != 1 {
		t.Fatalf("np ingress ports wrong: %+v", nps[0].Spec.Ingress)
	}
}

// TestCreateSvcHandlerBadParamsFails verifies the handler is defensive: a
// missing "port" field in a port spec must fail the task with a clear error
// rather than panicking on a type assertion.
func TestCreateSvcHandlerBadParamsFails(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	cs := fake.NewSimpleClientset()
	RegisterK8sHandlers(eng, cs)

	params := map[string]any{
		"namespace": "ns1", "pod_name": "p1", "pod_uid": "uid-1",
		"selector": map[string]string{"app": "p1"}, "type": "NodePort",
		"ports": []map[string]any{{"target_port": 31555, "protocol": "TCP"}}, // missing "port"
	}
	id, err := eng.Submit(context.Background(), "k8s_create_svc", "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	got, _ := store.GetTask(context.Background(), id)
	if got.Error == nil {
		t.Fatal("expected non-nil error message")
	}
	// No service should have been created.
	svcs, _ := ListServices(context.Background(), cs, "ns1")
	if len(svcs) != 0 {
		t.Fatalf("expected 0 svc, got %d", len(svcs))
	}
}

// TestDeleteSvcHandlerDeletesService pre-creates a Service, submits a
// k8s_delete_svc task, and verifies the Service is gone.
func TestDeleteSvcHandlerDeletesService(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	cs := fake.NewSimpleClientset(&corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name: "s1", Namespace: "ns1",
			Labels: map[string]string{"managed-by": "control-panel"},
		},
	})
	RegisterK8sHandlers(eng, cs)

	params := map[string]any{"namespace": "ns1", "name": "s1"}
	id, err := eng.Submit(context.Background(), "k8s_delete_svc", "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	svcs, err := ListServices(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(svcs) != 0 {
		t.Fatalf("expected 0 svc after delete, got %d", len(svcs))
	}
}

// TestCreateNPHandlerCreatesNetworkPolicy submits a k8s_create_np task and
// verifies the NetworkPolicy was created with the expected ingress port.
func TestCreateNPHandlerCreatesNetworkPolicy(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	cs := fake.NewSimpleClientset()
	RegisterK8sHandlers(eng, cs)

	params := map[string]any{
		"namespace": "ns1", "pod_name": "p1", "pod_uid": "uid-1",
		"pod_selector": map[string]string{"app": "p1"},
		"ingress_ports": []map[string]any{{"protocol": "TCP", "port": 31555}},
	}
	id, err := eng.Submit(context.Background(), "k8s_create_np", "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	nps, err := ListNetworkPolicies(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(nps) != 1 {
		t.Fatalf("expected 1 np, got %d", len(nps))
	}
	np := nps[0]
	if len(np.OwnerReferences) != 1 || np.OwnerReferences[0].UID != "uid-1" {
		t.Fatalf("ownerRef wrong: %+v", np.OwnerReferences)
	}
	if np.Spec.PodSelector.MatchLabels["app"] != "p1" {
		t.Fatalf("podSelector wrong: %+v", np.Spec.PodSelector)
	}
	if len(np.Spec.Ingress) != 1 || len(np.Spec.Ingress[0].Ports) != 1 {
		t.Fatalf("ingress wrong: %+v", np.Spec.Ingress)
	}
	port := np.Spec.Ingress[0].Ports[0]
	if port.Protocol == nil || *port.Protocol != corev1.ProtocolTCP {
		t.Fatalf("ingress protocol wrong: %+v", port)
	}
	if port.Port.IntVal != 31555 {
		t.Fatalf("ingress port wrong: %+v", port.Port)
	}
}

// TestDeleteNPHandlerDeletesNetworkPolicy pre-creates a NetworkPolicy,
// submits a k8s_delete_np task, and verifies the policy is gone.
func TestDeleteNPHandlerDeletesNetworkPolicy(t *testing.T) {
	store, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer store.Close()
	eng := tasks.NewEngine(store)
	cs := fake.NewSimpleClientset(&networkingv1.NetworkPolicy{
		ObjectMeta: metav1.ObjectMeta{
			Name: "np1", Namespace: "ns1",
			Labels: map[string]string{"managed-by": "control-panel"},
		},
	})
	RegisterK8sHandlers(eng, cs)

	params := map[string]any{"namespace": "ns1", "name": "np1"}
	id, err := eng.Submit(context.Background(), "k8s_delete_np", "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)

	nps, err := ListNetworkPolicies(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(nps) != 0 {
		t.Fatalf("expected 0 np after delete, got %d", len(nps))
	}
}

// waitFor polls the task status until it reaches want or the deadline elapses.
func waitFor(t *testing.T, store *db.Store, id int64, want string, timeout time.Duration) {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		got, err := store.GetTask(context.Background(), id)
		if err == nil && got.Status == want {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	got, _ := store.GetTask(context.Background(), id)
	status := "(unknown)"
	if got != nil {
		status = got.Status
	}
	t.Fatalf("task %d never reached %s (last status=%s)", id, want, status)
}
