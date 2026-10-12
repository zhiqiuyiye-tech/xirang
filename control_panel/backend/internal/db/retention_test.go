package db

import (
	"context"
	"errors"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
	"time"
)

func retentionTask(t *testing.T, store *Store, now time.Time, kind, status, params string, finished *time.Time, steps int) int64 {
	t.Helper()
	id, err := store.CreateTask(context.Background(), Task{Type: kind, TargetKind: "storage", TargetID: 7, Status: status, ParamsJSON: params, CreatedAt: now.Add(-500 * 24 * time.Hour)})
	if err != nil {
		t.Fatal(err)
	}
	if _, err := store.db.Exec(`UPDATE tasks SET finished_at=? WHERE id=?`, finished, id); err != nil {
		t.Fatal(err)
	}
	for seq := 1; seq <= steps; seq++ {
		if _, err := store.CreateStep(context.Background(), id, seq, "test-step"); err != nil {
			t.Fatal(err)
		}
	}
	return id
}

func retentionAudit(t *testing.T, store *Store, at time.Time) {
	t.Helper()
	if err := store.InsertAudit(context.Background(), AuditLog{Actor: "test-user", Action: "test", Result: "success", At: at}); err != nil {
		t.Fatal(err)
	}
}

func retentionRowCount(t *testing.T, store *Store, table string) int {
	t.Helper()
	var count int
	switch table {
	case "tasks", "task_steps", "audit_log":
	default:
		t.Fatal("invalid test table")
	}
	if err := store.db.QueryRow(`SELECT COUNT(*) FROM ` + table).Scan(&count); err != nil {
		t.Fatal(err)
	}
	return count
}

func TestPruneHistoryBoundariesAndSnapshots(t *testing.T) {
	store := newStore(t)
	now := time.Date(2026, 10, 11, 3, 0, 0, 0, time.UTC)
	taskCutoff, auditCutoff := now.Add(-90*24*time.Hour), now.Add(-365*24*time.Hour)
	expired := taskCutoff.Add(-time.Second)
	recent := taskCutoff.Add(time.Second)
	var expiredIDs []int64
	for _, status := range []string{"succeeded", "failed", "cancelled"} {
		expiredIDs = append(expiredIDs, retentionTask(t, store, now, "ordinary", status, "{}", &expired, 1))
	}
	const snapshot = `{"worker_id":7,"vg_name":"vg_data","lv_name":"nfs_share","mount_point":"/data02/share","size_gb":100,"fs_type":"ext4"}`
	pinned := retentionTask(t, store, now, "storage_provision_nfs", "succeeded", snapshot, &expired, 1)
	var kept []int64
	for _, status := range []string{"pending", "running", "paused"} {
		kept = append(kept, retentionTask(t, store, now, "ordinary", status, "{}", &expired, 1))
	}
	kept = append(kept, retentionTask(t, store, now, "ordinary", "failed", "{}", nil, 1))
	kept = append(kept, retentionTask(t, store, now, "ordinary", "succeeded", "{}", &recent, 1))
	kept = append(kept, retentionTask(t, store, now, "ordinary", "succeeded", "{}", &taskCutoff, 1))
	retentionAudit(t, store, auditCutoff.Add(-time.Second))
	retentionAudit(t, store, auditCutoff)
	retentionAudit(t, store, auditCutoff.Add(time.Second))

	result, err := store.PruneHistory(context.Background(), now, HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 100})
	if err != nil {
		t.Fatal(err)
	}
	if result != (HistoryPruneResult{Tasks: 3, Steps: 4, Audit: 1}) {
		t.Fatalf("result=%+v", result)
	}
	for _, id := range expiredIDs {
		if _, err := store.GetTask(context.Background(), id); !errors.Is(err, ErrNotFound) {
			t.Fatalf("expired task %d still present: %v", id, err)
		}
	}
	got, err := store.GetTask(context.Background(), pinned)
	if err != nil || got.ParamsJSON != snapshot {
		t.Fatalf("snapshot changed/deleted: task=%+v err=%v", got, err)
	}
	if steps, err := store.ListSteps(context.Background(), pinned); err != nil || len(steps) != 0 {
		t.Fatalf("pinned old steps not removed: %v %v", steps, err)
	}
	for _, id := range kept {
		if _, err := store.GetTask(context.Background(), id); err != nil {
			t.Fatalf("protected task %d deleted: %v", id, err)
		}
		if steps, err := store.ListSteps(context.Background(), id); err != nil || len(steps) != 1 {
			t.Fatalf("protected task %d steps changed: %v %v", id, steps, err)
		}
	}
	if got := retentionRowCount(t, store, "audit_log"); got != 2 {
		t.Fatalf("audit rows=%d, want 2", got)
	}
}

