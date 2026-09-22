package ssh

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io"
	"net"
	"strings"
	"testing"
	"time"

	xssh "golang.org/x/crypto/ssh"

	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
)

func startTestSSHd(t *testing.T, rootPassword string) (addr string, testPrivKey string) {
	t.Helper()
	l, err := net.Listen("tcp", "127.0.0.1:0")
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { l.Close() })

	k, err := rsa.GenerateKey(rand.Reader, 2048)
	if err != nil {
		t.Fatal(err)
	}
	der := x509.MarshalPKCS1PrivateKey(k)
	testPrivKey = string(pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: der}))

	pub, err := xssh.NewPublicKey(&k.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	authorized := string(xssh.MarshalAuthorizedKey(pub))

	config := &xssh.ServerConfig{
		PasswordCallback: func(c xssh.ConnMetadata, pass []byte) (*xssh.Permissions, error) {
			if c.User() == "root" && string(pass) == rootPassword {
				return nil, nil
			}
			return nil, fmt.Errorf("password rejected")
		},
		PublicKeyCallback: func(c xssh.ConnMetadata, key xssh.PublicKey) (*xssh.Permissions, error) {
			if string(xssh.MarshalAuthorizedKey(key)) == authorized {
				return nil, nil
			}
			return nil, fmt.Errorf("pubkey rejected")
		},
	}
	signer, err := xssh.NewSignerFromKey(k)
	if err != nil {
		t.Fatal(err)
	}
	config.AddHostKey(signer)

	go func() {
		for {
			conn, err := l.Accept()
			if err != nil {
				return
			}
			go func(c net.Conn) {
				defer c.Close()
				_, chans, reqs, err := xssh.NewServerConn(c, config)
				if err != nil {
					return
				}
				go xssh.DiscardRequests(reqs)
				for newCh := range chans {
					ch, reqs, _ := newCh.Accept()
					go func(ch xssh.Channel, reqs <-chan *xssh.Request) {
						defer ch.Close()
						// Handle exec/shell request: the client's Session.Start
						// sends an "exec" request with wantReply=true and blocks
						// until a response is received. Reply true, then write
						// stdout and send exit-status 0.
						for req := range reqs {
							if req.WantReply {
								req.Reply(true, nil)
							}
							if req.Type == "exec" || req.Type == "shell" {
								break
							}
						}
						_, _ = io.Copy(io.Discard, ch)
						ch.Write([]byte("hello\n"))
						ch.SendRequest("exit-status", false, xssh.Marshal(struct{ C uint32 }{0}))
					}(ch, reqs)
				}
			}(conn)
		}
	}()
	return l.Addr().String(), testPrivKey
}

func newTestManager(t *testing.T) *Manager {
	c, err := crypto.New(make([]byte, 32))
	if err != nil {
		t.Fatal(err)
	}
	return NewManager(c, 2, time.Minute)
}

func mustEncrypt(t *testing.T, s string) string {
	t.Helper()
	c, _ := crypto.New(make([]byte, 32))
	enc, err := c.Encrypt([]byte(s))
	if err != nil {
		t.Fatal(err)
	}
	return enc
}

func TestRun_PasswordAuth(t *testing.T) {
	addr, _ := startTestSSHd(t, "pw123")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	encPw := mustEncrypt(t, "pw123")
	w := db.WorkerNode{ID: 1, Host: host, Port: p, Username: "root", AuthMode: "password", EncPassword: &encPw}
	m := newTestManager(t)
	out, _, code, err := m.Run(context.Background(), w, "true")
	if err != nil {
		t.Fatalf("err: %v", err)
	}
	if code != 0 || out == "" {
		t.Fatalf("code=%d out=%q", code, out)
	}
}

func TestRun_KeyAuth(t *testing.T) {
	addr, priv := startTestSSHd(t, "should-not-be-used")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	encKey := mustEncrypt(t, priv)
	w := db.WorkerNode{ID: 2, Host: host, Port: p, Username: "root", AuthMode: "key", EncPrivateKey: &encKey}
	m := newTestManager(t)
	if _, _, _, err := m.Run(context.Background(), w, "true"); err != nil {
		t.Fatalf("key auth err: %v", err)
	}
}

func TestRun_KeyFallsBackToPassword(t *testing.T) {
	addr, _ := startTestSSHd(t, "pw123")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	badKey := mustEncrypt(t, "-----BEGIN RSA PRIVATE KEY-----\ninvalid\n-----END RSA PRIVATE KEY-----")
	goodPw := mustEncrypt(t, "pw123")
	w := db.WorkerNode{ID: 3, Host: host, Port: p, Username: "root", AuthMode: "both", EncPrivateKey: &badKey, EncPassword: &goodPw}
	m := newTestManager(t)
	if _, _, _, err := m.Run(context.Background(), w, "true"); err != nil {
		t.Fatalf("fallback failed: %v", err)
	}
}

func TestRun_AllFail(t *testing.T) {
	addr, _ := startTestSSHd(t, "correct")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	badPw := mustEncrypt(t, "wrong")
	w := db.WorkerNode{ID: 4, Host: host, Port: p, Username: "root", AuthMode: "password", EncPassword: &badPw}
	m := newTestManager(t)
	if _, _, _, err := m.Run(context.Background(), w, "true"); err == nil {
		t.Fatal("expected error when all auth fails")
	}
}

// TestRunWithStdin verifies C3: RunWithStdin can execute a command while
// feeding stdin to the remote process. The test SSH server accepts any exec
// command and replies with stdout "hello" + exit-status 0; the stdin written
// by the client is buffered by the channel and discarded. This confirms the
// plumbing (sess.Stdin + sess.Start + sess.Wait) works end-to-end without
// hanging or error.
func TestRunWithStdin(t *testing.T) {
	addr, _ := startTestSSHd(t, "pw123")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	encPw := mustEncrypt(t, "pw123")
	w := db.WorkerNode{ID: 5, Host: host, Port: p, Username: "root", AuthMode: "password", EncPassword: &encPw}
	m := newTestManager(t)
	stdin := strings.NewReader("root:newpass\n")
	out, _, code, err := m.RunWithStdin(context.Background(), w, "chpasswd", stdin)
	if err != nil {
		t.Fatalf("err: %v", err)
	}
	if code != 0 {
		t.Fatalf("code=%d out=%q", code, out)
	}
}

// TestRunWithStdin_NilStdin verifies that RunWithStdin with a nil stdin
// reader behaves identically to Run (the existing callers that don't need
// stdin are unaffected).
func TestRunWithStdin_NilStdin(t *testing.T) {
	addr, _ := startTestSSHd(t, "pw123")
	host, port, _ := net.SplitHostPort(addr)
	p := 0
	fmt.Sscanf(port, "%d", &p)
	encPw := mustEncrypt(t, "pw123")
	w := db.WorkerNode{ID: 6, Host: host, Port: p, Username: "root", AuthMode: "password", EncPassword: &encPw}
	m := newTestManager(t)
	out, _, code, err := m.RunWithStdin(context.Background(), w, "true", nil)
	if err != nil {
		t.Fatalf("err: %v", err)
	}
	if code != 0 || out == "" {
		t.Fatalf("code=%d out=%q", code, out)
	}
}
