package ssh

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"time"

	xssh "golang.org/x/crypto/ssh"

	"xirang/control_panel/internal/db"
)

// keepaliveTimeout bounds the pooled-connection keepalive probe. A half-dead
// connection (peer rebooted, NAT entry expired) would otherwise block
// SendRequest until TCP retransmission gives up (~15 min on Linux), ignoring
// ctx cancellation and the caller's deadline entirely.
const keepaliveTimeout = 10 * time.Second

// errKeepaliveTimeout is returned when a pooled connection fails its bounded
// keepalive probe; the caller closes the connection and dials a fresh one.
var errKeepaliveTimeout = errors.New("ssh keepalive timed out")

// ping verifies a pooled client is still alive, bounded by keepaliveTimeout
// (and ctx). On timeout the client is closed, which forces the in-flight
// SendRequest to return and unblocks its goroutine.
func ping(ctx context.Context, c *xssh.Client) error {
	type result struct{ err error }
	done := make(chan result, 1)
	go func() {
		_, _, err := c.SendRequest("keepalive@openssh.com", true, nil)
		done <- result{err}
	}()
	probeTimeout := keepaliveTimeout
	if deadline, ok := ctx.Deadline(); ok {
		// Leave most of the caller's budget for a fresh connection if the idle
		// transport is half-dead. Otherwise a stale pool alone fails a heartbeat.
		if budget := time.Until(deadline) / 3; budget < probeTimeout {
			probeTimeout = budget
		}
	}
	t := time.NewTimer(probeTimeout)
	defer t.Stop()
	select {
	case r := <-done:
		return r.err
	case <-t.C:
		c.Close()
		return errKeepaliveTimeout
	case <-ctx.Done():
		c.Close()
		return ctx.Err()
	}
}

// Runner is the SSH command-execution interface. *Manager implements it.
// Handlers depend on the interface (not the concrete *Manager) so tests can
// inject a mock runner.
type Runner interface {
	Run(ctx context.Context, w db.WorkerNode, cmd string) (stdout, stderr string, exitCode int, err error)
	RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, stdin io.Reader) (stdout, stderr string, exitCode int, err error)
}

func (m *Manager) acquire(ctx context.Context, w db.WorkerNode) (*xssh.Client, error) {
	m.mu.Lock()
	pool := m.pools[w.ID]
	if len(pool) > 0 {
		// Pop the most-recently released connection (tail) - prefer fresh
		// connections whose underlying TCP is least likely to have been
		// reaped by an intermediary NAT/firewall.
		pc := pool[len(pool)-1]
		m.pools[w.ID] = pool[:len(pool)-1]
		m.mu.Unlock()
		// Spec §5: ping before use, evict and rebuild broken connections.
		// A keepalive global request verifies the underlying connection is
		// still alive; if it errors (or times out) the connection is dead -
		// close it and dial a new one. Only retry once (don't loop forever on
		// a bad pool).
		if err := ping(ctx, pc.client); err != nil {
			pc.client.Close()
			if ctx.Err() != nil {
				return nil, ctx.Err()
			}
			return m.dial(ctx, w)
		}
		return pc.client, nil
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
	m.pools[wID] = append(pool, pooledConn{client: c, releasedAt: time.Now()})
}

// Run executes cmd on w and returns stdout, stderr, exit code. It is a
// convenience wrapper around RunWithStdin for commands that don't need stdin.
func (m *Manager) Run(ctx context.Context, w db.WorkerNode, cmd string) (stdout, stderr string, exitCode int, err error) {
	return m.RunWithStdin(ctx, w, cmd, nil)
}

// RunWithStdin executes cmd on w, feeding stdin (if non-nil) to the process's
// stdin. Using stdin instead of interpolating values into the command string
// prevents shell injection and keeps secrets out of the process table (ps).
func (m *Manager) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, stdin io.Reader) (stdout, stderr string, exitCode int, err error) {
	client, err := m.acquire(ctx, w)
	if err != nil {
		return "", "", -1, fmt.Errorf("ssh connection acquisition: %w", err)
	}
	// NewSession and Start are synchronous SSH requests too, so watching only
	// Wait misses stalled channel opens and exec acknowledgements.
	stop := context.AfterFunc(ctx, func() { _ = client.Close() })
	reuse := false
	defer func() {
		if stopped := stop(); reuse && stopped && ctx.Err() == nil {
			m.release(w.ID, client)
		} else {
			client.Close()
		}
	}()
	sess, err := client.NewSession()
	if err != nil {
		if ctx.Err() != nil {
			err = ctx.Err()
		}
		return "", "", -1, fmt.Errorf("ssh session open: %w", err)
	}
	defer sess.Close()
	var outB, errB bytes.Buffer
	sess.Stdout = &outB
	sess.Stderr = &errB
	if stdin != nil {
		sess.Stdin = stdin
	}
	if err := sess.Start(cmd); err != nil {
		if ctx.Err() != nil {
			err = ctx.Err()
		}
		return "", "", -1, fmt.Errorf("ssh exec start: %w", err)
	}
	done := make(chan error, 1)
	go func() { done <- sess.Wait() }()
	select {
	case err := <-done:
		if ctx.Err() != nil {
			return outB.String(), errB.String(), -1, fmt.Errorf("ssh wait for command completion: %w", ctx.Err())
		}
		if ee, ok := err.(*xssh.ExitError); ok {
			reuse = true
			return outB.String(), errB.String(), ee.ExitStatus(), nil
		}
		if err != nil {
			return outB.String(), errB.String(), -1, err
		}
		reuse = true
		return outB.String(), errB.String(), 0, nil
	case <-ctx.Done():
		// Closing the transport interrupts SSH requests without relying on the
		// optional signal request (which can itself block). Wait for output-copy
		// goroutines before reading buffers to avoid a cancellation data race.
		_ = client.Close()
		<-done
		return outB.String(), errB.String(), -1, fmt.Errorf("ssh wait for command completion: %w", ctx.Err())
	}
}

func (m *Manager) TestConnection(ctx context.Context, w db.WorkerNode) error {
	ctx, cancel := context.WithTimeout(ctx, 15*time.Second)
	defer cancel()
	_, stderr, code, err := m.Run(ctx, w, "true")
	if err != nil {
		return err
	}
	if code != 0 {
		return fmt.Errorf("connection test exited %d: %s", code, stderr)
	}
	return nil
}
