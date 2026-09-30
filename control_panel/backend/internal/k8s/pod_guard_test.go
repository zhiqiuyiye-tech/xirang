package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestCheckNFSPodUsage_DirectNFSVolume(t *testing.T) {
	client := fake.NewSimpleClientset(
		&corev1.Pod{
			ObjectMeta: metav1.ObjectMeta{Name: "my-app", Namespace: "default"},
			Spec: corev1.PodSpec{
				Volumes: []corev1.Volume{
					{
						Name: "nfs-vol",
						VolumeSource: corev1.VolumeSource{
							NFS: &corev1.NFSVolumeSource{
								Server: "192.168.1.10",
								Path:   "/data02/notebook_a_200g",
							},
						},
					},
				},
			},
		},
	)

	inUse, blockers, err := CheckNFSPodUsage(context.Background(), client, "192.168.1.10", "/data02/notebook_a_200g")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !inUse {
		t.Fatal("expected volume to be in use")
	}
	if len(blockers) != 1 || blockers[0] != "default/my-app (direct nfs)" {
		t.Fatalf("unexpected blockers: %v", blockers)
	}
}

func TestCheckNFSPodUsage_PVCMount(t *testing.T) {
	client := fake.NewSimpleClientset(
		&corev1.Pod{
			ObjectMeta: metav1.ObjectMeta{Name: "job-1", Namespace: "prod"},
			Spec: corev1.PodSpec{
				Volumes: []corev1.Volume{
					{
						Name: "data",
						VolumeSource: corev1.VolumeSource{
							PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{
								ClaimName: "data-claim",
							},
						},
					},
				},
			},
		},
		&corev1.PersistentVolumeClaim{
			ObjectMeta: metav1.ObjectMeta{Name: "data-claim", Namespace: "prod"},
			Spec: corev1.PersistentVolumeClaimSpec{
				VolumeName: "pv-nfs",
			},
			Status: corev1.PersistentVolumeClaimStatus{
				Phase: corev1.ClaimBound,
			},
		},
		&corev1.PersistentVolume{
			ObjectMeta: metav1.ObjectMeta{Name: "pv-nfs"},
			Spec: corev1.PersistentVolumeSpec{
				PersistentVolumeSource: corev1.PersistentVolumeSource{
					NFS: &corev1.NFSVolumeSource{
						Server: "192.168.1.10",
						Path:   "/data02/notebook_a_200g",
					},
				},
			},
		},
	)

	inUse, blockers, err := CheckNFSPodUsage(context.Background(), client, "192.168.1.10", "/data02/notebook_a_200g")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !inUse {
		t.Fatal("expected volume to be in use")
	}
	if len(blockers) != 1 {
		t.Fatalf("expected 1 blocker, got: %v", blockers)
	}
}

func TestCheckNFSPodUsage_DifferentExportPath(t *testing.T) {
	client := fake.NewSimpleClientset(
		&corev1.Pod{
			ObjectMeta: metav1.ObjectMeta{Name: "other-app", Namespace: "default"},
			Spec: corev1.PodSpec{
				Volumes: []corev1.Volume{
					{
						Name: "nfs-vol",
						VolumeSource: corev1.VolumeSource{
							NFS: &corev1.NFSVolumeSource{
								Server: "192.168.1.10",
								Path:   "/data02/other_export",
							},
						},
					},
				},
			},
		},
	)

	inUse, blockers, err := CheckNFSPodUsage(context.Background(), client, "192.168.1.10", "/data02/notebook_a_200g")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if inUse || len(blockers) > 0 {
		t.Fatalf("expected not in use, got inUse=%v, blockers=%v", inUse, blockers)
	}
}

func TestCheckNFSPodUsage_UnknownExportPath_BlocksIfAnyNFSOnWorker(t *testing.T) {
	client := fake.NewSimpleClientset(
		&corev1.Pod{
			ObjectMeta: metav1.ObjectMeta{Name: "app", Namespace: "default"},
			Spec: corev1.PodSpec{
				Volumes: []corev1.Volume{
					{
						Name: "nfs-vol",
						VolumeSource: corev1.VolumeSource{
							NFS: &corev1.NFSVolumeSource{
								Server: "192.168.1.10",
								Path:   "/data02/some_export",
							},
						},
					},
				},
			},
		},
	)

	// Passing empty exportPath: conservative rule blocks because worker has an active NFS mount
	inUse, blockers, err := CheckNFSPodUsage(context.Background(), client, "192.168.1.10", "")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if !inUse || len(blockers) == 0 {
		t.Fatalf("expected blocked when exportPath is unknown and worker has mounts, got inUse=%v", inUse)
	}
}
