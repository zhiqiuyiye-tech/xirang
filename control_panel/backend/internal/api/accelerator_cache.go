package api

import (
	"context"
	"crypto/sha256"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/workers"
)

type workerAcceleratorIdentity struct {
	host        string
	port        int
	username    string
	authMode    string
	credentials [32]byte
}

type workerAcceleratorCacheEntry struct {
	identity workerAcceleratorIdentity
	done     chan struct{}
	info     workers.AcceleratorInfo
	retryAt  time.Time
}

func acceleratorIdentity(node db.WorkerNode) workerAcceleratorIdentity {
	var password, privateKey string
	if node.EncPassword != nil {
		password = *node.EncPassword
	}
	if node.EncPrivateKey != nil {
		privateKey = *node.EncPrivateKey
	}
	return workerAcceleratorIdentity{node.Host, node.Port, node.Username, node.AuthMode, sha256.Sum256([]byte(password + "\x00" + privateKey))}
}

// Hardware is stable across notebook changes. Only changed SSH configuration,
// explicit refresh or a retry of a failed probe should run vendor tools again.
// Heartbeats also change updated_at, so that timestamp is not a cache key.
func (h *workerHandlers) cachedAccelerators(ctx context.Context, node db.WorkerNode, refresh bool) workers.AcceleratorInfo {
	identity := acceleratorIdentity(node)
	h.acceleratorMu.Lock()
	if h.acceleratorCache == nil {
		h.acceleratorCache = make(map[int64]*workerAcceleratorCacheEntry)
	}
	entry := h.acceleratorCache[node.ID]
	if refresh || entry == nil || entry.identity != identity || (!entry.retryAt.IsZero() && !time.Now().Before(entry.retryAt)) {
		entry = &workerAcceleratorCacheEntry{identity: identity, done: make(chan struct{})}
		h.acceleratorCache[node.ID] = entry
		h.acceleratorMu.Unlock()
		info := h.ws.DiscoverAccelerators(ctx, node)
		h.acceleratorMu.Lock()
		entry.info = info
		if info.Status != "available" {
			entry.retryAt = time.Now().Add(30 * time.Second)
		}
		close(entry.done)
		h.acceleratorMu.Unlock()
		return info
	}
	h.acceleratorMu.Unlock()
	select {
	case <-entry.done:
		return entry.info
	case <-ctx.Done():
		return workers.AcceleratorInfo{Status: "unknown", Devices: []workers.AcceleratorModel{}, Error: "设备采集已取消"}
	}
}

func (h *workerHandlers) pruneAcceleratorCache(nodes []db.WorkerNode) {
	active := make(map[int64]bool, len(nodes))
	for _, node := range nodes {
		active[node.ID] = true
	}
	h.acceleratorMu.Lock()
	defer h.acceleratorMu.Unlock()
	for id := range h.acceleratorCache {
		if !active[id] {
			delete(h.acceleratorCache, id)
		}
	}
}
