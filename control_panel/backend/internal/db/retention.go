package db

import (
	"context"
	"database/sql"
	"fmt"
	"time"
)

// HistoryRetentionPolicy controls bounded pruning of task and audit history.
type HistoryRetentionPolicy struct {
	TaskRetention  time.Duration
	AuditRetention time.Duration
	BatchSize      int
}

// HistoryPruneResult reports rows deleted by a committed pruning batch.
type HistoryPruneResult struct {
	Tasks int64
	Steps int64
	Audit int64
}

// PruneHistory removes one bounded batch of expired history in a single
// transaction. Succeeded NFS provision tasks remain as resource snapshots.
func (s *Store) PruneHistory(ctx context.Context, now time.Time, policy HistoryRetentionPolicy) (HistoryPruneResult, error) {
	if policy.TaskRetention <= 0 {
		return HistoryPruneResult{}, fmt.Errorf("task retention must be positive")
	}
	if policy.AuditRetention <= 0 {
		return HistoryPruneResult{}, fmt.Errorf("audit retention must be positive")
	}
	if policy.BatchSize <= 0 {
		return HistoryPruneResult{}, fmt.Errorf("history prune batch size must be positive")
	}
	if now.IsZero() {
		return HistoryPruneResult{}, fmt.Errorf("history prune time must be nonzero")
	}
	if err := ctx.Err(); err != nil {
		return HistoryPruneResult{}, err
	}

	now = now.UTC()
	taskCutoff := now.Add(-policy.TaskRetention)
	auditCutoff := now.Add(-policy.AuditRetention)

	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return HistoryPruneResult{}, fmt.Errorf("begin history prune: %w", err)
	}
	defer tx.Rollback()

	var result HistoryPruneResult
	stepQuery := `
WITH raw_cutoff(value) AS (SELECT ?), cutoff(instant) AS (SELECT ` + sqliteTimestampInstantExpr("raw_cutoff.value") + ` FROM raw_cutoff)
DELETE FROM task_steps
WHERE id IN (
  SELECT step.id
  FROM task_steps AS step
  JOIN tasks AS task ON task.id = step.task_id
  WHERE task.status IN ('succeeded', 'failed', 'cancelled')
    AND task.finished_at IS NOT NULL
    AND ` + sqliteTimestampInstantExpr("task.finished_at") + ` < (SELECT instant FROM cutoff)
  ORDER BY step.id
  LIMIT ?
)`
	result.Steps, err = deleteHistoryBatch(ctx, tx, stepQuery, taskCutoff, policy.BatchSize)
	if err != nil {
		return HistoryPruneResult{}, fmt.Errorf("prune task steps: %w", err)
	}

	taskQuery := `
WITH raw_cutoff(value) AS (SELECT ?), cutoff(instant) AS (SELECT ` + sqliteTimestampInstantExpr("raw_cutoff.value") + ` FROM raw_cutoff)
DELETE FROM tasks
WHERE id IN (
  SELECT task.id
  FROM tasks AS task
  WHERE task.status IN ('succeeded', 'failed', 'cancelled')
    AND task.finished_at IS NOT NULL
    AND ` + sqliteTimestampInstantExpr("task.finished_at") + ` < (SELECT instant FROM cutoff)
    AND NOT (task.type = 'storage_provision_nfs' AND task.status = 'succeeded')
    AND NOT EXISTS (
      SELECT 1 FROM task_steps AS remaining_step WHERE remaining_step.task_id = task.id
    )
  ORDER BY task.id
  LIMIT ?
)`
	result.Tasks, err = deleteHistoryBatch(ctx, tx, taskQuery, taskCutoff, policy.BatchSize)
	if err != nil {
		return HistoryPruneResult{}, fmt.Errorf("prune tasks: %w", err)
	}

	auditQuery := `
WITH raw_cutoff(value) AS (SELECT ?), cutoff(instant) AS (SELECT ` + sqliteTimestampInstantExpr("raw_cutoff.value") + ` FROM raw_cutoff)
DELETE FROM audit_log
WHERE id IN (
  SELECT audit.id
  FROM audit_log AS audit
  WHERE ` + sqliteTimestampInstantExpr("audit.at") + ` < (SELECT instant FROM cutoff)
  ORDER BY ` + sqliteTimestampInstantExpr("audit.at") + `, audit.id
  LIMIT ?
)`
	result.Audit, err = deleteHistoryBatch(ctx, tx, auditQuery, auditCutoff, policy.BatchSize)
	if err != nil {
		return HistoryPruneResult{}, fmt.Errorf("prune audit history: %w", err)
	}

	if err := tx.Commit(); err != nil {
		return HistoryPruneResult{}, fmt.Errorf("commit history prune: %w", err)
	}
	return result, nil
}

