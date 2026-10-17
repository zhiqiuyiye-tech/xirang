package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

// checkPodUsage checks every live alias, or the conservative whole-worker rule
// when the volume has no proven export binding. Queries are never cached.
func (h *deleteLVHandler) checkPodUsage(ctx context.Context, r *tasks.Reporter, workerHost string, paths []string, step string) error {
	sh, err := r.Step(step)
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	if h.podGuardChecker == nil {
		err = fmt.Errorf("Kubernetes pod usage checker is unavailable")
	} else {
		if len(paths) == 0 {
			paths = []string{""}
		}
		for _, path := range paths {
			var inUse bool
			var blockers []string
			inUse, blockers, err = h.podGuardChecker(ctx, workerHost, path)
			if err != nil {
				err = fmt.Errorf("failed to evaluate pod usage guard: %w", err)
				break
			}
			if inUse {
				err = fmt.Errorf("cannot delete: volume is in use by pods (%s)", strings.Join(blockers, "; "))
				break
			}
		}
	}
	if err != nil {
		sh.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return err
	}
	sh.Done("succeeded", "", "", "no active pods referencing volume")
	return nil
}

func (h *deleteLVHandler) inspectDevice(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev, step string) (DeviceIdentity, error) {
	sh, err := r.Step(step)
	if err != nil {
		r.Fail(err.Error())
		return DeviceIdentity{}, err
	}
	identity, err := h.recovery.Inspect(ctx, w, dev)
	if err != nil {
		sh.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return identity, err
	}
	data, _ := json.Marshal(identity)
	sh.Done("succeeded", string(data), "", "")
	return identity, nil
}

func isFilesystemInUse(stdout, stderr string) bool {
	return strings.Contains(strings.ToLower(stdout+"\n"+stderr), "filesystem in use")
}

func (h *deleteLVHandler) recoverNamespaceAndRemove(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, paths []string, identity DeviceIdentity, removeCmd string) error {
	budget := h.cleanupTimeout
	if budget <= 0 {
		budget = time.Minute
	}
	recoveryCtx, cancel := context.WithTimeout(ctx, budget)
	defer cancel()
	sh, err := r.Step("scan_namespace_holders")
	if err != nil {
		return err
	}
	snapshot, err := h.recovery.Scan(recoveryCtx, w, dev)
	if err != nil {
		sh.Done("failed", "", "", err.Error())
		return fmt.Errorf("namespace scan failed; retain volume: %w", err)
	}
	diagnostic := summarizeNamespaceHolders(snapshot.Holders)
	if snapshot.Device != identity {
		err = fmt.Errorf("logical volume identity changed; retain volume")
	} else if len(snapshot.Holders) == 0 {
		err = fmt.Errorf("no residual mount holder found; check open file handles and other mount namespaces")
	}
	if err != nil {
		sh.Done("failed", diagnostic, "", err.Error())
		return err
	}
	sh.Done("succeeded", diagnostic, "", "")
	authStep, err := r.Step("resolve_namespace_holders_for_retry")
	if err != nil {
		return err
	}
	// Resolve the actual holders of the selected device. The handbook
	// workflow deliberately does not use Kubernetes or a workload allowlist.
	authStep.Done("succeeded", diagnostic, "", "exact-device namespace holders resolved for the requested LV")
	unmountStep, err := r.Step("unmount_namespace_holders")
	if err != nil {
		return err
	}
	if err = h.unmountNamespaceHolders(recoveryCtx, w, snapshot); err != nil {
		unmountStep.Done("failed", diagnostic, "", err.Error())
		return fmt.Errorf("namespace unmount failed; no deletion retry: %w", err)
	}
	unmountStep.Done("succeeded", diagnostic, "", "ordinary unmount executed in each holding mount namespace")
	// Revalidate the stable LV identity immediately before the retry.
	current, err := h.inspectDevice(recoveryCtx, r, w, dev, "verify_lv_identity_before_retry")
	if err != nil {
		return err
	}
	if current != identity {
		return fmt.Errorf("logical volume identity changed before retry; retain volume")
	}
	retry, err := r.Step("lvremove_retry")
	if err != nil {
		return err
	}
	out, stderr, code, runErr := h.runner.Run(recoveryCtx, w, removeCmd)
	if runErr != nil || code != 0 {
		err = fmt.Errorf("lvremove retry failed (code=%d): %s", code, strings.TrimSpace(stderr+"\n"+out))
		if runErr != nil {
			err = fmt.Errorf("%w: %v", err, runErr)
		}
		retry.Done("failed", out, stderr, err.Error())
		return err
	}
	retry.Done("succeeded", out, stderr, "removed after verified ordinary namespace unmount")
	return nil
}

func summarizeNamespaceHolders(holders []NamespaceHolder) string {
	type record struct {
		Namespace string   `json:"namespace"`
		PID       int      `json:"pid"`
		Paths     []string `json:"paths"`
	}
	records := make([]record, 0, len(holders))
	for _, holder := range holders {
		item := record{Namespace: holder.Namespace, PID: holder.PID}
		for _, mount := range holder.Mounts {
			item.Paths = append(item.Paths, mount.Path)
		}
		records = append(records, item)
	}
	data, _ := json.Marshal(records)
	return string(data)
}

// unmountNamespaceHolders ordinarily unmounts every residual mount of the
// discovered holders inside each holder's own mount namespace. Every holder is
// attempted so one failure cannot leave another holder's copy mounted, and the
// collected failures are reported together.
func (h *deleteLVHandler) unmountNamespaceHolders(ctx context.Context, w db.WorkerNode, snapshot NamespaceSnapshot) error {
	failures := []string{}
	for _, holder := range snapshot.Holders {
		for _, mount := range holder.Mounts {
			out, stderr, code, err := h.runner.Run(ctx, w, NamespaceUnmountCmd(holder.PID, mount.Path))
			if err == nil && code == 0 {
				continue
			}
			reason := strings.TrimSpace(stderr + "\n" + out)
			if err != nil {
				reason = fmt.Sprintf("%v: %s", err, reason)
			}
			failures = append(failures, fmt.Sprintf("PID %d %s (code=%d): %s", holder.PID, mount.Path, code, reason))
		}
	}
	if len(failures) > 0 {
		return fmt.Errorf("namespace unmount failed; retain volume: %s", strings.Join(failures, "; "))
	}
	return nil
}
