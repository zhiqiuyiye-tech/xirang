package db

import (
	"context"
	"database/sql"
	"errors"
	"time"
)

func (s *Store) SaveInventorySnapshot(ctx context.Context, snapshot InventorySnapshot) error {
	now := time.Now().UTC()
	_, err := s.db.ExecContext(ctx, `
INSERT INTO storage_inventory_snapshots
  (worker_id, schema_version, payload_json, collected_at, last_attempted_at, last_error, updated_at)
VALUES (?, ?, ?, ?, ?, NULL, ?)
ON CONFLICT(worker_id) DO UPDATE SET
  schema_version=excluded.schema_version,
  payload_json=excluded.payload_json,
  collected_at=excluded.collected_at,
  last_attempted_at=excluded.last_attempted_at,
  last_error=NULL,
  updated_at=excluded.updated_at`,
		snapshot.WorkerID, snapshot.SchemaVersion, snapshot.PayloadJSON, snapshot.CollectedAt,
		snapshot.LastAttemptedAt, now)
	return err
}

func (s *Store) RecordInventoryFailure(ctx context.Context, workerID int64, attemptedAt time.Time, message string) error {
	now := time.Now().UTC()
	_, err := s.db.ExecContext(ctx, `
INSERT INTO storage_inventory_snapshots
  (worker_id, schema_version, payload_json, collected_at, last_attempted_at, last_error, updated_at)
VALUES (?, 1, '', NULL, ?, ?, ?)
ON CONFLICT(worker_id) DO UPDATE SET
  last_attempted_at=excluded.last_attempted_at,
  last_error=excluded.last_error,
  updated_at=excluded.updated_at`, workerID, attemptedAt, message, now)
	return err
}

func (s *Store) GetInventorySnapshot(ctx context.Context, workerID int64) (*InventorySnapshot, error) {
	var snapshot InventorySnapshot
	err := s.db.QueryRowContext(ctx, `
SELECT worker_id, schema_version, payload_json, collected_at, last_attempted_at, last_error, updated_at
FROM storage_inventory_snapshots WHERE worker_id=?`, workerID).Scan(
		&snapshot.WorkerID, &snapshot.SchemaVersion, &snapshot.PayloadJSON, &snapshot.CollectedAt,
		&snapshot.LastAttemptedAt, &snapshot.LastError, &snapshot.UpdatedAt,
	)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &snapshot, nil
}

func (s *Store) ListInventorySnapshots(ctx context.Context) ([]InventorySnapshot, error) {
	rows, err := s.db.QueryContext(ctx, `
SELECT worker_id, schema_version, payload_json, collected_at, last_attempted_at, last_error, updated_at
FROM storage_inventory_snapshots ORDER BY worker_id`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	out := make([]InventorySnapshot, 0)
	for rows.Next() {
		var snapshot InventorySnapshot
		if err := rows.Scan(&snapshot.WorkerID, &snapshot.SchemaVersion, &snapshot.PayloadJSON,
			&snapshot.CollectedAt, &snapshot.LastAttemptedAt, &snapshot.LastError, &snapshot.UpdatedAt); err != nil {
			return nil, err
		}
		out = append(out, snapshot)
	}
	return out, rows.Err()
}
