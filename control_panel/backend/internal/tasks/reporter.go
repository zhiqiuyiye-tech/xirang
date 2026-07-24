package tasks

import (
	"context"

	"xirang/control_panel/internal/db"
)

// Reporter persists task progress to the store and emits StepEvents through
// the engine so SSE subscribers observe updates. It holds a *Engine reference
// (not just a store) so Done/Succeed/Fail can reach subscribers.
type Reporter struct {
	store  *db.Store
	engine *Engine
	taskID int64
	seq    int
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
	return &StepHandle{r: r, id: id, seq: r.seq, name: name}, nil
}

// WriteStdout is a no-op in this milestone: intermediate stdout is not streamed;
// the final stdout is persisted in Done.
func (s *StepHandle) WriteStdout(_ string) {}

// Done finalizes the step with the given status/output and emits a StepEvent
// to subscribers.
func (s *StepHandle) Done(status, stdout, stderr, errMsg string) {
	_ = s.r.store.UpdateStep(context.Background(), s.id, status, stdout, stderr, errMsg, true)
	s.r.engine.emit(StepEvent{TaskID: s.r.taskID, StepID: s.id, Seq: s.seq, Name: s.name, Status: status})
}

// Succeed marks the task succeeded (finished) and emits a terminal StepEvent.
func (r *Reporter) Succeed() {
	_ = r.store.SetTaskStatus(context.Background(), r.taskID, "succeeded", true)
	r.engine.emit(StepEvent{TaskID: r.taskID, Status: "succeeded"})
}

// Fail records the error message, marks the task failed (finished), and emits
// a terminal StepEvent.
func (r *Reporter) Fail(errMsg string) {
	_ = r.store.SetTaskError(context.Background(), r.taskID, errMsg)
	r.engine.emit(StepEvent{TaskID: r.taskID, Status: "failed"})
}
