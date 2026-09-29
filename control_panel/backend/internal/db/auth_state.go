package db

import (
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/sha256"
	"crypto/x509"
	"database/sql"
	"encoding/hex"
	"encoding/pem"
	"errors"
	"fmt"
	"strings"

	"golang.org/x/crypto/bcrypt"
)

const disabledPasswordHash = "__DISABLED_AFTER_KEY_BOOTSTRAP__"

var (
	ErrAuthStateConflict   = errors.New("admin auth state changed")
	ErrAuthRecoveryPending = errors.New("admin auth recovery is pending")
)

func (s *Store) ValidateAdminAuthState(ctx context.Context) error {
	admin, err := s.GetAdminByUsername(ctx, "admin")
	if err != nil {
		return fmt.Errorf("read admin auth state: %w", err)
	}
	if admin.AuthVersion <= 0 {
		return errors.New("admin auth_version must be positive")
	}

	switch admin.AuthState {
	case AuthStatePasswordBootstrap:
		if admin.PublicKeyPEM != nil || admin.PublicKeyFingerprint != nil {
			return errors.New("PASSWORD_BOOTSTRAP must not contain a public key")
		}
		if _, err := bcrypt.Cost([]byte(admin.PasswordHash)); err != nil {
			return fmt.Errorf("PASSWORD_BOOTSTRAP requires a valid bcrypt hash: %w", err)
		}
		return nil
	case AuthStateKeyActive:
		if admin.PasswordHash != disabledPasswordHash {
			return errors.New("KEY_ACTIVE requires disabled password authentication")
		}
		if admin.PublicKeyPEM == nil || admin.PublicKeyFingerprint == nil {
			return errors.New("KEY_ACTIVE requires a public key and fingerprint")
		}
		return validateCanonicalP256PublicKey(*admin.PublicKeyPEM, *admin.PublicKeyFingerprint)
	case AuthStateRecoveryPending:
		return ErrAuthRecoveryPending
	default:
		return fmt.Errorf("unknown admin auth state %q", admin.AuthState)
	}
}

func (s *Store) InitializeAdminAuth(ctx context.Context, bootstrapPasswordHash string) error {
	if _, err := bcrypt.Cost([]byte(bootstrapPasswordHash)); err != nil {
		return fmt.Errorf("invalid bootstrap password hash: %w", err)
	}
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()

	var state AuthState
	var passwordHash string
	var publicKeyPEM, fingerprint sql.NullString
	if err := tx.QueryRowContext(ctx, `SELECT auth_state, password_hash, public_key_pem, public_key_fingerprint
		FROM admin WHERE username='admin'`).Scan(&state, &passwordHash, &publicKeyPEM, &fingerprint); err != nil {
		return err
	}

	switch state {
	case AuthStatePasswordBootstrap:
		if publicKeyPEM.Valid || fingerprint.Valid {
			return errors.New("PASSWORD_BOOTSTRAP must not contain a public key")
		}
		if passwordHash == pendingInitHash {
			result, err := tx.ExecContext(ctx, `UPDATE admin SET password_hash=?
				WHERE username='admin' AND auth_state=? AND password_hash=? AND public_key_pem IS NULL AND public_key_fingerprint IS NULL`,
				bootstrapPasswordHash, AuthStatePasswordBootstrap, pendingInitHash)
			if err != nil {
				return err
			}
			if rows, err := result.RowsAffected(); err != nil || rows != 1 {
				return ErrAuthStateConflict
			}
		} else if _, err := bcrypt.Cost([]byte(passwordHash)); err != nil {
			return fmt.Errorf("PASSWORD_BOOTSTRAP requires a valid bcrypt hash: %w", err)
		}
		return tx.Commit()
	case AuthStateKeyActive:
		if passwordHash != disabledPasswordHash || !publicKeyPEM.Valid || !fingerprint.Valid {
			return errors.New("inconsistent KEY_ACTIVE state")
		}
		if err := validateCanonicalP256PublicKey(publicKeyPEM.String, fingerprint.String); err != nil {
			return err
		}
		return tx.Commit()
	case AuthStateRecoveryPending:
		if passwordHash != pendingInitHash || publicKeyPEM.Valid || fingerprint.Valid {
			return errors.New("inconsistent RECOVERY_PENDING state")
		}
		result, err := tx.ExecContext(ctx, `UPDATE admin SET auth_state=?, password_hash=?
			WHERE username='admin' AND auth_state=? AND password_hash=? AND public_key_pem IS NULL AND public_key_fingerprint IS NULL`,
			AuthStatePasswordBootstrap, bootstrapPasswordHash, AuthStateRecoveryPending, pendingInitHash)
		if err != nil {
			return err
		}
		if rows, err := result.RowsAffected(); err != nil || rows != 1 {
			return ErrAuthStateConflict
		}
		if _, err := tx.ExecContext(ctx, "DELETE FROM auth_challenges"); err != nil {
			return err
		}
		if _, err := tx.ExecContext(ctx, `INSERT INTO audit_log (actor, action, result, at)
			VALUES ('system', 'auth.recovery_bootstrap', 'success', datetime('now'))`); err != nil {
			return err
		}
		return tx.Commit()
	default:
		return fmt.Errorf("unknown admin auth state %q", state)
	}
}

