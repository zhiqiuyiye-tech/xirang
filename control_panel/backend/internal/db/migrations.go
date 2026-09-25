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
	if _, err := db.Exec(`
CREATE TABLE IF NOT EXISTS schema_migrations (
  version     INTEGER PRIMARY KEY,
  applied_at  TIMESTAMP NOT NULL
);`); err != nil {
		return fmt.Errorf("init schema_migrations: %w", err)
	}

	migrations := []migration{
		{
			version: 1,
			apply: func(tx *sql.Tx) error {
				_, err := tx.Exec(migration0001)
				return err
			},
		},
		{
			version: 2,
			apply: func(tx *sql.Tx) error {
				has, err := tableHasColumn(tx, "admin", "auth_version")
				if err != nil {
					return err
				}
				if !has {
					_, err = tx.Exec("ALTER TABLE admin ADD COLUMN auth_version INTEGER NOT NULL DEFAULT 1")
				}
				return err
			},
		},
		{
			version: 3,
			apply: func(tx *sql.Tx) error {
				for _, col := range []struct {
					name string
					ddl  string
				}{
					{"last_checked_at", "ALTER TABLE worker_nodes ADD COLUMN last_checked_at TIMESTAMP"},
					{"status_error", "ALTER TABLE worker_nodes ADD COLUMN status_error TEXT"},
					{"health_failures", "ALTER TABLE worker_nodes ADD COLUMN health_failures INTEGER NOT NULL DEFAULT 0"},
				} {
					has, err := tableHasColumn(tx, "worker_nodes", col.name)
					if err != nil {
						return err
					}
					if !has {
						if _, err := tx.Exec(col.ddl); err != nil {
							return err
						}
					}
				}
				_, err := tx.Exec(`
CREATE TABLE IF NOT EXISTS storage_inventory_snapshots (
  worker_id         INTEGER PRIMARY KEY REFERENCES worker_nodes(id) ON DELETE CASCADE,
  schema_version    INTEGER NOT NULL DEFAULT 1,
  payload_json      TEXT NOT NULL DEFAULT '',
  collected_at      TIMESTAMP,
  last_attempted_at TIMESTAMP NOT NULL,
  last_error        TEXT,
  updated_at        TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS notebook_metadata (
  stable_key    TEXT PRIMARY KEY,
  key_kind      TEXT NOT NULL,
  namespace     TEXT NOT NULL,
  workspace_id  TEXT NOT NULL DEFAULT '',
  project_id    TEXT NOT NULL DEFAULT '',
  last_pod_uid  TEXT NOT NULL,
  owner_name    TEXT NOT NULL DEFAULT '',
  note          TEXT NOT NULL DEFAULT '',
  updated_by    TEXT NOT NULL,
  created_at    TIMESTAMP NOT NULL,
  updated_at    TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_notebook_metadata_namespace ON notebook_metadata(namespace);
`)
				return err
			},
		},
	}

	for _, m := range migrations {
		var exists int
		if err := db.QueryRow("SELECT COUNT(1) FROM schema_migrations WHERE version=?", m.version).Scan(&exists); err != nil {
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

func tableHasColumn(tx *sql.Tx, table, column string) (bool, error) {
	rows, err := tx.Query("PRAGMA table_info(" + table + ")")
	if err != nil {
		return false, err
	}
	defer rows.Close()
	for rows.Next() {
		var cid int
		var name, ctype string
		var notnull, pk int
		var defaultValue sql.NullString
		if err := rows.Scan(&cid, &name, &ctype, &notnull, &defaultValue, &pk); err != nil {
			return false, err
		}
		if name == column {
			return true, nil
		}
	}
	return false, rows.Err()
}
