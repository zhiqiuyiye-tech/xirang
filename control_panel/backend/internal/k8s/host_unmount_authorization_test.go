package k8s

import (
	"context"
	"testing"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	"xirang/control_panel/internal/storage"
)

func TestAuthorizeHostUnmountSharedEvidenceRemainsExplicitlyScoped(t *testing.T) {
	client, holders := cleanupFixture()
	holders[0].Mounts[0].Optional = []string{"shared:578", "master:99"}
	pod, _ := client.CoreV1().Pods("monitoring").Get(context.Background(), "promtail-random", metav1.GetOptions{})
	propagation := corev1.MountPropagationHostToContainer
	pod.Spec.Containers[0].VolumeMounts[0].MountPropagation = &propagation
	_, _ = client.CoreV1().Pods("monitoring").Update(context.Background(), pod, metav1.UpdateOptions{})
	allowed := []string{"monitoring/promtail/promtail"}
	if err := AuthorizeHostUnmount(context.Background(), client, "10.0.0.10", "/data/lv", holders, allowed); err != nil {
		t.Fatal(err)
	}
	// Scoped host propagation authorization must not authorize direct cleanup
	// inside a container using the original private-only recovery path.
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, allowed); err == nil {
		t.Fatal("host unmount permission leaked into container cleanup")
	}
	if err := AuthorizeHostUnmount(context.Background(), client, "10.0.0.10", "/data/lv", holders, nil); err == nil {
		t.Fatal("empty allowlist authorized shared holders")
	}
	holders[0].Members = append(holders[0].Members, storage.NamespaceProcess{PID: 124, StartTime: "100", Cgroup: "0::/unknown.service"})
	if err := AuthorizeHostUnmount(context.Background(), client, "10.0.0.10", "/data/lv", holders, allowed); err == nil {
		t.Fatal("unknown namespace member was authorized")
	}
}

func TestAuthorizeHostUnmountRejectsUnknownPropagationMetadata(t *testing.T) {
	client, holders := cleanupFixture()
	holders[0].Mounts[0].Optional = []string{"future:1"}
	if err := AuthorizeHostUnmount(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err == nil {
		t.Fatal("unknown propagation metadata accepted")
	}
}
