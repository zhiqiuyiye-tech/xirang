package tasks

import (
	"context"

	"xirang/control_panel/internal/db"
)

// Reporter persists task progress to the store and emits StepEvents through
// the engine so SSE subscribers observe updates. It holds a *Engine reference
// (not just a store) so Done/Succeed/Fail can reach subscribers.
//
// The finalized field makes Succeed/Fail idempotent: the first terminal call
// wins and subsequent calls are no-ops. This prevents the engine's
// post-handler r.Fail(err.Error()) from overwriting richer error detail that
// the handler already recorded via its own r.Fail(...).
type Reporter struct {
	store     *db.Store
	engine    *Engine
	taskID    int64
	seq       int
	finalized bool
}

// StepHandle represents an in-flight step created via Reporter.Step.
type StepHandle struct {
	r    *Reporter
	id   int64
	seq  int
	name string
}

// Step creates a new task_steps row (status running) and returns a handle
// the handler uses to finalize the step.
func (r *Reporter) Step(name string) (*StepHandle, error) {
	r.seq++
	id, err := r.store.CreateStep(context.Background(), r.taskID, r.seq, name)
	if err != nil {
		return nil, err
	}
	r.engine.emit(StepEvent{TaskID: r.taskID, StepID: id, Seq: r.seq, Name: name, Status: "running"})
	return &StepHandle{r: r, id: id, seq: r.seq, name: name}, nil
}

// WriteStdout is a no-op in this milestone: intermediate stdout is not streamed;
// the final stdout is persisted in Done.
func (s *StepHandle) WriteStdout(_ string) {}

// Done finalizes the step with the given status/output and emits a StepEvent
// to subscribers.
func (s *StepHandle) Done(status, stdout, stderr, errMsg string) {
	_ = s.r.store.UpdateStep(context.Background(), s.id, status, stdout, stderr, errMsg, true)
	s.r.engine.emit(StepEvent{
		TaskID: s.r.taskID,
		StepID: s.id,
		Seq:    s.seq,
		Name:   s.name,
		Status: status,
		Stdout: stdout,
		Stderr: stderr,
		Error:  errMsg,
	})
}

// Succeed marks the task succeeded (finished) and emits a terminal StepEvent.
// No-op if the task is already finalized (Fail or Succeed was called earlier).
func (r *Reporter) Succeed() {
	if r.finalized {
		return
	}
	r.finalized = true
	_ = r.store.SetTaskStatus(context.Background(), r.taskID, "succeeded", true)
	r.engine.emit(StepEvent{TaskID: r.taskID, Status: "succeeded"})
}

// Fail records the error message, marks the task failed (finished), and emits
// a terminal StepEvent. No-op if the task is already finalized, so the first
// terminal call (typically from the handler with rich detail) is preserved
// and the engine's fallback r.Fail(err.Error()) after a handler error is a
// safe no-op.
func (r *Reporter) Fail(errMsg string) {
	if r.finalized {
		return
	}
	r.finalized = true
	_ = r.store.SetTaskError(context.Background(), r.taskID, errMsg)
	r.engine.emit(StepEvent{TaskID: r.taskID, Status: "failed"})
}
