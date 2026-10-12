package api

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync/atomic"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kruntime "k8s.io/apimachinery/pkg/runtime"
	ktypes "k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/kubernetes/fake"
	corev1client "k8s.io/client-go/kubernetes/typed/core/v1"
	clienttesting "k8s.io/client-go/testing"

	"xirang/control_panel/internal/db"
)

const displayWorkerCount = 100

const (
	displayNFSHosts = "nfs-hosts"
	displayPods     = "pods"
	displayServices = "services"
)

type displayEndpoint struct {
	name string
	path string
}

var displayEndpoints = []displayEndpoint{
	{name: displayNFSHosts, path: "/api/v1/storage/nfs-hosts?all=true"},
	{name: displayPods, path: "/api/v1/k8s/pods"},
	{name: displayServices, path: "/api/v1/k8s/services"},
}

type kubernetesDisplayFixture struct {
	router               http.Handler
	store                *db.Store
	token                string
	client               *fake.Clientset
	serviceObserver      *displayServiceConcurrencyObserver
	totalPods            int
	notebookPods         int
	namespaces           int
	servicesPerNamespace int
}

type displayObservedKubernetesClient struct {
	kubernetes.Interface
	observer *displayServiceConcurrencyObserver
}

type displayObservedCoreV1 struct {
	corev1client.CoreV1Interface
	observer *displayServiceConcurrencyObserver
}

type displayObservedServices struct {
	corev1client.ServiceInterface
	observer *displayServiceConcurrencyObserver
}

type displayServiceConcurrencyObserver struct {
	active atomic.Int32
	max    atomic.Int32
	delay  time.Duration
}

func (c *displayObservedKubernetesClient) CoreV1() corev1client.CoreV1Interface {
	return &displayObservedCoreV1{CoreV1Interface: c.Interface.CoreV1(), observer: c.observer}
}

func (c *displayObservedCoreV1) Services(namespace string) corev1client.ServiceInterface {
	return &displayObservedServices{ServiceInterface: c.CoreV1Interface.Services(namespace), observer: c.observer}
}

func (s *displayObservedServices) List(ctx context.Context, options metav1.ListOptions) (*corev1.ServiceList, error) {
	active := s.observer.active.Add(1)
	for {
		observed := s.observer.max.Load()
		if active <= observed || s.observer.max.CompareAndSwap(observed, active) {
			break
		}
	}
	if s.observer.delay > 0 {
		time.Sleep(s.observer.delay)
	}
	defer s.observer.active.Add(-1)
	return s.ServiceInterface.List(ctx, options)
}

// TestKubernetesDisplayListingFixture checks the small benchmark fixture and
// all three authenticated HTTP response paths without timing them.
func TestKubernetesDisplayListingFixture(t *testing.T) {
	fixture := buildKubernetesDisplayFixture(t, 100, 10, true)
	for _, endpoint := range displayEndpoints {
		fixture.client.ClearActions()
		req, recorder := newDisplayRequest(t, fixture, endpoint)
		fixture.router.ServeHTTP(recorder, req)
		if recorder.Code != http.StatusOK {
			t.Fatalf("%s: code=%d body=%s", endpoint.name, recorder.Code, recorder.Body.String())
		}
		assertDisplayResponse(t, fixture, endpoint, recorder.Body.Bytes())
		assertDisplayListActions(t, fixture.client.Actions(), endpoint, fixture.namespaces)
		if endpoint.name == displayServices && fixture.serviceObserver.max.Load() != 8 {
			t.Fatalf("maximum concurrent namespaced Service lists=%d, want 8", fixture.serviceObserver.max.Load())
		}
	}
}

// BenchmarkKubernetesDisplayListing runs each endpoint against the same
// fixture sizes used by the normal integrity test, with unrelated Pods and
// non-NFS PVC/PV pairs present in every scenario.
func BenchmarkKubernetesDisplayListing(b *testing.B) {
	scenarios := []struct {
		pods       int
		namespaces int
	}{
		{pods: 1_000, namespaces: 10},
		{pods: 1_000, namespaces: 100},
		{pods: 10_000, namespaces: 10},
		{pods: 10_000, namespaces: 100},
	}
	for _, scenario := range scenarios {
		name := fmt.Sprintf("pods=%d/namespaces=%d", scenario.pods, scenario.namespaces)
		b.Run(name, func(b *testing.B) {
			b.StopTimer()
			fixture := newKubernetesDisplayFixture(b, scenario.pods, scenario.namespaces)
			for _, endpoint := range displayEndpoints {
				endpoint := endpoint
				b.Run(endpoint.name, func(b *testing.B) {
					benchmarkDisplayEndpoint(b, fixture, endpoint)
				})
			}
		})
	}
}

