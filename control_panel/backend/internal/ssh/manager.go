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

type Manager struct {
	cipher      *crypto.Cipher
	poolSize    int
	idleTimeout time.Duration
	mu          sync.Mutex
	pools       map[int64][]*xssh.Client // workerID -> idle connections
}

func NewManager(c *crypto.Cipher, poolSize int, idle time.Duration) *Manager {
	if poolSize < 1 {
		poolSize = 1
	}
	return &Manager{cipher: c, poolSize: poolSize, idleTimeout: idle, pools: map[int64][]*xssh.Client{}}
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
