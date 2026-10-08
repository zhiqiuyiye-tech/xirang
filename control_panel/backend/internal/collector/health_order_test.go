package collector

import (
	"context"
	"errors"
	"io"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

type orderedHealthRunner struct {
	blockHeartbeat bool
	started        chan struct{}
	release        chan struct{}
}

func (r *orderedHealthRunner) Run(ctx context.Context, _ db.WorkerNode, command string) (string, string, int, error) {
	heartbeat := command == "true"
	if heartbeat == r.blockHeartbeat {
		close(r.started)
		select {
		case <-r.release:
		case <-ctx.Done():
			return "", "", -1, ctx.Err()
		}
	}
	if heartbeat {
		return "", "", -1, errors.New("connection refused")
	}
	return "###LSBLK###\n", "", 0, nil
}
func (r *orderedHealthRunner) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, _ io.Reader) (string, string, int, error) {
	return r.Run(ctx, w, cmd)
}

func TestConcurrentHeartbeatAndInventoryUseLatestStartedCheck(t *testing.T) {
	for _, blockHeartbeat := range []bool{true, false} {
		t.Run(map[bool]string{true: "old_heartbeat", false: "old_inventory"}[blockHeartbeat], func(t *testing.T) {
			store, id := newTestStore(t)
			runner := &orderedHealthRunner{blockHeartbeat: blockHeartbeat, started: make(chan struct{}), release: make(chan struct{})}
			c := New(store, runner, Config{HeartbeatTimeout: time.Second, InventoryTimeout: time.Second, OfflineThreshold: 1})
			ctx := context.Background()
			done := make(chan error, 1)
			if blockHeartbeat {
				go func() { done <- c.checkHeartbeat(ctx, id) }()
			} else {
				go func() { done <- c.collectInventory(ctx, id) }()
			}
			select {
			case <-runner.started:
			case <-time.After(time.Second):
				t.Fatal("older check did not start")
			}
			if blockHeartbeat {
				if err := c.collectInventory(ctx, id); err != nil {
					t.Fatal(err)
				}
			} else {
				if err := c.checkHeartbeat(ctx, id); err == nil {
					t.Fatal("expected heartbeat failure")
				}
			}
			before, err := store.GetWorker(ctx, id)
			if err != nil {
				t.Fatal(err)
			}
			close(runner.release)
			<-done
			after, err := store.GetWorker(ctx, id)
			if err != nil {
				t.Fatal(err)
			}
			if before.Status != after.Status || before.HealthFailures != after.HealthFailures || !before.LastCheckedAt.Equal(*after.LastCheckedAt) {
				t.Fatalf("older concurrent check overwrote latest: before=%+v after=%+v", before, after)
			}
			want := "offline"
			if blockHeartbeat {
				want = "online"
			}
			if after.Status != want {
				t.Fatalf("status=%s want %s", after.Status, want)
			}
		})
	}
}

func TestHeartbeatOwnDeadlineCountsAsFailure(t *testing.T) {
	store, id := newTestStore(t)
	c := New(store, &fakeRunner{blockCh: make(chan struct{})}, Config{HeartbeatTimeout: 10 * time.Millisecond, OfflineThreshold: 2})
	for i := 0; i < 2; i++ {
		if err := c.checkHeartbeat(context.Background(), id); !errors.Is(err, context.DeadlineExceeded) {
			t.Fatalf("err=%v", err)
		}
	}
	w, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "offline" || w.HealthFailures != 2 {
		t.Fatalf("heartbeat deadlines did not reach offline threshold: %+v", w)
	}
}
