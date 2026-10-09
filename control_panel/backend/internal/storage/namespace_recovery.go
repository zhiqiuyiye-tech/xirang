package storage

import (
	"bytes"
	"context"
	_ "embed"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"reflect"
	"regexp"
	"strings"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
)

// ErrNamespaceStateUnknown means remote cleanup exit/resource release could not
// be confirmed. The caller must quarantine subsequent destructive operations.
var ErrNamespaceStateUnknown = errors.New("namespace recovery state unknown")

//go:embed namespace_recovery.py
var namespaceRecoveryHelper string

type DeviceIdentity struct {
	UUID       string `json:"uuid"`
	MajorMinor string `json:"major_minor"`
}
type NamespaceSnapshot struct {
	Device  DeviceIdentity    `json:"device"`
	Holders []NamespaceHolder `json:"holders"`
}
type NamespaceHolder struct {
	PID       int                `json:"pid"`
	Namespace string             `json:"namespace"`
	StartTime string             `json:"start_time"`
	Cgroup    string             `json:"cgroup"`
	RootDev   uint64             `json:"root_dev"`
	RootIno   uint64             `json:"root_ino"`
	Mounts    []NamespaceMount   `json:"mounts"`
	Members   []NamespaceProcess `json:"members"`
}
type NamespaceProcess struct {
	PID       int    `json:"pid"`
	StartTime string `json:"start_time"`
	Cgroup    string `json:"cgroup"`
}
type NamespaceMount struct {
	ID       int      `json:"id"`
	ParentID int      `json:"parent_id"`
	Device   string   `json:"device"`
	Root     string   `json:"root"`
	Path     string   `json:"path"`
	Optional []string `json:"optional"`
}

type NamespaceRecovery struct {
	runner         ssh.Runner
	reserved       []string
	unmountTimeout time.Duration
}

func NewNamespaceRecovery(runner ssh.Runner, reserved []string, unmountTimeout time.Duration) *NamespaceRecovery {
	if unmountTimeout <= 0 {
		unmountTimeout = 10 * time.Second
	}
	if unmountTimeout > 10*time.Second {
		unmountTimeout = 10 * time.Second
	}
	return &NamespaceRecovery{runner: runner, reserved: append([]string{}, reserved...), unmountTimeout: unmountTimeout}
}

var recoveryLVPath = regexp.MustCompile(`^/dev/[A-Za-z0-9_+][A-Za-z0-9_+.-]*/[A-Za-z0-9_+][A-Za-z0-9_+.-]*$`)
var recoveryDevice = regexp.MustCompile(`^(0|[1-9][0-9]*):(0|[1-9][0-9]*)$`)
var recoveryNamespace = regexp.MustCompile(`^mnt:\[[1-9][0-9]*\]$`)
var recoveryStart = regexp.MustCompile(`^[0-9]+$`)

func validRecoveryIdentity(id DeviceIdentity) bool {
	return id.UUID != "" && len(id.UUID) <= 128 && recoveryDevice.MatchString(id.MajorMinor)
}

