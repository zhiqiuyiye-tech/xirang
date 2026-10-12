package config

import (
	"strings"
	"testing"
	"time"
)

func historyTestEnv(t *testing.T) {
	t.Helper()
	setMinimalEnv()
	t.Cleanup(unsetMinimalEnv)
	for _, key := range []string{"TASK_RETENTION_DAYS", "AUDIT_RETENTION_DAYS", "HISTORY_CLEANUP_INTERVAL", "HISTORY_CLEANUP_BATCH_SIZE"} {
		t.Setenv(key, "")
	}
}

func TestHistoryRetentionDefaults(t *testing.T) {
	historyTestEnv(t)
	cfg, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	if cfg.TaskRetention != 90*24*time.Hour || cfg.AuditRetention != 365*24*time.Hour || cfg.HistoryCleanupInterval != time.Hour || cfg.HistoryCleanupBatchSize != 500 {
		t.Fatalf("retention defaults: task=%s audit=%s interval=%s batch=%d", cfg.TaskRetention, cfg.AuditRetention, cfg.HistoryCleanupInterval, cfg.HistoryCleanupBatchSize)
	}
}

func TestHistoryRetentionCustomConfiguration(t *testing.T) {
	historyTestEnv(t)
	t.Setenv("TASK_RETENTION_DAYS", "30")
	t.Setenv("AUDIT_RETENTION_DAYS", "180")
	t.Setenv("HISTORY_CLEANUP_INTERVAL", "10m")
	t.Setenv("HISTORY_CLEANUP_BATCH_SIZE", "25")
	cfg, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	if cfg.TaskRetention != 30*24*time.Hour || cfg.AuditRetention != 180*24*time.Hour || cfg.HistoryCleanupInterval != 10*time.Minute || cfg.HistoryCleanupBatchSize != 25 {
		t.Fatalf("custom retention: task=%s audit=%s interval=%s batch=%d", cfg.TaskRetention, cfg.AuditRetention, cfg.HistoryCleanupInterval, cfg.HistoryCleanupBatchSize)
	}
}

func TestHistoryRetentionRejectsInvalidConfiguration(t *testing.T) {
	for _, tc := range []struct{ key, value string }{
		{"TASK_RETENTION_DAYS", "0"}, {"TASK_RETENTION_DAYS", "-1"}, {"TASK_RETENTION_DAYS", "90days"},
		{"TASK_RETENTION_DAYS", "106752"}, {"TASK_RETENTION_DAYS", "99999999999999999999999"},
		{"AUDIT_RETENTION_DAYS", "0"}, {"AUDIT_RETENTION_DAYS", "nonsense"},
		{"HISTORY_CLEANUP_INTERVAL", "0s"}, {"HISTORY_CLEANUP_INTERVAL", "invalid"},
		{"HISTORY_CLEANUP_INTERVAL", "1ns"}, {"HISTORY_CLEANUP_INTERVAL", "30s"},
		{"HISTORY_CLEANUP_BATCH_SIZE", "0"}, {"HISTORY_CLEANUP_BATCH_SIZE", "-1"}, {"HISTORY_CLEANUP_BATCH_SIZE", "500rows"},
	} {
		t.Run(tc.key+"="+tc.value, func(t *testing.T) {
			historyTestEnv(t)
			t.Setenv(tc.key, tc.value)
			if _, err := Load(); err == nil || !strings.Contains(err.Error(), tc.key) {
				t.Fatalf("invalid %s accepted or wrong error: %v", tc.key, err)
			}
		})
	}
}
