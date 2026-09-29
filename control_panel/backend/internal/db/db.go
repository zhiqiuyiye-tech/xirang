package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	_ "modernc.org/sqlite"
)

type Store struct {
	db *sql.DB
}

func Open(path string) (*Store, error) {
	if dir := filepath.Dir(path); dir != "" && dir != "." {
		if err := os.MkdirAll(dir, 0755); err != nil {
			return nil, fmt.Errorf("create db directory %s: %w", dir, err)
		}
	}
	d, err := sql.Open("sqlite", path+"?_pragma=foreign_keys(1)&_pragma=journal_mode(WAL)&_pragma=busy_timeout(5000)&_pragma=synchronous(NORMAL)")
	if err != nil {
		return nil, err
	}
	// SQLite allows a single writer at a time. Funneling everything through
	// one connection removes SQLITE_BUSY contention between the task engine's
	// step writes and API writes entirely (every query here is a sub-ms point
	// lookup or short scan, so the serialization cost is negligible at this
	// panel's scale). WAL + synchronous(NORMAL) keeps reads fast and reduces
	// fsyncs on the write path.
	d.SetMaxOpenConns(1)
	if err := d.Ping(); err != nil {
		d.Close()
		return nil, err
	}
	var sqliteVersion string
	if err := d.QueryRow("SELECT sqlite_version()").Scan(&sqliteVersion); err != nil {
		d.Close()
		return nil, fmt.Errorf("read sqlite runtime version: %w", err)
	}
	if !sqliteVersionAtLeast(sqliteVersion, 3, 35, 0) {
		d.Close()
		return nil, fmt.Errorf("SQLite runtime %q is older than required 3.35.0", sqliteVersion)
	}
	s := &Store{db: d}
	if err := runMigrations(d); err != nil {
		d.Close()
		return nil, fmt.Errorf("migrations: %w", err)
	}
	return s, nil
}

func (s *Store) Close() error { return s.db.Close() }

// Ping verifies that the underlying database connection is still alive.
func (s *Store) Ping() error { return s.db.Ping() }

func sqliteVersionAtLeast(version string, major, minor, patch int) bool {
	parts := strings.Split(version, ".")
	if len(parts) != 3 {
		return false
	}
	actual := [3]int{}
	for i, part := range parts {
		value, err := strconv.Atoi(part)
		if err != nil || value < 0 {
			return false
		}
		actual[i] = value
	}
	required := [3]int{major, minor, patch}
	for i := range actual {
		if actual[i] != required[i] {
			return actual[i] > required[i]
		}
	}
	return true
}
