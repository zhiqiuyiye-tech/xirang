package db

import (
	"context"
	"testing"
)

func TestCreateTaskAndGet(t *testing.T) {
	s := newStore(t)
	id, err := s.CreateTask(context.Background(), Task{
		Type: "set_root_password", TargetKind: "worker", TargetID: 1, Status: "pending", ParamsJSON: "{}",
	})
	if err != nil {
		t.Fatal(err)
	}
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "pending" {
		t.Fatalf("status=%q", got.Status)
	}
}

func TestSetTaskStatusRunning(t *testing.T) {
	s := newStore(t)
	id, _ := s.CreateTask(context.Background(), Task{Type: "t", TargetKind: "worker", TargetID: 1, Status: "pending", ParamsJSON: "{}"})
	if err := s.SetTaskStatus(context.Background(), id, "running", false); err != nil {
		t.Fatal(err)
	}
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "running" || got.StartedAt == nil {
		t.Fatalf("running not set: %+v", got)
	}
}

func TestSetTaskStatusSucceededSetsFinished(t *testing.T) {
	s := newStore(t)
	id, _ := s.CreateTask(context.Background(), Task{Type: "t", TargetKind: "worker", TargetID: 1, Status: "pending", ParamsJSON: "{}"})
	s.SetTaskStatus(context.Background(), id, "running", false)
	s.SetTaskStatus(context.Background(), id, "succeeded", true)
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "succeeded" || got.FinishedAt == nil {
		t.Fatalf("finished not set: %+v", got)
	}
}

func TestStepsLifecycle(t *testing.T) {
	s := newStore(t)
	tid, _ := s.CreateTask(context.Background(), Task{Type: "t", TargetKind: "worker", TargetID: 1, Status: "pending", ParamsJSON: "{}"})
	sid, _ := s.CreateStep(context.Background(), tid, 1, "chpasswd")
	s.UpdateStep(context.Background(), sid, "succeeded", "ok", "", "", true)
	steps, _ := s.ListSteps(context.Background(), tid)
	if len(steps) != 1 || steps[0].Status != "succeeded" {
		t.Fatalf("steps=%+v", steps)
	}
}

func TestMarkRunningTasksInterrupted(t *testing.T) {
	s := newStore(t)
	id, _ := s.CreateTask(context.Background(), Task{Type: "t", TargetKind: "worker", TargetID: 1, Status: "pending", ParamsJSON: "{}"})
	s.CreateStep(context.Background(), id, 1, "step1")
	s.SetTaskStatus(context.Background(), id, "running", false)
	n, err := s.MarkRunningTasksInterrupted(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if n != 1 {
		t.Fatalf("expected 1 interrupted, got %d", n)
	}
	got, _ := s.GetTask(context.Background(), id)
	if got.Status != "failed" {
		t.Fatalf("status=%q want failed", got.Status)
	}
}
