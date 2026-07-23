package db

import "time"

type Admin struct {
	ID           int64
	Username     string
	PasswordHash string
	CreatedAt    time.Time
}

type WorkerNode struct {
	ID            int64
	Name          string
	Host          string
	Port          int
	Username      string
	AuthMode      string
	EncPassword   *string
	EncPrivateKey *string
	Status        string
	LastSeenAt    *time.Time
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

type Task struct {
	ID         int64
	Type       string
	TargetKind string
	TargetID   int64
	Status     string
	ParamsJSON string
	Error      *string
	CreatedAt  time.Time
	StartedAt  *time.Time
	FinishedAt *time.Time
}

type TaskStep struct {
	ID         int64
	TaskID     int64
	Seq        int
	Name       string
	Status     string
	Stdout     *string
	Stderr     *string
	StartedAt  *time.Time
	FinishedAt *time.Time
	Error      *string
}

type AuditLog struct {
	ID         int64
	Actor      string
	Action     string
	Target     *string
	ParamsJSON *string
	Result     string
	At         time.Time
}
