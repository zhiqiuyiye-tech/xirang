package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes/fake"
)

func TestWholeWorkerPodGuardBlocksAssignedRawDevices(t *testing.T) {
	worker := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-a"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.10"}}}}
	other := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-b"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.11"}}}}
	for _, tc := range []struct {
		name, node, path string
		wantUse, wantErr bool
	}{
		{"target worker raw device", "worker-a", "", true, false},
		{"unknown placement", "", "", false, true},
		{"other worker raw device", "worker-b", "", false, false},
		{"confirmed unrelated NFS path", "worker-a", "/data02/nfs-share", false, false},
	} {
		t.Run(tc.name, func(t *testing.T) {
			pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "raw-device-pod", Namespace: "ns"}, Spec: corev1.PodSpec{
				NodeName:   tc.node,
				Volumes:    []corev1.Volume{{Name: "raw", VolumeSource: corev1.VolumeSource{CSI: &corev1.CSIVolumeSource{Driver: "confirmed-non-nfs.example"}}}},
				Containers: []corev1.Container{{Name: "app", VolumeDevices: []corev1.VolumeDevice{{Name: "raw", DevicePath: "/dev/data"}}}},
			}}
			client := fake.NewSimpleClientset(worker.DeepCopy(), other.DeepCopy(), pod)
			inUse, _, err := CheckNFSPodUsage(context.Background(), client, "10.0.0.10", tc.path, "confirmed-non-nfs.example")
			if inUse != tc.wantUse || (err != nil) != tc.wantErr {
				t.Fatalf("raw assignment proof: inUse=%v err=%v wantUse=%v wantErr=%v", inUse, err, tc.wantUse, tc.wantErr)
			}
		})
	}
}
