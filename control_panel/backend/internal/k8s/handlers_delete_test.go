package k8s

import (
	"context"
	"fmt"
	"path/filepath"
	"testing"
	"time"

	networkingv1 "k8s.io/api/networking/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/fake"
	ktesting "k8s.io/client-go/testing"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

func TestDeleteTaskExternalNotebook(t *testing.T) {
	pod, svc := notebookMapping()
	externalNP := &networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{Name: "platform-policy", Namespace: svc.Namespace, Labels: map[string]string{"service-name": svc.Name}}}
	cs := fake.NewSimpleClientset(pod, svc, externalNP)
	store, err := db.Open(filepath.Join(t.TempDir(), "test.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	RegisterK8sHandlers(eng, cs)
	id, err := eng.Submit(context.Background(), "k8s_delete_svc", "k8s", 0, map[string]any{"namespace": svc.Namespace, "name": svc.Name})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if _, err := cs.NetworkingV1().NetworkPolicies(svc.Namespace).Get(context.Background(), externalNP.Name, metav1.GetOptions{}); err != nil {
		t.Fatal("external policy must remain", err)
	}
}

func TestDeleteTaskCleanupFailureFails(t *testing.T) {
	for _, taskType := range []string{"k8s_delete_svc", "k8s_update_svc"} {
		t.Run(taskType, func(t *testing.T) {
			_, svc := notebookMapping()
			svc.Labels = map[string]string{"managed-by": "control-panel"}
			np := &networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{Name: "cp-policy", Namespace: svc.Namespace, UID: "np-1", ResourceVersion: "3", Labels: map[string]string{"managed-by": "control-panel", "service-name": svc.Name}}}
			cs := fake.NewSimpleClientset(svc, np)
			cs.PrependReactor("delete", "networkpolicies", func(ktesting.Action) (bool, runtime.Object, error) {
				return true, nil, fmt.Errorf("policy deletion forbidden")
			})
			store, err := db.Open(filepath.Join(t.TempDir(), "test.db"))
			if err != nil {
				t.Fatal(err)
			}
			defer store.Close()
			eng := tasks.NewEngine(store)
			RegisterK8sHandlers(eng, cs)
			id, err := eng.Submit(context.Background(), taskType, "k8s", 0, map[string]any{"namespace": svc.Namespace, "name": svc.Name, "mappings": []any{}})
			if err != nil {
				t.Fatal(err)
			}
			waitFor(t, store, id, "failed", 2*time.Second)
			task, _ := store.GetTask(context.Background(), id)
			if task.Error == nil {
				t.Fatal("cleanup failure missing task error")
			}
		})
	}
}

func TestDeleteTaskPreservesPoliciesCreatedAfterServiceDelete(t *testing.T) {
	_, svc := notebookMapping()
	svc.Labels = map[string]string{"managed-by": "control-panel"}
	oldNP := &networkingv1.NetworkPolicy{ObjectMeta: metav1.ObjectMeta{Name: "old-policy", Namespace: svc.Namespace, UID: "np-old", ResourceVersion: "3", Labels: map[string]string{"managed-by": "control-panel", "service-name": svc.Name}}}
	cs := fake.NewSimpleClientset(svc, oldNP)
	cs.PrependReactor("delete", "services", func(ktesting.Action) (bool, runtime.Object, error) {
		newNP := oldNP.DeepCopy()
		newNP.Name = "new-policy"
		newNP.UID = "np-new"
		if err := cs.Tracker().Add(newNP); err != nil {
			t.Error(err)
		}
		return false, nil, nil
	})
	cs.PrependReactor("delete", "networkpolicies", func(a ktesting.Action) (bool, runtime.Object, error) {
		opts := a.(ktesting.DeleteAction).GetDeleteOptions()
		if opts.Preconditions == nil || opts.Preconditions.UID == nil || *opts.Preconditions.UID != oldNP.UID || opts.Preconditions.ResourceVersion == nil || *opts.Preconditions.ResourceVersion != oldNP.ResourceVersion {
			t.Error("policy deletion needs snapshot identity preconditions")
		}
		return false, nil, nil
	})
	store, err := db.Open(filepath.Join(t.TempDir(), "test.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	RegisterK8sHandlers(eng, cs)
	id, err := eng.Submit(context.Background(), "k8s_delete_svc", "k8s", 0, map[string]any{"namespace": svc.Namespace, "name": svc.Name})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "succeeded", 2*time.Second)
	if _, err := cs.NetworkingV1().NetworkPolicies(svc.Namespace).Get(context.Background(), "new-policy", metav1.GetOptions{}); err != nil {
		t.Fatal("new service policy must survive", err)
	}
}

func TestDeleteTaskRejectsQueuedReplacement(t *testing.T) {
	_, svc := notebookMapping()
	svc.Labels = map[string]string{"managed-by": "control-panel"}
	cs := fake.NewSimpleClientset(svc)
	store, err := db.Open(filepath.Join(t.TempDir(), "test.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	RegisterK8sHandlers(eng, cs)
	id, err := eng.Submit(context.Background(), "k8s_delete_svc", "k8s", 0, map[string]any{"namespace": svc.Namespace, "name": svc.Name, "uid": "previous-svc", "resource_version": "6"})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	if _, err := cs.CoreV1().Services(svc.Namespace).Get(context.Background(), svc.Name, metav1.GetOptions{}); err != nil {
		t.Fatal("replacement must survive", err)
	}
}

func TestUpdateEmptyExternalRemainsForbidden(t *testing.T) {
	pod, svc := notebookMapping()
	cs := fake.NewSimpleClientset(pod, svc)
	store, err := db.Open(filepath.Join(t.TempDir(), "test.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	eng := tasks.NewEngine(store)
	RegisterK8sHandlers(eng, cs)
	id, err := eng.Submit(context.Background(), "k8s_update_svc", "k8s", 0, map[string]any{"namespace": svc.Namespace, "name": svc.Name, "mappings": []any{}})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	if _, err := cs.CoreV1().Services(svc.Namespace).Get(context.Background(), svc.Name, metav1.GetOptions{}); err != nil {
		t.Fatal("external update must not delete", err)
	}
}