func TestPruneHistoryBatchDoesNotCascadeUnboundedSteps(t *testing.T) {
	store := newStore(t)
	now := time.Now().UTC()
	expired := now.Add(-400 * 24 * time.Hour)
	id := retentionTask(t, store, now, "ordinary", "failed", "{}", &expired, 7)
	for n := 0; n < 5; n++ {
		retentionAudit(t, store, expired)
	}
	policy := HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 3}
	var results []HistoryPruneResult
	for n := 0; n < 4; n++ {
		result, err := store.PruneHistory(context.Background(), now, policy)
		if err != nil {
			t.Fatal(err)
		}
		results = append(results, result)
		if n < 2 {
			if _, err := store.GetTask(context.Background(), id); err != nil {
				t.Fatal("task deletion cascaded into remaining steps")
			}
		}
	}
	want := []HistoryPruneResult{{Tasks: 0, Steps: 3, Audit: 3}, {Tasks: 0, Steps: 3, Audit: 2}, {Tasks: 1, Steps: 1, Audit: 0}, {}}
	if !reflect.DeepEqual(results, want) {
		t.Fatalf("batches=%+v, want %+v", results, want)
	}
}

func TestPruneHistoryComparesInstantsAcrossTimezones(t *testing.T) {
	store := newStore(t)
	now := time.Date(2026, 10, 11, 0, 0, 0, 0, time.UTC)
	zone := time.FixedZone("UTC+8", 8*60*60)
	expired := now.Add(-90*24*time.Hour - time.Second).In(zone)
	boundary := now.Add(-90 * 24 * time.Hour).In(zone)
	retentionTask(t, store, now, "ordinary", "succeeded", "{}", &expired, 0)
	kept := retentionTask(t, store, now, "ordinary", "succeeded", "{}", &boundary, 0)
	retentionAudit(t, store, now.Add(-365*24*time.Hour-time.Second).In(zone))
	result, err := store.PruneHistory(context.Background(), now, HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 10})
	if err != nil || result.Tasks != 1 || result.Audit != 1 {
		t.Fatalf("timezone prune: %+v err=%v", result, err)
	}
	var exists int
	if err := store.db.QueryRow(`SELECT COUNT(*) FROM tasks WHERE id=?`, kept).Scan(&exists); err != nil || exists != 1 {
		t.Fatalf("equal instant cutoff deleted: count=%d err=%v", exists, err)
	}
}

func TestPruneHistoryInvalidPolicyAndCancellationKeepRows(t *testing.T) {
	store := newStore(t)
	now := time.Now().UTC()
	expired := now.Add(-500 * 24 * time.Hour)
	retentionTask(t, store, now, "ordinary", "failed", "{}", &expired, 1)
	retentionAudit(t, store, expired)
	valid := HistoryRetentionPolicy{TaskRetention: time.Hour, AuditRetention: time.Hour, BatchSize: 10}
	for _, invalid := range []HistoryRetentionPolicy{{}, {TaskRetention: -time.Hour, AuditRetention: time.Hour, BatchSize: 10}, {TaskRetention: time.Hour, AuditRetention: 0, BatchSize: 10}, {TaskRetention: time.Hour, AuditRetention: time.Hour, BatchSize: -1}} {
		if got, err := store.PruneHistory(context.Background(), now, invalid); err == nil || got != (HistoryPruneResult{}) {
			t.Fatalf("invalid policy %+v result=%+v err=%v", invalid, got, err)
		}
	}
	if _, err := store.PruneHistory(context.Background(), time.Time{}, valid); err == nil {
		t.Fatal("zero time accepted")
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	if _, err := store.PruneHistory(ctx, now, valid); !errors.Is(err, context.Canceled) {
		t.Fatalf("cancelled error=%v", err)
	}
	for _, table := range []string{"tasks", "task_steps", "audit_log"} {
		if got := retentionRowCount(t, store, table); got != 1 {
			t.Fatalf("%s modified by invalid/cancelled prune: %d", table, got)
		}
	}
}

func TestPruneHistoryRollsBackWholeBatch(t *testing.T) {
	store := newStore(t)
	now := time.Now().UTC()
	expired := now.Add(-500 * 24 * time.Hour)
	retentionTask(t, store, now, "ordinary", "failed", "{}", &expired, 1)
	retentionAudit(t, store, expired)
	if _, err := store.db.Exec(`CREATE TRIGGER reject_retention_audit BEFORE DELETE ON audit_log BEGIN SELECT RAISE(ABORT, 'test rollback'); END;`); err != nil {
		t.Fatal(err)
	}
	got, err := store.PruneHistory(context.Background(), now, HistoryRetentionPolicy{TaskRetention: time.Hour, AuditRetention: time.Hour, BatchSize: 10})
	if err == nil || got != (HistoryPruneResult{}) {
		t.Fatalf("rollback result=%+v err=%v", got, err)
	}
	for _, table := range []string{"tasks", "task_steps", "audit_log"} {
		if count := retentionRowCount(t, store, table); count != 1 {
			t.Fatalf("%s was not rolled back: %d", table, count)
		}
	}
}

func TestRetentionIndexesExist(t *testing.T) {
	store := newStore(t)
	for _, index := range []string{"idx_tasks_terminal_finished_at", "idx_audit_log_at"} {
		var count int
		if err := store.db.QueryRow(`SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND name=?`, index).Scan(&count); err != nil || count != 1 {
			t.Fatalf("missing %s: count=%d err=%v", index, count, err)
		}
	}
}

func TestPruneHistoryPreservesUnconfirmedTimestampText(t *testing.T) {
	store := newStore(t)
	now := time.Date(2026, 10, 11, 0, 0, 0, 0, time.UTC)
	old := now.Add(-500 * 24 * time.Hour)
	texts := []string{"2000-01-01 00:00:00 unknown-zone", "2000-01-01T00:00:00", now.Add(-90*24*time.Hour-time.Hour).Format("2006-01-02T15:04:05") + "-08:00"}
	for _, text := range texts {
		id := retentionTask(t, store, now, "ordinary", "succeeded", "{}", &old, 1)
		if _, err := store.db.Exec(`UPDATE tasks SET finished_at=? WHERE id=?`, text, id); err != nil {
			t.Fatal(err)
		}
	}
	retentionAudit(t, store, old)
	if _, err := store.db.Exec(`UPDATE audit_log SET at='2000-01-01 00:00:00 unknown-zone'`); err != nil {
		t.Fatal(err)
	}
	result, err := store.PruneHistory(context.Background(), now, HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 10})
	if err != nil || result != (HistoryPruneResult{}) {
		t.Fatalf("unconfirmed/future timestamps were pruned: %+v err=%v", result, err)
	}
}

