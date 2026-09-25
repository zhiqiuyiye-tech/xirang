package tasks

import (
	"context"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

type fakeHandler struct {
	steps []string
	fail  bool
}

func (f *fakeHandler) Run(ctx context.Context, task *db.Task, r *Reporter) error {
	for _, name := range f.steps {
		st, err := r.Step(name)
		if err != nil {
			return err
		}
		st.WriteStdout("doing " + name)
		st.Done("succeeded", "doing "+name, "", "")
	}
	if f.fail {
		r.Fail("boom")
		return errFailed
	}
	r.Succeed()
	return nil
}

var errFailed = errBoiler()

func errBoiler() error { return &failErr{} }

type failErr struct{}

func (*failErr) Error() string { return "boom" }

func TestEngineSubmitAndRun(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("fake", &fakeHandler{steps: []string{"a", "b"}})

	id, err := e.Submit(context.Background(), "fake", "worker", 1, map[string]any{"x": 1})
	if err != nil {
		t.Fatal(err)
	}
	waitFor(t, e, id, "succeeded", 2*time.Second)
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "succeeded" {
		t.Fatalf("status=%q", got.Status)
	}
	steps, _ := s.ListSteps(context.Background(), id)
	if len(steps) != 2 {
		t.Fatalf("steps=%d", len(steps))
	}
}

func TestEngineCompletionHookReceivesTerminalTask(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("fake", &fakeHandler{})
	done := make(chan db.Task, 1)
	e.OnComplete(func(task db.Task) { done <- task })
	id, err := e.Submit(context.Background(), "fake", "worker", 42, nil)
	if err != nil {
		t.Fatal(err)
	}
	select {
	case task := <-done:
		if task.ID != id || task.Status != "succeeded" || task.TargetID != 42 {
			t.Fatalf("unexpected completion task: %+v", task)
		}
	case <-time.After(2 * time.Second):
		t.Fatal("completion hook was not called")
	}
}

func TestEngineSubmitFailure(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("failer", &fakeHandler{steps: []string{"a"}, fail: true})
	id, _ := e.Submit(context.Background(), "failer", "worker", 1, nil)
	waitFor(t, e, id, "failed", 2*time.Second)
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "failed" || got.Error == nil {
		t.Fatalf("task=%+v", got)
	}
}

// TestEngineFailDoesNotOverwrite locks in I3: when a handler calls r.Fail()
// with a detailed message and then returns an error, the engine's fallback
// r.Fail(err.Error()) must NOT overwrite the handler's richer detail. The
// first terminal call wins (idempotent Fail).
func TestEngineFailDoesNotOverwrite(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("double-fail", &doubleFailHandler{})
	id, _ := e.Submit(context.Background(), "double-fail", "worker", 1, nil)
	waitFor(t, e, id, "failed", 2*time.Second)
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "failed" || got.Error == nil {
		t.Fatalf("task=%+v", got)
	}
	// The handler's detailed message must survive, not the engine's generic
	// "handler returned error" fallback.
	if *got.Error != "detailed handler error" {
		t.Fatalf("error=%q, want %q", *got.Error, "detailed handler error")
	}
}

// doubleFailHandler calls r.Fail with a detailed message and then returns an
// error. The engine will call r.Fail(err.Error()) again - that second call
// must be a no-op (I3).
type doubleFailHandler struct{}

func (*doubleFailHandler) Run(_ context.Context, _ *db.Task, r *Reporter) error {
	r.Fail("detailed handler error")
	return errGeneric
}

var errGeneric = &genericErr{}

type genericErr struct{}

func (*genericErr) Error() string { return "generic engine fallback" }

func TestEngineUnknownType(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	if _, err := e.Submit(context.Background(), "nope", "worker", 1, nil); err == nil {
		t.Fatal("expected error for unregistered type")
	}
}

// TestEngineRecoversPanic verifies that a panicking task handler fails the
// task instead of crashing the process. gin.Recovery only covers HTTP
// goroutines; task handlers run in engine goroutines.
func TestEngineRecoversPanic(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("panicky", &panicHandler{})
	id, _ := e.Submit(context.Background(), "panicky", "worker", 1, nil)
	waitFor(t, e, id, "failed", 2*time.Second)
	got, _ := s.GetTask(context.Background(), id)
	if got.Error == nil || !strings.Contains(*got.Error, "panicked") {
		t.Fatalf("error=%v, want panic message", got.Error)
	}
}

type panicHandler struct{}

func (*panicHandler) Run(_ context.Context, _ *db.Task, _ *Reporter) error {
	panic("kaboom")
}

// TestEngineSerializesPerTarget verifies the per-target slot: two tasks
// submitted for the same worker never run concurrently, while tasks for
// different workers do. The handler records overlapping executions via an
// atomic counter; maxOverlap must stay at 1 for the same target.
func TestEngineSerializesPerTarget(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)

	var mu sync.Mutex
	overlap, maxOverlap := 0, 0
	track := func() func() {
		mu.Lock()
		overlap++
		if overlap > maxOverlap {
			maxOverlap = overlap
		}
		mu.Unlock()
		return func() {
			mu.Lock()
			overlap--
			mu.Unlock()
		}
	}

	e.Register("slow", handlerFunc(func(ctx context.Context, task *db.Task, r *Reporter) error {
		done := track()
		defer done()
		time.Sleep(100 * time.Millisecond)
		r.Succeed()
		return nil
	}))

	// Two tasks on the same worker: serialized.
	id1, _ := e.Submit(context.Background(), "slow", "worker", 1, nil)
	id2, _ := e.Submit(context.Background(), "slow", "worker", 1, nil)
	waitFor(t, e, id1, "succeeded", 3*time.Second)
	waitFor(t, e, id2, "succeeded", 3*time.Second)
	mu.Lock()
	if maxOverlap != 1 {
		t.Fatalf("maxOverlap=%d, want 1 (same target must serialize)", maxOverlap)
	}
	mu.Unlock()

	// Two tasks on different workers: allowed to overlap.
	maxOverlap = 0
	overlap = 0
	id3, _ := e.Submit(context.Background(), "slow", "worker", 2, nil)
	id4, _ := e.Submit(context.Background(), "slow", "worker", 3, nil)
	waitFor(t, e, id3, "succeeded", 3*time.Second)
	waitFor(t, e, id4, "succeeded", 3*time.Second)
	mu.Lock()
	if maxOverlap != 2 {
		t.Fatalf("maxOverlap=%d, want 2 (different targets must run in parallel)", maxOverlap)
	}
	mu.Unlock()
}

