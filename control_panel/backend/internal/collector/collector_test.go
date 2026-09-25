package collector

import (
	"context"
	"errors"
	"io"
	"path/filepath"
	"sync"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

type fakeRunner struct {
	mu      sync.Mutex
	calls   []string
	out     string
	stderr  string
	code    int
	err     error
	blockCh chan struct{}
}

func (f *fakeRunner) Run(ctx context.Context, _ db.WorkerNode, command string) (string, string, int, error) {
	f.mu.Lock()
	f.calls = append(f.calls, command)
	block := f.blockCh
	out, stderr, code, err := f.out, f.stderr, f.code, f.err
	f.mu.Unlock()
	if block != nil {
		select {
		case <-block:
		case <-ctx.Done():
			return "", "", -1, ctx.Err()
		}
	}
	return out, stderr, code, err
}

func (f *fakeRunner) RunWithStdin(ctx context.Context, worker db.WorkerNode, command string, _ io.Reader) (string, string, int, error) {
	return f.Run(ctx, worker, command)
}

func (f *fakeRunner) callCount() int {
	f.mu.Lock()
	defer f.mu.Unlock()
	return len(f.calls)
}

func newTestStore(t *testing.T) (*db.Store, int64) {
	t.Helper()
	store, err := db.Open(filepath.Join(t.TempDir(), "collector.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	id, err := store.CreateWorker(context.Background(), db.WorkerNode{Name: "w", Host: "127.0.0.1", Port: 22, Username: "root", AuthMode: "password"})
	if err != nil {
		t.Fatal(err)
	}
	return store, id
}

func TestCollectInventoryPersistsLastGoodAndFailureMetadata(t *testing.T) {
	store, workerID := newTestStore(t)
	runner := &fakeRunner{out: "###VGS###\n###LVS###\n###PVS###\n###DF###\n###NFS###\ninactive\n###EXPORTS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="10000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""`}
	c := New(store, runner, Config{InventoryTimeout: time.Second, HeartbeatTimeout: time.Second, Concurrency: 1, ReservedMounts: []string{"/data01"}})
	if err := c.collectInventory(context.Background(), workerID); err != nil {
		t.Fatal(err)
	}
	first, err := store.GetInventorySnapshot(context.Background(), workerID)
	if err != nil || first.CollectedAt == nil || first.PayloadJSON == "" {
		t.Fatalf("successful snapshot missing: %+v err=%v", first, err)
	}

	runner.mu.Lock()
	runner.err = errors.New("ssh timeout")
	runner.mu.Unlock()
	if err := c.collectInventory(context.Background(), workerID); err == nil {
		t.Fatal("expected inventory failure")
	}
	after, _ := store.GetInventorySnapshot(context.Background(), workerID)
	if after.PayloadJSON != first.PayloadJSON || after.CollectedAt == nil || !after.CollectedAt.Equal(*first.CollectedAt) {
		t.Fatalf("failed collection overwrote last good data: before=%+v after=%+v", first, after)
	}
	if after.LastError == nil || *after.LastError == "" {
		t.Fatalf("failure metadata missing: %+v", after)
	}
}

func TestHeartbeatUsesOfflineThresholdAndRecovers(t *testing.T) {
	store, workerID := newTestStore(t)
	runner := &fakeRunner{err: errors.New("connection refused"), code: -1}
	c := New(store, runner, Config{HeartbeatTimeout: time.Second, InventoryTimeout: time.Second, Concurrency: 1, OfflineThreshold: 2})
	_ = c.checkHeartbeat(context.Background(), workerID)
	worker, _ := store.GetWorker(context.Background(), workerID)
	if worker.Status != "unknown" {
		t.Fatalf("first failure should preserve unknown, got %s", worker.Status)
	}
	_ = c.checkHeartbeat(context.Background(), workerID)
	worker, _ = store.GetWorker(context.Background(), workerID)
	if worker.Status != "offline" {
		t.Fatalf("second failure should mark offline: %+v", worker)
	}
	runner.mu.Lock()
	runner.err = nil
	runner.code = 0
	runner.mu.Unlock()
	if err := c.checkHeartbeat(context.Background(), workerID); err != nil {
		t.Fatal(err)
	}
	worker, _ = store.GetWorker(context.Background(), workerID)
	if worker.Status != "online" || worker.HealthFailures != 0 {
		t.Fatalf("success should recover worker: %+v", worker)
	}
}

func TestInventoryRequestsAreDeduplicatedWhileQueuedOrRunning(t *testing.T) {
	store, workerID := newTestStore(t)
	block := make(chan struct{})
	runner := &fakeRunner{blockCh: block, out: "###LSBLK###\n"}
	c := New(store, runner, Config{
		HeartbeatInterval: time.Hour, InventoryInterval: time.Hour,
		HeartbeatTimeout: time.Second, InventoryTimeout: time.Second, Concurrency: 1,
	})
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	c.Start(ctx)
	if !c.EnqueueInventory(workerID) {
		t.Fatal("first request should enqueue")
	}
	if c.EnqueueInventory(workerID) {
		t.Fatal("duplicate request should be coalesced")
	}
	deadline := time.Now().Add(time.Second)
	for runner.callCount() == 0 && time.Now().Before(deadline) {
		time.Sleep(time.Millisecond)
	}
	if !c.IsInventoryRefreshing(workerID) {
		t.Fatal("worker should report refreshing while command is blocked")
	}
	close(block)
	deadline = time.Now().Add(time.Second)
	for c.IsInventoryRefreshing(workerID) && time.Now().Before(deadline) {
		time.Sleep(time.Millisecond)
	}
	if c.IsInventoryRefreshing(workerID) || runner.callCount() != 1 {
		t.Fatalf("request did not finish exactly once: refreshing=%v calls=%d", c.IsInventoryRefreshing(workerID), runner.callCount())
	}
}
