package collector

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"sync"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/storage"
)

type Config struct {
	HeartbeatInterval time.Duration
	InventoryInterval time.Duration
	HeartbeatTimeout  time.Duration
	InventoryTimeout  time.Duration
	Concurrency       int
	OfflineThreshold  int
	ReservedMounts    []string
}

type jobKind string

const (
	jobHeartbeat jobKind = "heartbeat"
	jobInventory jobKind = "inventory"
)

type job struct {
	kind     jobKind
	workerID int64
}

type Collector struct {
	store  *db.Store
	runner ssh.Runner
	config Config
	queue  chan job

	startOnce  sync.Once
	mu         sync.Mutex
	pending    map[string]struct{}
	refreshing map[int64]bool
}

func New(store *db.Store, runner ssh.Runner, config Config) *Collector {
	if config.HeartbeatInterval <= 0 {
		config.HeartbeatInterval = time.Minute
	}
	if config.InventoryInterval <= 0 {
		config.InventoryInterval = 5 * time.Minute
	}
	if config.HeartbeatTimeout <= 0 {
		config.HeartbeatTimeout = 5 * time.Second
	}
	if config.InventoryTimeout <= 0 {
		config.InventoryTimeout = 45 * time.Second
	}
	if config.Concurrency <= 0 {
		config.Concurrency = 8
	}
	if config.OfflineThreshold <= 0 {
		config.OfflineThreshold = 2
	}
	if len(config.ReservedMounts) == 0 {
		config.ReservedMounts = []string{"/data01"}
	}
	return &Collector{
		store: store, runner: runner, config: config,
		queue: make(chan job, 1024), pending: make(map[string]struct{}), refreshing: make(map[int64]bool),
	}
}

func (c *Collector) Start(ctx context.Context) {
	c.startOnce.Do(func() {
		for i := 0; i < c.config.Concurrency; i++ {
			go c.worker(ctx)
		}
		go c.schedule(ctx)
	})
}

func (c *Collector) schedule(ctx context.Context) {
	heartbeatTicker := time.NewTicker(c.config.HeartbeatInterval)
	inventoryTicker := time.NewTicker(c.config.InventoryInterval)
	defer heartbeatTicker.Stop()
	defer inventoryTicker.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-heartbeatTicker.C:
			_, _ = c.EnqueueAllHeartbeats(ctx)
		case <-inventoryTicker.C:
			_, _ = c.EnqueueAllInventory(ctx)
		}
	}
}

func (c *Collector) worker(ctx context.Context) {
	for {
		select {
		case <-ctx.Done():
			return
		case item := <-c.queue:
			switch item.kind {
			case jobInventory:
				_ = c.collectInventory(ctx, item.workerID)
			case jobHeartbeat:
				_ = c.checkHeartbeat(ctx, item.workerID)
			}
			c.finish(item)
		}
	}
}

func jobKey(kind jobKind, workerID int64) string {
	return fmt.Sprintf("%s/%d", kind, workerID)
}

func (c *Collector) enqueue(item job) bool {
	key := jobKey(item.kind, item.workerID)
	c.mu.Lock()
	if _, exists := c.pending[key]; exists {
		c.mu.Unlock()
		return false
	}
	c.pending[key] = struct{}{}
	if item.kind == jobInventory {
		c.refreshing[item.workerID] = true
	}
	c.mu.Unlock()
	select {
	case c.queue <- item:
		return true
	default:
		c.mu.Lock()
		delete(c.pending, key)
		if item.kind == jobInventory {
			delete(c.refreshing, item.workerID)
		}
		c.mu.Unlock()
		return false
	}
}

func (c *Collector) finish(item job) {
	c.mu.Lock()
	defer c.mu.Unlock()
	delete(c.pending, jobKey(item.kind, item.workerID))
	if item.kind == jobInventory {
		delete(c.refreshing, item.workerID)
	}
}

func (c *Collector) EnqueueInventory(workerID int64) bool {
	return c.enqueue(job{kind: jobInventory, workerID: workerID})
}

func (c *Collector) EnqueueHeartbeat(workerID int64) bool {
	return c.enqueue(job{kind: jobHeartbeat, workerID: workerID})
}

func (c *Collector) EnqueueAllInventory(ctx context.Context) (int, error) {
	workers, err := c.store.ListWorkers(ctx)
	if err != nil {
		return 0, err
	}
	count := 0
	for _, worker := range workers {
		if c.EnqueueInventory(worker.ID) {
			count++
		}
	}
	return count, nil
}

func (c *Collector) EnqueueAllHeartbeats(ctx context.Context) (int, error) {
	workers, err := c.store.ListWorkers(ctx)
	if err != nil {
		return 0, err
	}
	count := 0
	for _, worker := range workers {
		if c.EnqueueHeartbeat(worker.ID) {
			count++
		}
	}
	return count, nil
}

func (c *Collector) IsInventoryRefreshing(workerID int64) bool {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.refreshing[workerID]
}

func (c *Collector) collectInventory(parent context.Context, workerID int64) error {
	worker, err := c.store.GetWorker(parent, workerID)
	if err != nil {
		return err
	}
	attemptedAt := time.Now().UTC()
	ctx, cancel := context.WithTimeout(parent, c.config.InventoryTimeout)
	defer cancel()
	inventory, err := storage.ListInventoryWithReserved(ctx, c.runner, *worker, c.config.ReservedMounts)
	if err != nil {
		message := truncateError(err.Error())
		_ = c.store.RecordInventoryFailure(parent, workerID, attemptedAt, message)
		return err
	}
	payload, err := json.Marshal(inventory)
	if err != nil {
		message := truncateError(err.Error())
		_ = c.store.RecordInventoryFailure(parent, workerID, attemptedAt, message)
		return err
	}
	collectedAt := time.Now().UTC()
	return c.store.SaveInventorySnapshot(parent, db.InventorySnapshot{
		WorkerID: workerID, SchemaVersion: 1, PayloadJSON: string(payload),
		CollectedAt: &collectedAt, LastAttemptedAt: attemptedAt,
	})
}

func (c *Collector) checkHeartbeat(parent context.Context, workerID int64) error {
	worker, err := c.store.GetWorker(parent, workerID)
	if err != nil {
		return err
	}
	checkedAt := time.Now().UTC()
	ctx, cancel := context.WithTimeout(parent, c.config.HeartbeatTimeout)
	defer cancel()
	_, stderr, code, runErr := c.runner.Run(ctx, *worker, "true")
	if runErr != nil || code != 0 {
		message := strings.TrimSpace(stderr)
		if runErr != nil {
			message = runErr.Error()
		}
		if message == "" {
			message = fmt.Sprintf("heartbeat exited %d", code)
		}
		if storeErr := c.store.RecordWorkerHealth(parent, workerID, false, checkedAt, truncateError(message), c.config.OfflineThreshold); storeErr != nil {
			return storeErr
		}
		if runErr != nil {
			return runErr
		}
		return fmt.Errorf("heartbeat exited %d", code)
	}
	return c.store.RecordWorkerHealth(parent, workerID, true, checkedAt, "", c.config.OfflineThreshold)
}

func truncateError(message string) string {
	const max = 2048
	message = strings.TrimSpace(message)
	if len(message) > max {
		return message[:max]
	}
	return message
}
