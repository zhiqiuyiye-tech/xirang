package k8s

import (
	"context"
	"errors"
	"path/filepath"
	"reflect"
	"strings"
	"sync"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/util/intstr"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/kubernetes/fake"
	corev1client "k8s.io/client-go/kubernetes/typed/core/v1"
	networkingv1client "k8s.io/client-go/kubernetes/typed/networking/v1"
	ktesting "k8s.io/client-go/testing"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func TestCreateSvcHandlerRollsBackServiceWhenPolicyCreationFails(t *testing.T) {
	for _, tc := range []struct {
		name          string
		rollbackError error
		wantStatus    string
		wantError     []string
	}{
		{name: "rollback succeeds", wantStatus: "failed", wantError: []string{"service rollback succeeded"}},
		{name: "rollback fails", rollbackError: errors.New("delete denied"), wantStatus: "failed", wantError: []string{"service rollback failed", "delete denied"}},
	} {
		t.Run(tc.name, func(t *testing.T) {
			cs := fake.NewSimpleClientset(k8sTestPod("pod1", "pod-uid", map[string]string{"app": "pod1"}))
			cs.PrependReactor("create", "services", func(a ktesting.Action) (bool, runtime.Object, error) {
				svc := a.(ktesting.CreateAction).GetObject().(*corev1.Service)
				svc.UID = "created-service-uid"
				svc.ResourceVersion = "created-service-rv"
				return false, nil, nil
			})
			cs.PrependReactor("create", "networkpolicies", func(ktesting.Action) (bool, runtime.Object, error) {
				return true, nil, errors.New("policy admission denied")
			})

			var gotDeletePreconditions *metav1.Preconditions
			cs.PrependReactor("delete", "services", func(a ktesting.Action) (bool, runtime.Object, error) {
				gotDeletePreconditions = a.(ktesting.DeleteAction).GetDeleteOptions().Preconditions
				if tc.rollbackError != nil {
					return true, nil, tc.rollbackError
				}
				return false, nil, nil
			})

			store, eng := newK8sTaskEngine(t, cs)
			defer store.Close()
			id := submitK8sTask(t, eng, "k8s_create_svc", map[string]any{
				"name": "svc1", "namespace": "ns1", "pod_name": "pod1", "pod_uid": "pod-uid",
				"selector": map[string]string{"app": "pod1"},
				"mappings": []map[string]any{{"pod_port": 8080}},
			})
			waitFor(t, store, id, tc.wantStatus, 2*time.Second)

			got, err := store.GetTask(context.Background(), id)
			if err != nil || got.Error == nil {
				t.Fatalf("expected task error, task=%+v err=%v", got, err)
			}
			for _, text := range tc.wantError {
				if !strings.Contains(*got.Error, text) {
					t.Errorf("task error %q does not contain %q", *got.Error, text)
				}
			}
			if gotDeletePreconditions == nil || gotDeletePreconditions.UID == nil || *gotDeletePreconditions.UID != "created-service-uid" || gotDeletePreconditions.ResourceVersion == nil || *gotDeletePreconditions.ResourceVersion != "created-service-rv" {
				t.Fatalf("rollback delete was not pinned to the created Service identity: %+v", gotDeletePreconditions)
			}
			steps, err := store.ListSteps(context.Background(), id)
			if err != nil {
				t.Fatal(err)
			}
			if len(steps) != 3 || steps[2].Name != "rollback_service" {
				t.Fatalf("expected explicit rollback step, got %+v", steps)
			}
			wantRollbackStatus := "succeeded"
			if tc.rollbackError != nil {
				wantRollbackStatus = "failed"
			}
			if steps[2].Status != wantRollbackStatus {
				t.Fatalf("rollback step status=%q, want %q", steps[2].Status, wantRollbackStatus)
			}
			_, getErr := cs.CoreV1().Services("ns1").Get(context.Background(), "svc1", metav1.GetOptions{})
			if tc.rollbackError == nil && getErr == nil {
				t.Fatal("Service should have been removed after successful rollback")
			}
			if tc.rollbackError != nil && getErr != nil {
				t.Fatalf("Service should remain when rollback fails: %v", getErr)
			}
		})
	}
}

func TestUpdateSvcHandlerValidatesServiceBeforeChangingPolicies(t *testing.T) {
	for _, tc := range []struct {
		name           string
		managed        bool
		requestVersion string
		serviceVersion string
	}{
		{name: "stale service version", managed: true, requestVersion: "stale", serviceVersion: "svc-rv"},
		{name: "external service", managed: false, requestVersion: "svc-rv", serviceVersion: "svc-rv"},
	} {
		t.Run(tc.name, func(t *testing.T) {
			labels := map[string]string{"owner": "other"}
			if tc.managed {
				labels["managed-by"] = "control-panel"
			}
			svc := &corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "svc1", Namespace: "ns1", UID: "svc-uid", ResourceVersion: tc.serviceVersion, Labels: labels}}
			np := networkPolicyForService("np1", "ns1", "svc1", "np-uid", "np-rv", 8080)
			original := np.DeepCopy()
			cs := fake.NewSimpleClientset(svc, np)
			store, eng := newK8sTaskEngine(t, cs)
			defer store.Close()
			id := submitPortUpdate(t, eng, tc.requestVersion)
			waitFor(t, store, id, "failed", 2*time.Second)

			updated, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), "np1", metav1.GetOptions{})
			if err != nil {
				t.Fatal(err)
			}
			if !reflect.DeepEqual(updated.Spec, original.Spec) {
				t.Fatalf("NetworkPolicy changed before service preflight succeeded: got=%+v want=%+v", updated.Spec, original.Spec)
			}
		})
	}
}

