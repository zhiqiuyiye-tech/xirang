package collector

import (
	"context"
	"errors"
	"strings"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

// A reachable SSH server can take longer than five seconds to authenticate,
// establish a session and execute true under load. Respect the supplied deadline
// rather than injecting an unconditional success into the collector.
type slowHeartbeatRunner struct {
	fakeRunner
	delay time.Duration
}

func (r *slowHeartbeatRunner) Run(ctx context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	timer := time.NewTimer(r.delay)
	defer timer.Stop()
	select {
	case <-timer.C:
		return "", "", 0, nil
	case <-ctx.Done():
		return "", "", -1, ctx.Err()
	}
}

func TestDefaultHeartbeatAllowsReachableSlowSSH(t *testing.T) {
	store, id := newTestStore(t)
	c := New(store, &slowHeartbeatRunner{delay: 6 * time.Second}, Config{})
	if err := c.checkHeartbeat(context.Background(), id); err != nil {
		t.Fatalf("reachable slow SSH incorrectly failed heartbeat: %v (timeout %s)", err, c.config.HeartbeatTimeout)
	}
	worker, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if worker.Status != "online" || worker.HealthFailures != 0 || worker.StatusError != nil {
		t.Fatalf("reachable worker did not recover: %+v", worker)
	}
}

func TestHeartbeatTimeoutDiagnosticIncludesConfiguredBudget(t *testing.T) {
	store, id := newTestStore(t)
	c := New(store, &fakeRunner{blockCh: make(chan struct{})}, Config{HeartbeatTimeout: 20 * time.Millisecond, OfflineThreshold: 2})
	for i := 0; i < 2; i++ {
		if err := c.checkHeartbeat(context.Background(), id); !errors.Is(err, context.DeadlineExceeded) {
			t.Fatalf("deadline cause lost: %v", err)
		}
	}
	worker, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if worker.Status != "offline" || worker.StatusError == nil {
		t.Fatalf("permanently stalled worker should remain unhealthy: %+v", worker)
	}
	if !strings.Contains(*worker.StatusError, "20ms") || !strings.Contains(*worker.StatusError, "WORKER_HEARTBEAT_TIMEOUT") {
		t.Fatalf("timeout lacks actionable budget: %q", *worker.StatusError)
	}
}
