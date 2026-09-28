package api

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	kruntime "k8s.io/apimachinery/pkg/runtime"
	ktypes "k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/kubernetes/fake"

	"xirang/control_panel/internal/db"
)

func TestListNFSHosts100WorkersAnd1000NotebookMountsUnderOneSecond(t *testing.T) {
	router, store, tokens, client := newRouterWithK8s(t)
	fakeClient, ok := client.(*fake.Clientset)
	if !ok {
		t.Fatal("expected the test router to use a fake Kubernetes client")
	}
	tracker := fakeClient.Tracker()
	ctx := context.Background()
	now := time.Now().UTC()
	payload := `{"nfs":{"active":true,"exports":["/data02/share"]},"lvs":[{"name":"lv_nb","vg_name":"vg_data","size_gb":50,"size_known":true,"mount_point":"/data02/share","is_nfs_export":true}]}`
	for i := 1; i <= 100; i++ {
		workerID, err := store.CreateWorker(ctx, db.WorkerNode{
			Name: fmt.Sprintf("worker-%d", i), Host: fmt.Sprintf("10.0.0.%d", i), Port: 22, Username: "root",
		})
		if err != nil {
			t.Fatal(err)
		}
		if err := store.SaveInventorySnapshot(ctx, db.InventorySnapshot{
			WorkerID: workerID, SchemaVersion: 1, PayloadJSON: payload,
			CollectedAt: &now, LastAttemptedAt: now,
		}); err != nil {
			t.Fatal(err)
		}
	}

	for i := 1; i <= 1000; i++ {
		podName := fmt.Sprintf("notebook-%04d", i)
		claimName := fmt.Sprintf("claim-%04d", i)
		pvName := fmt.Sprintf("pv-%04d", i)
		objects := []kruntime.Object{
			&corev1.Pod{
				ObjectMeta: metav1.ObjectMeta{Name: podName, Namespace: "ns1", UID: ktypes.UID(fmt.Sprintf("pod-uid-%04d", i))},
				Spec: corev1.PodSpec{Volumes: []corev1.Volume{{Name: "workspace", VolumeSource: corev1.VolumeSource{
					PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: claimName},
				}}}},
			},
			&corev1.PersistentVolumeClaim{
				ObjectMeta: metav1.ObjectMeta{Name: claimName, Namespace: "ns1"},
				Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: pvName},
				Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
			},
			&corev1.PersistentVolume{
				ObjectMeta: metav1.ObjectMeta{Name: pvName},
				Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
					NFS: &corev1.NFSVolumeSource{Server: "10.0.0.1", Path: fmt.Sprintf("/data02/share/tenant-%04d", i)},
				}},
			},
		}
		for _, object := range objects {
			if err := tracker.Add(object); err != nil {
				t.Fatalf("seed fixture %d: %v", i, err)
			}
		}
	}

	start := time.Now()
	req := httptest.NewRequest("GET", "/api/v1/storage/nfs-hosts?all=true", nil)
	req.Header.Set("Authorization", authHeader(t, tokens))
	resp := httptest.NewRecorder()
	router.ServeHTTP(resp, req)
	elapsed := time.Since(start)
	if resp.Code != http.StatusOK {
		t.Fatalf("code=%d body=%s", resp.Code, resp.Body.String())
	}
	var hosts []map[string]any
	if err := json.Unmarshal(resp.Body.Bytes(), &hosts); err != nil {
		t.Fatal(err)
	}
	if len(hosts) != 100 {
		t.Fatalf("expected 100 workers, got %d", len(hosts))
	}
	mounted := hosts[0]["virtual_disks"].([]any)[0].(map[string]any)["mounted_pods"].([]any)
	if len(mounted) != 1000 {
		t.Fatalf("expected the matched LV to include 1000 Notebook Pods, got %d", len(mounted))
	}
	if elapsed >= time.Second {
		t.Fatalf("100 workers and 1000 mounts took %v, want < 1s", elapsed)
	}

	listCounts := map[string]int{}
	for _, action := range fakeClient.Actions() {
		if action.GetVerb() == "list" {
			listCounts[action.GetResource().Resource]++
		}
	}
	for resource, want := range map[string]int{"pods": 1, "persistentvolumeclaims": 1, "persistentvolumes": 1} {
		if listCounts[resource] != want {
			t.Errorf("%s list calls=%d, want %d regardless of Pod/PVC count", resource, listCounts[resource], want)
		}
	}
}
