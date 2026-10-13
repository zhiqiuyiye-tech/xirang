package api

import (
	"context"
	"encoding/json"
	"errors"
	"net/http/httptest"
	"sync"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"k8s.io/client-go/kubernetes/fake"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
	"xirang/control_panel/internal/workers"
)

type countingAcceleratorSSH struct {
	*ssh.Manager
	mu      sync.Mutex
	calls   int
	err     error
	started chan struct{}
	release <-chan struct{}
}

func (s *countingAcceleratorSSH) Run(ctx context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	s.mu.Lock()
	s.calls++
	probeErr := s.err
	s.mu.Unlock()
	if probeErr != nil {
		return "", "", 0, probeErr
	}
	if s.started != nil {
		s.started <- struct{}{}
	}
	if s.release != nil {
		select {
		case <-s.release:
		case <-ctx.Done():
			return "", "", 0, ctx.Err()
		}
	}
	return "__NVIDIA__\nGPU-a, NVIDIA A100\n", "", 0, nil
}

func (s *countingAcceleratorSSH) count() int {
	s.mu.Lock()
	defer s.mu.Unlock()
	return s.calls
}

type testAcceleratorAllocations struct {
	mu   sync.Mutex
	used int64
}

func (s *testAcceleratorAllocations) Snapshot(context.Context) ([]k8s.NodeAcceleratorAllocation, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	return []k8s.NodeAcceleratorAllocation{{Name: "worker", Host: "10.0.0.1", Total: 2, Used: s.used}}, nil
}

func TestWorkerAcceleratorsCacheHardwareAcrossPageVisits(t *testing.T) {
	_, svc, store, _ := newRouter(t)
	id, err := svc.Create(context.Background(), workers.CreateReq{Name: "worker", Host: "10.0.0.1"})
	if err != nil {
		t.Fatal(err)
	}
	runner := &countingAcceleratorSSH{}
	allocations := &testAcceleratorAllocations{used: 1}
	client := fake.NewSimpleClientset()
	h := &workerHandlers{ws: workers.NewService(store, nil, runner, tasks.NewEngine(store)), store: store, client: client, allocations: allocations}
	r := gin.New()
	r.GET("/accelerators", h.accelerators)
	get := func(path string) []workerAcceleratorInfo {
		t.Helper()
		rec := httptest.NewRecorder()
		r.ServeHTTP(rec, httptest.NewRequest("GET", path, nil))
		if rec.Code != 200 {
			t.Fatalf("status=%d body=%s", rec.Code, rec.Body.String())
		}
		var rows []workerAcceleratorInfo
		if err := json.Unmarshal(rec.Body.Bytes(), &rows); err != nil {
			t.Fatal(err)
		}
		return rows
	}
	first := get("/accelerators")
	// Heartbeats update updated_at, but must not invalidate hardware discovery.
	if err := store.RecordWorkerHealth(context.Background(), id, true, time.Now().UTC(), "", 2); err != nil {
		t.Fatal(err)
	}
	allocations.mu.Lock()
	allocations.used = 2
	allocations.mu.Unlock()
	second := get("/accelerators")
	if first[0].Used == nil || *first[0].Used != 1 || second[0].Used == nil || *second[0].Used != 2 {
		t.Fatalf("workload changes did not refresh allocations: first=%+v second=%+v", first, second)
	}
	if len(client.Actions()) != 0 {
		t.Fatal("endpoint listed the cluster instead of using the watch snapshot")
	}
	if runner.count() != 1 {
		t.Fatalf("page revisit made %d SSH probes; want 1", runner.count())
	}
	if !first[0].CheckedAt.Equal(second[0].CheckedAt) {
		t.Fatal("cached sample timestamp changed")
	}
	get("/accelerators?refresh=1")
	if runner.count() != 2 {
		t.Fatalf("manual refresh probes=%d; want 2", runner.count())
	}
	node, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	node.Host = "10.0.0.2"
	if err := store.UpdateWorker(context.Background(), *node); err != nil {
		t.Fatal(err)
	}
	get("/accelerators")
	if runner.count() != 3 {
		t.Fatalf("changed worker host probes=%d; want 3", runner.count())
	}
	var wg sync.WaitGroup
	for range 8 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			rec := httptest.NewRecorder()
			r.ServeHTTP(rec, httptest.NewRequest("GET", "/accelerators", nil))
			if rec.Code != 200 {
				t.Errorf("concurrent response=%d", rec.Code)
			}
		}()
	}
	wg.Wait()
	if runner.count() != 3 {
		t.Fatalf("concurrent visits probes=%d; want 3", runner.count())
	}
}

func TestWorkerAcceleratorCacheRetriesFailedProbes(t *testing.T) {
	runner := &countingAcceleratorSSH{err: errors.New("SSH unavailable")}
	h := &workerHandlers{ws: workers.NewService(nil, nil, runner, tasks.NewEngine(nil))}
	node := db.WorkerNode{ID: 1, Host: "10.0.0.1"}
	ctx := context.Background()
	for range 2 {
		info := h.cachedAccelerators(ctx, node, false)
		if info.Status != "unknown" || info.Total != nil {
			t.Fatalf("failed probe=%+v", info)
		}
	}
	if runner.count() != 1 {
		t.Fatal("failure cache did not suppress repeated probes")
	}
	runner.mu.Lock()
	runner.err = nil
	runner.mu.Unlock()
	h.acceleratorMu.Lock()
	h.acceleratorCache[node.ID].retryAt = time.Now().Add(-time.Second)
	h.acceleratorMu.Unlock()
	if info := h.cachedAccelerators(ctx, node, false); info.Status != "available" {
		t.Fatalf("retry=%+v", info)
	}
	if runner.count() != 2 {
		t.Fatal("expired failure was not retried")
	}
}

func TestWorkerAcceleratorCacheDeduplicatesColdRequestsAndInvalidatesCredentials(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	release := make(chan struct{})
	runner := &countingAcceleratorSSH{started: make(chan struct{}, 16), release: release}
	h := &workerHandlers{ws: workers.NewService(nil, nil, runner, tasks.NewEngine(nil))}
	node := db.WorkerNode{ID: 1, Host: "10.0.0.1", Port: 22, Username: "root"}
	var wg sync.WaitGroup
	for range 8 {
		wg.Add(1)
		go func() {
			defer wg.Done()
			if info := h.cachedAccelerators(ctx, node, false); info.Status != "available" {
				t.Errorf("info=%+v", info)
			}
		}()
	}
	select {
	case <-runner.started:
	case <-ctx.Done():
		t.Fatal("probe not started")
	}
	close(release)
	wg.Wait()
	if runner.count() != 1 {
		t.Fatalf("cold concurrent probes=%d; want 1", runner.count())
	}
	key := "encrypted-key"
	node.EncPrivateKey = &key
	h.cachedAccelerators(ctx, node, false)
	if runner.count() != 2 {
		t.Fatal("changed credentials did not invalidate probe")
	}
	h.pruneAcceleratorCache(nil)
	if len(h.acceleratorCache) != 0 {
		t.Fatal("deleted worker retained in cache")
	}
}
