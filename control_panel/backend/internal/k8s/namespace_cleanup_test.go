package k8s

import (
	"context"
	"strings"
	"testing"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	"k8s.io/client-go/kubernetes/fake"
	k8stesting "k8s.io/client-go/testing"
	"xirang/control_panel/internal/storage"
)

const cleanupPodUID = "11111111-2222-3333-4444-555555555555"

var cleanupContainerID = strings.Repeat("a", 64)

func cleanupFixture() (*fake.Clientset, []storage.NamespaceHolder) {
	controller := true
	pod := &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "promtail-random", Namespace: "monitoring", UID: types.UID(cleanupPodUID), OwnerReferences: []metav1.OwnerReference{{APIVersion: "apps/v1", Kind: "DaemonSet", Name: "promtail", UID: "ds-uid", Controller: &controller}}}, Spec: corev1.PodSpec{NodeName: "worker-a", Volumes: []corev1.Volume{{Name: "logs", VolumeSource: corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: "/data"}}}}, Containers: []corev1.Container{{Name: "promtail", VolumeMounts: []corev1.VolumeMount{{Name: "logs", MountPath: "/host-data"}}}}}, Status: corev1.PodStatus{ContainerStatuses: []corev1.ContainerStatus{{Name: "promtail", ContainerID: "containerd://" + cleanupContainerID, State: corev1.ContainerState{Running: &corev1.ContainerStateRunning{}}}}}}
	node := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-a", UID: "node-uid"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.10"}, {Type: corev1.NodeHostName, Address: "worker.example"}}}}
	ds := &appsv1.DaemonSet{ObjectMeta: metav1.ObjectMeta{Name: "promtail", Namespace: "monitoring", UID: "ds-uid"}}
	cgroup := "0::/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod" + strings.ReplaceAll(cleanupPodUID, "-", "_") + ".slice/cri-containerd-" + cleanupContainerID + ".scope"
	holders := []storage.NamespaceHolder{{PID: 123, Namespace: "mnt:[456]", StartTime: "789", Cgroup: cgroup, RootDev: 10, RootIno: 20, Mounts: []storage.NamespaceMount{{ID: 30, ParentID: 29, Device: "253:0", Root: "/", Path: "/host-data/lv"}}, Members: []storage.NamespaceProcess{{PID: 123, StartTime: "789", Cgroup: cgroup}}}}
	return fake.NewSimpleClientset(node, pod, ds), holders
}

func TestAuthorizeNamespaceCleanup_ExactEvidence(t *testing.T) {
	client, holders := cleanupFixture()
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "worker.example", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err != nil {
		t.Fatal(err)
	}
	use, _, err := CheckNFSPodUsage(context.Background(), client, "10.0.0.10", "/data/lv")
	if err != nil || use {
		t.Fatalf("parent log hostPath must reach authorization: use=%v err=%v", use, err)
	}
	// cgroupfs layout is also matched using complete components, never prefixes.
	cg := "0::/kubepods/burstable/pod" + cleanupPodUID + "/" + cleanupContainerID
	holders[0].Cgroup, holders[0].Members[0].Cgroup = cg, cg
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err != nil {
		t.Fatal(err)
	}
}

