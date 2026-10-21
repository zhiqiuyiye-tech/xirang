# Storage Operation Safety Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` or `superpowers:executing-plans` to implement this plan task by task. This plan covers findings 5 and 7 only.

**Goal:** Reject resize operations on protected or active logical volumes (LVs), preserve safe Network File System (NFS) reclamation, and allow explicitly identified non-NFS Container Storage Interface (CSI) drivers without weakening fail-closed checks for unknown sources.

**Architecture:** Parse an operator-maintained list of non-NFS CSI driver names and pass it through the existing Kubernetes Pod-use guard. Add a live, read-only resize preflight that checks LV identity, mount and fstab targets, swap, device-mapper open count, and resolvable Pod use; reject before `lvextend` or `lvreduce` if state is unsafe or indeterminate.

**Tech Stack:** Go, `ssh.Runner`, Kubernetes `client-go`, Kubernetes API validation, Helm.

**Spec:** `control_panel/docs/superpowers/specs/2026-10-10-storage-operation-safety-design.md`

## Global Constraints

- A mounted, swap-active, or open LV cannot be shrunk. A grow cannot act on a swap-active LV or one configured beneath a protected or reserved path; a mounted, open or Pod-used LV can be grown online, per the 2026-10-21 amendment to the spec.
- A mounted NFS LV may still be reclaimed only through the existing Pod guard, protected/reserved path checks, unexport/unmount sequence, and LV identity revalidation.
- `STORAGE_NON_NFS_CSI_DRIVERS` defaults to empty; only exact configured driver names are excluded from NFS correlation.
- The NFS CSI driver `nfs.csi.k8s.io`, unlisted CSI drivers, malformed NFS source attributes, and failed Kubernetes safety queries remain fail-closed.
- Preserve unrelated uncommitted work in the current working tree. Do not stage or commit unrelated files; implementation commits are outside this plan unless separately requested.

---

### Task 1: Parse and deploy the non-NFS CSI driver list

**Files:**
- Modify: `control_panel/backend/internal/config/config.go`
- Test: `control_panel/backend/internal/config/config_test.go`
- Modify: `control_panel/charts/control-panel/values.yaml`
- Modify: `control_panel/charts/control-panel/templates/deployment.yaml`
- Modify: `control_panel/charts/control-panel/README.md`

**Interface:** Add `NonNFSCSIDrivers []string` to `config.Config`. Read `STORAGE_NON_NFS_CSI_DRIVERS` as a comma-separated string; an unset or empty value yields an empty list. Validate every non-empty entry with `k8s.io/apimachinery/pkg/util/validation.IsDNS1123Subdomain`.

- [x] **Step 1: Write the failing configuration test.** Add `TestLoadNonNFSCSIDrivers` to `config_test.go`; import `reflect`. The test must assert both the default-empty behavior and whitespace-trimmed entries:

```go
func TestLoadNonNFSCSIDrivers(t *testing.T) {
    setMinimalEnv()
    defer unsetMinimalEnv()
    t.Setenv("STORAGE_NON_NFS_CSI_DRIVERS", " ebs.csi.aws.com, pd.csi.storage.gke.io ")

    cfg, err := Load()
    if err != nil {
        t.Fatal(err)
    }
    want := []string{"ebs.csi.aws.com", "pd.csi.storage.gke.io"}
    if !reflect.DeepEqual(cfg.NonNFSCSIDrivers, want) {
        t.Fatalf("NonNFSCSIDrivers=%v, want %v", cfg.NonNFSCSIDrivers, want)
    }
}
```

Add a separate invalid-entry assertion using `t.Setenv("STORAGE_NON_NFS_CSI_DRIVERS", "not a driver")` and require `Load()` to return an error naming that environment variable. Add `os.Unsetenv("STORAGE_NON_NFS_CSI_DRIVERS")` to `unsetMinimalEnv`.

- [x] **Step 2: Verify the tests fail first.** From `control_panel/backend`, run:

