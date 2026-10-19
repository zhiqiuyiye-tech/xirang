package storage

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"reflect"
	"regexp"
	"time"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/tasks"
)

// DeletionMountInspection permits shared metadata only for deletion planning.
// It never grants permission to run an unmount command by itself.
type DeletionMountInspection struct {
	Device                    DeviceIdentity `json:"device"`
	RequiresHostAuthorization bool           `json:"requires_host_authorization"`
}

// SharedHostUnmountPlan contains one host LV leaf mount, other LV holders
// found in the selected scope, and a digest of scanned views and members.
// Mode states whether scope completeness is kernel-proven or manually attested.
// The digest is a change detector, not an authorization token.
type SharedHostUnmountPlan struct {
	Mode    string            `json:"mode"`
	Device  DeviceIdentity    `json:"device"`
	Host    NamespaceHolder   `json:"host"`
	Holders []NamespaceHolder `json:"holders"`
	Proof   string            `json:"proof"`
}

type sharedMaintenanceContextKey struct{}

func withSharedHostMaintenance(ctx context.Context) context.Context {
	return context.WithValue(ctx, sharedMaintenanceContextKey{}, true)
}

func hostUnmountMode(ctx context.Context) string {
	confirmed, _ := ctx.Value(sharedMaintenanceContextKey{}).(bool)
	if confirmed {
		return "maintenance"
	}
	return "strict"
}

func hostScopeDescription(ctx context.Context) string {
	if hostUnmountMode(ctx) == "maintenance" {
		return "maintenance attested; process-visible scope only, not complete kernel namespace proof"
	}
	return "complete kernel namespace scope verified"
}

var sharedMountProof = regexp.MustCompile(`^[0-9a-f]{64}$`)

func (n *NamespaceRecovery) InspectForDeletion(ctx context.Context, w db.WorkerNode, dev string) (DeletionMountInspection, error) {
	var inspection DeletionMountInspection
	err := n.call(ctx, w, dev, "delete_inspect", nil, &inspection)
	if err == nil && !validRecoveryIdentity(inspection.Device) {
		err = errors.New("invalid logical volume identity")
	}
	return inspection, err
}

func validateSharedHostPlan(plan SharedHostUnmountPlan) error {
	if (plan.Mode != "strict" && plan.Mode != "maintenance") || plan.Host.PID != 1 || len(plan.Host.Mounts) != 1 || !sharedMountProof.MatchString(plan.Proof) || plan.Holders == nil {
		return errors.New("invalid shared host unmount plan")
	}
	holders := append([]NamespaceHolder{plan.Host}, plan.Holders...)
	return validateRecoverySnapshot(NamespaceSnapshot{Device: plan.Device, Holders: holders}, true)
}

func (n *NamespaceRecovery) PlanHostUnmount(ctx context.Context, w db.WorkerNode, dev string, device DeviceIdentity, paths []string) (SharedHostUnmountPlan, error) {
	var plan SharedHostUnmountPlan
	if !validRecoveryIdentity(device) || len(paths) != 1 {
		return plan, errors.New("shared host unmount requires one known LV mount")
	}
	if err := ValidateMountPoint(paths[0], n.reserved); err != nil {
		return plan, err
	}
	payload := map[string]any{"device": device, "paths": paths, "mode": hostUnmountMode(ctx)}
	if err := n.call(ctx, w, dev, "host_plan", payload, &plan); err != nil {
		return plan, err
	}
	if err := validateSharedHostPlan(plan); err != nil {
		return plan, err
	}
	if plan.Mode != hostUnmountMode(ctx) || plan.Device != device || plan.Host.Mounts[0].Path != paths[0] {
		return plan, errors.New("host mode, mount or logical volume identity changed")
	}
	return plan, nil
}

func (n *NamespaceRecovery) UnmountHost(ctx context.Context, w db.WorkerNode, dev string, plan SharedHostUnmountPlan) error {
	if err := validateSharedHostPlan(plan); err != nil {
		return err
	}
	if plan.Mode != hostUnmountMode(ctx) {
		return errors.New("host unmount mode does not match the confirmed task context")
	}
	var result struct {
		Unmounted bool           `json:"unmounted"`
		Device    DeviceIdentity `json:"device"`
	}
	if err := n.call(ctx, w, dev, "host_unmount", plan, &result); err != nil {
		return err
	}
	if !result.Unmounted || result.Device != plan.Device {
		return fmt.Errorf("%w: host unmount or device identity not confirmed", ErrNamespaceStateUnknown)
	}
	return nil
}

func (h *deleteLVHandler) inspectDeletionDevice(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string) (DeletionMountInspection, error) {
	step, err := r.Step("verify_lv_identity")
	if err != nil {
		r.Fail(err.Error())
		return DeletionMountInspection{}, err
	}
	inspection, err := h.recovery.InspectForDeletion(ctx, w, dev)
	if err != nil {
		step.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return inspection, err
	}
	data, _ := json.Marshal(inspection)
	step.Done("succeeded", string(data), "", "")
	return inspection, nil
}

