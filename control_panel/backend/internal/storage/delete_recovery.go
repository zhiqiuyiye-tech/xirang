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

// isTargetBusy reports the handbook's own failure case: a host unmount that the
// kernel refused because something still holds the mount. util-linux says
// "target is busy" and older versions say "device is busy".
func isTargetBusy(stdout, stderr string) bool {
	return strings.Contains(strings.ToLower(stdout+"\n"+stderr), "busy")
}

// isNotMounted reports an unmount whose path was already released. A holder can
// exit or release its own copy between the holder lookup and the unmount, and
// that already satisfies the release step.
func isNotMounted(stdout, stderr string) bool {
	return strings.Contains(strings.ToLower(stdout+"\n"+stderr), "not mounted")
}

// retryBusyUnmounts repeats the host unmounts that reported the target busy.
// Their holder was released inside its mount namespace in between, which is the
// handbook order. A retry that still fails names the remaining local user of the
// mount instead of the holder, so the operator knows to look beyond mounts.
func (h *deleteLVHandler) retryBusyUnmounts(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, commands []string) error {
	for _, command := range commands {
		step, err := r.Step("umount_after_holder_release")
		if err != nil {
			r.Fail(err.Error())
			return err
		}
		out, stderr, code, runErr := h.runner.Run(ctx, w, command)
		if runErr != nil || code != 0 {
			message := fmt.Sprintf("host unmount still failing after releasing holders (code=%d): %s", code, strings.TrimSpace(stderr+"\n"+out))
			if runErr != nil {
				message += "; " + runErr.Error()
			}
			step.Done("failed", out, stderr, message)
			r.Fail(message)
			return fmt.Errorf("%s", message)
		}
		step.Done("succeeded", out, stderr, "")
	}
	return nil
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
	snapshot, err := h.recovery.Holders(recoveryCtx, w, dev)
	if err != nil {
		sh.Done("failed", "", "", err.Error())
		return fmt.Errorf("namespace holder lookup failed; retain volume: %w", err)
	}
	diagnostic := summarizeHolders(snapshot)
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

func summarizeHolders(holders NamespaceHolders) string {
	data, _ := json.Marshal(holders.Holders)
	return string(data)
}

// unmountNamespaceHolders ordinarily unmounts every residual mount of the
// discovered holders inside each holder's own mount namespace. Every holder is
// attempted so one failure cannot leave another holder's copy mounted, and the
// collected failures are reported together.
func (h *deleteLVHandler) unmountNamespaceHolders(ctx context.Context, w db.WorkerNode, holders NamespaceHolders) error {
	failures := []string{}
	for _, holder := range holders.Holders {
		for _, path := range holder.Paths {
			out, stderr, code, err := h.runner.Run(ctx, w, NamespaceUnmountCmd(holder.PID, path))
			if err == nil && code == 0 {
				continue
			}
			if err == nil && isNotMounted(out, stderr) {
				// The holder released its own copy between the lookup and this
				// command. Nothing is mounted there any more, which is the goal,
				// so this is not a failure.
				continue
			}
			reason := strings.TrimSpace(stderr + "\n" + out)
			if err != nil {
				reason = fmt.Sprintf("%v: %s", err, reason)
			}
			failures = append(failures, fmt.Sprintf("PID %d %s (code=%d): %s", holder.PID, path, code, reason))
		}
	}
	if len(failures) > 0 {
		return fmt.Errorf("namespace unmount failed; retain volume: %s", strings.Join(failures, "; "))
	}
	return nil
}
