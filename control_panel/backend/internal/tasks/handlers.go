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
	TaskID int64  `json:"task_id"`
	StepID int64  `json:"step_id"`
	Seq    int    `json:"seq"`
	Name   string `json:"name"`
	Status string `json:"status"`
	Stdout string `json:"stdout,omitempty"`
	Stderr string `json:"stderr,omitempty"`
	Error  string `json:"error,omitempty"`
}