// TestEngineTaskTimeout verifies a task whose handler blocks past the run
// timeout is marked failed with the deadline error rather than running
// forever.
func TestEngineTaskTimeout(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.SetTaskTimeout(100 * time.Millisecond)
	e.Register("blocked", handlerFunc(func(ctx context.Context, task *db.Task, r *Reporter) error {
		<-ctx.Done() // simulate a handler that only stops on ctx cancellation
		return ctx.Err()
	}))
	id, _ := e.Submit(context.Background(), "blocked", "worker", 1, nil)
	waitFor(t, e, id, "failed", 3*time.Second)
	got, _ := s.GetTask(context.Background(), id)
	if got.Error == nil || !strings.Contains(*got.Error, "deadline") {
		t.Fatalf("error=%v, want deadline exceeded", got.Error)
	}
}

// handlerFunc adapts a function to Handler for tests.
type handlerFunc func(ctx context.Context, task *db.Task, r *Reporter) error

func (f handlerFunc) Run(ctx context.Context, task *db.Task, r *Reporter) error {
	return f(ctx, task, r)
}

func TestEngineSubscribeEvents(t *testing.T) {
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	e := NewEngine(s)
	e.Register("fake", &fakeHandler{steps: []string{"a"}})
	id, _ := e.Submit(context.Background(), "fake", "worker", 1, nil)
	ch, cancel := e.Subscribe(id)
	defer cancel()
	var got []StepEvent
	timeout := time.After(2 * time.Second)
	for len(got) < 1 {
		select {
		case ev := <-ch:
			got = append(got, ev)
		case <-timeout:
			t.Fatalf("timed out, got=%v", got)
		}
	}
}

func waitFor(t *testing.T, e *Engine, id int64, want string, timeout time.Duration) {
	t.Helper()
	deadline := time.Now().Add(timeout)
	for time.Now().Before(deadline) {
		got, err := e.store.GetTask(context.Background(), id)
		if err == nil && got.Status == want {
			return
		}
		time.Sleep(10 * time.Millisecond)
	}
	t.Fatalf("task %d never reached %s", id, want)
}
