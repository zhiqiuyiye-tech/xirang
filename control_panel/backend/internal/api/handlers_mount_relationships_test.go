package api

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
)

func TestNFSAPIShowsManyToManyPodAndVolumeRelations(t *testing.T) {
	router, store, tokens, client := newRouterWithK8s(t)
	ctx := context.Background()
	workerID, err := store.CreateWorker(ctx, db.WorkerNode{
		Name: "worker-a", Host: "10.0.0.1", Port: 22, Username: "root",
	})
	if err != nil {
		t.Fatal(err)
	}
	collectedAt := time.Now().UTC()
	payload := `{"nfs":{"active":true,"exports":["/nfs/one","/nfs/two"]},"lvs":[{"name":"lv-one","vg_name":"vg_data","size_gb":100,"mount_point":"/nfs/one","is_nfs_export":true},{"name":"lv-two","vg_name":"vg_data","size_gb":200,"mount_point":"/nfs/two","is_nfs_export":true}]}`
	if err := store.SaveInventorySnapshot(ctx, db.InventorySnapshot{
		WorkerID: workerID, SchemaVersion: 1, PayloadJSON: payload,
		CollectedAt: &collectedAt, LastAttemptedAt: collectedAt,
	}); err != nil {
		t.Fatal(err)
	}

	podOne := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-multi", Namespace: "ns1", UID: "uid-one"},
		Spec: corev1.PodSpec{
			Volumes: []corev1.Volume{
				{Name: "one", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "claim-one"}}},
				{Name: "two", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "claim-two"}}},
			},
			Containers: []corev1.Container{{Name: "notebook", VolumeMounts: []corev1.VolumeMount{
				{Name: "one", MountPath: "/workspace/one"},
				{Name: "two", MountPath: "/workspace/two", ReadOnly: true},
			}}},
			InitContainers: []corev1.Container{{Name: "init", VolumeMounts: []corev1.VolumeMount{{Name: "one", MountPath: "/init/one"}}}},
		},
	}
	podTwo := &corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-shared", Namespace: "ns1", UID: "uid-two"},
		Spec: corev1.PodSpec{
			Volumes: []corev1.Volume{{Name: "shared", VolumeSource: corev1.VolumeSource{
				PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "claim-one"},
			}}},
			Containers: []corev1.Container{{Name: "notebook", VolumeMounts: []corev1.VolumeMount{{Name: "shared", MountPath: "/shared"}}}},
		},
	}
	for _, pod := range []*corev1.Pod{podOne, podTwo} {
		if _, err := client.CoreV1().Pods("ns1").Create(ctx, pod, metav1.CreateOptions{}); err != nil {
			t.Fatal(err)
		}
	}
	claims := []corev1.PersistentVolumeClaim{
		{ObjectMeta: metav1.ObjectMeta{Name: "claim-one", Namespace: "ns1"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "pv-one"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
		{ObjectMeta: metav1.ObjectMeta{Name: "claim-two", Namespace: "ns1"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "pv-two"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
	}
	for i := range claims {
		if _, err := client.CoreV1().PersistentVolumeClaims("ns1").Create(ctx, &claims[i], metav1.CreateOptions{}); err != nil {
			t.Fatal(err)
		}
	}
	pvs := []corev1.PersistentVolume{
		{ObjectMeta: metav1.ObjectMeta{Name: "pv-one"}, Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.1", Path: "/nfs/one/notebook"}}}},
		{ObjectMeta: metav1.ObjectMeta{Name: "pv-two"}, Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.1", Path: "/nfs/two/notebook"}}}},
	}
	for i := range pvs {
		if _, err := client.CoreV1().PersistentVolumes().Create(ctx, &pvs[i], metav1.CreateOptions{}); err != nil {
			t.Fatal(err)
		}
	}
	for _, pod := range []*corev1.Pod{podOne, podTwo} {
		stableKey, keyKind, workspaceID, projectID := k8s.StableKeyForPod(pod.Namespace, string(pod.UID), nil)
		if err := store.UpsertNotebookMetadata(ctx, db.NotebookMetadata{
			StableKey: stableKey, KeyKind: keyKind, Namespace: pod.Namespace, WorkspaceID: workspaceID,
			ProjectID: projectID, LastPodUID: string(pod.UID), OwnerName: pod.Name, Note: "allocation note", UpdatedBy: "admin",
		}); err != nil {
			t.Fatal(err)
		}
	}

	podsReq := httptest.NewRequest("GET", "/api/v1/k8s/pods", nil)
	podsReq.Header.Set("Authorization", authHeader(t, tokens))
	podsResp := httptest.NewRecorder()
	router.ServeHTTP(podsResp, podsReq)
	if podsResp.Code != http.StatusOK {
		t.Fatalf("pods code=%d body=%s", podsResp.Code, podsResp.Body.String())
	}
	var podResponses []map[string]any
	if err := json.Unmarshal(podsResp.Body.Bytes(), &podResponses); err != nil {
		t.Fatal(err)
	}
	if len(podResponses) != 2 {
		t.Fatalf("expected 2 Notebook Pods, got %s", podsResp.Body.String())
	}
	podMountCounts := map[string]int{}
	for _, pod := range podResponses {
		podMountCounts[pod["name"].(string)] = len(pod["nfs_mounts"].([]any))
	}
	if podMountCounts["notebook-multi"] != 2 || podMountCounts["notebook-shared"] != 1 {
		t.Fatalf("one Pod should use two volumes and another should share one: %v", podMountCounts)
	}

	hostReq := httptest.NewRequest("GET", "/api/v1/storage/nfs-hosts", nil)
	hostReq.Header.Set("Authorization", authHeader(t, tokens))
	hostResp := httptest.NewRecorder()
	router.ServeHTTP(hostResp, hostReq)
	if hostResp.Code != http.StatusOK {
		t.Fatalf("nfs-hosts code=%d body=%s", hostResp.Code, hostResp.Body.String())
	}
	var hosts []map[string]any
	if err := json.Unmarshal(hostResp.Body.Bytes(), &hosts); err != nil {
		t.Fatal(err)
	}
	if len(hosts) != 1 || hosts[0]["mount_association_status"] != "available" {
		t.Fatalf("expected one fully associated Worker: %s", hostResp.Body.String())
	}
	lvPods := map[string][]map[string]any{}
	for _, raw := range hosts[0]["virtual_disks"].([]any) {
		lv := raw.(map[string]any)
		name := lv["name"].(string)
		for _, pod := range lv["mounted_pods"].([]any) {
			lvPods[name] = append(lvPods[name], pod.(map[string]any))
		}
	}
	if len(lvPods["lv-one"]) != 2 || len(lvPods["lv-two"]) != 1 {
		t.Fatalf("shared and per-Pod LV reverse relations are incomplete: %+v", lvPods)
	}
	if lvPods["lv-one"][0]["owner_name"] == "" || lvPods["lv-one"][0]["note"] != "allocation note" {
		t.Fatalf("owner and note metadata should appear on the virtual disk: %+v", lvPods["lv-one"])
	}
}
