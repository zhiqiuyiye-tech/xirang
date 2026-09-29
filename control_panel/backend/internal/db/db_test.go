package db

import (
	"database/sql"
	"path/filepath"
	"testing"
)

func TestOpenRunsMigrations(t *testing.T) {
	s, err := Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	for _, tbl := range []string{"admin", "worker_nodes", "tasks", "task_steps", "audit_log", "schema_migrations", "auth_challenges"} {
		var name string
		err := s.db.QueryRow(
			"SELECT name FROM sqlite_master WHERE type='table' AND name=?", tbl,
		).Scan(&name)
		if err != nil {
			t.Fatalf("table %s missing: %v", tbl, err)
		}
	}
}

func TestOpenForeignKeysOn(t *testing.T) {
	s, _ := Open(filepath.Join(t.TempDir(), "t.db"))
	defer s.Close()
	var fk int
	if err := s.db.QueryRow("PRAGMA foreign_keys").Scan(&fk); err != nil {
		t.Fatal(err)
	}
	if fk != 1 {
		t.Fatalf("foreign_keys pragma = %d, want 1", fk)
	}
}

func TestUpgradeFromV1Database(t *testing.T) {
	dbPath := filepath.Join(t.TempDir(), "v1.db")
	rawDB, err := sql.Open("sqlite", dbPath)
	if err != nil {
		t.Fatal(err)
	}
	// Simulate an older v1 database with no schema_migrations and no auth_version column
	if _, err := rawDB.Exec(migration0001); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	if _, err := rawDB.Exec("UPDATE admin SET password_hash='preserved_hash' WHERE username='admin'"); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	rawDB.Close()

	// Open with Store which should run migrations safely without data loss
	store, err := Open(dbPath)
	if err != nil {
		t.Fatalf("failed to open existing v1 database: %v", err)
	}
	defer store.Close()

	var hash string
	var authVer int64
	err = store.db.QueryRow("SELECT password_hash, auth_version FROM admin WHERE username='admin'").Scan(&hash, &authVer)
	if err != nil {
		t.Fatalf("failed to query admin row: %v", err)
	}
	if hash != "preserved_hash" {
		t.Fatalf("hash was not preserved: got %q, want preserved_hash", hash)
	}
	if authVer != 2 {
		t.Fatalf("auth_version = %d, want 2 after password-auth migration", authVer)
	}
}

func TestUpgradeFromV3DatabaseAddsKeyAuthStateOnce(t *testing.T) {
	dbPath := filepath.Join(t.TempDir(), "v3.db")
	rawDB, err := sql.Open("sqlite", dbPath)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := rawDB.Exec(migration0001); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	if _, err := rawDB.Exec("ALTER TABLE admin ADD COLUMN auth_version INTEGER NOT NULL DEFAULT 1"); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	if _, err := rawDB.Exec("UPDATE admin SET password_hash='legacy-hash', auth_version=6 WHERE username='admin'"); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	if _, err := rawDB.Exec(`CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, applied_at TIMESTAMP NOT NULL)`); err != nil {
		rawDB.Close()
		t.Fatal(err)
	}
	for _, version := range []int{1, 2, 3} {
		if _, err := rawDB.Exec("INSERT INTO schema_migrations(version, applied_at) VALUES(?, datetime('now'))", version); err != nil {
			rawDB.Close()
			t.Fatal(err)
		}
	}
	if err := rawDB.Close(); err != nil {
		t.Fatal(err)
	}

	store, err := Open(dbPath)
	if err != nil {
		t.Fatalf("upgrade v3 database: %v", err)
	}
	var hash, state string
	var authVersion int64
	var publicKey, fingerprint sql.NullString
	err = store.db.QueryRow(`SELECT password_hash, auth_state, auth_version, public_key_pem, public_key_fingerprint FROM admin WHERE username='admin'`).
		Scan(&hash, &state, &authVersion, &publicKey, &fingerprint)
	if err != nil {
		store.Close()
		t.Fatalf("read upgraded admin: %v", err)
	}
	if hash != "legacy-hash" || state != "PASSWORD_BOOTSTRAP" || authVersion != 7 || publicKey.Valid || fingerprint.Valid {
		store.Close()
		t.Fatalf("unexpected upgraded admin: hash=%q state=%q version=%d publicKey=%v fingerprint=%v", hash, state, authVersion, publicKey, fingerprint)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}

	reopened, err := Open(dbPath)
	if err != nil {
		t.Fatalf("reopen upgraded database: %v", err)
	}
	defer reopened.Close()
	if err := reopened.db.QueryRow("SELECT auth_version FROM admin WHERE username='admin'").Scan(&authVersion); err != nil {
		t.Fatal(err)
	}
	if authVersion != 7 {
		t.Fatalf("auth_version after reopening = %d, want 7", authVersion)
	}
}