func benchmarkDisplayEndpoint(b *testing.B, fixture *kubernetesDisplayFixture, endpoint displayEndpoint) {
	b.ReportAllocs()
	b.ResetTimer()
	responseBytes := 0
	listCalls := 0
	for i := 0; i < b.N; i++ {
		// Keep request construction, fake action cleanup, response decoding,
		// assertions, and action counting out of the timed interval.
		b.StopTimer()
		fixture.client.ClearActions()
		req, recorder := newDisplayRequest(b, fixture, endpoint)
		b.StartTimer()
		fixture.router.ServeHTTP(recorder, req)
		b.StopTimer()
		if recorder.Code != http.StatusOK {
			b.Fatalf("%s: code=%d body=%s", endpoint.name, recorder.Code, recorder.Body.String())
		}
		response := recorder.Body.Bytes()
		assertDisplayResponse(b, fixture, endpoint, response)
		listCalls = assertDisplayListActions(b, fixture.client.Actions(), endpoint, fixture.namespaces)
		responseBytes = len(response)
	}
	b.ReportMetric(float64(responseBytes), "response-bytes/op")
	b.ReportMetric(float64(listCalls), "api-list-calls/op")
}

func newKubernetesDisplayFixture(tb testing.TB, totalPods, namespaceCount int) *kubernetesDisplayFixture {
	return buildKubernetesDisplayFixture(tb, totalPods, namespaceCount, false)
}