```powershell
go test ./internal/config -run 'TestLoadNonNFSCSIDrivers$' -count=1
```

Expected: the test does not pass because `Config.NonNFSCSIDrivers` and environment parsing are not implemented.

- [x] **Step 3: Implement parsing and validation.** Add the config field, parse with `envSliceOr("STORAGE_NON_NFS_CSI_DRIVERS", nil)`, and validate each result. For invalid values, return an error with the environment variable and offending name; keep the default empty and do not add built-in CSI exclusions.

```go
c.NonNFSCSIDrivers = envSliceOr("STORAGE_NON_NFS_CSI_DRIVERS", nil)
for _, driver := range c.NonNFSCSIDrivers {
    if problems := validation.IsDNS1123Subdomain(driver); len(problems) != 0 {
        return c, fmt.Errorf("STORAGE_NON_NFS_CSI_DRIVERS entry %q is invalid: %s", driver, strings.Join(problems, ", "))
    }
}
```

- [x] **Step 4: Expose the setting through Helm and documentation.** Add `config.nonNfsCsiDrivers: []` to `values.yaml` with a comment that only confirmed non-NFS drivers belong in the list. Add this Deployment environment variable:

```yaml
- name: STORAGE_NON_NFS_CSI_DRIVERS
  value: {{ join "," (.Values.config.nonNfsCsiDrivers | default (list)) | quote }}
```

Document that an empty list preserves fail-closed behavior and that unlisted CSI drivers still block NFS reclaim.

- [x] **Step 5: Verify configuration and chart rendering.** Run:

```powershell
go test ./internal/config -count=1
helm template control-panel ./control_panel/charts/control-panel --set-string 'config.nonNfsCsiDrivers[0]=ebs.csi.aws.com'
```

Expected: config tests pass and rendered Deployment contains `STORAGE_NON_NFS_CSI_DRIVERS` with `ebs.csi.aws.com`.

### Task 2: Apply CSI classification to every NFS reclaim guard

**Files:**
- Modify: `control_panel/backend/internal/k8s/pod_guard.go`
- Modify: `control_panel/backend/internal/k8s/namespace_cleanup.go`
- Test: `control_panel/backend/internal/k8s/pod_guard_test.go`
- Test: `control_panel/backend/internal/k8s/namespace_cleanup_test.go`
- Modify: `control_panel/backend/cmd/server/main.go`

**Interfaces:**
- Extend `CheckNFSPodUsage(ctx, client, workerHost, exportPath, nonNFSDrivers ...string)`.
- Extend `AuthorizeNamespaceCleanup(ctx, client, workerHost, exportPath, holders, allowlist, nonNFSDrivers ...string)`.
- `main.go` passes `cfg.NonNFSCSIDrivers` to both the regular storage Pod guard and namespace-cleanup recheck.

- [x] **Step 1: Add failing CSI classification tests.** Add separate tests named `TestCheckNFSPodUsage_KnownNonNFSCSI`, `TestCheckNFSPodUsage_UnlistedCSI`, and `TestCheckNFSPodUsage_NFSCsiMissingAttributes`. The first test uses a PV-backed CSI volume whose exact driver is passed in `nonNFSDrivers`; it must return `inUse=false` and no error. The second uses the same PV with an empty allowlist and must return an error. The third uses `nfs.csi.k8s.io` with a missing server or share and must return an error. Add `TestCheckNFSPodUsage_AllowlistedInlineCSI` for an inline CSI volume using an explicitly configured non-NFS driver; it must return `inUse=false` with no error. Keep the existing unknown-CSI test as the unlisted-driver regression.

- [x] **Step 2: Verify the new tests fail first.** Run:

```powershell
go test ./internal/k8s -run 'TestCheckNFSPodUsage_(KnownNonNFSCSI|AllowlistedInlineCSI|UnlistedCSI|NFSCsiMissingAttributes)$' -count=1
```

