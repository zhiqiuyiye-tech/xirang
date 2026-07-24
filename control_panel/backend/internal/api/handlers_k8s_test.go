package api

import (
	"bytes"
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/kubernetes/fake"

	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

// newRouterWithK8s is the k8s-aware variant of newRouter: it builds a router
// with a fake k8s clientset injected and RegisterK8sHandlers wired, returning
// the fake clientset so tests can assert on the cluster state after async
// tasks run. Existing non-k8s tests use newRouter (which delegates here
// internally with a fake clientset of its own).
func newRouterWithK8s(t *testing.T) (*gin.Engine, *db.Store, *auth.Tokens, kubernetes.Interface) {
	t.Helper()
	gin.SetMode(gin.TestMode)
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	t.Cleanup(func() { s.Close() })
	c, _ := crypto.New(make([]byte, 32))
	sshm := ssh.NewManager(c, 2, time.Minute)
	eng := tasks.NewEngine(s)
	ws := workers.NewService(s, c, sshm, eng)
	tk := auth.NewTokens("secret", time.Hour)
	cs := fake.NewSimpleClientset()
	k8s.RegisterK8sHandlers(eng, cs)
	return NewRouter(tk, ws, s, eng, cs), s, tk, cs
}

// TestCreateServiceViaAPI drives the full HTTP path: POST /api/v1/k8s/services
// returns 202 + task_id, and the async handler creates the Service in the fake
// clientset. Verifies the create endpoint is async (202) and wires through to
// the k8s_create_svc task handler registered on the engine.
func TestCreateServiceViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	body, _ := json.Marshal(map[string]any{
		"namespace": "ns1", "pod_name": "p1", "pod_uid": "u1",
		"selector": map[string]string{"app": "p1"}, "type": "NodePort",
		"ports": []map[string]any{{"port": 31555, "target_port": 31555, "node_port": 31555, "protocol": "TCP"}},
	})
	req := httptest.NewRequest("POST", "/api/v1/k8s/services", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if resp["task_id"] == nil {
		t.Fatalf("no task_id in response: %s", w.Body.String())
	}

	// Wait for the async task to create the Service, then verify.
	waitForK8s(t, cs, "ns1", 1, 2*time.Second)
	svcs, err := k8s.ListServices(context.Background(), cs, "ns1")
	if err != nil {
		t.Fatal(err)
	}
	if len(svcs) != 1 {
		t.Fatalf("expected 1 svc created, got %d", len(svcs))
	}
}

// TestListServicesViaAPI verifies the sync list path: GET /api/v1/k8s/services
// returns 200 and the JSON array of Services managed by the control panel.
func TestListServicesViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	// Pre-create a service via the k8s package directly so the list has data.
	_, err := k8s.CreateService(context.Background(), cs, k8s.CreateServiceReq{
		Namespace: "ns1", PodName: "p1", PodUID: "u1",
		Selector: map[string]string{"app": "p1"}, Type: "NodePort",
		Ports: []k8s.PortSpec{{Port: 31555, TargetPort: 31555, NodePort: 31555, Protocol: "TCP"}},
	})
	if err != nil {
		t.Fatal(err)
	}

	req := httptest.NewRequest("GET", "/api/v1/k8s/services?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var list []map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &list); err != nil {
		t.Fatal(err)
	}
	if len(list) != 1 {
		t.Fatalf("expected 1 svc in list, got %d", len(list))
	}
}

// TestDeleteServiceViaAPI verifies the async delete path: DELETE returns 202 +
// task_id, and the k8s_delete_svc task removes the Service. The Service is
// pre-created directly in the fake clientset with a fixed name (the fake
// clientset does not populate GenerateName, so k8s.CreateService cannot be
// used to get a named Service back).
func TestDeleteServiceViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	// Pre-create a service with a known name for the delete to target.
	_, err := cs.CoreV1().Services("ns1").Create(context.Background(), &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{
			Name: "svc-to-delete", Namespace: "ns1",
			Labels: map[string]string{"managed-by": "control-panel"},
		},
	}, metav1.CreateOptions{})
	if err != nil {
		t.Fatal(err)
	}

	req := httptest.NewRequest("DELETE", "/api/v1/k8s/services/svc-to-delete?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var resp map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &resp); err != nil {
		t.Fatal(err)
	}
	if resp["task_id"] == nil {
		t.Fatalf("no task_id in response: %s", w.Body.String())
	}

	// Wait for the async delete to complete.
	waitForK8s(t, cs, "ns1", 0, 2*time.Second)
}