func (h *deleteLVHandler) authorizeHostUnmount(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, identity DeviceIdentity, paths []string, expected *SharedHostUnmountPlan, name string) (SharedHostUnmountPlan, error) {
	step, err := r.Step(name)
	if err != nil {
		r.Fail(err.Error())
		return SharedHostUnmountPlan{}, err
	}
	plan, err := h.recovery.PlanHostUnmount(ctx, w, dev, identity, paths)
	if err == nil && expected != nil && !reflect.DeepEqual(plan, *expected) {
		err = errors.New("shared propagation scope or namespace membership changed; retaining volume")
	}
	if err == nil && len(plan.Holders) > 0 {
		if h.hostUnmountAuthorizer == nil {
			err = errors.New("shared host unmount has foreign holders; an explicit workload allowlist is required")
		} else {
			err = h.hostUnmountAuthorizer(ctx, w.Host, paths[0], plan.Holders)
		}
	}
	if err != nil {
		step.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return plan, err
	}
	step.Done("succeeded", summarizeNamespaceHolders(plan.Holders), "", hostScopeDescription(ctx)+"; all visible foreign LV holders explicitly authorized")
	return plan, nil
}

func (h *deleteLVHandler) unmountAuthorizedHost(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, paths []string, plan SharedHostUnmountPlan) error {
	fresh, err := h.authorizeHostUnmount(ctx, r, w, dev, plan.Device, paths, &plan, "recheck_host_unmount_scope")
	if err != nil {
		return err
	}
	if err := h.checkPodUsage(ctx, r, w.Host, paths, "verify_pod_usage_before_host_unmount"); err != nil {
		return err
	}
	step, err := r.Step("umount_host_authorized")
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	if err := h.recovery.UnmountHost(ctx, w, dev, fresh); err != nil {
		if errors.Is(err, ErrNamespaceStateUnknown) {
			if guarded, ok := h.runner.(*guardedStorageRunner); ok {
				guarded.BlockWorker(w.ID, err.Error())
			}
		}
		step.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return err
	}
	step.Done("succeeded", "", "", "ordinary host unmount completed after propagation authorization; helper exited")
	return h.releaseSharedDevice(ctx, r, w, dev, paths, plan.Device)
}

// releaseSharedDevice uses the same residual-container release sequence as
// ordinary deletion, retaining the task-bound shared-host verification mode.
func (h *deleteLVHandler) releaseSharedDevice(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, paths []string, identity DeviceIdentity) error {
	return h.releaseResidualMounts(ctx, r, w, dev, paths, identity, true)
}

// releaseResidualMounts fills the gap between host umount and lvremove: the
// holders of the exact device are discovered from kernel evidence and the
// residual mount is ordinarily unmounted inside each holder's mount namespace,
// which is the handbook step before lvremove. The discovery is best effort -
// it only supplies the holder PID and path the handbook unmount needs - so a
// host that cannot be read skips that unmount instead of blocking lvremove.
func (h *deleteLVHandler) releaseResidualMounts(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, paths []string, identity DeviceIdentity, sharedHost bool) error {
	budget := h.cleanupTimeout
	if budget <= 0 {
		budget = time.Minute
	}
	ctx, cancel := context.WithTimeout(ctx, budget)
	defer cancel()
	step, err := r.Step("scan_namespace_holders_before_remove")
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	snapshot, scanErr := h.recovery.Scan(ctx, w, dev)
	if scanErr != nil {
		// The lookup exists only to name the holder for the handbook unmount.
		// A host whose process evidence cannot be read must not block the
		// handbook order: nothing is destroyed unless lvremove itself allows
		// it, so record the failure and continue to lvremove.
		reason := fmt.Errorf("namespace holder lookup failed; handbook unmount skipped, lvremove decides: %w", scanErr)
		step.Done("failed", "", "", reason.Error())
		return nil
	}
	if snapshot.Device != identity {
		// The lookup described a different device, so its holders belong to
		// another volume; unmounting them would modify the wrong namespace.
		err := errors.New("LV identity changed after host umount; retaining volume")
		step.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return err
	}
	step.Done("succeeded", summarizeNamespaceHolders(snapshot.Holders), "", "process-visible residual mounts inspected before first lvremove")
	if len(snapshot.Holders) > 0 {
		unmountStep, err := r.Step("unmount_namespace_holders_before_remove")
		if err != nil {
			r.Fail(err.Error())
			return err
		}
		// Handbook order: enter each holder's mount namespace and perform an
		// ordinary unmount there. No workload allowlist, process identity
		// pinning or open-count check gates this step; lvremove itself refuses
		// a volume that some namespace still holds.
		if err := h.unmountNamespaceHolders(ctx, w, snapshot); err != nil {
			unmountStep.Done("failed", summarizeNamespaceHolders(snapshot.Holders), "", err.Error())
			r.Fail(err.Error())
			return err
		}
		unmountStep.Done("succeeded", summarizeNamespaceHolders(snapshot.Holders), "", "ordinary unmount executed in each holding mount namespace")
	}
	if sharedHost {
		return h.verifySharedReleased(ctx, r, w, dev, identity, "verify_shared_device_released")
	}
	return nil
}

func (h *deleteLVHandler) verifySharedReleased(ctx context.Context, r *tasks.Reporter, w db.WorkerNode, dev string, identity DeviceIdentity, name string) error {
	step, err := r.Step(name)
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	if err := h.recovery.VerifySharedReleased(ctx, w, dev, identity); err != nil {
		step.Done("failed", "", "", err.Error())
		r.Fail(err.Error())
		return err
	}
	step.Done("succeeded", "", "", hostScopeDescription(ctx)+"; same LV; visible mounts absent; Open Count=0")
	return nil
}