func TestUpdateSvcHandlerRestoresPoliciesWhenServiceUpdateFails(t *testing.T) {
	svc := managedTestService("svc-rv")
	np := networkPolicyForService("np1", "ns1", "svc1", "np-uid", "np-rv", 8080)
	original := np.DeepCopy()
	cs := fake.NewSimpleClientset(svc, np)
	cs.PrependReactor("update", "services", func(ktesting.Action) (bool, runtime.Object, error) {
		return true, nil, errors.New("service update denied")
	})
	store, eng := newK8sTaskEngine(t, cs)
	defer store.Close()
	id := submitPortUpdate(t, eng, "svc-rv")
	waitFor(t, store, id, "failed", 2*time.Second)

	updated, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), "np1", metav1.GetOptions{})
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(updated.Spec, original.Spec) {
		t.Fatalf("policy spec was not restored after Service update failure: got=%+v want=%+v", updated.Spec, original.Spec)
	}
	task, err := store.GetTask(context.Background(), id)
	if err != nil || task.Error == nil || !strings.Contains(*task.Error, "rollback succeeded") {
		t.Fatalf("expected successful rollback in task error, task=%+v err=%v", task, err)
	}
}

func TestUpdateSvcHandlerRestoresEarlierPoliciesWhenLaterPolicyUpdateFails(t *testing.T) {
	svc := managedTestService("svc-rv")
	np1 := networkPolicyForService("np1", "ns1", "svc1", "np-uid-1", "np-rv-1", 8080)
	np2 := networkPolicyForService("np2", "ns1", "svc1", "np-uid-2", "np-rv-2", 8081)
	originals := map[string]*networkingv1.NetworkPolicy{"np1": np1.DeepCopy(), "np2": np2.DeepCopy()}
	cs := fake.NewSimpleClientset(svc, np1, np2)
	updateCalls := 0
	cs.PrependReactor("update", "networkpolicies", func(ktesting.Action) (bool, runtime.Object, error) {
		updateCalls++
		if updateCalls == 2 {
			return true, nil, errors.New("second policy update denied")
		}
		return false, nil, nil
	})
	store, eng := newK8sTaskEngine(t, cs)
	defer store.Close()
	id := submitPortUpdate(t, eng, "svc-rv")
	waitFor(t, store, id, "failed", 2*time.Second)

	for name, original := range originals {
		updated, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), name, metav1.GetOptions{})
		if err != nil {
			t.Fatal(err)
		}
		if !reflect.DeepEqual(updated.Spec, original.Spec) {
			t.Errorf("policy %s was not restored after a later policy update failed: got=%+v want=%+v", name, updated.Spec, original.Spec)
		}
	}
}