func buildKubernetesDisplayFixture(tb testing.TB, totalPods, namespaceCount int, observeServiceConcurrency bool) *kubernetesDisplayFixture {
	tb.Helper()
	if totalPods < 2 || totalPods%2 != 0 || namespaceCount < 1 || (totalPods/2)%namespaceCount != 0 {
		tb.Fatalf("fixture requires an even Pod count split evenly across namespaces: pods=%d namespaces=%d", totalPods, namespaceCount)
	}

	fakeClient := fake.NewSimpleClientset()
	var apiClient kubernetes.Interface = fakeClient
	var serviceObserver *displayServiceConcurrencyObserver
	if observeServiceConcurrency {
		serviceObserver = &displayServiceConcurrencyObserver{delay: 10 * time.Millisecond}
		apiClient = &displayObservedKubernetesClient{Interface: fakeClient, observer: serviceObserver}
	}
	router, store, tokens, _ := newRouterWithK8sClient(tb, apiClient)
	authorizationToken, err := tokens.Issue(1, "admin", 2)
	if err != nil {
		tb.Fatalf("issue fixture authorization token: %v", err)
	}
	fixture := &kubernetesDisplayFixture{
		router:               router,
		store:                store,
		token:                "Bearer " + authorizationToken,
		client:               fakeClient,
		serviceObserver:      serviceObserver,
		totalPods:            totalPods,
		notebookPods:         totalPods / 2,
		namespaces:           namespaceCount,
		servicesPerNamespace: 10,
	}

	ctx := context.Background()
	now := time.Now().UTC()
	inventoryPayload := `{"nfs":{"active":true,"exports":["/data02/share"]},"lvs":[{"name":"lv_nb","vg_name":"vg_data","size_gb":50,"size_known":true,"mount_point":"/data02/share","is_nfs_export":true}]}`
	for i := 1; i <= displayWorkerCount; i++ {
		workerID, err := store.CreateWorker(ctx, db.WorkerNode{
			Name: fmt.Sprintf("worker-%d", i), Host: fmt.Sprintf("10.0.0.%d", i), Port: 22, Username: "root",
		})
		if err != nil {
			tb.Fatalf("create fixture worker %d: %v", i, err)
		}
		if err := store.SaveInventorySnapshot(ctx, db.InventorySnapshot{
			WorkerID: workerID, SchemaVersion: 1, PayloadJSON: inventoryPayload,
			CollectedAt: &now, LastAttemptedAt: now,
		}); err != nil {
			tb.Fatalf("save fixture inventory %d: %v", i, err)
		}
	}

	tracker := fakeClient.Tracker()
	for i := 0; i < totalPods; i++ {
		isNotebook := i < fixture.notebookPods
		classIndex := i
		class := "ordinary"
		podName := fmt.Sprintf("ordinary-%05d", i-fixture.notebookPods)
		if isNotebook {
			class, podName = "notebook", fmt.Sprintf("notebook-%05d", i)
		} else {
			classIndex -= fixture.notebookPods
		}
		namespace := fmt.Sprintf("ns-%03d", classIndex%namespaceCount)
		claimName := fmt.Sprintf("claim-%05d", i)
		pvName := fmt.Sprintf("pv-%05d", i)
		podUID := ktypes.UID(fmt.Sprintf("pod-uid-%05d", i))
		pvcUID := ktypes.UID(fmt.Sprintf("pvc-uid-%05d", i))
		pod := &corev1.Pod{
			ObjectMeta: metav1.ObjectMeta{
				Name: podName, Namespace: namespace, UID: podUID,
				Labels: map[string]string{"display-class": class, "service-group": "shared"},
			},
			Spec: corev1.PodSpec{
				Volumes: []corev1.Volume{{Name: "workspace", VolumeSource: corev1.VolumeSource{
					PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: claimName},
				}}},
				Containers: []corev1.Container{{Name: "main", VolumeMounts: []corev1.VolumeMount{{Name: "workspace", MountPath: "/workspace"}}}},
			},
		}
		pvc := &corev1.PersistentVolumeClaim{
			ObjectMeta: metav1.ObjectMeta{Name: claimName, Namespace: namespace, UID: pvcUID},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: pvName},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		}
		pv := &corev1.PersistentVolume{
			ObjectMeta: metav1.ObjectMeta{Name: pvName, UID: ktypes.UID(fmt.Sprintf("pv-uid-%05d", i))},
			Spec: corev1.PersistentVolumeSpec{
				ClaimRef: &corev1.ObjectReference{APIVersion: "v1", Kind: "PersistentVolumeClaim", Namespace: namespace, Name: claimName, UID: pvcUID},
			},
		}
		if isNotebook {
			pv.Spec.PersistentVolumeSource.NFS = &corev1.NFSVolumeSource{
				Server: "10.0.0.1", Path: fmt.Sprintf("/data02/share/tenant-%05d", i),
			}
		} else {
			pv.Spec.PersistentVolumeSource.HostPath = &corev1.HostPathVolumeSource{Path: fmt.Sprintf("/fixture/non-nfs/%05d", i)}
		}
		for _, object := range []kruntime.Object{pod, pvc, pv} {
			if err := tracker.Add(object); err != nil {
				tb.Fatalf("seed fixture object %s: %v", object.GetObjectKind().GroupVersionKind().Kind, err)
			}
		}
	}

	for nsIndex := 0; nsIndex < namespaceCount; nsIndex++ {
		namespace := fmt.Sprintf("ns-%03d", nsIndex)
		for serviceIndex := 0; serviceIndex < fixture.servicesPerNamespace; serviceIndex++ {
			service := displayFixtureService(namespace, serviceIndex)
			if err := tracker.Add(service); err != nil {
				tb.Fatalf("seed fixture service %s/%s: %v", namespace, service.Name, err)
			}
		}
	}
	return fixture
}

