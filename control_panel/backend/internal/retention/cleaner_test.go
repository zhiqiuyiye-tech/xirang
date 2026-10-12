package retention

import (
	"context"
	"errors"
	"testing"
	"time"

	"xirang/control_panel/internal/db"
)

type pruneFunc func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error)

func (f pruneFunc) PruneHistory(ctx context.Context, now time.Time, policy db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
	return f(ctx, now, policy)
}

func testPolicy() db.HistoryRetentionPolicy {
	return db.HistoryRetentionPolicy{TaskRetention: 90 * 24 * time.Hour, AuditRetention: 365 * 24 * time.Hour, BatchSize: 500}
}

func TestSweepDrainsBoundedBatchesWithFixedCutoff(t *testing.T) {
	now := time.Date(2026, 10, 11, 0, 0, 0, 0, time.UTC)
	results := []db.HistoryPruneResult{{Tasks: 2, Steps: 500, Audit: 4}, {Tasks: 3, Steps: 1, Audit: 5}, {}}
	calls := 0
	store := pruneFunc(func(_ context.Context, gotNow time.Time, policy db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		if !gotNow.Equal(now) || policy != testPolicy() {
			t.Errorf("wrong cutoff/policy: %v %+v", gotNow, policy)
		}
		if calls >= len(results) {
			t.Fatal("continued after empty batch")
		}
		result := results[calls]
		calls++
		return result, nil
	})
	cleaner, err := New(store, testPolicy(), time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	got, err := cleaner.Sweep(context.Background(), now)
	want := db.HistoryPruneResult{Tasks: 5, Steps: 501, Audit: 9}
	if err != nil || got != want || calls != 3 {
		t.Fatalf("result=%+v err=%v calls=%d", got, err, calls)
	}
}

func TestSweepReturnsCommittedCountsOnFailure(t *testing.T) {
	failure := errors.New("test failure")
	calls := 0
	cleaner, err := New(pruneFunc(func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		calls++
		if calls == 1 {
			return db.HistoryPruneResult{Steps: 10}, nil
		}
		return db.HistoryPruneResult{}, failure
	}), testPolicy(), time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	got, err := cleaner.Sweep(context.Background(), time.Now().UTC())
	if !errors.Is(err, failure) || got != (db.HistoryPruneResult{Steps: 10}) || calls != 2 {
		t.Fatalf("result=%+v err=%v calls=%d", got, err, calls)
	}
}

func TestSweepCancellationStopsBeforeNextBatch(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	calls := 0
	cleaner, err := New(pruneFunc(func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		calls++
		cancel()
		return db.HistoryPruneResult{Tasks: 1}, nil
	}), testPolicy(), time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	got, err := cleaner.Sweep(ctx, time.Now().UTC())
	if !errors.Is(err, context.Canceled) || got.Tasks != 1 || calls != 1 {
		t.Fatalf("result=%+v err=%v calls=%d", got, err, calls)
	}
}

func TestRunStartsPeriodicallyAndStops(t *testing.T) {
	calls := make(chan struct{}, 10)
	store := pruneFunc(func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		calls <- struct{}{}
		return db.HistoryPruneResult{}, nil
	})
	cleaner, err := New(store, testPolicy(), 10*time.Millisecond)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	done := make(chan struct{})
	go func() { defer close(done); cleaner.Run(ctx) }()
	for n := 0; n < 2; n++ {
		select {
		case <-calls:
		case <-time.After(2 * time.Second):
			t.Fatal("missing initial or periodic cleanup")
		}
	}
	cancel()
	select {
	case <-done:
	case <-time.After(2 * time.Second):
		t.Fatal("cleaner did not stop on cancellation")
	}
}

func TestRunCancelledContextDoesNotPrune(t *testing.T) {
	calls := 0
	cleaner, err := New(pruneFunc(func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		calls++
		return db.HistoryPruneResult{}, nil
	}), testPolicy(), time.Hour)
	if err != nil {
		t.Fatal(err)
	}
	ctx, cancel := context.WithCancel(context.Background())
	cancel()
	cleaner.Run(ctx)
	if calls != 0 {
		t.Fatalf("cancelled cleaner pruned %d batches", calls)
	}
}

func TestNewRejectsInvalidConfiguration(t *testing.T) {
	store := pruneFunc(func(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error) {
		return db.HistoryPruneResult{}, nil
	})
	for _, tc := range []struct {
		store    Pruner
		policy   db.HistoryRetentionPolicy
		interval time.Duration
	}{
		{nil, testPolicy(), time.Hour},
		{store, db.HistoryRetentionPolicy{}, time.Hour},
		{store, db.HistoryRetentionPolicy{TaskRetention: time.Hour, AuditRetention: time.Hour, BatchSize: -1}, time.Hour},
		{store, testPolicy(), 0},
	} {
		if got, err := New(tc.store, tc.policy, tc.interval); got != nil || err == nil {
			t.Errorf("invalid config accepted: %+v cleaner=%v err=%v", tc, got, err)
		}
	}
}