Expected: allowlisted non-NFS cases fail because the current checker rejects every CSI driver except `nfs.csi.k8s.io`.

- [x] **Step 3: Implement explicit classification in `CheckNFSPodUsage`.** Convert the variadic list to a set once. For a PV-backed CSI source or inline CSI source, apply this order: (1) `nfs.csi.k8s.io` is parsed as NFS and missing/invalid attributes are errors; (2) an exact configured driver name is skipped as non-NFS; (3) every other CSI source returns an error. An allowlisted CSI source must not be reported as an NFS match.

- [x] **Step 4: Propagate the configured list to cleanup rechecks.** Add the variadic parameter to `AuthorizeNamespaceCleanup`, pass it to its final `CheckNFSPodUsage` call, and pass `cfg.NonNFSCSIDrivers` from both closures in `cmd/server/main.go`.

- [x] **Step 5: Verify the guard and cleanup tests.** Run:

```powershell
go test ./internal/k8s -run 'TestCheckNFSPodUsage|TestAuthorizeNamespaceCleanup' -count=1
```

Expected: configured non-NFS drivers do not block unrelated NFS reclaim; unlisted CSI, malformed NFS CSI data, and Kubernetes query failures still fail closed.

### Task 3: Build and test the read-only resize safety probe

**Files:**
- Create: `control_panel/backend/internal/storage/resize_safety.go`
- Test: `control_panel/backend/internal/storage/resize_safety_test.go`

**Interfaces:**
- Define an internal `lvResizeSafetyState` with JSON fields `mount_targets`, `fstab_targets`, `swap_active`, and `device_open_count`.
- Define `buildLVResizeSafetyCommand(lvDev string) string` and `parseLVResizeSafetyState(output string) (lvResizeSafetyState, error)`.
- The probe is read-only and emits one JSON object. Any missing, malformed, negative, or inconclusive safety value is an error.

- [x] **Step 1: Add failing command and parser tests.** Add tests for an empty/unused state, multiple mount and fstab targets, active swap, a nonzero open count, malformed JSON, missing JSON fields, and shell-safe quoting. Use this valid fixture as the baseline:

```go
const unusedLVResizeState = `{"mount_targets":[],"fstab_targets":[],"swap_active":false,"device_open_count":0}`
```

- [x] **Step 2: Verify the tests fail first.** Run:

```powershell
go test ./internal/storage -run 'Test(BuildLVResizeSafetyCommand|ParseLVResizeSafetyState)$' -count=1
```

Expected: failure because the type and functions do not exist.

- [x] **Step 3: Implement the read-only command builder.** Validate the `/dev/<vg>/<lv>` path before interpolation and quote it with the existing `shellLiteral`. Resolve the device path; read live mount targets with `findmnt`; read fstab targets using evaluated source identity; inspect `/proc/swaps` after resolving device paths; and obtain the device-mapper open count. Emit only the four JSON fields. Do not call `lvextend`, `lvreduce`, `lvremove`, `umount`, `sed`, `exportfs`, or any other mutating command from this probe.

- [x] **Step 4: Implement strict state parsing.** Decode one JSON object, reject trailing output or absent fields, reject negative `device_open_count`, and validate/deduplicate every target path with the existing mount-point path rules. Treat a normal “not mounted/not configured” result as an empty list; treat other remote command errors as failures.

- [x] **Step 5: Verify the probe tests.** Run:

```powershell
go test ./internal/storage -run 'Test(BuildLVResizeSafetyCommand|ParseLVResizeSafetyState)$' -count=1
```

Expected: all safe-state, unsafe-state, and malformed-evidence cases pass.

### Task 4: Enforce preflight before grow or shrink

**Files:**
- Modify: `control_panel/backend/internal/storage/handlers.go` (`resizeLVHandler` and `RegisterStorageHandlers`)
- Test: `control_panel/backend/internal/storage/handlers_test.go`
- Test: `control_panel/backend/internal/storage/delete_safety_test.go`