func displayFixtureService(namespace string, index int) *corev1.Service {
	names := []string{
		"fixture-managed-notebook",
		"fixture-external-nodeport-notebook",
		"fixture-external-nodeport-ordinary",
		"fixture-external-nodeport-no-match",
		"fixture-external-clusterip-notebook",
		"fixture-external-loadbalancer-notebook",
		"fixture-external-nodeport-mixed",
		"fixture-external-clusterip-ordinary",
		"fixture-external-nodeport-notebook-2",
		"fixture-external-nodeport-no-match-2",
	}
	classSelector := func(class string) map[string]string {
		return map[string]string{"display-class": class}
	}
	service := &corev1.Service{
		ObjectMeta: metav1.ObjectMeta{Name: names[index], Namespace: namespace},
		Spec:       corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort},
	}
	switch index {
	case 0:
		service.Labels = map[string]string{"managed-by": "control-panel"}
		service.Spec.Type = corev1.ServiceTypeClusterIP
		service.Spec.Selector = classSelector("notebook")
	case 1, 8:
		service.Spec.Selector = classSelector("notebook")
	case 2:
		service.Spec.Selector = classSelector("ordinary")
	case 3, 9:
		service.Spec.Selector = classSelector("no-match")
	case 4:
		service.Spec.Type = corev1.ServiceTypeClusterIP
		service.Spec.Selector = classSelector("notebook")
	case 5:
		service.Spec.Type = corev1.ServiceTypeLoadBalancer
		service.Spec.Selector = classSelector("notebook")
	case 6:
		service.Spec.Selector = map[string]string{"service-group": "shared"}
	case 7:
		service.Spec.Type = corev1.ServiceTypeClusterIP
		service.Spec.Selector = classSelector("ordinary")
	}
	return service
}

func newDisplayRequest(tb testing.TB, fixture *kubernetesDisplayFixture, endpoint displayEndpoint) (*http.Request, *httptest.ResponseRecorder) {
	tb.Helper()
	req := httptest.NewRequest(http.MethodGet, endpoint.path, nil)
	req.Header.Set("Authorization", fixture.token)
	return req, httptest.NewRecorder()
}

