package storage

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
	"xirang/control_panel/internal/tasks"
)

// RegisterStorageHandlers registers the storage task handlers on the engine:
// storage_provision_nfs / storage_reclaim_nfs (LVM+NFS lifecycle), install_deps
// (lvm2/nfs-utils), storage_create_vg (auto-pool unused disks), storage_resize_lv
// (lvextend/lvreduce), and storage_delete_lv (generalized LV teardown). Each
// handler parses task.ParamsJSON, fetches the target worker, and executes the
// command sequence via the SSH runner.
func RegisterStorageHandlers(eng *tasks.Engine, runner ssh.Runner, store *db.Store) {
	eng.Register("storage_provision_nfs", &provisionHandler{runner: runner, store: store})
	eng.Register("storage_reclaim_nfs", &reclaimHandler{runner: runner, store: store})
	eng.Register("install_deps", &installDepsHandler{runner: runner, store: store})
	eng.Register("storage_create_vg", &createVGHandler{runner: runner, store: store})
	eng.Register("storage_resize_lv", &resizeLVHandler{runner: runner, store: store})
	eng.Register("storage_delete_lv", &deleteLVHandler{runner: runner, store: store})
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
	// ExportOpts is interpolated into the exports step's shell command, so it
	// MUST be validated too - a single quote would break out of the echo.
	if err := ValidateExportOpts(p.ExportOpts); err != nil {
		r.Fail(fmt.Sprintf("invalid export_opts: %v", err))
		return err
	}
	if p.SizeGB <= 0 {
		r.Fail("size_gb must be > 0")
		return fmt.Errorf("size_gb must be > 0")
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
// Each undo step is recorded via the reporter with its REAL outcome (a
// failed undo shows as failed), but rollback itself never blocks the failure
// path - every step is attempted regardless.
func (h *provisionHandler) rollback(ctx context.Context, w db.WorkerNode, r *tasks.Reporter, req ProvisionReq, done []string) {
	rb := RollbackFor(req, done)
	for _, st := range rb {
		sh, err := r.Step(st.Name)
		if err != nil {
			continue // best-effort: skip steps that can't be recorded
		}
		out, stderr, code, _ := h.runner.Run(ctx, w, st.Cmd)
		if code != 0 {
			sh.Done("failed", out, stderr, fmt.Sprintf("rollback step %s failed (code=%d): %s", st.Name, code, stderr))
			continue
		}
		sh.Done("succeeded", out, stderr, "")
	}
}

// --- reclaimHandler ---

type reclaimHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *reclaimHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		TaskID     int64  `json:"task_id"` // provision task to reclaim (reads its params)
		WorkerID   int64  `json:"worker_id"`
		VGName     string `json:"vg_name"`
		LVName     string `json:"lv_name"`
		MountPoint string `json:"mount_point"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	// If task_id given, read the original provision task's params (which hold
	// the vg/lv/mount_point/worker_id) so the UI can delete by task_id without
	// re-entering them.
	if p.TaskID != 0 {
		prov, err := h.store.GetTask(ctx, p.TaskID)
		if err != nil {
			r.Fail(fmt.Sprintf("load provision task %d: %v", p.TaskID, err))
			return err
		}
		var pp struct {
			WorkerID   int64  `json:"worker_id"`
			VGName     string `json:"vg_name"`
			LVName     string `json:"lv_name"`
			MountPoint string `json:"mount_point"`
		}
		if err := json.Unmarshal([]byte(prov.ParamsJSON), &pp); err != nil {
			r.Fail(fmt.Sprintf("parse provision params: %v", err))
			return err
		}
		p.WorkerID, p.VGName, p.LVName, p.MountPoint = pp.WorkerID, pp.VGName, pp.LVName, pp.MountPoint
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

// --- installDepsHandler ---

// installDepsHandler installs lvm2 and nfs on a worker via SSH. It probes the
// package manager (yum/dnf/apt), checks if deps are already installed
// (idempotent skip), installs if missing, and verifies after install.
type installDepsHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *installDepsHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID int64 `json:"worker_id"`
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

	// 1. detect package manager
	st, err := r.Step("detect_pm")
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	out, stderr, code, _ := h.runner.Run(ctx, *w, DetectPMOutput())
	if code != 0 {
		st.Done("failed", out, stderr, "detect_pm failed")
		r.Fail("detect_pm failed")
		return fmt.Errorf("detect_pm failed")
	}
	pm, err := ParsePM(out)
	if err != nil {
		st.Done("failed", out, stderr, err.Error())
		r.Fail(err.Error())
		return err
	}
	st.Done("succeeded", out, stderr, "")

	// 2. check if deps already installed
	st2, err := r.Step("check_deps")
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	out2, _, _, _ := h.runner.Run(ctx, *w, CheckDepsCmd())
	lvm2, nfs := ParseDepsCheck(out2)
	if !lvm2 || !nfs {
		st2.Done("succeeded", out2, "", fmt.Sprintf("lvm2=%v nfs=%v, will install", lvm2, nfs))

		// 3. install
		st3, err := r.Step("install")
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		cmd, err := InstallDepsCmd(pm)
		if err != nil {
			st3.Done("failed", "", "", err.Error())
			r.Fail(err.Error())
			return err
		}
		out3, stderr3, code3, _ := h.runner.Run(ctx, *w, cmd)
		if code3 != 0 {
			st3.Done("failed", out3, stderr3, fmt.Sprintf("install failed code=%d", code3))
			r.Fail(fmt.Sprintf("install failed: %s", stderr3))
			return fmt.Errorf("install failed")
		}
		st3.Done("succeeded", out3, stderr3, "")

		// 4. verify
		st4, err := r.Step("verify")
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		out4, _, _, _ := h.runner.Run(ctx, *w, CheckDepsCmd())
		lvm22, nfs2 := ParseDepsCheck(out4)
		if !lvm22 || !nfs2 {
			st4.Done("failed", out4, "", "deps still missing after install")
			r.Fail("install reported success but deps still missing")
			return fmt.Errorf("verify failed")
		}
		st4.Done("succeeded", out4, "", "deps installed and verified")
	} else {
		// Idempotent: already installed, skip install + verify
		st2.Done("succeeded", out2, "", "already installed, skipping package install")
	}

	// 5. configure NFSv4 in /etc/nfs.conf
	st5, err := r.Step("configure_nfs_v4")
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	out5, stderr5, code5, _ := h.runner.Run(ctx, *w, ConfigureNFSv4Cmd())
	if code5 != 0 {
		st5.Done("failed", out5, stderr5, fmt.Sprintf("configure_nfs_v4 failed code=%d", code5))
		r.Fail(fmt.Sprintf("configure nfs.conf failed: %s", stderr5))
		return fmt.Errorf("configure_nfs_v4 failed")
	}
	st5.Done("succeeded", out5, stderr5, "configured /etc/nfs.conf with forced NFSv4")

	// 6. enable and start NFS service
	st6, err := r.Step("enable_nfs_service")
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	out6, stderr6, code6, _ := h.runner.Run(ctx, *w, EnableNFSServiceCmd(pm))
	if code6 != 0 {
		st6.Done("failed", out6, stderr6, fmt.Sprintf("enable_nfs_service failed code=%d", code6))
		r.Fail(fmt.Sprintf("enable nfs service failed: %s", stderr6))
		return fmt.Errorf("enable_nfs_service failed")
	}
	st6.Done("succeeded", out6, stderr6, "nfs service enabled and started")

	r.Succeed()
	return nil
}

// --- createVGHandler ---

// createVGHandler pvcreates each unused disk and vgcreates a SEPARATE VG per
// disk (named <prefix>_<basename>, e.g. vg_data_sdb), rather than merging all
// disks into one VG. One-VG-per-disk sidesteps LVM's same-physical-block-size
// constraint, so disks of different sector sizes (512e vs 4Kn) can coexist. The
// VG name prefix defaults to vg_data. For each disk it first checks whether the
// derived VG name is already taken; if so it skips that disk (idempotent) so a
// re-run doesn't fail on a VG that already exists.
type createVGHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *createVGHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID int64    `json:"worker_id"`
		VGName   string   `json:"vg_name"` // VG name PREFIX; each disk becomes <prefix>_<basename>
		Disks    []string `json:"disks"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	if p.VGName == "" {
		p.VGName = "vg_data"
	}
	if err := ValidateName(p.VGName); err != nil {
		r.Fail(fmt.Sprintf("invalid vg_name prefix: %v", err))
		return err
	}
	if len(p.Disks) == 0 {
		r.Fail("no disks provided")
		return fmt.Errorf("no disks provided")
	}
	for _, d := range p.Disks {
		if err := ValidateDisk(d); err != nil {
			r.Fail(fmt.Sprintf("invalid disk %q: %v", d, err))
			return err
		}
	}
	w, err := h.store.GetWorker(ctx, p.WorkerID)
	if err != nil {
		r.Fail(err.Error())
		return err
	}

	// Per disk: detect whether the derived VG already exists; if so skip it
	// (idempotent). pvcreate is still safe to re-run, but vgcreate fails on an
	// existing name, so we skip the whole disk to avoid a confusing failure.
	for _, d := range p.Disks {
		vg := VGNameForDisk(p.VGName, d)
		detect, err := r.Step("detect_vg:" + vg)
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		// `vgs <name>` exits 0 if the VG exists, non-zero otherwise; the echo
		// gives a parseable token regardless of exit status.
		out, stderr, _, _ := h.runner.Run(ctx, *w, fmt.Sprintf("vgs %s >/dev/null 2>&1 && echo exists || echo absent", vg))
		exists := strings.Contains(out, "exists")
		if exists {
			detect.Done("succeeded", out, stderr, "vg "+vg+" already exists, skipping disk "+d)
			continue
		}
		detect.Done("succeeded", out, stderr, "vg "+vg+" absent, will create")

		// pvcreate + vgcreate for this disk only.
		for _, s := range []Step{
			{Name: "pvcreate:" + d, Cmd: fmt.Sprintf("wipefs -a %s && pvcreate %s", d, d)},
			{Name: "vgcreate:" + vg, Cmd: fmt.Sprintf("vgcreate %s %s", vg, d)},
		} {
			sh, err := r.Step(s.Name)
			if err != nil {
				r.Fail(fmt.Sprintf("create step: %v", err))
				return err
			}
			out, stderr, code, err := h.runner.Run(ctx, *w, s.Cmd)
			if err != nil || code != 0 {
				sh.Done("failed", out, stderr, fmt.Sprintf("step %s failed code=%d", s.Name, code))
				r.Fail(fmt.Sprintf("create vg failed at %s: %s", s.Name, stderr))
				return fmt.Errorf("create vg failed at %s", s.Name)
			}
			sh.Done("succeeded", out, stderr, "")
		}
	}
	r.Succeed()
	return nil
}

// --- resizeLVHandler ---

// resizeLVHandler extends (action=grow, default) or reduces (action=shrink) an
// LV by DeltaGB, using -r so the filesystem is resized in the same operation.
type resizeLVHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *resizeLVHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID int64  `json:"worker_id"`
		VGName   string `json:"vg_name"`
		LVName   string `json:"lv_name"`
		Action   string `json:"action"`  // "grow" (default) | "shrink"
		DeltaGB  int    `json:"delta_gb"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	for _, f := range []string{p.VGName, p.LVName} {
		if err := ValidateName(f); err != nil {
			r.Fail(fmt.Sprintf("invalid param: %v", err))
			return err
		}
	}
	if p.DeltaGB <= 0 {
		r.Fail("delta_gb must be > 0")
		return fmt.Errorf("delta_gb must be > 0")
	}
	grow := p.Action != "shrink"
	w, err := h.store.GetWorker(ctx, p.WorkerID)
	if err != nil {
		r.Fail(err.Error())
		return err
	}
	for _, s := range ResizeLVSteps(ResizeLVReq{VGName: p.VGName, LVName: p.LVName, Grow: grow, DeltaGB: p.DeltaGB}) {
		sh, err := r.Step(s.Name)
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		out, stderr, code, err := h.runner.Run(ctx, *w, s.Cmd)
		if err != nil || code != 0 {
			sh.Done("failed", out, stderr, fmt.Sprintf("step %s failed code=%d", s.Name, code))
			r.Fail(fmt.Sprintf("resize failed at %s: %s", s.Name, stderr))
			return fmt.Errorf("resize failed at %s", s.Name)
		}
		sh.Done("succeeded", out, stderr, "")
	}
	r.Succeed()
	return nil
}

// --- deleteLVHandler ---

// deleteLVHandler tears down and removes an arbitrary LV (not just ones the
// panel provisioned), releasing its space back to the VG. It first detects the
// mount point via findmnt so it can clean /etc/exports, umount, and clean
// /etc/fstab before lvremove. Works for LVs created outside the control panel.
type deleteLVHandler struct {
	runner ssh.Runner
	store  *db.Store
}

func (h *deleteLVHandler) Run(ctx context.Context, task *db.Task, r *tasks.Reporter) error {
	var p struct {
		WorkerID int64  `json:"worker_id"`
		VGName   string `json:"vg_name"`
		LVName   string `json:"lv_name"`
	}
	if err := json.Unmarshal([]byte(task.ParamsJSON), &p); err != nil {
		r.Fail(fmt.Sprintf("parse params: %v", err))
		return err
	}
	for _, f := range []string{p.VGName, p.LVName} {
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
	lvDev := fmt.Sprintf("/dev/%s/%s", p.VGName, p.LVName)

	// 1. detect mount point. findmnt --source resolves the /dev/vg/lv symlink to
	// the dm device, so it matches however the LV was mounted. Non-zero exit
	// means "not mounted" (not an error): we skip the exports/umount steps.
	st, err := r.Step("detect_mount")
	if err != nil {
		r.Fail(fmt.Sprintf("create step: %v", err))
		return err
	}
	out, stderr, code, _ := h.runner.Run(ctx, *w, fmt.Sprintf("findmnt -n -o TARGET --source %s 2>/dev/null", lvDev))
	mountPoint := strings.TrimSpace(out)
	if code == 0 && mountPoint != "" {
		st.Done("succeeded", out, stderr, "mounted at "+mountPoint)
	} else {
		mountPoint = ""
		st.Done("succeeded", out, stderr, "not mounted")
	}

	// 2. teardown + remove.
	for _, s := range DeleteLVSteps(DeleteLVReq{VGName: p.VGName, LVName: p.LVName, MountPoint: mountPoint}) {
		sh, err := r.Step(s.Name)
		if err != nil {
			r.Fail(fmt.Sprintf("create step: %v", err))
			return err
		}
		out, stderr, code, err := h.runner.Run(ctx, *w, s.Cmd)
		if err != nil || code != 0 {
			sh.Done("failed", out, stderr, fmt.Sprintf("step %s failed code=%d", s.Name, code))
			r.Fail(fmt.Sprintf("delete failed at %s: %s", s.Name, stderr))
			return fmt.Errorf("delete failed at %s", s.Name)
		}
		sh.Done("succeeded", out, stderr, "")
	}
	r.Succeed()
	return nil
}
