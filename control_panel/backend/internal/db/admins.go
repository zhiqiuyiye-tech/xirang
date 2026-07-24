package db

import (
	"context"
	"database/sql"
	"errors"
)

var ErrNotFound = errors.New("not found")

func (s *Store) GetAdminByUsername(ctx context.Context, username string) (*Admin, error) {
	var a Admin
	err := s.db.QueryRowContext(ctx,
		"SELECT id, username, password_hash, created_at FROM admin WHERE username=?", username,
	).Scan(&a.ID, &a.Username, &a.PasswordHash, &a.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (s *Store) UpsertAdminPassword(ctx context.Context, username, hash string) error {
	_, err := s.db.ExecContext(ctx,
		"UPDATE admin SET password_hash=? WHERE username=?", hash, username)
	return err
}

func (s *Store) IsAdminSeeded(ctx context.Context) (bool, error) {
	var hash string
	err := s.db.QueryRowContext(ctx,
		"SELECT password_hash FROM admin WHERE username='admin'").Scan(&hash)
	if err != nil {
		return false, err
	}
	return hash != pendingInitHash, nil
}
