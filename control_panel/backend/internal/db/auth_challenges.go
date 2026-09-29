package db

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"time"
)

var (
	ErrChallengeUnavailable   = errors.New("challenge unavailable")
	ErrChallengeLimitExceeded = errors.New("challenge pending limit exceeded")
)

// CreateAuthChallenge atomically enforces source/global pending limits and
// inserts the challenge. This Store uses one SQLite connection and supports a
// single service process; multi-replica use is not supported.
func (s *Store) CreateAuthChallenge(ctx context.Context, challenge AuthChallenge, maxPendingPerIP, maxPendingGlobal int) error {
	if challenge.ChallengeID == "" || challenge.Nonce == "" || challenge.ClientIP == "" || challenge.AuthVersion <= 0 || !challenge.Purpose.valid() || !challenge.ExpiresAt.After(challenge.CreatedAt) {
		return errors.New("invalid auth challenge")
	}
	if maxPendingPerIP <= 0 || maxPendingGlobal <= 0 {
		return errors.New("challenge pending limits must be positive")
	}

	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	now := challenge.CreatedAt.UTC()
	if _, err := tx.ExecContext(ctx, `DELETE FROM auth_challenges
		WHERE expires_at <= ? OR (consumed_at IS NOT NULL AND consumed_at < ?)`, now, now.Add(-24*time.Hour)); err != nil {
		return err
	}
	var sourcePending, globalPending int
	if err := tx.QueryRowContext(ctx, `SELECT COUNT(*) FROM auth_challenges
		WHERE client_ip=? AND consumed_at IS NULL AND expires_at>?`, challenge.ClientIP, now).Scan(&sourcePending); err != nil {
		return err
	}
	if err := tx.QueryRowContext(ctx, `SELECT COUNT(*) FROM auth_challenges
		WHERE consumed_at IS NULL AND expires_at>?`, now).Scan(&globalPending); err != nil {
		return err
	}
	if sourcePending >= maxPendingPerIP || globalPending >= maxPendingGlobal {
		return ErrChallengeLimitExceeded
	}
	if _, err := tx.ExecContext(ctx, `INSERT INTO auth_challenges
		(challenge_id, nonce, purpose, auth_version, key_fingerprint, new_key_fingerprint, client_ip, created_at, expires_at, consumed_at)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)`,
		challenge.ChallengeID, challenge.Nonce, challenge.Purpose, challenge.AuthVersion,
		challenge.KeyFingerprint, challenge.NewKeyFingerprint, challenge.ClientIP,
		challenge.CreatedAt.UTC(), challenge.ExpiresAt.UTC()); err != nil {
		return err
	}
	return tx.Commit()
}

// ConsumeAuthChallenge claims a live challenge for exactly one request. The
// challenge is marked consumed before signature verification by the caller.
func (s *Store) ConsumeAuthChallenge(ctx context.Context, challengeID string, purpose AuthChallengePurpose, now time.Time) (AuthChallenge, error) {
	var challenge AuthChallenge
	var consumedAt time.Time
	err := s.db.QueryRowContext(ctx, `UPDATE auth_challenges SET consumed_at=?
		WHERE challenge_id=? AND purpose=? AND consumed_at IS NULL AND expires_at>?
		RETURNING challenge_id, nonce, purpose, auth_version, key_fingerprint, new_key_fingerprint,
			client_ip, created_at, expires_at, consumed_at`,
		now.UTC(), challengeID, purpose, now.UTC()).Scan(
		&challenge.ChallengeID, &challenge.Nonce, &challenge.Purpose, &challenge.AuthVersion,
		&challenge.KeyFingerprint, &challenge.NewKeyFingerprint, &challenge.ClientIP,
		&challenge.CreatedAt, &challenge.ExpiresAt, &consumedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return AuthChallenge{}, ErrChallengeUnavailable
	}
	if err != nil {
		return AuthChallenge{}, fmt.Errorf("consume auth challenge: %w", err)
	}
	challenge.ConsumedAt = &consumedAt
	return challenge, nil
}

func (purpose AuthChallengePurpose) valid() bool {
	return purpose == AuthChallengeLogin || purpose == AuthChallengeBootstrap || purpose == AuthChallengeKeyRotate
}