func TestUpdateSvcHandlerDoesNotOverwritePolicyChangedAfterUpdate(t *testing.T) {
	svc := managedTestService("svc-rv")
	np := networkPolicyForService("np1", "ns1", "svc1", "np-uid", "np-rv", 8080)
	cs := fake.NewSimpleClientset(svc, np)
	cs.PrependReactor("update", "networkpolicies", func(a ktesting.Action) (bool, runtime.Object, error) {
		a.(ktesting.UpdateAction).GetObject().(*networkingv1.NetworkPolicy).ResourceVersion = "np-updated-rv"
		return false, nil, nil
	})
	cs.PrependReactor("update", "services", func(ktesting.Action) (bool, runtime.Object, error) {
		replacement := networkPolicyForService("np1", "ns1", "svc1", "np-uid", "np-concurrent-rv", 9999)
		if err := cs.Tracker().Update(networkingv1.SchemeGroupVersion.WithResource("networkpolicies"), replacement, "ns1"); err != nil {
			t.Errorf("install concurrent policy change: %v", err)
		}
		return true, nil, errors.New("service update denied")
	})
	store, eng := newK8sTaskEngine(t, cs)
	defer store.Close()
	id := submitPortUpdate(t, eng, "svc-rv")
	waitFor(t, store, id, "failed", 2*time.Second)

	got, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), "np1", metav1.GetOptions{})
	if err != nil {
		t.Fatal(err)
	}
	if got.ResourceVersion != "np-concurrent-rv" || got.Spec.Ingress[0].Ports[0].Port.IntVal != 9999 {
		t.Fatalf("concurrent policy update was overwritten: %+v", got)
	}
	task, err := store.GetTask(context.Background(), id)
	if err != nil || task.Error == nil || !strings.Contains(*task.Error, "rollback incomplete") {
		t.Fatalf("incomplete rollback must be exposed in task error: task=%+v err=%v", task, err)
	}
}

func TestDeleteNPHandlerUsesSuppliedIdentity(t *testing.T) {
	np := &networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{
		Name: "np1", Namespace: "ns1", UID: "np-current-uid", ResourceVersion: "np-current-rv",
		Labels: map[string]string{"managed-by": "control-panel"},
	}}
	cs := fake.NewSimpleClientset(np)
	store, eng := newK8sTaskEngine(t, cs)
	defer store.Close()
	id := submitK8sTask(t, eng, "k8s_delete_np", map[string]any{
		"namespace": "ns1", "name": "np1", "uid": "old-uid", "resource_version": "np-current-rv",
	})
	waitFor(t, store, id, "failed", 2*time.Second)
	if _, err := cs.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), "np1", metav1.GetOptions{}); err != nil {
		t.Fatalf("replacement policy must survive stale delete request: %v", err)
	}
}

func TestDeleteNPHandlerDeletesWithUIDAndResourceVersionPreconditions(t *testing.T) {
	np := &networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{
		Name: "np1", Namespace: "ns1", UID: "np-uid", ResourceVersion: "np-rv",
		Labels: map[string]string{"managed-by": "control-panel"},
	}}
	cs := fake.NewSimpleClientset(np)
	var gotPreconditions *metav1.Preconditions
	cs.PrependReactor("delete", "networkpolicies", func(a ktesting.Action) (bool, runtime.Object, error) {
		gotPreconditions = a.(ktesting.DeleteAction).GetDeleteOptions().Preconditions
		return false, nil, nil
	})
	store, eng := newK8sTaskEngine(t, cs)
	defer store.Close()
	id := submitK8sTask(t, eng, "k8s_delete_np", map[string]any{
		"namespace": "ns1", "name": "np1", "uid": "np-uid", "resource_version": "np-rv",
	})
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if gotPreconditions == nil || gotPreconditions.UID == nil || *gotPreconditions.UID != "np-uid" || gotPreconditions.ResourceVersion == nil || *gotPreconditions.ResourceVersion != "np-rv" {
		t.Fatalf("NetworkPolicy delete was not pinned to its supplied identity: %+v", gotPreconditions)
	}
}