func deleteHistoryBatch(ctx context.Context, tx *sql.Tx, query string, cutoff time.Time, batchSize int) (int64, error) {
	result, err := tx.ExecContext(ctx, query, cutoff, batchSize)
	if err != nil {
		return 0, err
	}
	return result.RowsAffected()
}

// sqliteTimestampInstantExpr turns the modernc driver's timestamp text into a
// sortable UTC key while retaining fractional digits. The driver includes both
// a numeric offset and a zone label (for example, " +1400 UTC+14"), which
// SQLite's date functions do not parse as-is. Converting only the whole-second
// portion avoids SQLite's millisecond date-function precision from changing
// the exact cutoff comparison; the original fraction is appended as 9 digits.
func sqliteTimestampInstantExpr(value string) string {
	offsetPosition := "(CASE WHEN instr(" + value + ", ' +') > 0 THEN instr(" + value + ", ' +') WHEN instr(" + value + ", ' -') > 0 THEN instr(" + value + ", ' -') ELSE 0 END)"
	baseEnd := "(CASE WHEN " + offsetPosition + " > 0 THEN " + offsetPosition + " - 1 ELSE length(" + value + ") - CASE WHEN substr(" + value + ", -1, 1) = 'Z' THEN 1 ELSE 0 END END)"
	offsetText := "CASE WHEN substr(" + value + ", " + offsetPosition + " + 4, 1) = ':' THEN substr(" + value + ", " + offsetPosition + " + 1, 6) ELSE substr(" + value + ", " + offsetPosition + " + 1, 3) || ':' || substr(" + value + ", " + offsetPosition + " + 4, 2) END"
	normalizedTime := "substr(" + value + ", 1, 19) || CASE WHEN " + offsetPosition + " > 0 THEN " + offsetText + " ELSE '' END"
	fractionDigits := "CASE WHEN substr(" + value + ", 20, 1) = '.' THEN substr(" + value + ", 21, " + baseEnd + " - 20) ELSE '' END"
	paddedFraction := "substr((" + fractionDigits + " || '000000000'), 1, 9)"
	// Reject unfamiliar suffixes instead of silently interpreting their local
	// wall-clock prefix as UTC. Only driver-format offsets, plain UTC text and
	// a trailing Z are supported; unknown representations remain unpruned.
	validBase := "(" + baseEnd + " = 19 OR (substr(" + value + ", 20, 1) = '.' AND " + baseEnd + " BETWEEN 21 AND 29 AND substr(" + value + ", 21, " + baseEnd + " - 20) NOT GLOB '*[^0-9]*'))"
	// Space-separated, zone-less SQLite timestamps are UTC by convention.
	// ISO T timestamps need an explicit supported offset or trailing Z; a
	// bare ISO wall time has no confirmed timezone and must remain unpruned.
	confirmedZone := "(substr(" + value + ", 11, 1) = ' ' OR " + offsetPosition + " > 0 OR substr(" + value + ", -1, 1) = 'Z')"
	return "(CASE WHEN " + validBase + " AND " + confirmedZone + " THEN strftime('%Y-%m-%d %H:%M:%S', " + normalizedTime + ") || '.' || " + paddedFraction + " ELSE NULL END)"
}
