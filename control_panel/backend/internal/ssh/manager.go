package ssh

import (
	"context"
	"errors"
	"fmt"
	"net"
	"sync"
	"time"

	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"

	xssh "golang.org/x/crypto/ssh"
)

// pooledConn wraps an SSH client with the time it was released back to the
// pool. The releasedAt timestamp lets the idle-eviction goroutine close
// connections that haven't been reused within idleTimeout (spec §5: "idle
// connections closed after 5 min").
type pooledConn struct {
	client     *xssh.Client
	releasedAt time.Time
}

type Manager struct {
	cipher      *crypto.Cipher
	poolSize    int
	idleTimeout time.Duration
	mu          sync.Mutex
	pools       map[int64][]pooledConn // workerID -> idle connections (LIFO: tail = most recent)
	stopCh      chan struct{}
	closeOnce   sync.Once
}

func NewManager(c *crypto.Cipher, poolSize int, idle time.Duration) *Manager {
	if poolSize < 1 {
		poolSize = 1
	}
	m := &Manager{
		cipher:      c,
		poolSize:    poolSize,
		idleTimeout: idle,
		pools:       map[int64][]pooledConn{},
		stopCh:      make(chan struct{}),
	}
	// Spec §5: idle connections are closed after idleTimeout. The eviction
	// goroutine ticks every idleTimeout/2 (capped at 1 minute) so eviction
	// lag stays within one idleTimeout. When idleTimeout <= 0 (useful for
	// tests), no goroutine is started.
	if idle > 0 {
		go m.idleEvictLoop()
	}
	return m
}

// idleEvictLoop periodically closes pooled connections that have been idle
// (released but not re-acquired) for longer than idleTimeout. It exits when
// stopCh is closed (Manager.Close).
func (m *Manager) idleEvictLoop() {
	tick := m.idleTimeout / 2
	if tick > time.Minute {
		tick = time.Minute
	}
	if tick <= 0 {
		tick = time.Minute
	}
	t := time.NewTicker(tick)
	defer t.Stop()
	for {
		select {
		case <-m.stopCh:
			return
		case <-t.C:
			m.evictIdle()
		}
	}
}

// evictIdle closes pooled clients whose time since release exceeds
// idleTimeout. Closing an SSH client closes the underlying TCP connection (a
// fast syscall), so it is safe to do under the mutex.
func (m *Manager) evictIdle() {
	m.mu.Lock()
	defer m.mu.Unlock()
	now := time.Now()
	for wID, pool := range m.pools {
		kept := pool[:0]
		for _, pc := range pool {
			if now.Sub(pc.releasedAt) > m.idleTimeout {
				pc.client.Close()
				continue
			}
			kept = append(kept, pc)
		}
		m.pools[wID] = kept
	}
}

// Close stops the idle-eviction goroutine (if running) and closes all pooled
// SSH clients, clearing the pools. It is safe to call multiple times.
func (m *Manager) Close() {
	m.closeOnce.Do(func() { close(m.stopCh) })
	m.mu.Lock()
	defer m.mu.Unlock()
	for wID, pool := range m.pools {
		for _, pc := range pool {
			pc.client.Close()
		}
		delete(m.pools, wID)
	}
}

// buildAuth constructs auth methods in priority order: private key first
// (if EncPrivateKey set + decrypts + parses), then password (if EncPassword
// set + decrypts). Key-first, password-fallback. If neither produces a
// usable method, an error is returned.
func (m *Manager) buildAuth(w db.WorkerNode) ([]xssh.AuthMethod, error) {
	var methods []xssh.AuthMethod
	if w.EncPrivateKey != nil {
		key, err := m.cipher.Decrypt(*w.EncPrivateKey)
		if err != nil {
			return nil, fmt.Errorf("decrypt private key: %w", err)
		}
		signer, err := xssh.ParsePrivateKey(key)
		if err == nil {
			methods = append(methods, xssh.PublicKeys(signer))
		}
	}
	if w.EncPassword != nil {
		pw, err := m.cipher.Decrypt(*w.EncPassword)
		if err != nil {
			return nil, fmt.Errorf("decrypt password: %w", err)
		}
		methods = append(methods, xssh.Password(string(pw)))
	}
	if len(methods) == 0 {
		return nil, errors.New("no credentials configured for worker")
	}
	return methods, nil
}

func (m *Manager) dial(ctx context.Context, w db.WorkerNode) (*xssh.Client, error) {
	methods, err := m.buildAuth(w)
	if err != nil {
		return nil, err
	}
	cfg := &xssh.ClientConfig{
		User:            w.Username,
		Auth:            methods,
		HostKeyCallback: xssh.InsecureIgnoreHostKey(), // internal network deployment, trusted
		Timeout:         10 * time.Second,
	}
	addr := fmt.Sprintf("%s:%d", w.Host, w.Port)
	d := net.Dialer{}
	conn, err := d.DialContext(ctx, "tcp", addr)
	if err != nil {
		return nil, err
	}
	ncc, chans, reqs, err := xssh.NewClientConn(conn, addr, cfg)
	if err != nil {
		conn.Close()
		return nil, err
	}
	// NewClient wraps the Conn into a *Client and internally handles
	// global requests (DiscardRequests equivalent) and channel opens
	// (rejecting unknown channel types) - the manual goroutines in the
	// brief's draft are unnecessary with this API.
	return xssh.NewClient(ncc, chans, reqs), nil
}