func assertDisplayResponse(tb testing.TB, fixture *kubernetesDisplayFixture, endpoint displayEndpoint, body []byte) {
	tb.Helper()
	switch endpoint.name {
	case displayNFSHosts:
		var hosts []map[string]any
		if err := json.Unmarshal(body, &hosts); err != nil {
			tb.Fatalf("decode NFS hosts response: %v", err)
		}
		if len(hosts) != displayWorkerCount {
			tb.Fatalf("NFS hosts count=%d, want %d", len(hosts), displayWorkerCount)
		}
		var matchedHost map[string]any
		for _, host := range hosts {
			if host["host"] == "10.0.0.1" {
				matchedHost = host
				break
			}
		}
		if matchedHost == nil {
			tb.Fatal("NFS hosts response omitted matching worker 10.0.0.1")
		}
		disks, ok := matchedHost["virtual_disks"].([]any)
		if !ok {
			tb.Fatalf("matching worker virtual_disks has type %T", matchedHost["virtual_disks"])
		}
		var mountedPods []any
		for _, rawDisk := range disks {
			disk, ok := rawDisk.(map[string]any)
			if ok && disk["name"] == "lv_nb" {
				mountedPods, ok = disk["mounted_pods"].([]any)
				if !ok {
					tb.Fatalf("lv_nb mounted_pods has type %T", disk["mounted_pods"])
				}
				break
			}
		}
		if len(mountedPods) != fixture.notebookPods {
			tb.Fatalf("matched LV mounted_pods=%d, want %d", len(mountedPods), fixture.notebookPods)
		}
		for _, rawPod := range mountedPods {
			pod, ok := rawPod.(map[string]any)
			if !ok || !strings.Contains(fmt.Sprint(pod["pod_name"]), "notebook") {
				tb.Fatalf("NFS association exposed a non-notebook Pod: %#v", rawPod)
			}
		}
	case displayPods:
		var pods []map[string]any
		if err := json.Unmarshal(body, &pods); err != nil {
			tb.Fatalf("decode Pods response: %v", err)
		}
		if len(pods) != fixture.notebookPods {
			tb.Fatalf("notebook Pod response count=%d, want %d", len(pods), fixture.notebookPods)
		}
		for _, pod := range pods {
			if !strings.Contains(fmt.Sprint(pod["name"]), "notebook") {
				tb.Fatalf("Pods response exposed ordinary Pod: %#v", pod["name"])
			}
			mounts, ok := pod["nfs_mounts"].([]any)
			if !ok || len(mounts) != 1 {
				tb.Fatalf("Pod %v mounts=%v, want one NFS mount", pod["name"], pod["nfs_mounts"])
			}
			mount, ok := mounts[0].(map[string]any)
			if !ok || mount["status"] != "matched" {
				tb.Fatalf("Pod %v mount=%v, want matched", pod["name"], mounts[0])
			}
		}
	case displayServices:
		var services []map[string]any
		if err := json.Unmarshal(body, &services); err != nil {
			tb.Fatalf("decode Services response: %v", err)
		}
		wantServices := fixture.namespaces * fixture.servicesPerNamespace
		if len(services) != wantServices {
			tb.Fatalf("Service response count=%d, want %d", len(services), wantServices)
		}
		byKey := make(map[string]map[string]any, len(services))
		for _, service := range services {
			key := fmt.Sprint(service["namespace"]) + "/" + fmt.Sprint(service["name"])
			byKey[key] = service
			if rawRefs, exists := service["pods"]; exists && rawRefs != nil {
				refs, ok := rawRefs.([]any)
				if !ok {
					tb.Fatalf("Service %s pods has type %T", key, rawRefs)
				}
				for _, rawRef := range refs {
					ref, ok := rawRef.(map[string]any)
					if !ok || !strings.Contains(fmt.Sprint(ref["name"]), "notebook") {
						tb.Fatalf("Service %s exposed an ordinary Pod: %#v", key, rawRef)
					}
				}
			}
		}
		wantFlags := map[string]struct {
			managed   bool
			deletable bool
			podCount  int
		}{
			"fixture-managed-notebook":               {managed: true, deletable: true, podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-nodeport-notebook":     {deletable: true, podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-nodeport-ordinary":     {},
			"fixture-external-nodeport-no-match":     {},
			"fixture-external-clusterip-notebook":    {podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-loadbalancer-notebook": {podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-nodeport-mixed":        {podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-clusterip-ordinary":    {},
			"fixture-external-nodeport-notebook-2":   {deletable: true, podCount: fixture.notebookPods / fixture.namespaces},
			"fixture-external-nodeport-no-match-2":   {},
		}
		for nsIndex := 0; nsIndex < fixture.namespaces; nsIndex++ {
			namespace := fmt.Sprintf("ns-%03d", nsIndex)
			for name, want := range wantFlags {
				service, ok := byKey[namespace+"/"+name]
				if !ok {
					tb.Fatalf("Services response omitted %s/%s", namespace, name)
				}
				if service["managed"] != want.managed || service["deletable"] != want.deletable {
					tb.Fatalf("Service %s/%s flags managed=%v deletable=%v, want %v/%v", namespace, name, service["managed"], service["deletable"], want.managed, want.deletable)
				}
				podCount := 0
				if rawRefs := service["pods"]; rawRefs != nil {
					refs, ok := rawRefs.([]any)
					if !ok {
						tb.Fatalf("Service %s/%s pods has type %T", namespace, name, rawRefs)
					}
					podCount = len(refs)
				}
				if podCount != want.podCount {
					tb.Fatalf("Service %s/%s notebook Pod refs=%d, want %d", namespace, name, podCount, want.podCount)
				}
			}
		}
	default:
		tb.Fatalf("unknown display endpoint %q", endpoint.name)
	}
}

func assertDisplayListActions(tb testing.TB, actions []clienttesting.Action, endpoint displayEndpoint, namespaceCount int) int {
	tb.Helper()
	actual := make(map[string]int)
	total := 0
	for _, action := range actions {
		if action.GetVerb() != "list" {
			continue
		}
		key := action.GetResource().Resource + "\x00" + action.GetNamespace()
		actual[key]++
		total++
	}
	expected := make(map[string]int)
	switch endpoint.name {
	case displayNFSHosts, displayPods:
		expected["pods\x00"] = 1
		expected["persistentvolumeclaims\x00"] = 1
		expected["persistentvolumes\x00"] = 1
	case displayServices:
		expected["pods\x00"] = 1
		for nsIndex := 0; nsIndex < namespaceCount; nsIndex++ {
			expected["services\x00"+fmt.Sprintf("ns-%03d", nsIndex)] = 1
		}
	default:
		tb.Fatalf("unknown display endpoint %q", endpoint.name)
	}
	for key, want := range expected {
		if got := actual[key]; got != want {
			tb.Errorf("%s list action %q=%d, want %d (all=%v)", endpoint.name, key, got, want, actual)
		}
	}
	for key, got := range actual {
		if expected[key] != got {
			tb.Errorf("%s unexpected list action %q=%d (expected=%v)", endpoint.name, key, got, expected)
		}
	}
	if total != len(expected) {
		tb.Errorf("%s list action total=%d, want %d", endpoint.name, total, len(expected))
	}
	return total
}
