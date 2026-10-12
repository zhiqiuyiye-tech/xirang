// Package retention performs bounded history cleanup without changing resource snapshots.
package retention

import (
	"context"
	"fmt"
	"log"
	"time"

	"xirang/control_panel/internal/db"
)

const sweepBudget = 30 * time.Second

// Pruner commits one bounded database batch or reports a rolled-back failure.
type Pruner interface {
	PruneHistory(context.Context, time.Time, db.HistoryRetentionPolicy) (db.HistoryPruneResult, error)
}

type Cleaner struct {
	store    Pruner
	policy   db.HistoryRetentionPolicy
	interval time.Duration
}

func New(store Pruner, policy db.HistoryRetentionPolicy, interval time.Duration) (*Cleaner, error) {
	if store == nil || policy.TaskRetention <= 0 || policy.AuditRetention <= 0 || policy.BatchSize <= 0 || interval <= 0 {
		return nil, fmt.Errorf("history cleanup requires a store, positive retention durations, batch size and interval")
	}
	return &Cleaner{store: store, policy: policy, interval: interval}, nil
}

// Sweep drains separate small transactions using one stable cutoff. The caller
// supplies a deadline; cancellation is checked before every new batch.
func (c *Cleaner) Sweep(ctx context.Context, now time.Time) (db.HistoryPruneResult, error) {
	var total db.HistoryPruneResult
	for {
		if err := ctx.Err(); err != nil {
			return total, err
		}
		result, err := c.store.PruneHistory(ctx, now, c.policy)
		if err != nil {
			return total, err
		}
		total.Tasks += result.Tasks
		total.Steps += result.Steps
		total.Audit += result.Audit
		if result == (db.HistoryPruneResult{}) {
			return total, nil
		}
	}
}

// Run prunes at startup and periodically, and returns after cancellation. Each
// sweep is time-bounded so a large backlog cannot keep the worker busy forever.
func (c *Cleaner) Run(ctx context.Context) {
	if ctx.Err() != nil {
		return
	}
	c.runSweep(ctx)
	ticker := time.NewTicker(c.interval)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			c.runSweep(ctx)
		}
	}
}

func (c *Cleaner) runSweep(ctx context.Context) {
	if ctx.Err() != nil {
		return
	}
	sweepCtx, cancel := context.WithTimeout(ctx, sweepBudget)
	defer cancel()
	result, err := c.Sweep(sweepCtx, time.Now().UTC())
	if result != (db.HistoryPruneResult{}) {
		log.Printf("history cleanup: tasks=%d steps=%d audit=%d", result.Tasks, result.Steps, result.Audit)
	}
	if err != nil && ctx.Err() == nil {
		log.Printf("warn: history cleanup: %v", err)
	}
}
