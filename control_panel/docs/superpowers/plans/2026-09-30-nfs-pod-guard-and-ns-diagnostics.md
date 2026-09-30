# NFS LV Deletion: Pod Guard and Mount Namespace Diagnostics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent deletion of NFS logical volumes while any Kubernetes Pod is using the export, detect and diagnose multi-namespace host holders (like Promtail) when `lvremove` encounters "in use", and provide actionable guidance without unsafe force-unmounting.

**Architecture:** Add a Pod-usage guard evaluator invoked before SSH teardown and immediately prior to `lvremove`. Combine fresh Kubernetes cluster-wide Pod/PVC/PV queries with strict worker/path normalization. Enhance the storage deletion command runner with a `/proc/*/mountinfo` scanner that attributes lingering device holders to specific process PIDs and container commandlines when LVM reports "filesystem in use".

**Tech Stack:** Go 1.26, Kubernetes client-go (`v0.32.0`), Linux `/proc` filesystem and LVM CLI via SSH, Gin, SQLite.

**Spec:** `control_panel/docs/superpowers/specs/2026-09-30-nfs-lv-pod-guard-design.md`

## Global Constraints

- Never mutate `/etc/exports`, `/etc/fstab`, or run `umount` if any Pod is still using the NFS volume.
- Never kill host processes or run lazy `umount -l` automatically.
- Keep `internal/storage` independent of `internal/api` by using a dedicated interface or function callback for Pod checking.
- Do not commit `control_panel_dev.db`.

---

### Task 1: Pod Guard Evaluator & Types

**Files:**
- Create: `control_panel/backend/internal/k8s/pod_guard.go`
- Test: `control_panel/backend/internal/k8s/pod_guard_test.go`

**Interfaces:**
- Produces: `CheckNFSPodUsage(ctx context.Context, client kubernetes.Interface, workerHost string, exportPath string) (inUse bool, blockers []string, err error)`

- [ ] **Step 1: Write the failing test for Pod usage detection**
  Include tests for:
  1. Pod directly using `volumes[].nfs` with matching server and path.
  2. Pod using `persistentVolumeClaim` bound to an NFS PV (both direct `spec.nfs` and `spec.csi`).
  3. Non-notebook Pods (e.g., standard workload or test pod).
  4. Pod on a *different* export path (must return `inUse: false`).
  5. Unknown export path (`exportPath == ""`): any NFS mount on that worker blocks; zero mounts allows.

- [ ] **Step 2: Run test to verify it fails**
  Run: `go test ./internal/k8s -run '^TestCheckNFSPodUsage' -count=1`
  Expected: Compilation error (`CheckNFSPodUsage` undefined).

- [ ] **Step 3: Implement `CheckNFSPodUsage`**
  Query Pods across all namespaces (no "notebook" filter, no `ResourceVersion: "0"`).
  Traverse PVC -> PV -> NFS source (reuse normalization patterns).
  Identify blockers formatted as `namespace/pod-name (pvc: <name>, export: <path>)`.

- [ ] **Step 4: Run test to verify it passes**
  Run: `go test ./internal/k8s -run '^TestCheckNFSPodUsage' -count=1`
  Expected: PASS.

- [ ] **Step 5: Commit**
  ```bash
  git add control_panel/backend/internal/k8s/pod_guard.go control_panel/backend/internal/k8s/pod_guard_test.go
  git commit -m "feat(k8s): implement cluster-wide NFS Pod usage guard evaluator"
  ```

---

### Task 2: Multi-Namespace Holder Diagnostic Command

**Files:**
- Modify: `control_panel/backend/internal/storage/commands.go`
- Test: `control_panel/backend/internal/storage/commands_test.go`

**Interfaces:**
- Produces: `FindDeviceHoldersCmd(devicePath string) string` in shell commands.

- [ ] **Step 1: Write the failing test for holder diagnosis shell command**
  Test that `FindDeviceHoldersCmd("/dev/vg_data/lv_nb")` produces a robust shell script inspecting `/proc/*/mountinfo` or `/proc/*/mounts` matching the resolved DM or block device and formatting PID, cmdline, and mountpoint.

- [ ] **Step 2: Run test to verify it fails**
  Run: `go test ./internal/storage -run '^TestFindDeviceHoldersCmd' -count=1`
  Expected: FAIL.

