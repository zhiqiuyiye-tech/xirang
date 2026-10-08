package ssh

import (
	"context"
	"crypto/ed25519"
	"crypto/rand"
	"errors"
	"fmt"
	"net"
	"strconv"
	"sync"
	"testing"
	"time"

	xssh "golang.org/x/crypto/ssh"
	"xirang/control_panel/internal/db"
)

type healthSSHServer struct {
	listener    net.Listener
	mu          sync.Mutex
	connections []net.Conn
}

func (s *healthSSHServer) closeConnections() {
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, conn := range s.connections {
		_ = conn.Close()
	}
}

// Serve actual SSH traffic, with deliberately stalled protocol stages to
// reproduce unreachable pooled transports and servers ignoring requests.
func startHealthSSHServer(t *testing.T, mode string) (*healthSSHServer, db.WorkerNode) {
	t.Helper()
	listener, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	server := &healthSSHServer{listener: listener}
	t.Cleanup(func() { _ = listener.Close(); server.closeConnections() })
	_, key, err := ed25519.GenerateKey(rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	signer, err := xssh.NewSignerFromKey(key)
	if err != nil {
		t.Fatal(err)
	}
	config := &xssh.ServerConfig{PasswordCallback: func(_ xssh.ConnMetadata, password []byte) (*xssh.Permissions, error) {
		if string(password) != "correct" {
			return nil, fmt.Errorf("password rejected")
		}
		return nil, nil
	}}
	config.AddHostKey(signer)
	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			server.mu.Lock()
			server.connections = append(server.connections, conn)
			number := len(server.connections)
			server.mu.Unlock()
			go func() {
				defer conn.Close()
				if mode == "handshake" {
					_, _ = conn.Read(make([]byte, 4096))
					_, _ = conn.Read(make([]byte, 4096))
					return
				}
				sc, chans, requests, err := xssh.NewServerConn(conn, config)
				if err != nil {
					return
				}
				defer sc.Close()
				go func() {
					for req := range requests {
						if mode == "stale_pool" && number == 1 {
							continue
						}
						if req.WantReply {
							_ = req.Reply(false, nil)
						}
					}
				}()
				for newChannel := range chans {
					if mode == "session" {
						continue
					}
					channel, requests, err := newChannel.Accept()
					if err != nil {
						continue
					}
					go func() {
						defer channel.Close()
						for req := range requests {
							if mode == "exec" {
								continue
							}
							if req.WantReply {
								_ = req.Reply(true, nil)
							}
							if req.Type != "exec" {
								continue
							}
							if mode == "wait" {
								continue
							}
							status := uint32(0)
							if mode == "nonzero" {
								status = 7
							}
							// Exercise output collection as well as successful exit status.
							_, _ = channel.Write([]byte("healthy\n"))
							_, _ = channel.SendRequest("exit-status", false, xssh.Marshal(struct{ Status uint32 }{status}))
							return
						}
					}()
				}
			}()
		}
	}()
	host, port, err := net.SplitHostPort(listener.Addr().String())
	if err != nil {
		t.Fatal(err)
	}
	p, err := strconv.Atoi(port)
	if err != nil {
		t.Fatal(err)
	}
	password := mustEncrypt(t, "correct")
	return server, db.WorkerNode{ID: 101, Host: host, Port: p, Username: "root", EncPassword: &password}
}

func TestRunHonorsContextDuringEverySSHStage(t *testing.T) {
	for _, stage := range []string{"handshake", "session", "exec", "wait"} {
		t.Run(stage, func(t *testing.T) {
			server, w := startHealthSSHServer(t, stage)
			manager := newTestManager(t)
			defer manager.Close()
			ctx, cancel := context.WithTimeout(context.Background(), 60*time.Millisecond)
			defer cancel()
			done := make(chan error, 1)
			go func() { _, _, _, err := manager.Run(ctx, w, "true"); done <- err }()
			select {
			case err := <-done:
				if !errors.Is(err, context.DeadlineExceeded) {
					t.Fatalf("expected deadline error during %s, got %v", stage, err)
				}
			case <-time.After(750 * time.Millisecond):
				server.closeConnections()
				<-done
				t.Fatalf("SSH %s ignored context deadline", stage)
			}
		})
	}
}

func TestRunReplacesStalledPooledConnectionWithinDeadline(t *testing.T) {
	_, w := startHealthSSHServer(t, "stale_pool")
	manager := newTestManager(t)
	defer manager.Close()
	client, err := manager.dial(context.Background(), w)
	if err != nil {
		t.Fatal(err)
	}
	manager.release(w.ID, client)
	ctx, cancel := context.WithTimeout(context.Background(), 300*time.Millisecond)
	defer cancel()
	out, _, code, err := manager.Run(ctx, w, "true")
	if err != nil || code != 0 || out != "healthy\n" {
		t.Fatalf("stalled pooled connection prevented healthy fresh check: code=%d out=%q err=%v", code, out, err)
	}
}

func TestConnectionRejectsNonzeroRemoteExit(t *testing.T) {
	_, w := startHealthSSHServer(t, "nonzero")
	manager := newTestManager(t)
	defer manager.Close()
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	if err := manager.TestConnection(ctx, w); err == nil {
		t.Fatal("failed remote true command was reported healthy")
	}
}

func TestRunRejectsAuthenticationFailure(t *testing.T) {
	_, w := startHealthSSHServer(t, "healthy")
	wrong := mustEncrypt(t, "wrong")
	w.EncPassword = &wrong
	manager := newTestManager(t)
	defer manager.Close()
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()
	_, _, code, err := manager.Run(ctx, w, "true")
	if err == nil || code != -1 {
		t.Fatalf("authentication rejection accepted as healthy: code=%d err=%v", code, err)
	}
}
