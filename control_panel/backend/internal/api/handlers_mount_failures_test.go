package api

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"strconv"
	"strings"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kruntime "k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/fake"
	k8stesting "k8s.io/client-go/testing"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
)

func TestPVCListFailurePreservesPodAndStorageData(t *testing.T) {
	router, store, tokens, client := newRouterWithK8s(t)
	ctx := context.Background()
	workerID, err := store.CreateWorker(ctx, db.WorkerNode{
		Name: "worker-a", Host: "worker-a", Port: 22, Username: "root",
	})
	if err != nil {
		t.Fatal(err)
	}
	collectedAt := time.Now().UTC()
	payload := `{"nfs":{"active":true,"exports":["/exports/notebook"]},"lvs":[{"name":"lv-notebook","vg_name":"vg_data","size_gb":100,"mount_point":"/exports/notebook","is_nfs_export":true}]}`
	if err := store.SaveInventorySnapshot(ctx, db.InventorySnapshot{
		WorkerID: workerID, SchemaVersion: 1, PayloadJSON: payload,
		CollectedAt: &collectedAt, LastAttemptedAt: collectedAt,
	}); err != nil {
		t.Fatal(err)
	}
	pod := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns1", UID: "pod-a"},
		Spec: corev1.PodSpec{Volumes: []corev1.Volume{{Name: "workspace", VolumeSource: corev1.VolumeSource{
			PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "workspace-data"},
		}}}},
	}
	if _, err := client.CoreV1().Pods("ns1").Create(ctx, pod, metav1.CreateOptions{}); err != nil {
		t.Fatal(err)
	}
	stableKey, keyKind, workspaceID, projectID := k8s.StableKeyForPod("ns1", "pod-a", nil)
	if err := store.UpsertNotebookMetadata(ctx, db.NotebookMetadata{
		StableKey: stableKey, KeyKind: keyKind, Namespace: "ns1", WorkspaceID: workspaceID,
		ProjectID: projectID, LastPodUID: "pod-a", OwnerName: "Alice", Note: "retained note", UpdatedBy: "admin",
	}); err != nil {
		t.Fatal(err)
	}
	fakeClient, ok := client.(*fake.Clientset)
	if !ok {
		t.Fatal("expected the test router to use a fake Kubernetes client")
	}
	fakeClient.PrependReactor("list", "persistentvolumeclaims", func(k8stesting.Action) (bool, kruntime.Object, error) {
		return true, nil, errors.New("sensitive test error text")
	})

	podsReq := httptest.NewRequest("GET", "/api/v1/k8s/pods", nil)
	podsReq.Header.Set("Authorization", authHeader(t, tokens))
	podsResp := httptest.NewRecorder()
	router.ServeHTTP(podsResp, podsReq)
	if podsResp.Code != http.StatusOK {
		t.Fatalf("pods response code=%d body=%s", podsResp.Code, podsResp.Body.String())
	}
	var pods []map[string]any
	if err := json.Unmarshal(podsResp.Body.Bytes(), &pods); err != nil {
		t.Fatal(err)
	}
	if len(pods) != 1 || pods[0]["owner_name"] != "Alice" || pods[0]["note"] != "retained note" ||
		pods[0]["nfs_mounts_status"] != "lookup_failed" || pods[0]["nfs_mounts_error"] != "pvc_list_failed" ||
		len(pods[0]["nfs_mounts"].([]any)) != 0 {
		t.Fatalf("PVC lookup failure should preserve the Pod and metadata without fabricating claims: %s", podsResp.Body.String())
	}
	if strings.Contains(podsResp.Body.String(), "sensitive test error text") {
		t.Fatalf("raw Kubernetes error text leaked: %s", podsResp.Body.String())
	}

	hostsReq := httptest.NewRequest("GET", "/api/v1/storage/nfs-hosts", nil)
	hostsReq.Header.Set("Authorization", authHeader(t, tokens))
	hostsResp := httptest.NewRecorder()
	router.ServeHTTP(hostsResp, hostsReq)
	if hostsResp.Code != http.StatusOK {
		t.Fatalf("nfs-hosts response code=%d body=%s", hostsResp.Code, hostsResp.Body.String())
	}
	var hosts []map[string]any
	if err := json.Unmarshal(hostsResp.Body.Bytes(), &hosts); err != nil {
		t.Fatal(err)
	}
	if len(hosts) != 1 || hosts[0]["mount_association_status"] != "lookup_failed" ||
		hosts[0]["mount_association_error"] != "pvc_list_failed" || len(hosts[0]["unmatched_mounts"].([]any)) != 0 {
		t.Fatalf("storage overview must mark the failed lookup, not report no mounts: %s", hostsResp.Body.String())
	}
	hostLVs := hosts[0]["virtual_disks"].([]any)
	if len(hostLVs) != 1 || len(hostLVs[0].(map[string]any)["mounted_pods"].([]any)) != 0 {
		t.Fatalf("storage snapshot should remain available with empty association arrays: %s", hostsResp.Body.String())
	}

	inventoryReq := httptest.NewRequest("GET", "/api/v1/storage/inventory?worker_id="+strconv.FormatInt(workerID, 10), nil)
	inventoryReq.Header.Set("Authorization", authHeader(t, tokens))
	inventoryResp := httptest.NewRecorder()
	router.ServeHTTP(inventoryResp, inventoryReq)
	if inventoryResp.Code != http.StatusOK {
		t.Fatalf("inventory response code=%d body=%s", inventoryResp.Code, inventoryResp.Body.String())
	}
	var inventory map[string]any
	if err := json.Unmarshal(inventoryResp.Body.Bytes(), &inventory); err != nil {
		t.Fatal(err)
	}
	if inventory["mount_association_status"] != "lookup_failed" || inventory["mount_association_error"] != "pvc_list_failed" ||
		len(inventory["lvs"].([]any)) != 1 || len(inventory["unmatched_mounts"].([]any)) != 0 {
		t.Fatalf("worker inventory must retain its LV and expose lookup failure: %s", inventoryResp.Body.String())
	}
	data := inventory["data"].(map[string]any)
	if data["mount_association_status"] != "lookup_failed" || len(data["lvs"].([]any)[0].(map[string]any)["mounted_pods"].([]any)) != 0 {
		t.Fatalf("nested inventory must carry the same association state: %+v", data)
	}
}

func TestPodListFailureUsesExistingErrorResponseOnK8sPods(t *testing.T) {
	router, _, tokens, client := newRouterWithK8s(t)
	fakeClient, ok := client.(*fake.Clientset)
	if !ok {
		t.Fatal("expected the test router to use a fake Kubernetes client")
	}
	fakeClient.PrependReactor("list", "pods", func(k8stesting.Action) (bool, kruntime.Object, error) {
		return true, nil, errors.New("private Pod list details")
	})
	req := httptest.NewRequest("GET", "/api/v1/k8s/pods", nil)
	req.Header.Set("Authorization", authHeader(t, tokens))
	resp := httptest.NewRecorder()
	router.ServeHTTP(resp, req)
	if resp.Code != http.StatusInternalServerError || strings.Contains(resp.Body.String(), "private Pod list details") {
		t.Fatalf("Pod list failure should remain an error without leaking API details: code=%d body=%s", resp.Code, resp.Body.String())
	}
	var body map[string]any
	if err := json.Unmarshal(resp.Body.Bytes(), &body); err != nil || body["error"] != "pod_list_failed" {
		t.Fatalf("Pod list failure should return its safe category code: %s", resp.Body.String())
	}
}
