package db

import "testing"

func TestTaskStepsLookupIndexExists(t *testing.T) {
	store := newStore(t)
	var count int
	if err := store.db.QueryRow(`SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name='idx_task_steps_task_seq'`).Scan(&count); err != nil {
		t.Fatal(err)
	}
	if count != 1 {
		t.Fatalf("task_steps lookup index count=%d, want 1", count)
	}
}

func TestSQLiteVersionAtLeast(t *testing.T) {
	cases := []struct {
		version string
		want    bool
	}{
		{"3.35.0", true},
		{"3.53.3", true},
		{"3.35.1", true},
		{"3.34.99", false},
		{"3.9.0", false},
		{"3.35", false},
		{"not-a-version", false},
		{"", false},
	}
	for _, tc := range cases {
		t.Run(tc.version, func(t *testing.T) {
			if got := sqliteVersionAtLeast(tc.version, 3, 35, 0); got != tc.want {
				t.Fatalf("sqliteVersionAtLeast(%q) = %v, want %v", tc.version, got, tc.want)
			}
		})
	}
}
