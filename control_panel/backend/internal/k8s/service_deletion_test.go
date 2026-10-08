package k8s

import (
	"context"
	"encoding/json"
	"fmt"
	"testing"

	corev1 "k8s.io/api/core/v1"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/util/intstr"
	"k8s.io/client-go/kubernetes/fake"
	ktesting "k8s.io/client-go/testing"
)

func notebookMapping() (*corev1.Pod, *corev1.Service) {
	return &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-one", Namespace: "ns1", UID: "pod-1", Labels: map[string]string{"app": "nb"}}},
		&corev1.Service{ObjectMeta: metav1.ObjectMeta{Name: "platform-ports", Namespace: "ns1", UID: "svc-1", ResourceVersion: "7"}, Spec: corev1.ServiceSpec{Type: corev1.ServiceTypeNodePort, Selector: map[string]string{"app": "nb"}, Ports: []corev1.ServicePort{{Port: 8888, TargetPort: intstr.FromInt(8888), NodePort: 31088}}}}
}

func TestDeleteServiceExternalNotebookMapping(t *testing.T) {
	pod, svc := notebookMapping()
	cs := fake.NewSimpleClientset(pod, svc)
	if err := DeleteService(context.Background(), cs, svc.Namespace, svc.Name); err != nil {
		t.Fatal(err)
	}
	if _, err := cs.CoreV1().Services(svc.Namespace).Get(context.Background(), svc.Name, metav1.GetOptions{}); !apierrors.IsNotFound(err) {
		t.Fatalf("service should be gone: %v", err)
	}
}

func TestDeleteServiceExternalSafety(t *testing.T) {
	for _, tc := range []struct {
		name   string
		change func(*corev1.Pod, *corev1.Service)
		extra  bool
	}{
		{"clusterIP", func(_ *corev1.Pod, s *corev1.Service) { s.Spec.Type = corev1.ServiceTypeClusterIP }, false},
		{"loadBalancer", func(_ *corev1.Pod, s *corev1.Service) { s.Spec.Type = corev1.ServiceTypeLoadBalancer }, false},
		{"ordinary pod", func(p *corev1.Pod, _ *corev1.Service) { p.Name = "web-app" }, false},
		{"unmatched selector", func(_ *corev1.Pod, s *corev1.Service) { s.Spec.Selector = map[string]string{"app": "other"} }, false},
		{"empty selector", func(_ *corev1.Pod, s *corev1.Service) { s.Spec.Selector = nil }, false},
		{"missing empty label", func(_ *corev1.Pod, s *corev1.Service) { s.Spec.Selector = map[string]string{"missing": ""} }, false},
		{"mixed notebook and ordinary targets", func(_ *corev1.Pod, _ *corev1.Service) {}, true},
		{"protected namespace", func(p *corev1.Pod, s *corev1.Service) { p.Namespace = "kube-system"; s.Namespace = p.Namespace }, false},
	} {
		t.Run(tc.name, func(t *testing.T) {
			pod, svc := notebookMapping()
			tc.change(pod, svc)
			objects := []runtime.Object{pod, svc}
			if tc.extra {
				objects = append(objects, &corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "web-app", Namespace: svc.Namespace, Labels: pod.Labels}})
			}
			cs := fake.NewSimpleClientset(objects...)
			if err := DeleteService(context.Background(), cs, svc.Namespace, svc.Name); err == nil {
				t.Fatal("unsafe external deletion accepted")
			}
			for _, a := range cs.Actions() {
				if a.GetVerb() == "delete" {
					t.Fatal("unsafe delete issued")
				}
			}
		})
	}
}

func TestDeleteServiceUsesIdentityPreconditions(t *testing.T) {
	for _, managed := range []bool{false, true} {
		t.Run(fmt.Sprint(managed), func(t *testing.T) {
			pod, svc := notebookMapping()
			if managed {
				svc.Labels = map[string]string{"managed-by": "control-panel"}
			}
			cs := fake.NewSimpleClientset(pod, svc)
			called := false
			cs.PrependReactor("delete", "services", func(a ktesting.Action) (bool, runtime.Object, error) {
				called = true
				options := a.(ktesting.DeleteAction).GetDeleteOptions()
				if options.Preconditions == nil || options.Preconditions.UID == nil || *options.Preconditions.UID != svc.UID || options.Preconditions.ResourceVersion == nil || *options.Preconditions.ResourceVersion != svc.ResourceVersion {
					t.Error("delete must pin UID and resource version of validated service")
				}
				return true, nil, apierrors.NewConflict(schema.GroupResource{Resource: "services"}, svc.Name, fmt.Errorf("service replaced"))
			})
			if err := DeleteService(context.Background(), cs, svc.Namespace, svc.Name); err == nil {
				t.Fatal("conflict should propagate")
			}
			if !called {
				t.Fatal("eligible mapping was not deleted")
			}
		})
	}
}

func TestListServicesExposesDeletionEligibility(t *testing.T) {
	pod, svc := notebookMapping()
	cluster := svc.DeepCopy()
	cluster.Name = "internal"
	cluster.Spec.Type = corev1.ServiceTypeClusterIP
	cs := fake.NewSimpleClientset(pod, svc, cluster)
	list, err := ListServicesForNotebooks(context.Background(), cs)
	if err != nil {
		t.Fatal(err)
	}
	for _, info := range list {
		data, _ := json.Marshal(info)
		var fields map[string]any
		_ = json.Unmarshal(data, &fields)
		want := info.Name == svc.Name
		if fields["deletable"] != want {
			t.Fatalf("%s deletable=%v, want %v", info.Name, fields["deletable"], want)
		}
		if info.Managed {
			t.Fatal("external service should remain uneditable")
		}
	}
}

func TestDeleteServiceFailsClosedWhenPodDiscoveryFails(t *testing.T) {
	pod, svc := notebookMapping()
	cs := fake.NewSimpleClientset(pod, svc)
	cs.PrependReactor("list", "pods", func(ktesting.Action) (bool, runtime.Object, error) {
		return true, nil, fmt.Errorf("pod discovery unavailable")
	})
	if err := DeleteService(context.Background(), cs, svc.Namespace, svc.Name); err == nil {
		t.Fatal("pod discovery failure must reject deletion")
	}
	for _, a := range cs.Actions() {
		if a.GetVerb() == "delete" {
			t.Fatal("delete issued after failed discovery")
		}
	}
}
