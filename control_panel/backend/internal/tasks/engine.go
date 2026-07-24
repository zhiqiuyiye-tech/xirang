package tasks

import (
	"context"
	"encoding/json"
	"fmt"
	"sync"

	"xirang/control_panel/internal/db"
)

// Engine is the in-process scheduler for long operations. Handlers are
// registered by type name and run in their own goroutine. Progress is
// recorded to the tasks/task_steps tables and streamed to SSE subscribers.
type Engine struct {
	store    *db.Store
	handlers map[string]Handler
	mu       sync.Mutex
	subs     map[int64][]chan StepEvent
	subsMu   sync.Mutex
}

// NewEngine returns an Engine backed by the given store.
func NewEngine(store *db.Store) *Engine {
	return &Engine{store: store, handlers: map[string]Handler{}, subs: map[int64][]chan StepEvent{}}
}

// Register associates typeName with a handler. Registration is expected to
// happen at startup before any Submit calls.
func (e *Engine) Register(typeName string, h Handler) {
	e.mu.Lock()
	defer e.mu.Unlock()
	e.handlers[typeName] = h
}

// Submit looks up the registered handler, persists a pending task row,
// flips it to running, and launches the handler in a goroutine. Unknown
// types return an error and create no row.
func (e *Engine) Submit(ctx context.Context, typeName, targetKind string, targetID int64, params map[string]any) (int64, error) {
	e.mu.Lock()
	h, ok := e.handlers[typeName]
	e.mu.Unlock()
	if !ok {
		return 0, fmt.Errorf("unknown task type %q", typeName)
	}
	paramsJSON := "{}"
	if params != nil {
		b, err := json.Marshal(params)
		if err != nil {
			return 0, err
		}
		paramsJSON = string(b)
	}
	id, err := e.store.CreateTask(ctx, db.Task{
		Type: typeName, TargetKind: targetKind, TargetID: targetID,
		Status: "pending", ParamsJSON: paramsJSON,
	})
	if err != nil {
		return 0, err
	}
	_ = e.store.SetTaskStatus(ctx, id, "running", false)
	go e.run(id, h)
	return id, nil
}

// run executes the handler. On handler error, the task is marked failed via
// the reporter. Handler-driven Succeed/Fail calls also persist terminal state.
func (e *Engine) run(id int64, h Handler) {
	task, err := e.store.GetTask(context.Background(), id)
	if err != nil {
		return
	}
	r := &Reporter{store: e.store, engine: e, taskID: id}
	if err := h.Run(context.Background(), task, r); err != nil {
		r.Fail(err.Error())
	}
}

// Recover marks any tasks left running/pending from a previous process as
// failed. It does not re-run them.
func (e *Engine) Recover(ctx context.Context) error {
	_, err := e.store.MarkRunningTasksInterrupted(ctx)
	return err
}

// Subscribe registers a buffered channel for StepEvents on the given task.
// After registering, existing task_steps are replayed under the subsMu lock
// so late subscribers (e.g. a frontend opening SSE after task creation)
// still observe history. The returned cancel func removes and closes the
// channel.
func (e *Engine) Subscribe(taskID int64) (<-chan StepEvent, func()) {
	ch := make(chan StepEvent, 16)
	e.subsMu.Lock()
	e.subs[taskID] = append(e.subs[taskID], ch)
	// Replay existing steps while still holding the lock: this guarantees
	// emit cannot drop an event to this channel mid-registration. Late
	// subscribers see history; the replay fills the buffered channel.
	if steps, err := e.store.ListSteps(context.Background(), taskID); err == nil {
		for _, st := range steps {
			select {
			case ch <- StepEvent{TaskID: taskID, StepID: st.ID, Seq: st.Seq, Name: st.Name, Status: st.Status}:
			default:
			}
		}
	}
	e.subsMu.Unlock()
	cancel := func() {
		e.subsMu.Lock()
		defer e.subsMu.Unlock()
		subs := e.subs[taskID]
		for i, c := range subs {
			if c == ch {
				e.subs[taskID] = append(subs[:i], subs[i+1:]...)
				close(c)
				break
			}
		}
	}
	return ch, cancel
}

// emit fans out a StepEvent to all subscribers for the task. Non-blocking:
// if a subscriber's buffer is full, the event is dropped (subscribers are
// expected to keep up; SSE clients dropping events is acceptable).
func (e *Engine) emit(ev StepEvent) {
	e.subsMu.Lock()
	defer e.subsMu.Unlock()
	for _, c := range e.subs[ev.TaskID] {
		select {
		case c <- ev:
		default:
		}
	}
}
