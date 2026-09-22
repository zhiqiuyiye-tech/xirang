package db

import (
	"database/sql"
	"fmt"
)

const pendingInitHash = "__PENDING_INIT__"

const migration0001 = `
CREATE TABLE IF NOT EXISTS admin (
  id            INTEGER PRIMARY KEY,
  username      TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at    TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS worker_nodes (
  id              INTEGER PRIMARY KEY,
  name            TEXT NOT NULL,
  host            TEXT NOT NULL,
  port            INTEGER NOT NULL DEFAULT 22,
  username        TEXT NOT NULL DEFAULT 'root',
  auth_mode       TEXT NOT NULL,
  enc_password    TEXT,
  enc_private_key TEXT,
  status          TEXT NOT NULL DEFAULT 'unknown',
  last_seen_at    TIMESTAMP,
  created_at      TIMESTAMP NOT NULL,
  updated_at      TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS tasks (
  id           INTEGER PRIMARY KEY,
  type         TEXT NOT NULL,
  target_kind  TEXT NOT NULL,
  target_id    INTEGER NOT NULL,
  status       TEXT NOT NULL,
  params_json  TEXT NOT NULL,
  error        TEXT,
  created_at   TIMESTAMP NOT NULL,
  started_at   TIMESTAMP,
  finished_at  TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE TABLE IF NOT EXISTS task_steps (
  id          INTEGER PRIMARY KEY,
  task_id     INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  seq         INTEGER NOT NULL,
  name        TEXT NOT NULL,
  status      TEXT NOT NULL,
  stdout      TEXT,
  stderr      TEXT,
  started_at  TIMESTAMP,
  finished_at TIMESTAMP,
  error       TEXT
);
CREATE TABLE IF NOT EXISTS audit_log (
  id          INTEGER PRIMARY KEY,
  actor       TEXT NOT NULL,
  action      TEXT NOT NULL,
  target      TEXT,
  params_json TEXT,
  result      TEXT NOT NULL,
  at          TIMESTAMP NOT NULL
);

INSERT OR IGNORE INTO admin (id, username, password_hash, created_at)
  VALUES (1, 'admin', '__PENDING_INIT__', '1970-01-01 00:00:00');
`

type migration struct {
	version int
	apply   func(tx *sql.Tx) error
}

func runMigrations(db *sql.DB) error {
	_, err := db.Exec(`
CREATE TABLE IF NOT EXISTS schema_migrations (
  version     INTEGER PRIMARY KEY,
  applied_at  TIMESTAMP NOT NULL
);`)
	if err != nil {
		return fmt.Errorf("init schema_migrations: %w", err)
	}

	migrations := []migration{
		{
			version: 1,
			apply: func(tx *sql.Tx) error {
				if _, err := tx.Exec(migration0001); err != nil {
					return err
				}
				return nil
			},
		},
		{
			version: 2,
			apply: func(tx *sql.Tx) error {
				rows, err := tx.Query("PRAGMA table_info(admin)")
				if err != nil {
					return err
				}
				defer rows.Close()

				hasCol := false
				for rows.Next() {
					var cid int
					var name, ctype string
					var notnull, pk int
					var dfltValue sql.NullString
					if err := rows.Scan(&cid, &name, &ctype, &notnull, &dfltValue, &pk); err != nil {
						return err
					}
					if name == "auth_version" {
						hasCol = true
						break
					}
				}
				if !hasCol {
					if _, err := tx.Exec("ALTER TABLE admin ADD COLUMN auth_version INTEGER NOT NULL DEFAULT 1;"); err != nil {
						return err
					}
				}
				return nil
			},
		},
	}

	for _, m := range migrations {
		var exists int
		err := db.QueryRow("SELECT COUNT(1) FROM schema_migrations WHERE version=?", m.version).Scan(&exists)
		if err != nil {
			return fmt.Errorf("check migration %d: %w", m.version, err)
		}
		if exists > 0 {
			continue
		}

		tx, err := db.Begin()
		if err != nil {
			return fmt.Errorf("begin migration %d: %w", m.version, err)
		}
		if err := m.apply(tx); err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("apply migration %d: %w", m.version, err)
		}
		if _, err := tx.Exec("INSERT INTO schema_migrations (version, applied_at) VALUES (?, datetime('now'))", m.version); err != nil {
			_ = tx.Rollback()
			return fmt.Errorf("record migration %d: %w", m.version, err)
		}
		if err := tx.Commit(); err != nil {
			return fmt.Errorf("commit migration %d: %w", m.version, err)
		}
	}

	return nil
}