func newK8sTaskEngine(t *testing.T, client kubernetes.Interface) (*db.Store, *tasks.Engine) {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "k8s-safety.db"))
	if err != nil {
		t.Fatal(err)
	}
	eng := tasks.NewEngine(store)
	RegisterK8sHandlers(eng, client)
	return store, eng
}

func submitK8sTask(t *testing.T, eng *tasks.Engine, taskType string, params map[string]any) int64 {
	t.Helper()
	id, err := eng.Submit(context.Background(), taskType, "k8s", 1, params)
	if err != nil {
		t.Fatal(err)
	}
	return id
}

func submitPortUpdate(t *testing.T, eng *tasks.Engine, resourceVersion string) int64 {
	t.Helper()
	return submitK8sTask(t, eng, "k8s_update_svc", map[string]any{
		"namespace": "ns1", "name": "svc1", "resource_version": resourceVersion,
		"mappings": []map[string]any{{"pod_port": 9000}},
	})
}

func managedTestService(resourceVersion string) *corev1.Service {
	return &corev1.Service{ObjectMeta: metav1.ObjectMeta{
		Name: "svc1", Namespace: "ns1", UID: "svc-uid", ResourceVersion: resourceVersion,
		Labels: map[string]string{"managed-by": "control-panel"},
	}}
}

func networkPolicyForService(name, namespace, serviceName, uid, resourceVersion string, port int32) *networkingv1.NetworkPolicy {
	protocol := corev1.ProtocolTCP
	portValue := intstrFromInt(port)
	return &networkingv1.NetworkPolicy{
		ObjectMeta: metav1.ObjectMeta{
			Name: name, Namespace: namespace, UID: typesUID(uid), ResourceVersion: resourceVersion,
			Labels: map[string]string{"managed-by": "control-panel", "service-name": serviceName},
		},
		Spec: networkingv1.NetworkPolicySpec{
			PodSelector: metav1.LabelSelector{MatchLabels: map[string]string{"app": "pod1"}},
			Ingress: []networkingv1.NetworkPolicyIngressRule{{
				From:  []networkingv1.NetworkPolicyPeer{{PodSelector: &metav1.LabelSelector{MatchLabels: map[string]string{"role": "client"}}}},
				Ports: []networkingv1.NetworkPolicyPort{{Protocol: &protocol, Port: &portValue}},
			}},
			PolicyTypes: []networkingv1.PolicyType{networkingv1.PolicyTypeIngress},
		},
	}
}

func intstrFromInt(port int32) intstr.IntOrString {
	return intstr.FromInt32(port)
}

func TestCreateSvcRollbackUsesIndependentCleanupContextAfterTimeout(t *testing.T) {
	base := fake.NewSimpleClientset(k8sTestPod("pod1", "pod-uid", map[string]string{"app": "pod1"}))
	base.PrependReactor("create", "services", func(a ktesting.Action) (bool, runtime.Object, error) {
		svc := a.(ktesting.CreateAction).GetObject().(*corev1.Service)
		svc.UID = "created-uid"
		svc.ResourceVersion = "created-rv"
		return false, nil, nil
	})
	base.PrependReactor("create", "networkpolicies", func(ktesting.Action) (bool, runtime.Object, error) {
		return true, nil, errors.New("network policy creation failed")
	})
	client := &cleanupContextClient{Interface: base, waitForServiceCreateCancel: true}
	store, eng := newK8sTaskEngine(t, client)
	defer store.Close()
	eng.SetTaskTimeout(time.Second)

	id := submitK8sTask(t, eng, "k8s_create_svc", map[string]any{
		"name": "svc-timeout", "namespace": "ns1", "pod_name": "pod1", "pod_uid": "pod-uid",
		"selector": map[string]string{"app": "pod1"}, "mappings": []map[string]any{{"pod_port": 8080}},
	})
	waitFor(t, store, id, "failed", 3*time.Second)

	client.mu.Lock()
	deleteContextErr := client.serviceDeleteContextErr
	deleteDeadlineRemaining := client.serviceDeleteDeadlineRemaining
	preconditions := client.serviceDeletePreconditions
	client.mu.Unlock()
	if deleteContextErr != nil {
		t.Fatalf("Service rollback reused expired task context: %v", deleteContextErr)
	}
	if deleteDeadlineRemaining <= 9*time.Second || deleteDeadlineRemaining > 10*time.Second {
		t.Fatalf("Service rollback context deadline remaining=%v, want close to 10s", deleteDeadlineRemaining)
	}
	if preconditions == nil || preconditions.UID == nil || *preconditions.UID != "created-uid" || preconditions.ResourceVersion == nil || *preconditions.ResourceVersion != "created-rv" {
		t.Fatalf("Service rollback lost resource identity preconditions: %+v", preconditions)
	}
	if _, err := base.CoreV1().Services("ns1").Get(context.Background(), "svc-timeout", metav1.GetOptions{}); err == nil {
		t.Fatal("created Service should be deleted by rollback")
	}
}

