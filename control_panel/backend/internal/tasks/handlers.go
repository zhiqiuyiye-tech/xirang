package tasks

import (
	"context"

	"xirang/control_panel/internal/db"
)

// Handler runs a long operation on behalf of the engine. Implementations
// record progress via the Reporter and return nil on success; a non-nil
// error causes the engine to mark the task failed.
type Handler interface {
	Run(ctx context.Context, task *db.Task, r *Reporter) error
}

// StepEvent is emitted by the engine whenever a step (or the task itself)
// transitions state. Subscribers receive these on their channel.
type StepEvent struct {
	TaskID int64
	StepID int64
	Seq    int
	Name   string
	Status string
}