func TestAuthorizeNamespaceCleanup_RejectsIncompleteOrForgedEvidence(t *testing.T) {
	cases := []struct {
		name   string
		mutate func(*fake.Clientset, []storage.NamespaceHolder)
		allow  []string
	}{
		{"empty allowlist", nil, nil},
		{"wrong container allowlist", nil, []string{"monitoring/promtail/other"}},
		{"malformed allowlist", nil, []string{"monitoring/promtail/promtail/extra"}},
		{"unknown root", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].RootIno = 0 }, nil},
		{"no members", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].Members = nil }, nil},
		{"unknown shared member", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Members = append(h[0].Members, storage.NamespaceProcess{PID: 124, StartTime: "790", Cgroup: "0::/system.slice/sshd.service"})
		}, nil},
		{"representative mismatch", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].Members[0].StartTime = "790" }, nil},
		{"pod uid prefix", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Cgroup = strings.ReplaceAll(h[0].Cgroup, ".slice/cri-", "extra.slice/cri-")
			h[0].Members[0].Cgroup = h[0].Cgroup
		}, nil},
		{"container id prefix", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Cgroup = strings.ReplaceAll(h[0].Cgroup, cleanupContainerID, cleanupContainerID[:12])
			h[0].Members[0].Cgroup = h[0].Cgroup
		}, nil},
		{"forged non-kubernetes hierarchy", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Cgroup = "0::/system.slice/pod" + cleanupPodUID + "/" + cleanupContainerID
			h[0].Members[0].Cgroup = h[0].Cgroup
		}, nil},
		{"host process", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Cgroup = "0::/"
			h[0].Members[0].Cgroup = h[0].Cgroup
		}, nil},
		{"wrong mount path", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].Mounts[0].Path = "/unrelated/lv" }, nil},
		{"wrong filesystem root", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].Mounts[0].Root = "/files" }, nil},
		{"no mounts", func(_ *fake.Clientset, h []storage.NamespaceHolder) { h[0].Mounts = nil }, nil},
		{"owner uid changed", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			ds, _ := c.AppsV1().DaemonSets("monitoring").Get(context.Background(), "promtail", metav1.GetOptions{})
			ds.UID = "new-uid"
			_, _ = c.AppsV1().DaemonSets("monitoring").Update(context.Background(), ds, metav1.UpdateOptions{})
		}, nil},
		{"pod name alone", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.OwnerReferences = nil
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"wrong node", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.NodeName = "elsewhere"
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"runtime id changed", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Status.ContainerStatuses[0].ContainerID = "containerd://" + strings.Repeat("b", 64)
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"host PID container", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.HostPID = true
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"container not running", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Status.ContainerStatuses[0].State.Running = nil
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"propagating mount", func(_ *fake.Clientset, h []storage.NamespaceHolder) {
			h[0].Mounts[0].Optional = []string{"master:1"}
		}, nil},
		{"container root hostpath", func(c *fake.Clientset, h []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.Volumes[0].HostPath.Path = "/"
			p.Spec.Containers[0].VolumeMounts[0].MountPath = "/"
			h[0].Mounts[0].Path = "/data/lv"
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"masked inherited target", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.Volumes = append(p.Spec.Volumes, corev1.Volume{Name: "mask", VolumeSource: corev1.VolumeSource{EmptyDir: &corev1.EmptyDirVolumeSource{}}})
			p.Spec.Containers[0].VolumeMounts = append(p.Spec.Containers[0].VolumeMounts, corev1.VolumeMount{Name: "mask", MountPath: "/host-data/lv"})
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"direct hostpath target", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.Volumes[0].HostPath.Path = "/data/lv"
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
		{"direct nfs business reference", func(c *fake.Clientset, _ []storage.NamespaceHolder) {
			p, _ := c.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
			p.Spec.Volumes = append(p.Spec.Volumes, corev1.Volume{Name: "business", VolumeSource: corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: "10.0.0.10", Path: "/data/lv"}}})
			_, _ = c.CoreV1().Pods("monitoring").Update(context.Background(), p, metav1.UpdateOptions{})
		}, nil},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			c, h := cleanupFixture()
			if tc.mutate != nil {
				tc.mutate(c, h)
			}
			allow := tc.allow
			if allow == nil && tc.name != "empty allowlist" {
				allow = []string{"monitoring/promtail/promtail"}
			}
			if err := AuthorizeNamespaceCleanup(context.Background(), c, "10.0.0.10", "/data/lv", h, allow); err == nil {
				t.Fatal("unsafe evidence must deny cleanup")
			}
		})
	}
}

func TestAuthorizeNamespaceCleanup_AllHoldersAndMembers(t *testing.T) {
	client, holders := cleanupFixture()
	holders[0].Members = append(holders[0].Members, storage.NamespaceProcess{PID: 124, StartTime: "790", Cgroup: holders[0].Cgroup})
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err != nil {
		t.Fatal(err)
	}
	other := holders[0]
	other.Namespace = "mnt:[457]"
	other.Cgroup = "0::/system.slice/sshd.service"
	other.PID = 125
	other.Members = []storage.NamespaceProcess{{PID: 125, StartTime: other.StartTime, Cgroup: other.Cgroup}}
	holders = append(holders, other)
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err == nil {
		t.Fatal("one authorized holder must not authorize an unknown holder")
	}
}

func TestAuthorizeNamespaceCleanup_FreshIdentityChanges(t *testing.T) {
	for _, resource := range []string{"pods", "nodes"} {
		t.Run(resource, func(t *testing.T) {
			client, holders := cleanupFixture()
			client.PrependReactor("get", resource, func(action k8stesting.Action) (bool, runtime.Object, error) {
				get := action.(k8stesting.GetAction)
				obj, err := client.Tracker().Get(action.GetResource(), action.GetNamespace(), get.GetName())
				if err != nil {
					return true, nil, err
				}
				obj = obj.DeepCopyObject()
				switch changed := obj.(type) {
				case *corev1.Pod:
					changed.UID = "replacement-pod"
				case *corev1.Node:
					changed.UID = "replacement-node"
				}
				return true, obj, nil
			})
			if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err == nil {
				t.Fatal("fresh identity replacement must deny")
			}
		})
	}
}

func TestAuthorizeNamespaceCleanup_QueryFailureAndUnknownWorker(t *testing.T) {
	c, h := cleanupFixture()
	for _, host := range []string{"unknown-worker", "10.0.0.99"} {
		if err := AuthorizeNamespaceCleanup(context.Background(), c, host, "/data/lv", h, []string{"monitoring/promtail/promtail"}); err == nil {
			t.Fatal("unknown worker must deny")
		}
	}
	if err := AuthorizeNamespaceCleanup(context.Background(), nil, "10.0.0.10", "/data/lv", h, []string{"monitoring/promtail/promtail"}); err == nil {
		t.Fatal("missing client must deny")
	}
	for _, resource := range []string{"pods", "nodes", "daemonsets", "persistentvolumeclaims", "persistentvolumes"} {
		c, h := cleanupFixture()
		c.PrependReactor("*", resource, func(k8stesting.Action) (bool, runtime.Object, error) { return true, nil, context.DeadlineExceeded })
		if err := AuthorizeNamespaceCleanup(context.Background(), c, "10.0.0.10", "/data/lv", h, []string{"monitoring/promtail/promtail"}); err == nil {
			t.Fatalf("%s failure must deny", resource)
		}
	}
}
