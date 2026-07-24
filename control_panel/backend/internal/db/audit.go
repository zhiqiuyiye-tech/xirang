package db

import (
	"context"
	"time"
)

func (s *Store) InsertAudit(ctx context.Context, a AuditLog) error {
	if a.At.IsZero() {
		a.At = time.Now().UTC()
	}
	if a.Actor == "" {
		a.Actor = "admin"
	}
	_, err := s.db.ExecContext(ctx,
		`INSERT INTO audit_log (actor, action, target, params_json, result, at) VALUES (?,?,?,?,?,?)`,
		a.Actor, a.Action, a.Target, a.ParamsJSON, a.Result, a.At)
	return err
}

func (s *Store) ListAudit(ctx context.Context, limit int) ([]AuditLog, error) {
	if limit <= 0 {
		limit = 100
	}
	rows, err := s.db.QueryContext(ctx,
		`SELECT id, actor, action, target, params_json, result, at FROM audit_log ORDER BY id DESC LIMIT ?`, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []AuditLog
	for rows.Next() {
		var a AuditLog
		if err := rows.Scan(&a.ID, &a.Actor, &a.Action, &a.Target, &a.ParamsJSON, &a.Result, &a.At); err != nil {
			return nil, err
		}
		out = append(out, a)
	}
	return out, rows.Err()
}
