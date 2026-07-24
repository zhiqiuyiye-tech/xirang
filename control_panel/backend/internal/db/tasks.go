package db

import (
	"context"
	"database/sql"
	"errors"
	"time"
)

func (s *Store) CreateTask(ctx context.Context, t Task) (int64, error) {
	if t.CreatedAt.IsZero() {
		t.CreatedAt = time.Now().UTC()
	}
	res, err := s.db.ExecContext(ctx,
		`INSERT INTO tasks (type, target_kind, target_id, status, params_json, created_at)
		 VALUES (?,?,?,?,?,?)`,
		t.Type, t.TargetKind, t.TargetID, t.Status, t.ParamsJSON, t.CreatedAt)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) GetTask(ctx context.Context, id int64) (*Task, error) {
	var t Task
	err := s.db.QueryRowContext(ctx,
		`SELECT id, type, target_kind, target_id, status, params_json, error, created_at, started_at, finished_at
		 FROM tasks WHERE id=?`, id,
	).Scan(&t.ID, &t.Type, &t.TargetKind, &t.TargetID, &t.Status, &t.ParamsJSON, &t.Error, &t.CreatedAt, &t.StartedAt, &t.FinishedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &t, nil
}

func (s *Store) ListTasks(ctx context.Context, limit int) ([]Task, error) {
	if limit <= 0 {
		limit = 100
	}
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, type, target_kind, target_id, status, params_json, error, created_at, started_at, finished_at
		 FROM tasks ORDER BY id DESC LIMIT ?`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []Task
	for rows.Next() {
		var t Task
		if err := rows.Scan(&t.ID, &t.Type, &t.TargetKind, &t.TargetID, &t.Status, &t.ParamsJSON, &t.Error, &t.CreatedAt, &t.StartedAt, &t.FinishedAt); err != nil {
			return nil, err
		}
		out = append(out, t)
	}
	return out, rows.Err()
}

func (s *Store) SetTaskStatus(ctx context.Context, id int64, status string, finished bool) error {
	now := time.Now().UTC()
	if finished {
		_, err := s.db.ExecContext(ctx,
			`UPDATE tasks SET status=?, finished_at=? WHERE id=?`, status, now, id)
		return err
	}
	if status == "running" {
		_, err := s.db.ExecContext(ctx,
			`UPDATE tasks SET status=?, started_at=COALESCE(started_at,?) WHERE id=?`, status, now, id)
		return err
	}
	_, err := s.db.ExecContext(ctx, `UPDATE tasks SET status=? WHERE id=?`, status, id)
	return err
}

func (s *Store) SetTaskError(ctx context.Context, id int64, errMsg string) error {
	_, err := s.db.ExecContext(ctx,
		`UPDATE tasks SET error=?, status='failed', finished_at=? WHERE id=?`,
		errMsg, time.Now().UTC(), id)
	return err
}

func (s *Store) CreateStep(ctx context.Context, taskID int64, seq int, name string) (int64, error) {
	now := time.Now().UTC()
	res, err := s.db.ExecContext(ctx,
		`INSERT INTO task_steps (task_id, seq, name, status, started_at) VALUES (?,?,?,?,?)`,
		taskID, seq, name, "running", now)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) UpdateStep(ctx context.Context, stepID int64, status, stdout, stderr, errMsg string, finished bool) error {
	if finished {
		_, err := s.db.ExecContext(ctx,
			`UPDATE task_steps SET status=?, stdout=?, stderr=?, error=?, finished_at=? WHERE id=?`,
			status, stdout, stderr, errMsg, time.Now().UTC(), stepID)
		return err
	}
	_, err := s.db.ExecContext(ctx,
		`UPDATE task_steps SET status=?, stdout=?, stderr=?, error=? WHERE id=?`,
		status, stdout, stderr, errMsg, stepID)
	return err
}

func (s *Store) ListSteps(ctx context.Context, taskID int64) ([]TaskStep, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, task_id, seq, name, status, stdout, stderr, started_at, finished_at, error
		 FROM task_steps WHERE task_id=? ORDER BY seq`, taskID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []TaskStep
	for rows.Next() {
		var st TaskStep
		if err := rows.Scan(&st.ID, &st.TaskID, &st.Seq, &st.Name, &st.Status, &st.Stdout, &st.Stderr, &st.StartedAt, &st.FinishedAt, &st.Error); err != nil {
			return nil, err
		}
		out = append(out, st)
	}
	return out, rows.Err()
}

// MarkRunningTasksInterrupted 将所有 running 的 task（及其 running 步骤）标记为 failed。
// 返回受影响的 task 行数。仅用于启动恢复。
func (s *Store) MarkRunningTasksInterrupted(ctx context.Context) (int, error) {
	now := time.Now().UTC()
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()
	res, err := tx.ExecContext(ctx,
		`UPDATE tasks SET status='failed', error='interrupted by restart', finished_at=? WHERE status IN ('running','pending')`, now)
	if err != nil {
		return 0, err
	}
	n, _ := res.RowsAffected()
	if _, err := tx.ExecContext(ctx,
		`UPDATE task_steps SET status='failed', finished_at=? WHERE status='running'`, now); err != nil {
		return 0, err
	}
	return int(n), tx.Commit()
}
