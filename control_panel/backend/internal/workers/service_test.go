package workers

import (
	"context"
	"encoding/json"
	"errors"
	"io"
	"path/filepath"
	"testing"

	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
)

type fakeSSH struct{}

func (fakeSSH) Run(_ context.Context, _ db.WorkerNode, cmd string) (string, string, int, error) {
	return "ok", "", 0, nil
}
func (fakeSSH) TestConnection(_ context.Context, _ db.WorkerNode) error { return nil }

func setup(t *testing.T) *Service {
	t.Helper()
	s, _ := db.Open(filepath.Join(t.TempDir(), "t.db"))
	t.Cleanup(func() { s.Close() })
	c, _ := crypto.New(make([]byte, 32))
	sshm := ssh.NewManager(c, 2, 0)
	eng := tasks.NewEngine(s)
	return NewService(s, c, sshm, eng)
}

type workerSSHStub struct {
	testErr error
}

func (s *workerSSHStub) Run(_ context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	return "", "", 0, nil
}
func (s *workerSSHStub) RunWithStdin(_ context.Context, _ db.WorkerNode, _ string, _ io.Reader) (string, string, int, error) {
	return "", "", 0, nil
}
func (s *workerSSHStub) TestConnection(_ context.Context, _ db.WorkerNode) error { return s.testErr }

func TestConnectionPersistsWorkerStatus(t *testing.T) {
	store, err := db.Open(filepath.Join(t.TempDir(), "health.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	cipher, _ := crypto.New(make([]byte, 32))
	engine := tasks.NewEngine(store)
	stub := &workerSSHStub{}
	svc := NewService(store, cipher, stub, engine)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})

	if err := svc.TestConnection(context.Background(), id); err != nil {
		t.Fatal(err)
	}
	worker, _ := store.GetWorker(context.Background(), id)
	if worker.Status != "online" || worker.LastSeenAt == nil || worker.LastCheckedAt == nil {
		t.Fatalf("successful test did not persist online status: %+v", worker)
	}

	stub.testErr = errors.New("connection refused")
	if err := svc.TestConnection(context.Background(), id); err == nil {
		t.Fatal("expected connection failure")
	}
	worker, _ = store.GetWorker(context.Background(), id)
	if worker.Status != "offline" || worker.StatusError == nil || *worker.StatusError != "connection refused" {
		t.Fatalf("failed manual test did not persist offline status: %+v", worker)
	}
}

func TestCreateAndGet(t *testing.T) {
	svc := setup(t)
	id, err := svc.Create(context.Background(), CreateReq{Name: "w1", Host: "10.0.0.1", Port: 22, Username: "root"})
	if err != nil {
		t.Fatal(err)
	}
	got, _ := svc.Get(context.Background(), id)
	if got.Name != "w1" {
		t.Fatalf("name=%q", got.Name)
	}
}

// TestCreateRejectsBadPort verifies the port range validation (1-65535).
func TestCreateRejectsBadPort(t *testing.T) {
	svc := setup(t)
	if _, err := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 99999, Username: "root"}); err == nil {
		t.Fatal("expected error for out-of-range port")
	}
	if _, err := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: -1, Username: "root"}); err == nil {
		t.Fatal("expected error for negative port")
	}
}

// TestUpdatePartialKeepsOmittedFields verifies partial-update semantics: a
// PUT that only changes the name must NOT zero port/username/host (a zero
// port would produce host:0 and break SSH entirely).
func TestUpdatePartialKeepsOmittedFields(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "10.0.0.1", Port: 2222, Username: "ops"})
	if err := svc.Update(context.Background(), id, UpdateReq{Name: "renamed"}); err != nil {
		t.Fatal(err)
	}
	got, _ := svc.Get(context.Background(), id)
	if got.Name != "renamed" {
		t.Fatalf("name=%q want renamed", got.Name)
	}
	if got.Host != "10.0.0.1" {
		t.Fatalf("host=%q, want unchanged 10.0.0.1", got.Host)
	}
	if got.Port != 2222 {
		t.Fatalf("port=%d, want unchanged 2222 (zero value must not clobber)", got.Port)
	}
	if got.Username != "ops" {
		t.Fatalf("username=%q, want unchanged ops", got.Username)
	}
}

// TestUpdateRejectsBadPort verifies an explicitly provided invalid port is
// rejected rather than silently ignored.
func TestUpdateRejectsBadPort(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	if err := svc.Update(context.Background(), id, UpdateReq{Port: 70000}); err == nil {
		t.Fatal("expected error for out-of-range port")
	}
	// The failed update must not have modified the worker.
	got, _ := svc.Get(context.Background(), id)
	if got.Port != 22 {
		t.Fatalf("port=%d, want unchanged 22", got.Port)
	}
}

func TestSetPanelPassword(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	if err := svc.SetPanelPassword(context.Background(), id, "secret"); err != nil {
		t.Fatal(err)
	}
	got, _ := svc.Get(context.Background(), id)
	if got.EncPassword == nil || *got.EncPassword == "secret" {
		t.Fatalf("password not encrypted: %+v", got.EncPassword)
	}
	if got.AuthMode != "password" {
		t.Fatalf("auth_mode=%q", got.AuthMode)
	}
}

func TestSetPrivateKeySetsBothMode(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	svc.SetPanelPassword(context.Background(), id, "pw") // 先设密码
	if err := svc.SetPrivateKey(context.Background(), id, "-----BEGIN RSA PRIVATE KEY-----\nx\n-----END RSA PRIVATE KEY-----"); err != nil {
		t.Fatal(err)
	}
	got, _ := svc.Get(context.Background(), id)
	if got.AuthMode != "both" {
		t.Fatalf("auth_mode=%q want both", got.AuthMode)
	}
}

func TestChangeRootPasswordSubmitsTask(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	// ChangeRootPassword 需能连上；本测试聚焦于"提交任务"，连接用真 ssh manager 到不可达主机应失败任务
	taskID, err := svc.ChangeRootPassword(context.Background(), id, "newpw")
	if err != nil {
		t.Fatal(err)
	}
	if taskID <= 0 {
		t.Fatal("expected task id")
	}
}

// TestChangeRootPasswordEncryptsParams verifies C1: the password stored in
// tasks.params_json is AES-encrypted, not plaintext. After ChangeRootPassword
// returns, the task row's params_json should contain a base64 ciphertext that
// decrypts back to the original password.
func TestChangeRootPasswordEncryptsParams(t *testing.T) {
	svc := setup(t)
	id, _ := svc.Create(context.Background(), CreateReq{Name: "w", Host: "h", Port: 22, Username: "root"})
	plaintext := "s3cr3t'with\"quotes"
	taskID, err := svc.ChangeRootPassword(context.Background(), id, plaintext)
	if err != nil {
		t.Fatal(err)
	}
	task, err := svc.store.GetTask(context.Background(), taskID)
	if err != nil {
		t.Fatal(err)
	}
	var p struct {
		Password string `json:"password"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		t.Fatal(err)
	}
	if p.Password == "" {
		t.Fatal("params_json password is empty")
	}
	if p.Password == plaintext {
		t.Fatal("params_json contains plaintext password")
	}
	dec, err := svc.c.Decrypt(p.Password)
	if err != nil {
		t.Fatalf("decrypt failed: %v", err)
	}
	if string(dec) != plaintext {
		t.Fatalf("decrypted=%q want=%q", string(dec), plaintext)
	}
}