func TestUpdateSvcRollbackUsesIndependentCleanupContextAfterTimeout(t *testing.T) {
	service := managedTestService("svc-rv")
	policy := networkPolicyForService("np-timeout", "ns1", "svc1", "np-uid", "np-rv", 8080)
	originalSpec := policy.Spec.DeepCopy()
	base := fake.NewSimpleClientset(service, policy)
	client := &cleanupContextClient{Interface: base, waitForServiceUpdateCancel: true}
	store, eng := newK8sTaskEngine(t, client)
	defer store.Close()
	eng.SetTaskTimeout(time.Second)

	id := submitPortUpdate(t, eng, "svc-rv")
	waitFor(t, store, id, "failed", 3*time.Second)

	updated, err := base.NetworkingV1().NetworkPolicies("ns1").Get(context.Background(), policy.Name, metav1.GetOptions{})
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(updated.Spec, *originalSpec) {
		t.Fatalf("policy was not restored after task deadline: got=%+v want=%+v", updated.Spec, *originalSpec)
	}
	client.mu.Lock()
	defer client.mu.Unlock()
	if len(client.policyGetContextErrs) < 2 || client.policyGetContextErrs[len(client.policyGetContextErrs)-1] != nil {
		t.Fatalf("policy rollback GET reused expired task context: %+v", client.policyGetContextErrs)
	}
	if len(client.policyGetDeadlineRemaining) < 2 || client.policyGetDeadlineRemaining[len(client.policyGetDeadlineRemaining)-1] <= 9*time.Second || client.policyGetDeadlineRemaining[len(client.policyGetDeadlineRemaining)-1] > 10*time.Second {
		t.Fatalf("policy rollback GET context is not bounded to 10s: %+v", client.policyGetDeadlineRemaining)
	}
	if len(client.policyUpdateContextErrs) < 2 || client.policyUpdateContextErrs[len(client.policyUpdateContextErrs)-1] != nil {
		t.Fatalf("policy rollback UPDATE reused expired task context: %+v", client.policyUpdateContextErrs)
	}
	if len(client.policyUpdateDeadlineRemaining) < 2 || client.policyUpdateDeadlineRemaining[len(client.policyUpdateDeadlineRemaining)-1] <= 9*time.Second || client.policyUpdateDeadlineRemaining[len(client.policyUpdateDeadlineRemaining)-1] > 10*time.Second {
		t.Fatalf("policy rollback UPDATE context is not bounded to 10s: %+v", client.policyUpdateDeadlineRemaining)
	}
}

type cleanupContextClient struct {
	kubernetes.Interface
	mu                             sync.Mutex
	waitForServiceCreateCancel     bool
	waitForServiceUpdateCancel     bool
	serviceDeleteContextErr        error
	serviceDeleteDeadlineRemaining time.Duration
	serviceDeletePreconditions     *metav1.Preconditions
	policyGetContextErrs           []error
	policyGetDeadlineRemaining     []time.Duration
	policyUpdateContextErrs        []error
	policyUpdateDeadlineRemaining  []time.Duration
}