func TestPruneHistorySubsecondBoundary(t *testing.T) {
	store := newStore(t)
	now := time.Date(2026, 10, 11, 0, 0, 0, 123456789, time.UTC)
	boundary := now.Add(-90 * 24 * time.Hour)
	expired := boundary.Add(-time.Nanosecond)
	retentionTask(t, store, now, "ordinary", "failed", "{}", &expired, 0)
	retentionTask(t, store, now, "ordinary", "failed", "{}", &boundary, 0)
	got, err := store.PruneHistory(context.Background(), now, HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 10})
	if err != nil || got.Tasks != 1 {
		t.Fatalf("strict subsecond boundary result=%+v err=%v", got, err)
	}
}

func TestRetentionUpgradePreservesData(t *testing.T) {
	path := filepath.Join(t.TempDir(), "retention-upgrade.db")
	store, err := Open(path)
	if err != nil {
		t.Fatal(err)
	}
	now := time.Now().UTC()
	id := retentionTask(t, store, now, "storage_provision_nfs", "succeeded", `{"kept":true}`, &now, 1)
	if _, err := store.db.Exec(`DROP INDEX idx_tasks_terminal_finished_at; DROP INDEX idx_audit_log_at; DELETE FROM schema_migrations WHERE version=6;`); err != nil {
		store.Close()
		t.Fatal(err)
	}
	if err := store.Close(); err != nil {
		t.Fatal(err)
	}
	reopened, err := Open(path)
	if err != nil {
		t.Fatal(err)
	}
	defer reopened.Close()
	got, err := reopened.GetTask(context.Background(), id)
	if err != nil || got.ParamsJSON != `{"kept":true}` {
		t.Fatalf("upgrade lost snapshot: %+v %v", got, err)
	}
	for _, name := range []string{"idx_tasks_terminal_finished_at", "idx_audit_log_at", "idx_task_steps_task_seq"} {
		var count int
		if err := reopened.db.QueryRow(`SELECT COUNT(*) FROM sqlite_master WHERE name=? AND type='index'`, name).Scan(&count); err != nil || count != 1 {
			t.Fatalf("upgrade missing %s: %d %v", name, count, err)
		}
	}
}

func TestRetentionQueriesUseCutoffIndexes(t *testing.T) {
	store := newStore(t)
	for _, tc := range []struct{ query, index string }{
		{`SELECT id FROM tasks WHERE status IN ('succeeded','failed','cancelled') AND ` + sqliteTimestampInstantExpr("finished_at") + ` < '2026-01-01 00:00:00.000000000'`, "idx_tasks_terminal_finished_at"},
		{`SELECT id FROM audit_log WHERE ` + sqliteTimestampInstantExpr("at") + ` < '2026-01-01 00:00:00.000000000'`, "idx_audit_log_at"},
	} {
		rows, err := store.db.Query(`EXPLAIN QUERY PLAN ` + tc.query)
		if err != nil {
			t.Fatal(err)
		}
		var details []string
		for rows.Next() {
			var id, parent, unused int
			var detail string
			if err := rows.Scan(&id, &parent, &unused, &detail); err != nil {
				rows.Close()
				t.Fatal(err)
			}
			details = append(details, detail)
		}
		err = rows.Err()
		rows.Close()
		if err != nil || !strings.Contains(strings.Join(details, "\n"), tc.index) {
			t.Fatalf("cutoff index %s unused: %v err=%v", tc.index, details, err)
		}
	}
}