func (n *NamespaceRecovery) Inspect(ctx context.Context, w db.WorkerNode, lvDev string) (DeviceIdentity, error) {
	var id DeviceIdentity
	err := n.call(ctx, w, lvDev, "inspect", nil, &id)
	if err == nil && !validRecoveryIdentity(id) {
		err = errors.New("invalid logical volume identity")
	}
	return id, err
}
func (n *NamespaceRecovery) Scan(ctx context.Context, w db.WorkerNode, lvDev string) (NamespaceSnapshot, error) {
	var snapshot NamespaceSnapshot
	err := n.call(ctx, w, lvDev, "scan", nil, &snapshot)
	if err == nil {
		err = validateRecoverySnapshot(snapshot, false)
	}
	return snapshot, err
}
func (n *NamespaceRecovery) Cleanup(ctx context.Context, w db.WorkerNode, lvDev string, snapshot NamespaceSnapshot) error {
	if err := validateRecoverySnapshot(snapshot, true); err != nil {
		return err
	}
	var result struct {
		Cleaned bool `json:"cleaned"`
	}
	if err := n.call(ctx, w, lvDev, "cleanup", snapshot, &result); err != nil {
		return err
	}
	if !result.Cleaned {
		return fmt.Errorf("%w: cleanup not confirmed", ErrNamespaceStateUnknown)
	}
	return nil
}
func (n *NamespaceRecovery) VerifyReleased(ctx context.Context, w db.WorkerNode, lvDev string, identity DeviceIdentity) error {
	if !validRecoveryIdentity(identity) {
		return errors.New("invalid expected device identity")
	}
	var result struct {
		Released bool           `json:"released"`
		Device   DeviceIdentity `json:"device"`
	}
	if err := n.call(ctx, w, lvDev, "verify", identity, &result); err != nil {
		return err
	}
	if !result.Released || result.Device != identity {
		return errors.New("device release or identity not confirmed")
	}
	return nil
}
func validateRecoverySnapshot(s NamespaceSnapshot, requireHolders bool) error {
	if !validRecoveryIdentity(s.Device) || s.Holders == nil || len(s.Holders) > 4096 || (requireHolders && len(s.Holders) == 0) {
		return errors.New("invalid namespace snapshot")
	}
	namespaces := map[string]bool{}
	for _, h := range s.Holders {
		if h.PID <= 0 || !recoveryNamespace.MatchString(h.Namespace) || !recoveryStart.MatchString(h.StartTime) || h.Cgroup == "" || h.RootIno == 0 || len(h.Mounts) == 0 || len(h.Members) == 0 || len(h.Members) > 32768 || namespaces[h.Namespace] {
			return errors.New("invalid namespace holder")
		}
		namespaces[h.Namespace] = true
		found := false
		members := map[int]bool{}
		for _, m := range h.Members {
			if m.PID <= 0 || members[m.PID] || !recoveryStart.MatchString(m.StartTime) || m.Cgroup == "" {
				return errors.New("invalid namespace member")
			}
			members[m.PID] = true
			if m.PID == h.PID && m.StartTime == h.StartTime && m.Cgroup == h.Cgroup {
				found = true
			}
		}
		if !found {
			return errors.New("representative absent from members")
		}
		ids := map[int]bool{}
		paths := map[string]bool{}
		for _, m := range h.Mounts {
			if m.ID <= 0 || m.ParentID <= 0 || m.Device != s.Device.MajorMinor || !strings.HasPrefix(m.Path, "/") || m.Path == "/" || strings.ContainsRune(m.Path, 0) || !strings.HasPrefix(m.Root, "/") || m.Optional == nil || ids[m.ID] || paths[m.Path] {
				return errors.New("invalid namespace mount")
			}
			ids[m.ID] = true
			paths[m.Path] = true
		}
	}
	return nil
}
func recoveryQuote(value string) string { return "'" + strings.ReplaceAll(value, "'", "'\"'\"'") + "'" }
func (n *NamespaceRecovery) call(ctx context.Context, w db.WorkerNode, dev, operation string, payload any, result any) error {
	if n.runner == nil || !recoveryLVPath.MatchString(dev) || strings.Contains(dev, "/mapper/") {
		return errors.New("recovery requires /dev/VG/LV and an SSH runner")
	}
	if err := ctx.Err(); err != nil {
		return err
	}
	// The outer GNU timeout bounds even blocked probes. A cleanup child has its
	// own watchdog; killing helpers never means killing business processes.
	ctx, cancel := context.WithTimeout(ctx, 60*time.Second)
	defer cancel()
	budget := 60 * time.Second
	if deadline, ok := ctx.Deadline(); ok {
		budget = time.Until(deadline)
	}
	if budget < time.Second {
		return errors.New("insufficient recovery deadline")
	}
	req := map[string]any{"operation": operation, "lv_dev": dev, "reserved": n.reserved, "unmount_timeout": n.unmountTimeout.Seconds(), "payload": payload}
	input, err := json.Marshal(req)
	if err != nil {
		return err
	}
	command := "# cp-storage-namespace-" + operation + "\n" +
		"env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin LC_ALL=C /bin/sh -c " + recoveryQuote(
		"command -v python3 >/dev/null && command -v timeout >/dev/null && timeout --version | grep -q 'GNU coreutils' || { echo 'namespace recovery requires host Python3 and GNU timeout' >&2; exit 127; }; exec timeout --signal=TERM --kill-after=2s "+fmt.Sprintf("%.3fs", budget.Seconds())+" python3 -I -c "+recoveryQuote(namespaceRecoveryHelper))
	out, _, code, runErr := n.runner.RunWithStdin(ctx, w, command, bytes.NewReader(input))
	unknown := func(err error) error {
		if operation == "cleanup" {
			return fmt.Errorf("%w: %v", ErrNamespaceStateUnknown, err)
		}
		return err
	}
	if runErr != nil {
		return unknown(fmt.Errorf("remote %s transport: %w", operation, runErr))
	}
	if code == 124 || code == 137 || ctx.Err() != nil {
		return unknown(fmt.Errorf("remote %s timed out (exit %d)", operation, code))
	}
	if len(out) > 8<<20 {
		return unknown(errors.New("remote response exceeds limit"))
	}
	value, err := decodeRecoveryJSON(out)
	if err != nil {
		return unknown(fmt.Errorf("invalid %s response: %w", operation, err))
	}
	object, ok := value.(map[string]any)
	if !ok {
		return unknown(errors.New("response must be an object"))
	}
	success, ok := object["ok"].(bool)
	if !ok {
		return unknown(errors.New("missing response status"))
	}
	if !success {
		if len(object) != 3 {
			return unknown(errors.New("invalid failure response"))
		}
		message, mok := object["error"].(string)
		state, sok := object["state_unknown"].(bool)
		if !mok || !sok || message == "" {
			return unknown(errors.New("invalid failure response"))
		}
		if state {
			return fmt.Errorf("%w: %s", ErrNamespaceStateUnknown, message)
		}
		return fmt.Errorf("remote %s failed: %s", operation, message)
	}
	if code != 0 || len(object) != 2 {
		return unknown(fmt.Errorf("invalid success response (exit %d)", code))
	}
	if err := checkRecoverySchema(object["result"], reflect.TypeOf(result).Elem()); err != nil {
		return unknown(err)
	}
	b, _ := json.Marshal(object["result"])
	if err := json.Unmarshal(b, result); err != nil {
		return unknown(err)
	}
	return nil
}

