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
		"SELECT id, username, password_hash, auth_version, created_at FROM admin WHERE username=?", username,
	).Scan(&a.ID, &a.Username, &a.PasswordHash, &a.AuthVersion, &a.CreatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrNotFound
	}
	if err != nil {
		return nil, err
	}
	return &a, nil
}

func (s *Store) GetAdminAuthVersion(ctx context.Context, id int64) (int64, error) {
	var ver int64
	err := s.db.QueryRowContext(ctx,
		"SELECT auth_version FROM admin WHERE id=?", id,
	).Scan(&ver)
	if errors.Is(err, sql.ErrNoRows) {
		return 0, ErrNotFound
	}
	if err != nil {
		return 0, err
	}
	return ver, nil
}

func (s *Store) UpdateAdminPasswordAndBumpVersion(ctx context.Context, username, newHash string) (int64, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()

	res, err := tx.ExecContext(ctx,
		"UPDATE admin SET password_hash=?, auth_version=auth_version+1 WHERE username=?", newHash, username)
	if err != nil {
		return 0, err
	}
	n, err := res.RowsAffected()
	if err != nil {
		return 0, err
	}
	if n == 0 {
		return 0, ErrNotFound
	}

	var newVer int64
	if err := tx.QueryRowContext(ctx,
		"SELECT auth_version FROM admin WHERE username=?", username).Scan(&newVer); err != nil {
		return 0, err
	}
	if err := tx.Commit(); err != nil {
		return 0, err
	}
	return newVer, nil
}

func (s *Store) RevokeAdminSessions(ctx context.Context, username string) (int64, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()

	res, err := tx.ExecContext(ctx,
		"UPDATE admin SET auth_version=auth_version+1 WHERE username=?", username)
	if err != nil {
		return 0, err
	}
	n, err := res.RowsAffected()
	if err != nil {
		return 0, err
	}
	if n == 0 {
		return 0, ErrNotFound
	}

	var newVer int64
	if err := tx.QueryRowContext(ctx,
		"SELECT auth_version FROM admin WHERE username=?", username).Scan(&newVer); err != nil {
		return 0, err
	}
	if err := tx.Commit(); err != nil {
		return 0, err
	}
	return newVer, nil
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