func (s *Store) BootstrapAdminKey(ctx context.Context, expectedVersion int64, publicKeyPEM, fingerprint string) (int64, error) {
	if err := validateCanonicalP256PublicKey(publicKeyPEM, fingerprint); err != nil {
		return 0, err
	}
	return s.updateAdminPublicKey(ctx, AuthStatePasswordBootstrap, expectedVersion, "", publicKeyPEM, fingerprint, true)
}

func (s *Store) RotateAdminKey(ctx context.Context, expectedVersion int64, expectedFingerprint, publicKeyPEM, fingerprint string) (int64, error) {
	if err := validateCanonicalP256PublicKey(publicKeyPEM, fingerprint); err != nil {
		return 0, err
	}
	return s.updateAdminPublicKey(ctx, AuthStateKeyActive, expectedVersion, expectedFingerprint, publicKeyPEM, fingerprint, false)
}

func (s *Store) updateAdminPublicKey(ctx context.Context, expectedState AuthState, expectedVersion int64, expectedFingerprint, publicKeyPEM, fingerprint string, bootstrap bool) (int64, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()

	var query string
	var args []any
	if bootstrap {
		query = `UPDATE admin SET auth_state=?, public_key_pem=?, public_key_fingerprint=?, password_hash=?, auth_version=auth_version+1
			WHERE username='admin' AND auth_state=? AND public_key_pem IS NULL AND public_key_fingerprint IS NULL AND auth_version=?
			RETURNING auth_version`
		args = []any{AuthStateKeyActive, publicKeyPEM, fingerprint, disabledPasswordHash, expectedState, expectedVersion}
	} else {
		query = `UPDATE admin SET public_key_pem=?, public_key_fingerprint=?, auth_version=auth_version+1
			WHERE username='admin' AND auth_state=? AND auth_version=? AND public_key_fingerprint=?
			RETURNING auth_version`
		args = []any{publicKeyPEM, fingerprint, expectedState, expectedVersion, expectedFingerprint}
	}

	var newVersion int64
	if err := tx.QueryRowContext(ctx, query, args...).Scan(&newVersion); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return 0, ErrAuthStateConflict
		}
		return 0, err
	}
	if err := tx.Commit(); err != nil {
		return 0, err
	}
	return newVersion, nil
}

func validateCanonicalP256PublicKey(publicKeyPEM, fingerprint string) error {
	block, rest := pem.Decode([]byte(publicKeyPEM))
	if block == nil || block.Type != "PUBLIC KEY" || len(strings.TrimSpace(string(rest))) != 0 {
		return errors.New("invalid public key PEM")
	}
	parsed, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return fmt.Errorf("parse public key PEM: %w", err)
	}
	publicKey, ok := parsed.(*ecdsa.PublicKey)
	if !ok || publicKey.Curve != elliptic.P256() || publicKey.X == nil || publicKey.Y == nil || !publicKey.Curve.IsOnCurve(publicKey.X, publicKey.Y) {
		return errors.New("public key must be ECDSA P-256")
	}
	canonicalDER, err := x509.MarshalPKIXPublicKey(publicKey)
	if err != nil {
		return fmt.Errorf("marshal public key: %w", err)
	}
	canonicalPEM := pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: canonicalDER})
	if string(canonicalPEM) != publicKeyPEM {
		return errors.New("public key PEM is not canonical")
	}
	digest := sha256.Sum256(canonicalDER)
	if fingerprint != hex.EncodeToString(digest[:]) {
		return errors.New("public key fingerprint mismatch")
	}
	return nil
}