- [ ] **Step 3: Implement `FindDeviceHoldersCmd`**
  Script will:
  1. Resolve device major:minor or dm-name using `lsblk -no MAJ:MIN` or `readlink -f`.
  2. Grep `/proc/[0-9]*/mountinfo` for the target device or path.
  3. Extract PID and print `/proc/$pid/cmdline` and mount targets to stderr/stdout for diagnostic logging.

- [ ] **Step 4: Run test to verify it passes**
  Run: `go test ./internal/storage -run '^TestFindDeviceHoldersCmd' -count=1`
  Expected: PASS.

- [ ] **Step 5: Commit**
  ```bash
  git add control_panel/backend/internal/storage/commands.go control_panel/backend/internal/storage/commands_test.go
  git commit -m "feat(storage): add multi-namespace mount holder diagnostic command"
  ```

---

### Task 3: Wire Pod Guard & Namespace Diagnostics into `storage_delete_lv`

**Files:**
- Modify: `control_panel/backend/internal/storage/handlers.go`
- Modify: `control_panel/backend/cmd/server/main.go`
- Test: `control_panel/backend/internal/storage/handlers_test.go`

**Interfaces:**
- Consumes: `PodGuardChecker` func/interface injected into `deleteLVHandler`.

- [ ] **Step 1: Write the failing tests in `handlers_test.go`**
  1. `TestDeleteLVHandler_BlockedByActivePod`: Deletion fails at `check_pod_usage` before any unmount/sed command if Pod guard reports active blockers.
  2. `TestDeleteLVHandler_DiagnosesNamespaceHoldersOnInUse`: When `lvremove` fails with "contains a filesystem in use", the handler runs `FindDeviceHoldersCmd` and includes the detected PIDs/containers in the task error report.

- [ ] **Step 2: Run test to verify it fails**
  Run: `go test ./internal/storage -run '^TestDeleteLVHandler_(BlockedByActivePod|DiagnosesNamespaceHoldersOnInUse)' -count=1`
  Expected: FAIL.

- [ ] **Step 3: Update `deleteLVHandler`**
  1. Preflight step: `check_pod_usage`. Calls `PodGuardChecker`.
  2. If blocked, fail immediately and list the Pod names.
  3. If `lvremove` fails with "in use", run `FindDeviceHoldersCmd`. Append detected holder details (e.g., Promtail / container PID) to the final failure message.

- [ ] **Step 4: Wire in `cmd/server/main.go` and `api/handlers_storage.go`**
  Pass the `k8s.CheckNFSPodUsage` adapter into `RegisterStorageHandlers`.

- [ ] **Step 5: Run tests to verify they pass**
  Run: `go test ./internal/storage ./cmd/server ./internal/api -count=1`
  Expected: PASS.

- [ ] **Step 6: Commit**
  ```bash
  git add control_panel/backend/internal/storage/handlers.go control_panel/backend/internal/storage/handlers_test.go control_panel/backend/cmd/server/main.go control_panel/backend/internal/api/
  git commit -m "feat(storage): enforce Pod guard and mount namespace diagnosis in deleteLV"
  ```

---

### Task 4: UI Error Presentation & Version Bump to 1.0.5

**Files:**
- Modify: `control_panel/charts/control-panel/Chart.yaml`
- Modify: `control_panel/charts/control-panel/README.md`
- Modify: `control_panel/backend/internal/api/web/index.html`
- Modify: `control_panel/backend/internal/api/web/app.js`

- [ ] **Step 1: Update UI handling for detailed holder/Pod error messages**
  Ensure long error messages in the task detail and alert prompts wrap cleanly and highlight the blocking Pods or holder PIDs so operators can immediately act on them.

- [ ] **Step 2: Bump version to 1.0.5**
  Bump version in `Chart.yaml`, `README.md`, and `index.html`.

- [ ] **Step 3: Run full test and validation suite**
  Run:
  - `go test ./...`
  - `go vet ./...`
  - `helm lint ./control_panel/charts/control-panel`
  - `npm test` in `control_panel/backend/web-build`

- [ ] **Step 4: Commit**
  ```bash
  git add control_panel/
  git commit -m "fix(control-panel): release 1.0.5 with Pod-aware NFS deletion and namespace holder diagnostics"
  ```
