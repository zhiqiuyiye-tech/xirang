package db

import (
	"context"
	"database/sql"
	"errors"
	"time"
)

func (s *Store) CreateWorker(ctx context.Context, w WorkerNode) (int64, error) {
	now := time.Now().UTC()
	if w.Status == "" {
		w.Status = "unknown"
	}
	if w.AuthMode == "" {
		w.AuthMode = "key"
	}
	res, err := s.db.ExecContext(ctx,
		`INSERT INTO worker_nodes (name, host, port, username, auth_mode, enc_password, enc_private_key, status, created_at, updated_at)
		 VALUES (?,?,?,?,?,?,?,? ,?,?)`,
		w.Name, w.Host, w.Port, w.Username, w.AuthMode, w.EncPassword, w.EncPrivateKey, w.Status, now, now)
	if err != nil {
		return 0, err
	}
	return res.LastInsertId()
}

func (s *Store) ListWorkers(ctx context.Context) ([]WorkerNode, error) {
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, name, host, port, username, auth_mode, enc_password, enc_private_key, status, last_seen_at, created_at, updated_at
		 FROM worker_nodes ORDER BY id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []WorkerNode
	for rows.Next() {
		var w WorkerNode
		if err := rows.Scan(&w.ID, &w.Name, &w.Host, &w.Port, &w.Username, &w.AuthMode, &w.EncPassword, &w.EncPrivateKey, &w.Status, &w.LastSeenAt, &w.CreatedAt, &w.UpdatedAt); err != nil {
			return nil, err
		}
		out = append(out, w)
	}
	return out, rows.Err()
}

func (s *Store) GetWorker(ctx context.Context, id int64) (*WorkerNode, error) {
	var w WorkerNode
	err := s.db.QueryRowContext(ctx,
		`SELECT id, name, host, port, username, auth_mode, enc_password, enc_private_key, status, last_seen_at, created_at, updated_at
		 FROM worker_nodes WHERE id=?`, id,
	).Scan(&w.ID, &w.Name, &w.Host, &w.Port, &w.Username, &w.AuthMode, &w.EncPassword, &w.EncPrivateKey, &w.Status, &w.LastSeenAt, &w.CreatedAt, &w.UpdatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &w, nil
}

func (s *Store) UpdateWorker(ctx context.Context, w WorkerNode) error {
	_, err := s.db.ExecContext(ctx,
		`UPDATE worker_nodes SET name=?, host=?, port=?, username=?, updated_at=? WHERE id=?`,
		w.Name, w.Host, w.Port, w.Username, time.Now().UTC(), w.ID)
	return err
}

func (s *Store) DeleteWorker(ctx context.Context, id int64) error {
	_, err := s.db.ExecContext(ctx, "DELETE FROM worker_nodes WHERE id=?", id)
	return err
}

func (s *Store) SetWorkerCredentials(ctx context.Context, id int64, encPassword, encPrivateKey *string, authMode string) error {
	_, err := s.db.ExecContext(ctx,
		`UPDATE worker_nodes SET enc_password=?, enc_private_key=?, auth_mode=?, updated_at=? WHERE id=?`,
		encPassword, encPrivateKey, authMode, time.Now().UTC(), id)
	return err
}

func (s *Store) SetWorkerStatus(ctx context.Context, id int64, status string) error {
	_, err := s.db.ExecContext(ctx,
		`UPDATE worker_nodes SET status=?, last_seen_at=?, updated_at=? WHERE id=?`,
		status, time.Now().UTC(), time.Now().UTC(), id)
	return err
}