// TestCreateNetworkPolicyViaAPI verifies POST /api/v1/k8s/network-policies
// returns 202 + task_id and creates the NetworkPolicy.
func TestCreateNetworkPolicyViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	body, _ := json.Marshal(map[string]any{
		"namespace": "ns1", "pod_name": "p1", "pod_uid": "u1",
		"pod_selector": map[string]string{"app": "p1"},
		"ingress_ports": []map[string]any{{"protocol": "TCP", "port": 31555}},
	})
	req := httptest.NewRequest("POST", "/api/v1/k8s/network-policies", bytes.NewReader(body))
	req.Header.Set("Authorization", authHeader(t, tk))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}

	// Wait for async creation.
	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) {
		nps, _ := k8s.ListNetworkPolicies(context.Background(), cs, "ns1")
		if len(nps) >= 1 {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	nps, _ := k8s.ListNetworkPolicies(context.Background(), cs, "ns1")
	if len(nps) != 1 {
		t.Fatalf("expected 1 np created, got %d", len(nps))
	}
}

// TestListNetworkPoliciesViaAPI verifies the sync list path for network policies.
func TestListNetworkPoliciesViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	_, err := k8s.CreateNetworkPolicy(context.Background(), cs, k8s.CreateNetworkPolicyReq{
		Namespace: "ns1", PodName: "p1", PodUID: "u1",
		PodSelector:  map[string]string{"app": "p1"},
		IngressPorts: []k8s.IngressPortSpec{{Protocol: "TCP", Port: 31555}},
	})
	if err != nil {
		t.Fatal(err)
	}

	req := httptest.NewRequest("GET", "/api/v1/k8s/network-policies?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}
	var list []map[string]any
	if err := json.Unmarshal(w.Body.Bytes(), &list); err != nil {
		t.Fatal(err)
	}
	if len(list) != 1 {
		t.Fatalf("expected 1 np in list, got %d", len(list))
	}
}

// TestDeleteNetworkPolicyViaAPI verifies DELETE returns 202 + task_id and
// removes the NetworkPolicy. The policy is pre-created directly in the fake
// clientset with a fixed name (the fake clientset does not populate
// GenerateName).
func TestDeleteNetworkPolicyViaAPI(t *testing.T) {
	r, _, tk, cs := newRouterWithK8s(t)
	_, err := cs.NetworkingV1().NetworkPolicies("ns1").Create(context.Background(), &networkingv1.NetworkPolicy{
		ObjectMeta: metav1.ObjectMeta{
			Name: "np-to-delete", Namespace: "ns1",
			Labels: map[string]string{"managed-by": "control-panel"},
		},
	}, metav1.CreateOptions{})
	if err != nil {
		t.Fatal(err)
	}

	req := httptest.NewRequest("DELETE", "/api/v1/k8s/network-policies/np-to-delete?namespace=ns1", nil)
	req.Header.Set("Authorization", authHeader(t, tk))
	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)
	if w.Code != http.StatusAccepted {
		t.Fatalf("code=%d body=%s", w.Code, w.Body.String())
	}

	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) {
		nps, _ := k8s.ListNetworkPolicies(context.Background(), cs, "ns1")
		if len(nps) == 0 {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	nps, _ := k8s.ListNetworkPolicies(context.Background(), cs, "ns1")
	if len(nps) != 0 {
		t.Fatalf("expected 0 np after delete, got %d", len(nps))
	}
}

// TestK8sEndpointsRequireAuth verifies all six k8s endpoints are behind
// BearerMiddleware (authed group): no Authorization header -> 401.
func TestK8sEndpointsRequireAuth(t *testing.T) {
	r, _, _, _ := newRouterWithK8s(t)
	endpoints := []struct {
		method, path string
	}{
		{"POST", "/api/v1/k8s/services"},
		{"GET", "/api/v1/k8s/services?namespace=ns1"},
		{"DELETE", "/api/v1/k8s/services/x?namespace=ns1"},
		{"POST", "/api/v1/k8s/network-policies"},
		{"GET", "/api/v1/k8s/network-policies?namespace=ns1"},
		{"DELETE", "/api/v1/k8s/network-policies/x?namespace=ns1"},
	}
	for _, e := range endpoints {
		req := httptest.NewRequest(e.method, e.path, nil)
		w := httptest.NewRecorder()
		r.ServeHTTP(w, req)
		if w.Code != http.StatusUnauthorized {
			t.Errorf("%s %s: code=%d, want 401", e.method, e.path, w.Code)
		}
	}
}

// TestK8sEndpointsUnavailableWithoutClient verifies that when the k8s client
// is nil (non-cluster / local dev), the sync list endpoints return 503 Service
// Unavailable rather than panicking. This is the brief's "nil k8sClient -> 503"
// requirement.
func TestK8sEndpointsUnavailableWithoutClient(t *testing.T) {
	t.Helper()
	gin.SetMode(gin.TestMode)
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	t.Cleanup(func() { s.Close() })
	c, _ := crypto.New(make([]byte, 32))
	sshm := ssh.NewManager(c, 2, time.Minute)
	eng := tasks.NewEngine(s)
	ws := workers.NewService(s, c, sshm, eng)
	tk := auth.NewTokens("secret", time.Hour)
	// Pass nil as the k8s client - simulates non-cluster / local dev.
	r := NewRouter(tk, ws, s, eng, nil)

	for _, path := range []string{"/api/v1/k8s/services?namespace=ns1", "/api/v1/k8s/network-policies?namespace=ns1"} {
		req := httptest.NewRequest("GET", path, nil)
		req.Header.Set("Authorization", authHeader(t, tk))
		w := httptest.NewRecorder()
		r.ServeHTTP(w, req)
		if w.Code != http.StatusServiceUnavailable {
			t.Errorf("%s: code=%d, want 503", path, w.Code)
		}
	}
}

// waitForK8s polls ListServices until it reaches want count or the deadline.
func waitForK8s(t *testing.T, cs kubernetes.Interface, namespace string, want int, timeout time.Duration) {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		svcs, _ := k8s.ListServices(context.Background(), cs, namespace)
		if len(svcs) == want {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	svcs, _ := k8s.ListServices(context.Background(), cs, namespace)
	t.Fatalf("services never reached count %d (last=%d)", want, len(svcs))
}
