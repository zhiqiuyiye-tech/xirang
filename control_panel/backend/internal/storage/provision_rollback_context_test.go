package storage

import (
	"context"
	"errors"
	"io"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

type rollbackBudgetRunner struct {
	mu        sync.Mutex
	ctxError  error
	remaining time.Duration
	transport bool
}

func (r *rollbackBudgetRunner) Run(ctx context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.ctxError = ctx.Err()
	if deadline, ok := ctx.Deadline(); ok {
		r.remaining = time.Until(deadline)
	}
	if ctx.Err() != nil {
		return "", "", 1, ctx.Err()
	}
	if r.transport {
		return "", "", 0, errors.New("rollback transport failure")
	}
	return "removed", "", 0, nil
}
func (r *rollbackBudgetRunner) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, _ io.Reader) (string, string, int, error) {
	return r.Run(ctx, w, cmd)
}

type rollbackBudgetHandler struct {
	runner  *rollbackBudgetRunner
	expired bool
}

func (h rollbackBudgetHandler) Run(ctx context.Context, _ *db.Task, reporter *tasks.Reporter) error {
	if h.expired {
		var cancel context.CancelFunc
		ctx, cancel = context.WithCancel(ctx)
		cancel()
	}
	(&provisionHandler{runner: h.runner}).rollback(ctx, db.WorkerNode{ID: 1}, reporter,
		ProvisionReq{VGName: "vg_data", LVName: "lv_created", MountPoint: "/data02/created"}, []string{"lvcreate"})
	reporter.Fail("original provisioning failure")
	return errors.New("original provisioning failure")
}

func TestProvisionRollbackHasIndependentBoundedContext(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "rollback.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	runner := &rollbackBudgetRunner{}
	engine := tasks.NewEngine(store)
	engine.Register("rollback-budget", rollbackBudgetHandler{runner: runner, expired: true})
	id, err := engine.Submit(context.Background(), "rollback-budget", "storage", 1, nil)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	runner.mu.Lock()
	defer runner.mu.Unlock()
	if runner.ctxError != nil || runner.remaining <= 0 || runner.remaining > 30*time.Second {
		t.Fatalf("cleanup inherited expired task context: err=%v remaining=%s", runner.ctxError, runner.remaining)
	}
}

func TestProvisionRollbackRecordsTransportFailure(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "rollback-transport.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	runner := &rollbackBudgetRunner{transport: true}
	engine := tasks.NewEngine(store)
	engine.Register("rollback-transport", rollbackBudgetHandler{runner: runner})
	id, err := engine.Submit(context.Background(), "rollback-transport", "storage", 1, nil)
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, store, id, "failed", 2*time.Second)
	steps, err := store.ListSteps(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if len(steps) != 1 || steps[0].Status != "failed" || steps[0].Error == nil || !strings.Contains(*steps[0].Error, "rollback transport failure") {
		t.Fatalf("transport failure reported as cleanup success: %+v", steps)
	}
}
