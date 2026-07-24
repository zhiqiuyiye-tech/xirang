package storage

import (
	"context"
	"encoding/json"
	"fmt"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
)

// RegisterStorageHandlers registers the two storage task handlers on the
// engine: storage_provision_nfs and storage_reclaim_nfs. Each handler parses
// task.ParamsJSON, fetches the target worker from the store, and executes the
// provision or reclaim command sequence via the SSH runner.
func RegisterStorageHandlers(eng *tasks.Engine, runner ssh.Runner, store *db.Store) {
	eng.Register("storage_provision_nfs", &provisionHandler{runner: runner, store: store})
	eng.Register("storage_reclaim_nfs", &reclaimHandler{runner: runner, store: store})
}

// --- provisionHandler ---

type provisionHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *provisionHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID   int64   `json:"worker_id"`
		VGName     string  `json:"vg_name"`
		LVName     string  `json:"lv_name"`
		SizeGB     float64 `json:"size_gb"`
		FSType     string  `json:"fs_type"`
		MountPoint string  `json:"mount_point"`
		ExportOpts string  `json:"export_opts"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	for _, f := range []string{p.VGName, p.LVName, p.MountPoint, p.FSType} {
		if err := ValidateName(f); err != nil {
			r.Fail(fmt.Sprintf("invalid param: %v", err))
			return err
		}
	}
	w, err := h.store.GetWorker(ctx, p.WorkerID)
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	req := ProvisionReq{p.VGName, p.LVName, int(p.SizeGB), p.FSType, p.MountPoint, p.ExportOpts}
	steps := ProvisionSteps(req)
	var done []string
	for _, st := range steps {
		sh, err := r.Step(st.Name)
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		out, stderr, code, err := h.runner.Run(ctx, *w, st.Cmd)
		if err != nil || code != 0 {
			sh.Done("failed", out, stderr, fmt.Sprintf("step %s failed code=%d", st.Name, code))
			// rollback: undo only successfully-completed steps (done does
			// NOT include the current failed step)
			h.rollback(ctx, *w, r, req, done)
			r.Fail(fmt.Sprintf("provision failed at step %s: %s", st.Name, stderr))
			return fmt.Errorf("provision failed at step %s", st.Name)
		}
		sh.Done("succeeded", out, stderr, "")
		done = append(done, st.Name)
	}
	r.Succeed()
	return nil
}

// rollback executes the best-effort undo sequence for a provision failure.
// Each undo step is recorded via the reporter even if the command itself
// fails, so the failure path is never blocked.
func (h *provisionHandler) rollback(ctx context.Context, w db.WorkerNode, r *tasks.Reporter, req ProvisionReq, done []string) {
	rb := RollbackFor(req, done)
	for _, st := range rb {
		sh, err := r.Step(st.Name)
		if err != nil {
			continue // best-effort: skip steps that can't be recorded
		}
		out, stderr, _, _ := h.runner.Run(ctx, w, st.Cmd)
		sh.Done("succeeded", out, stderr, "") // best-effort: always record
	}
}

// --- reclaimHandler ---

type reclaimHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *reclaimHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID   int64  `json:"worker_id"`
		VGName     string `json:"vg_name"`
		LVName     string `json:"lv_name"`
		MountPoint string `json:"mount_point"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	w, err := h.store.GetWorker(ctx, p.WorkerID)
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	for _, st := range ReclaimSteps(ReclaimReq{p.VGName, p.LVName, p.MountPoint}) {
		sh, err := r.Step(st.Name)
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		out, stderr, code, err := h.runner.Run(ctx, *w, st.Cmd)
		if err != nil || code != 0 {
			sh.Done("failed", out, stderr, fmt.Sprintf("code=%d", code))
			r.Fail(fmt.Sprintf("reclaim failed at %s: %s", st.Name, stderr))
			return fmt.Errorf("reclaim failed at %s", st.Name)
		}
		sh.Done("succeeded", out, stderr, "")
	}
	r.Succeed()
	return nil
}
