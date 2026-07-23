package db

import (
	"database/sql"
	"fmt"

	_ "modernc.org/sqlite"
)

type Store struct {
	db *sql.DB
}

func Open(path string) (*Store, error) {
	d, err := sql.Open("sqlite", path+"?_pragma=foreign_keys(1)&_pragma=journal_mode(WAL)&_pragma=busy_timeout(5000)")
	if err != nil {
		return nil, err
	}
	if err := d.Ping(); err != nil {
		d.Close()
		return nil, err
	}
	s := &Store{db: d}
	if _, err := d.Exec(migration0001); err != nil {
		d.Close()
		return nil, fmt.Errorf("migration 0001: %w", err)
	}
	return s, nil
}

func (s *Store) Close() error { return s.db.Close() }
