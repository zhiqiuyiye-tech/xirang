package main

import (
	"context"
	"database/sql"
	"path/filepath"
	"testing"

	"xirang/control_panel/internal/db"
)

func openStoreWithAdminSQL(t *testing.T, path, query string, args ...any) *db.Store {
	t.Helper()
	initial, err := db.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	if err := initial.Close(); err != nil {
		t.Fatal(err)
	}
	raw, err := sql.Open("sqlite", path)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := raw.Exec(query, args...); err != nil {
		raw.Close()
		t.Fatal(err)
	}
	if err := raw.Close(); err != nil {
		t.Fatal(err)
	}
	store, err := db.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { store.Close() })
	return store
}

func TestSeedAdminCompletesRecoveryBeforeServing(t *testing.T) {
	dbPath := filepath.Join(t.TempDir(), "seed-admin.db")
	store := openStoreWithAdminSQL(t, dbPath, `UPDATE admin SET auth_state=?, password_hash=?, auth_version=auth_version+1 WHERE username='admin'`, db.AuthStateRecoveryPending, "__PENDING_INIT__")

	if err := seedAdmin(context.Background(), store, "recovery-bootstrap-secret"); err != nil {
		t.Fatalf("seedAdmin() recovery error = %v", err)
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != db.AuthStatePasswordBootstrap || admin.PasswordHash == "__PENDING_INIT__" {
		t.Fatalf("recovery did not transition to PASSWORD_BOOTSTRAP: %+v", admin)
	}
	if err := store.ValidateAdminAuthState(context.Background()); err != nil {
		t.Fatalf("recovered state invalid: %v", err)
	}
	audits, err := store.ListAudit(context.Background(), 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(audits) != 1 || audits[0].Action != "auth.recovery_bootstrap" || audits[0].Result != "success" {
		t.Fatalf("unexpected recovery audit: %+v", audits)
	}
}

func TestSeedAdminRejectsInvalidActiveState(t *testing.T) {
	dbPath := filepath.Join(t.TempDir(), "invalid-active.db")
	store := openStoreWithAdminSQL(t, dbPath, `UPDATE admin SET auth_state=?, password_hash=? WHERE username='admin'`, db.AuthStateKeyActive, "__DISABLED_AFTER_KEY_BOOTSTRAP__")
	if err := seedAdmin(context.Background(), store, "initial-secret"); err == nil {
		t.Fatal("seedAdmin accepted KEY_ACTIVE without a valid public key")
	}
}