func (c *cleanupContextClient) CoreV1() corev1client.CoreV1Interface {
	return &cleanupContextCoreV1{CoreV1Interface: c.Interface.CoreV1(), owner: c}
}

func (c *cleanupContextClient) NetworkingV1() networkingv1client.NetworkingV1Interface {
	return &cleanupContextNetworkingV1{NetworkingV1Interface: c.Interface.NetworkingV1(), owner: c}
}

type cleanupContextCoreV1 struct {
	corev1client.CoreV1Interface
	owner *cleanupContextClient
}

func (c *cleanupContextCoreV1) Services(namespace string) corev1client.ServiceInterface {
	return &cleanupContextServices{ServiceInterface: c.CoreV1Interface.Services(namespace), owner: c.owner}
}

type cleanupContextServices struct {
	corev1client.ServiceInterface
	owner *cleanupContextClient
}

func (s *cleanupContextServices) Create(ctx context.Context, service *corev1.Service, options metav1.CreateOptions) (*corev1.Service, error) {
	created, err := s.ServiceInterface.Create(ctx, service, options)
	if err == nil && s.owner.waitForServiceCreateCancel {
		<-ctx.Done()
	}
	return created, err
}

func (s *cleanupContextServices) Update(ctx context.Context, service *corev1.Service, options metav1.UpdateOptions) (*corev1.Service, error) {
	if s.owner.waitForServiceUpdateCancel {
		<-ctx.Done()
		return nil, ctx.Err()
	}
	return s.ServiceInterface.Update(ctx, service, options)
}

func (s *cleanupContextServices) Delete(ctx context.Context, name string, options metav1.DeleteOptions) error {
	s.owner.mu.Lock()
	s.owner.serviceDeleteContextErr = ctx.Err()
	s.owner.serviceDeleteDeadlineRemaining = cleanupDeadlineRemaining(ctx)
	s.owner.serviceDeletePreconditions = options.Preconditions
	s.owner.mu.Unlock()
	return s.ServiceInterface.Delete(ctx, name, options)
}

type cleanupContextNetworkingV1 struct {
	networkingv1client.NetworkingV1Interface
	owner *cleanupContextClient
}

func (c *cleanupContextNetworkingV1) NetworkPolicies(namespace string) networkingv1client.NetworkPolicyInterface {
	return &cleanupContextNetworkPolicies{NetworkPolicyInterface: c.NetworkingV1Interface.NetworkPolicies(namespace), owner: c.owner}
}

type cleanupContextNetworkPolicies struct {
	networkingv1client.NetworkPolicyInterface
	owner *cleanupContextClient
}

func (p *cleanupContextNetworkPolicies) Get(ctx context.Context, name string, options metav1.GetOptions) (*networkingv1.NetworkPolicy, error) {
	p.owner.mu.Lock()
	p.owner.policyGetContextErrs = append(p.owner.policyGetContextErrs, ctx.Err())
	p.owner.policyGetDeadlineRemaining = append(p.owner.policyGetDeadlineRemaining, cleanupDeadlineRemaining(ctx))
	p.owner.mu.Unlock()
	return p.NetworkPolicyInterface.Get(ctx, name, options)
}

func (p *cleanupContextNetworkPolicies) Update(ctx context.Context, policy *networkingv1.NetworkPolicy, options metav1.UpdateOptions) (*networkingv1.NetworkPolicy, error) {
	p.owner.mu.Lock()
	p.owner.policyUpdateContextErrs = append(p.owner.policyUpdateContextErrs, ctx.Err())
	p.owner.policyUpdateDeadlineRemaining = append(p.owner.policyUpdateDeadlineRemaining, cleanupDeadlineRemaining(ctx))
	p.owner.mu.Unlock()
	return p.NetworkPolicyInterface.Update(ctx, policy, options)
}

func cleanupDeadlineRemaining(ctx context.Context) time.Duration {
	deadline, ok := ctx.Deadline()
	if !ok {
		return 0
	}
	return time.Until(deadline)
}
