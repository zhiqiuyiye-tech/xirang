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