// Token parsing rejects duplicate fields, null, trailing documents and missing
// fields, which encoding/json's permissive struct decoder alone would accept.
func decodeRecoveryJSON(text string) (any, error) {
	d := json.NewDecoder(strings.NewReader(text))
	d.UseNumber()
	v, err := readRecoveryValue(d, 0)
	if err != nil {
		return nil, err
	}
	if _, err = d.Token(); err != io.EOF {
		return nil, errors.New("trailing JSON data")
	}
	return v, nil
}
func readRecoveryValue(d *json.Decoder, depth int) (any, error) {
	if depth > 20 {
		return nil, errors.New("JSON nesting exceeds limit")
	}
	token, err := d.Token()
	if err != nil {
		return nil, err
	}
	if token == nil {
		return nil, errors.New("null not allowed")
	}
	delim, ok := token.(json.Delim)
	if !ok {
		return token, nil
	}
	switch delim {
	case '{':
		obj := map[string]any{}
		for d.More() {
			key, err := d.Token()
			if err != nil {
				return nil, err
			}
			s, ok := key.(string)
			if !ok {
				return nil, errors.New("invalid key")
			}
			if _, ok := obj[s]; ok {
				return nil, errors.New("duplicate field")
			}
			v, err := readRecoveryValue(d, depth+1)
			if err != nil {
				return nil, err
			}
			obj[s] = v
		}
		_, err := d.Token()
		return obj, err
	case '[':
		values := []any{}
		for d.More() {
			v, err := readRecoveryValue(d, depth+1)
			if err != nil {
				return nil, err
			}
			values = append(values, v)
		}
		_, err := d.Token()
		return values, err
	}
	return nil, errors.New("invalid delimiter")
}
func checkRecoverySchema(value any, t reflect.Type) error {
	switch t.Kind() {
	case reflect.Struct:
		obj, ok := value.(map[string]any)
		if !ok || len(obj) != t.NumField() {
			return errors.New("invalid result object schema")
		}
		for i := 0; i < t.NumField(); i++ {
			f := t.Field(i)
			v, ok := obj[f.Tag.Get("json")]
			if !ok {
				return fmt.Errorf("missing result field %s", f.Name)
			}
			if err := checkRecoverySchema(v, f.Type); err != nil {
				return err
			}
		}
	case reflect.Slice:
		array, ok := value.([]any)
		if !ok {
			return errors.New("result must be an array")
		}
		for _, v := range array {
			if err := checkRecoverySchema(v, t.Elem()); err != nil {
				return err
			}
		}
	case reflect.String:
		if _, ok := value.(string); !ok {
			return errors.New("result must be a string")
		}
	case reflect.Bool:
		if _, ok := value.(bool); !ok {
			return errors.New("result must be a boolean")
		}
	case reflect.Int, reflect.Uint64:
		if _, ok := value.(json.Number); !ok {
			return errors.New("result must be an integer")
		}
	default:
		return errors.New("unsupported result schema")
	}
	return nil
}
