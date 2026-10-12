package api

import (
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func TestIndexReferencedClaimsAndVolumesKeepsOnlySelectedPodReferences(t *testing.T) {
	pods := []corev1.Pod{
		{ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns-a"}, Spec: corev1.PodSpec{Volumes: []corev1.Volume{
			{Name: "one", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "shared"}}},
			{Name: "same-claim", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "shared"}}},
			{Name: "pending", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "pending"}}},
			{Name: "absent", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "absent"}}},
		}}},
		{ObjectMeta: metav1.ObjectMeta{Name: "notebook-b", Namespace: "ns-b"}, Spec: corev1.PodSpec{Volumes: []corev1.Volume{
			{Name: "different-ns", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "shared"}}},
		}}},
	}
	claims := []corev1.PersistentVolumeClaim{
		{ObjectMeta: metav1.ObjectMeta{Name: "shared", Namespace: "ns-a"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "pv-a"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
		{ObjectMeta: metav1.ObjectMeta{Name: "shared", Namespace: "ns-b"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "missing-pv"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
		{ObjectMeta: metav1.ObjectMeta{Name: "pending", Namespace: "ns-a"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "not-yet-bound"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimPending}},
		{ObjectMeta: metav1.ObjectMeta{Name: "unrelated", Namespace: "ns-a"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "other-pv"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
		{ObjectMeta: metav1.ObjectMeta{Name: "shared", Namespace: "unrelated"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: "other-pv"}, Status: corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound}},
	}
	volumes := []corev1.PersistentVolume{
		{ObjectMeta: metav1.ObjectMeta{Name: "pv-a"}, Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.1", Path: "/data/share"}}}},
		{ObjectMeta: metav1.ObjectMeta{Name: "other-pv"}},
		{ObjectMeta: metav1.ObjectMeta{Name: "not-yet-bound"}},
	}
	indexedClaims, indexedVolumes := indexReferencedClaimsAndVolumes(pods, claims, volumes)
	if len(indexedClaims) != 3 || len(indexedVolumes) != 1 || indexedVolumes["pv-a"].Name != "pv-a" {
		t.Fatalf("indexes retain unrelated objects: claims=%v volumes=%v", indexedClaims, indexedVolumes)
	}
	if indexedClaims[namespacedKey("ns-a", "shared")].Spec.VolumeName != "pv-a" || indexedClaims[namespacedKey("ns-b", "shared")].Spec.VolumeName != "missing-pv" {
		t.Fatal("namespace-qualified PVC references changed")
	}
	for _, tc := range []struct {
		pod   corev1.Pod
		wants map[string]string
	}{
		{pods[0], map[string]string{"shared": "unmatched", "pending": "pending", "absent": "missing_claim"}},
		{pods[1], map[string]string{"shared": "missing_pv"}},
	} {
		mounts := tracePodPVCReferences(tc.pod, indexedClaims, indexedVolumes)
		if len(mounts) != len(tc.wants) {
			t.Fatalf("mount relationship count changed: %+v", mounts)
		}
		for _, mount := range mounts {
			if want, ok := tc.wants[mount.PVCName]; !ok || mount.Status != want {
				t.Fatalf("lookup state changed: %+v want=%v", mount, tc.wants)
			}
		}
	}
}

func TestIndexReferencedClaimsAndVolumesWithoutReferences(t *testing.T) {
	claims, volumes := indexReferencedClaimsAndVolumes([]corev1.Pod{{ObjectMeta: metav1.ObjectMeta{Name: "notebook-no-volumes"}}}, []corev1.PersistentVolumeClaim{{ObjectMeta: metav1.ObjectMeta{Name: "irrelevant"}}}, []corev1.PersistentVolume{{ObjectMeta: metav1.ObjectMeta{Name: "irrelevant"}}})
	if len(claims) != 0 || len(volumes) != 0 {
		t.Fatal("unreferenced objects indexed")
	}
}
