package tasks

import (
	"context"
	"path/filepath"
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