**Interfaces:**
- `resizeLVHandler` receives `reservedMounts []string`, `podGuardChecker PodGuardChecker`, and `recovery *NamespaceRecovery`.
- A private `checkResizeSafety` helper accepts the context, worker, VG/LV names and returns the preflight `DeviceIdentity` or an error. It does not execute a resize command.

- [x] **Step 1: Add failing handler tests.** Use the existing scripted SSH runner and fake Pod guard to test both `grow` and `shrink` for these cases: any current mount target, a protected or reserved fstab target, active swap, nonzero device open count, Pod guard says in-use, Pod guard errors, preflight probe errors, and changed LV identity. In each rejected case assert the runner received no command beginning with `lvextend` or `lvreduce`. Add one safe unused-LV case that still executes the existing filesystem-aware resize command.

- [x] **Step 2: Verify the handler tests fail first.** Run:

```powershell
go test ./internal/storage -run 'TestResizeLVHandler(RejectsUnsafeState|AllowsUnusedLV)$' -count=1
```

Expected: the current handler runs the resize command without inspecting the live LV state.

- [x] **Step 3: Share the existing identity inspector and wire dependencies.** Create one `NamespaceRecovery` in `RegisterStorageHandlers`; pass it, configured reserved mounts, and `PodGuardChecker` to both handlers. Do not change the public storage task parameters.

- [x] **Step 4: Enforce the guard before mutation.** In `resizeLVHandler.Run`, after request validation and worker lookup, add a `resize_safety_preflight` task step. Call `checkResizeSafety`; it must inspect identity, run and parse the read-only probe, reject every mount target, reject swap-active or open LVs, apply `ValidateMountPoint` to fstab targets, and call the Pod guard for each resolvable target path. If the Pod guard is nil for a path that needs NFS correlation, or any probe is inconclusive, fail the step and return without running `ResizeLVSteps`.

- [x] **Step 5: Revalidate immediately before mutation.** Just before the first `ResizeLVSteps` command, repeat the identity read, safety probe, and Pod guard for all resolved target paths. Compare the new `UUID` and `MajorMinor` to the preflight identity. Fail without mutation if the identity changed, any mount/swap/open state became unsafe, or any recheck failed; otherwise execute the existing `ResizeLVSteps` unchanged.

- [x] **Step 6: Verify NFS reclaim remains supported.** Add `TestReclaimHandlerStillReclaimsUnusedMountedNFS` in `delete_safety_test.go`. Provide scripted responses for the live mount-point lookup and stable LV identity, configure the Pod guard to return `inUse=false` without error, and assert the existing export removal, unmount, fstab cleanup, unmounted verification, identity recheck, and `lvremove` steps all run in order. Add companion assertions that a Pod-in-use result and protected/reserved mount targets stop before `lvremove`.

- [x] **Step 7: Run focused and complete backend verification.** Run:

```powershell
go test ./internal/storage ./internal/k8s ./internal/config -count=1
go test ./... -count=1
```

Expected: all touched packages pass. The current full API suite has a known unrelated failure in `TestStorageEndpointsUseCachedSnapshotsAndRefresh` because its test router does not inject a collector; report that separately if it remains.

## Execution safety

The working tree already contains unrelated uncommitted changes. Inspect `git status` before execution, preserve those changes, and never use `git add -A` or restore unrelated files. No implementation commits are part of this plan unless the user separately requests them.

## Done When

- The non-NFS CSI list defaults to empty, parses trimmed entries, validates driver names, and renders through Helm.
- Allowlisted non-NFS CSI drivers do not block unrelated NFS reclaim; unlisted CSI sources still fail closed.
- Grow and shrink reject active, mounted, swap-backed, open, protected, reserved, or inconclusive target states before any mutating command.
- Existing NFS reclaim works only when the Pod guard proves the target export unused and current path and identity protections pass.
- All touched Go packages pass; any unrelated full-suite failure is reported accurately.
