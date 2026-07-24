package ssh

import (
	"bytes"
	"context"
	"time"

	xssh "golang.org/x/crypto/ssh"

	"xirang/control_panel/internal/db"
)

func (m *Manager) acquire(ctx context.Context, w db.WorkerNode) (*xssh.Client, error) {
	m.mu.Lock()
	pool := m.pools[w.ID]
	if len(pool) > 0 {
		c := pool[len(pool)-1]
		m.pools[w.ID] = pool[:len(pool)-1]
		m.mu.Unlock()
		return c, nil
	}
	m.mu.Unlock()
	return m.dial(ctx, w)
}

func (m *Manager) release(wID int64, c *xssh.Client) {
	m.mu.Lock()
	defer m.mu.Unlock()
	pool := m.pools[wID]
	if len(pool) >= m.poolSize {
		c.Close()
		return
	}
	m.pools[wID] = append(pool, c)
}

func (m *Manager) Run(ctx context.Context, w db.WorkerNode, cmd string) (stdout, stderr string, exitCode int, err error) {
	client, err := m.acquire(ctx, w)
	if err != nil {
		return "", "", -1, err
	}
	defer m.release(w.ID, client)
	sess, err := client.NewSession()
	if err != nil {
		return "", "", -1, err
	}
	defer sess.Close()
	var outB, errB bytes.Buffer
	sess.Stdout = &outB
	sess.Stderr = &errB
	if err := sess.Start(cmd); err != nil {
		return "", "", -1, err
	}
	done := make(chan error, 1)
	go func() { done <- sess.Wait() }()
	select {
	case err := <-done:
		if ee, ok := err.(*xssh.ExitError); ok {
			return outB.String(), errB.String(), ee.ExitStatus(), nil
		}
		if err != nil {
			return outB.String(), errB.String(), -1, err
		}
		return outB.String(), errB.String(), 0, nil
	case <-ctx.Done():
		_ = sess.Signal(xssh.SIGKILL)
		return outB.String(), errB.String(), -1, ctx.Err()
	}
}

func (m *Manager) TestConnection(ctx context.Context, w db.WorkerNode) error {
	ctx, cancel := context.WithTimeout(ctx, 15*time.Second)
	defer cancel()
	_, _, _, err := m.Run(ctx, w, "true")
	return err
}
