-- Migration 0001: initial schema
-- Mirrors internal/db/migrations.go:migration0001 for human inspection.
-- Code does not read this file; the Go constant is the source of truth.

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
