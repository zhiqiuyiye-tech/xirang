package db

import "time"

type Admin struct {
	ID           int64     `json:"id"`
	Username     string    `json:"username"`
	PasswordHash string    `json:"-"`
	CreatedAt    time.Time `json:"created_at"`
}

type WorkerNode struct {
	ID            int64      `json:"id"`
	Name          string     `json:"name"`
	Host          string     `json:"host"`
	Port          int        `json:"port"`
	Username      string     `json:"username"`
	AuthMode      string     `json:"auth_mode"`
	EncPassword   *string    `json:"-"`
	EncPrivateKey *string    `json:"-"`
	Status        string     `json:"status"`
	LastSeenAt    *time.Time `json:"last_seen_at"`
	CreatedAt     time.Time  `json:"created_at"`
	UpdatedAt     time.Time  `json:"updated_at"`
}

type Task struct {
	ID         int64      `json:"id"`
	Type       string     `json:"type"`
	TargetKind string     `json:"target_kind"`
	TargetID   int64      `json:"target_id"`
	Status     string     `json:"status"`
	ParamsJSON string     `json:"-"`
	Error      *string    `json:"error"`
	CreatedAt  time.Time  `json:"created_at"`
	StartedAt  *time.Time `json:"started_at"`
	FinishedAt *time.Time `json:"finished_at"`
}

type TaskStep struct {
	ID         int64      `json:"id"`
	TaskID     int64      `json:"task_id"`
	Seq        int        `json:"seq"`
	Name       string     `json:"name"`
	Status     string     `json:"status"`
	Stdout     *string    `json:"stdout"`
	Stderr     *string    `json:"stderr"`
	StartedAt  *time.Time `json:"started_at"`
	FinishedAt *time.Time `json:"finished_at"`
	Error      *string    `json:"error"`
}

type AuditLog struct {
	ID         int64      `json:"id"`
	Actor      string     `json:"actor"`
	Action     string     `json:"action"`
	Target     *string    `json:"target"`
	ParamsJSON *string    `json:"-"`
	Result     string     `json:"result"`
	At         time.Time  `json:"at"`
}
