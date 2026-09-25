package tasks

import (
	"context"
	"encoding/json"
	"fmt"
	"sync"
	"time"

	"xirang/control_panel/internal/db"
)

// defaultTaskTimeout bounds a single task run. Storage tasks SSH into worker
// nodes and run mkfs/lvcreate-class commands; a wedged remote command must
// not hold the task (and its per-target slot) open forever.
const defaultTaskTimeout = 30 * time.Minute

// maxConcurrentTasks caps the number of task goroutines executing at once.
// Per-target serialization already bounds load per worker; this bounds the
// panel's own goroutine/SSH-connection usage when tasks target many workers.
const maxConcurrentTasks = 16

// Engine is the in-process scheduler for long operations. Handlers are
// registered by type name and run in their own goroutine. Progress is
// recorded to the tasks/task_steps tables and streamed to SSE subscribers.
//
// Execution guarantees:
//   - at most one task runs per target at a time (worker-scoped serialization
//     so LVM/fstab/exports edits on one node never interleave; different
//     workers run in parallel),
//   - each task is bounded by a total timeout (SetTaskTimeout, default 30m),
//   - a panicking handler fails the task instead of killing the process.
type Engine struct {
	store    *db.Store
	handlers map[string]Handler
	mu       sync.Mutex
	subs     map[int64][]chan StepEvent
	subsMu   sync.Mutex

	// Optional terminal task observers (for cache invalidation/refresh).
	completionHooks []func(db.Task)

	// taskTimeout bounds each run; guarded by mu.
	taskTimeout time.Duration

	// slotsMu guards slots - the per-target serialization semaphores.
	slotsMu sync.Mutex
	slots   map[string]chan struct{}

	// inflight caps globally concurrent task goroutines.
	inflight chan struct{}
}

// NewEngine returns an Engine backed by the given store.
func NewEngine(store *db.Store) *Engine {
	return &Engine{
		store:       store,
		handlers:    map[string]Handler{},
		subs:        map[int64][]chan StepEvent{},
		taskTimeout: defaultTaskTimeout,
		slots:       map[string]chan struct{}{},
		inflight:    make(chan struct{}, maxConcurrentTasks),
	}
}

// SetTaskTimeout overrides the per-task run timeout. Call before serving
// traffic (main.go wires it from config). Non-positive values reset to the
// default.
func (e *Engine) SetTaskTimeout(d time.Duration) {
	if d <= 0 {
		d = defaultTaskTimeout
	}
	e.mu.Lock()
	e.taskTimeout = d
	e.mu.Unlock()
}

func (e *Engine) timeout() time.Duration {
	e.mu.Lock()
	defer e.mu.Unlock()
	return e.taskTimeout
}

// Register associates typeName with a handler. Registration is expected to
// happen at startup before any Submit calls.
func (e *Engine) Register(typeName string, h Handler) {
	e.mu.Lock()
	defer e.mu.Unlock()
	e.handlers[typeName] = h
}

// OnComplete registers an observer invoked after a task reaches a terminal
// state. Hooks must return quickly; panics are isolated from the task engine.
func (e *Engine) OnComplete(hook func(db.Task)) {
	if hook == nil {
		return
	}
	e.mu.Lock()
	defer e.mu.Unlock()
	e.completionHooks = append(e.completionHooks, hook)
}

func (e *Engine) notifyCompletion(id int64) {
	task, err := e.store.GetTask(context.Background(), id)
	if err != nil || (task.Status != "succeeded" && task.Status != "failed") {
		return
	}
	e.mu.Lock()
	hooks := append([]func(db.Task){}, e.completionHooks...)
	e.mu.Unlock()
	for _, hook := range hooks {
		func() {
			defer func() { _ = recover() }()
			hook(*task)
		}()
	}
}

// Submit looks up the registered handler, persists a pending task row, and
// launches the handler in a goroutine. The task row stays "pending" while it
// is queued behind another task on the same target and is flipped to
// "running" only when the handler actually starts (see run). Unknown types
// return an error and create no row.
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
	go e.run(id, targetKind, targetID, h)
	return id, nil
}

// slotFor returns (creating on first use) the serialization semaphore for a
// target. Keyed by kind+id: worker 3 and worker 4 have independent slots.
func (e *Engine) slotFor(targetKind string, targetID int64) chan struct{} {
	key := targetKind + "/" + fmt.Sprint(targetID)
	e.slotsMu.Lock()
	defer e.slotsMu.Unlock()
	if c, ok := e.slots[key]; ok {
		return c
	}
	c := make(chan struct{}, 1)
	e.slots[key] = c
	return c
}

// run executes the handler. The task is flipped to running only after its
// slot is acquired, so "running" means the handler is actually executing.
// On handler error or panic, the task is marked failed via the reporter.
// Handler-driven Succeed/Fail calls also persist terminal state.
func (e *Engine) run(id int64, targetKind string, targetID int64, h Handler) {
	task, err := e.store.GetTask(context.Background(), id)
	if err != nil {
		return
	}
	r := &Reporter{store: e.store, engine: e, taskID: id}
	defer e.notifyCompletion(id)

	// Serialize per target: at most one task goroutine per target executes at
	// a time. The previous task's own timeout guarantees the queue drains.
	slot := e.slotFor(targetKind, targetID)
	slot <- struct{}{}
	defer func() { <-slot }()

	// Global cap on concurrently running tasks.
	e.inflight <- struct{}{}
	defer func() { <-e.inflight }()

	// Recover panics: gin.Recovery only covers HTTP goroutines, task handlers
	// run here. A panic must fail the task, not take down the process.
	defer func() {
		if p := recover(); p != nil {
			r.Fail(fmt.Sprintf("task handler panicked: %v", p))
		}
	}()

	_ = e.store.SetTaskStatus(context.Background(), id, "running", false)

	ctx, cancel := context.WithTimeout(context.Background(), e.timeout())
	defer cancel()
	if err := h.Run(ctx, task, r); err != nil {
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
// Existing task_steps are replayed so late subscribers (e.g. a frontend
// opening SSE after task creation) still observe history. The returned cancel
// func removes and closes the channel.
//
// The replay query runs AFTER registration but OUTSIDE the subsMu lock: a DB
// query under the lock would stall every other Subscribe and every emit. A
// step that is both replayed and live-emitted between registration and the
// query is delivered twice; consumers treat StepEvents as idempotent status
// updates keyed by Seq (the frontend upserts by seq).
func (e *Engine) Subscribe(taskID int64) (<-chan StepEvent, func()) {
	ch := make(chan StepEvent, 16)
	e.subsMu.Lock()
	e.subs[taskID] = append(e.subs[taskID], ch)
	e.subsMu.Unlock()
	if steps, err := e.store.ListSteps(context.Background(), taskID); err == nil {
		for _, st := range steps {
			select {
			case ch <- StepEvent{TaskID: taskID, StepID: st.ID, Seq: st.Seq, Name: st.Name, Status: st.Status}:
			default:
			}
		}
	}
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
