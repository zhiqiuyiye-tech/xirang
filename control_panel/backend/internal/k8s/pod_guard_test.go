package k8s

import (
	"context"
	"testing"

	"k8s.io/apimachinery/pkg/runtime"
	k8stesting "k8s.io/client-go/testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestCheckNFSPodUsage_FailClosedAndAliases(t *testing.T) {
	node := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-a"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.10"}, {Type: corev1.NodeHostName, Address: "worker.example"}}}}
	cases := []struct {
		name             string
		volume           corev1.VolumeSource
		nodeName         string
		wantUse, wantErr bool
	}{
		{"ancestor nfs", corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.10", Path: "/data"}}, "", true, false},
		{"node hostname alias", corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: "worker.example.", Path: "/data/lv"}}, "", true, false},
		{"inline csi nfs", corev1.VolumeSource{CSI: &corev1.CSIVolumeSource{Driver: "nfs.csi.k8s.io", VolumeAttributes: map[string]string{"server": "worker-a", "share": "/data/lv"}}}, "", true, false},
		{"missing pvc", corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "missing"}}, "", false, true},
		{"malformed nfs", corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.10", Path: ""}}, "", false, true},
		{"unknown csi", corev1.VolumeSource{CSI: &corev1.CSIVolumeSource{Driver: "unknown.example"}}, "", false, true},
		{"target hostpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data/lv"}}, "worker-a", true, false},
		{"child hostpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data/lv/files"}}, "worker-a", true, false},
		{"parent hostpath subpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data"}}, "worker-a", true, false},
		{"parent log hostpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data"}}, "worker-a", false, false},
		{"unknown node hostpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data/lv"}}, "missing-node", false, true},
		{"similar hostpath", corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data/lv-other"}}, "worker-a", false, false},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			mount := corev1.VolumeMount{Name: "data", MountPath: "/mnt"}
			if tc.name == "parent hostpath subpath" {
				mount.SubPath = "lv"
			}
			pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "app", Namespace: "default"}, Spec: corev1.PodSpec{NodeName: tc.nodeName, Volumes: []corev1.Volume{{Name: "data", VolumeSource: tc.volume}}, Containers: []corev1.Container{{Name: "app", VolumeMounts: []corev1.VolumeMount{mount}}}}}
			client := fake.NewSimpleClientset(node.DeepCopy(), pod)
			use, _, err := CheckNFSPodUsage(context.Background(), client, "10.0.0.10", "/data/lv")
			if (err != nil) != tc.wantErr || use != tc.wantUse {
				t.Fatalf("use=%v err=%v; want use=%v error=%v", use, err, tc.wantUse, tc.wantErr)
			}
		})
	}
}

func TestCheckNFSPodUsage_UnresolvedPVCAndPV(t *testing.T) {
	for _, volumeName := range []string{"", "missing-pv"} {
		client := fake.NewSimpleClientset(&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "app", Namespace: "ns"}, Spec: corev1.PodSpec{Volumes: []corev1.Volume{{VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "data"}}}}}}, &corev1.PersistentVolumeClaim{ObjectMeta: metav1.ObjectMeta{Name: "data", Namespace: "ns"}, Spec: corev1.PersistentVolumeClaimSpec{VolumeName: volumeName}})
		if _, _, err := CheckNFSPodUsage(context.Background(), client, "10.0.0.10", "/data/lv"); err == nil {
			t.Fatalf("unresolved PVC/PV %q must stop", volumeName)
		}
	}
}

func TestCheckNFSPodUsage_QueryFailures(t *testing.T) {
	if _, _, err := CheckNFSPodUsage(context.Background(), nil, "10.0.0.10", "/data/lv"); err == nil {
		t.Fatal("nil client must stop")
	}
	for _, resource := range []string{"pods", "nodes", "persistentvolumeclaims", "persistentvolumes"} {
		client := fake.NewSimpleClientset()
		client.PrependReactor("list", resource, func(k8stesting.Action) (bool, runtime.Object, error) { return true, nil, context.DeadlineExceeded })
		if _, _, err := CheckNFSPodUsage(context.Background(), client, "10.0.0.10", "/data/lv"); err == nil {
			t.Fatalf("failed %s query must stop", resource)
		}
	}
}

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
