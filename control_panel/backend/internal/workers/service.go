package workers

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"strings"

	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
)

type CreateReq struct {
	Name     string
	Host     string
	Port     int
	Username string
}
type UpdateReq struct {
	Name     string
	Host     string
	Port     int
	Username string
}

type Service struct {
	store *db.Store
	c     *crypto.Cipher
	sshm  *ssh.Manager
	eng   *tasks.Engine
}

func NewService(store *db.Store, c *crypto.Cipher, sshm *ssh.Manager, eng *tasks.Engine) *Service {
	s := &Service{store: store, c: c, sshm: sshm, eng: eng}
	eng.Register("set_root_password", &rootPasswordHandler{service: s})
	return s
}

func (s *Service) Create(ctx context.Context, r CreateReq) (int64, error) {
	if r.Name == "" || r.Host == "" {
		return 0, errors.New("name and host required")
	}
	if r.Port == 0 {
		r.Port = 22
	}
	if r.Username == "" {
		r.Username = "root"
	}
	return s.store.CreateWorker(ctx, db.WorkerNode{
		Name: r.Name, Host: r.Host, Port: r.Port, Username: r.Username, AuthMode: "key",
	})
}

func (s *Service) List(ctx context.Context) ([]db.WorkerNode, error) {
	return s.store.ListWorkers(ctx)
}

func (s *Service) Get(ctx context.Context, id int64) (*db.WorkerNode, error) {
	return s.store.GetWorker(ctx, id)
}

func (s *Service) Update(ctx context.Context, id int64, r UpdateReq) error {
	w, err := s.store.GetWorker(ctx, id)
	if err != nil {
		return err
	}
	w.Name, w.Host, w.Port, w.Username = r.Name, r.Host, r.Port, r.Username
	return s.store.UpdateWorker(ctx, *w)
}

func (s *Service) Delete(ctx context.Context, id int64) error {
	return s.store.DeleteWorker(ctx, id)
}

func (s *Service) TestConnection(ctx context.Context, id int64) error {
	w, err := s.store.GetWorker(ctx, id)
	if err != nil {
		return err
	}
	return s.sshm.TestConnection(ctx, *w)
}

func (s *Service) SetPrivateKey(ctx context.Context, id int64, pem string) error {
	w, err := s.store.GetWorker(ctx, id)
	if err != nil {
		return err
	}
	enc, err := s.c.Encrypt([]byte(pem))
	if err != nil {
		return err
	}
	mode := "key"
	if w.EncPassword != nil {
		mode = "both"
	}
	return s.store.SetWorkerCredentials(ctx, id, w.EncPassword, &enc, mode)
}

func (s *Service) SetPanelPassword(ctx context.Context, id int64, password string) error {
	w, err := s.store.GetWorker(ctx, id)
	if err != nil {
		return err
	}
	enc, err := s.c.Encrypt([]byte(password))
	if err != nil {
		return err
	}
	mode := "password"
	if w.EncPrivateKey != nil {
		mode = "both"
	}
	return s.store.SetWorkerCredentials(ctx, id, &enc, w.EncPrivateKey, mode)
}

// ChangeRootPassword 提交任务：SSH 到 worker 执行 chpasswd，成功后同步密码入库。
// The password is AES-encrypted before being stored in params_json so the
// tasks table never holds plaintext credentials (spec: DB 只存 AES 密文).
func (s *Service) ChangeRootPassword(ctx context.Context, id int64, password string) (int64, error) {
	enc, err := s.c.Encrypt([]byte(password))
	if err != nil {
		return 0, fmt.Errorf("encrypt password: %w", err)
	}
	return s.eng.Submit(ctx, "set_root_password", "worker", id, map[string]any{
		"password": enc,
	})
}

// rootPasswordHandler：任务执行体
type rootPasswordHandler struct {
	service *Service
}

func (h *rootPasswordHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		Password string `json:"password"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(err.Error())
		return err
	}
	// C1: params_json stores AES ciphertext, not plaintext. Decrypt before use.
	plain, err := h.service.c.Decrypt(p.Password)
	if err != nil {
		r.Fail(fmt.Sprintf("decrypt password: %v", err))
		return err
	}
	w, err := h.service.store.GetWorker(ctx, task.TargetID)
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	st, _ := r.Step("chpasswd")
	// C3: feed credentials via stdin instead of interpolating into the command
	// string. This prevents shell injection (a single quote in the password could
	// break out of the echo pipe) and hides the password from ps.
	cmd := "chpasswd"
	stdin := strings.NewReader(w.Username + ":" + string(plain) + "\n")
	_, stderr, code, err := h.service.sshm.RunWithStdin(ctx, *w, cmd, stdin)
	if err != nil || code != 0 {
		st.Done("failed", "", stderr, fmt.Sprintf("chpasswd failed code=%d err=%v", code, err))
		r.Fail(fmt.Sprintf("chpasswd failed: %s", stderr))
		return errors.New("chpasswd failed")
	}
	st.Done("succeeded", "ok", "", "")
	// 成功后同步密码入库（等价于执行了 SetPanelPassword）
	enc, _ := h.service.c.Encrypt(plain)
	mode := "password"
	if w.EncPrivateKey != nil {
		mode = "both"
	}
	if err := h.service.store.SetWorkerCredentials(ctx, w.ID, &enc, w.EncPrivateKey, mode); err != nil {
		r.Fail(err.Error())
		return err
	}
	r.Succeed()
	return nil
}
