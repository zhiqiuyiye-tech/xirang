package api

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/client-go/kubernetes/fake"
	ktesting "k8s.io/client-go/testing"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

type acceleratorAPISSH struct {
	*ssh.Manager
	output string
	err    error
}

func (s *acceleratorAPISSH) Run(context.Context, db.WorkerNode, string) (string, string, int, error) {
	return s.output, "", 0, s.err
}

func TestWorkerAcceleratorRouteRequiresAuthentication(t *testing.T) {
	r, _, _, _ := newRouter(t)
	rec := httptest.NewRecorder()
	r.ServeHTTP(rec, httptest.NewRequest("GET", "/api/v1/workers/accelerators", nil))
	if rec.Code != http.StatusUnauthorized {
		t.Fatalf("status=%d", rec.Code)
	}
}

func TestWorkerAcceleratorsJoinByHostAndPreserveUnknown(t *testing.T) {
	for _, scenario := range []string{"available", "no cluster", "cluster error", "ssh error", "no matching node"} {
		t.Run(scenario, func(t *testing.T) {
			_, svc, store, _ := newRouter(t)
			id, err := svc.Create(context.Background(), workers.CreateReq{Name: "custom-alias", Host: "10.0.0.1"})
			if err != nil {
				t.Fatal(err)
			}
			svcSSH := &acceleratorAPISSH{output: "__NVIDIA__\nGPU-a, NVIDIA A100\nGPU-b, NVIDIA A100\n"}
			if scenario == "ssh error" {
				svcSSH.err = errors.New("ssh failed")
			}
			// Construct a service with a deterministic read-only SSH probe.
			ws := workers.NewService(store, nil, svcSSH, tasks.NewEngine(store))
			cs := fake.NewSimpleClientset(
				&corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: "worker-k8s"}, Status: corev1.NodeStatus{Addresses: []corev1.NodeAddress{{Type: corev1.NodeInternalIP, Address: "10.0.0.1"}}, Allocatable: corev1.ResourceList{"nvidia.com/gpu": resource.MustParse("2")}}},
				&corev1.Pod{ObjectMeta: metav1.ObjectMeta{Name: "notebook-a", Namespace: "ns"}, Spec: corev1.PodSpec{NodeName: "worker-k8s", Containers: []corev1.Container{{Name: "notebook", Resources: corev1.ResourceRequirements{Limits: corev1.ResourceList{"nvidia.com/gpu": resource.MustParse("1")}}}}}, Status: corev1.PodStatus{Phase: corev1.PodRunning}},
			)
			h := &workerHandlers{ws: ws, store: store, client: cs}
			if scenario == "no cluster" {
				h.client = nil
			}
			if scenario == "cluster error" {
				cs.PrependReactor("list", "pods", func(ktesting.Action) (bool, runtime.Object, error) { return true, nil, errors.New("forbidden") })
			}
			if scenario == "no matching node" {
				_, err := cs.CoreV1().Nodes().Get(context.Background(), "worker-k8s", metav1.GetOptions{})
				if err != nil {
					t.Fatal(err)
				}
				if err := cs.CoreV1().Nodes().Delete(context.Background(), "worker-k8s", metav1.DeleteOptions{}); err != nil {
					t.Fatal(err)
				}
			}
			r := gin.New()
			r.GET("/accelerators", h.accelerators)
			rec := httptest.NewRecorder()
			r.ServeHTTP(rec, httptest.NewRequest("GET", "/accelerators", nil))
			if rec.Code != http.StatusOK {
				t.Fatalf("status=%d body=%s", rec.Code, rec.Body.String())
			}
			var rows []struct {
				WorkerID         int64  `json:"worker_id"`
				Status           string `json:"status"`
				Total            *int64 `json:"total"`
				Used             *int64 `json:"used"`
				AllocationStatus string `json:"allocation_status"`
			}
			if err := json.Unmarshal(rec.Body.Bytes(), &rows); err != nil {
				t.Fatal(err)
			}
			if len(rows) != 1 || rows[0].WorkerID != id {
				t.Fatalf("rows=%+v", rows)
			}
			got := rows[0]
			if scenario == "ssh error" {
				if got.Total != nil || got.Status != "unknown" {
					t.Fatalf("rows=%+v", rows)
				}
			} else if got.Total == nil || *got.Total != 2 {
				t.Fatalf("rows=%+v", rows)
			}
			if scenario == "available" || scenario == "ssh error" {
				if got.Used == nil || *got.Used != 1 || got.AllocationStatus != "available" {
					t.Fatalf("rows=%+v", rows)
				}
			} else if got.Used != nil || got.AllocationStatus != "unknown" {
				t.Fatalf("rows=%+v", rows)
			}
		})
	}
}
