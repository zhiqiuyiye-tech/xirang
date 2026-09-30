# NFS LV deletion: Pod-use guard

Date: 2026-09-30

Status: Proposed; chat design approved, awaiting review of this document.

## Context

`storage_delete_lv` currently detects host-visible mount targets, removes NFS exports and fstab entries, unmounts them, and invokes `lvremove -f` (`-f` skips prompts but does not override an in-use filesystem). Task #31 reported no host-visible mount, yet LVM refused removal because the filesystem was still in use. That error alone does not prove a Pod is the holder; a process or another mount namespace can also retain it.

The existing Pod/NFS association shown by inventory is not a deletion guard: it filters Pod names containing `notebook`, follows PVC-backed NFS volumes, and can use stale storage snapshots. A destructive decision needs a fresh cluster-wide check in the task itself.

## Goals and non-goals

- Permit removal when the target LV has no Pod using its NFS export and the host filesystem is no longer in use.
- Reject removal **before changing exports, fstab, or mounts** while any Pod object still references the target export, including Pending and Terminating Pods. Report namespace, Pod name, and PV/PVC when available. The operator deletes the Pod; the control panel never deletes Pods automatically.
- Fail closed on Kubernetes query failure or an unresolved potentially relevant mount. Never kill processes, lazy-unmount, or force an in-use LV.
- Preserve deletion of LVs created outside the panel when their identity can be established or the conservative unknown-path rule is satisfied.
- Do not claim that absence of Pods proves the host device is free: a remaining OS-level holder must still cause a safe failure with diagnostics.

## Source and identity model

At task execution, treat a host-visible `findmnt` target as a known export path only when its source resolves to the selected LV. Read `/etc/fstab`, `/etc/exports`, and successful provision-task parameters as diagnostic hints, but **do not** use a stale entry by itself to prove the LV-to-export mapping after an unmount or failed delete; the LV may have been repurposed. If no live binding is proven, use the approved unknown-path rule. Conflicting or invalid live bindings fail closed.

Query Kubernetes **freshly** (without the display API's `ResourceVersion: "0"`) for all Pods across namespaces, PVCs, and PVs. Inspect every Pod, not only Notebook-named Pods. Resolve inline NFS and NFS CSI volumes as well as PVCs bound to native NFS PVs or `nfs.csi.k8s.io` PVs. Reuse the established server/path normalization and subpath matching rules. A Pod still present in the API remains a blocker, even if deletion has been requested, because mount teardown can lag Pod termination.

- **Known target path:** block a Pod whose NFS server identifies the selected worker and whose share path is the export path or a subpath. Different, unambiguously identified exports on that worker do not block this LV. If a source could be this export but its server/path identity is ambiguous, fail closed.
- **Unknown target path:** as approved by the operator, proceed only if no Pod is found using an NFS export on that worker. Any potentially matching/ambiguous source prevents deletion. If the relevant API lists fail, stop without mutating the worker.
- An unresolved PVC/PV reference that cannot be ruled out as a potential NFS mount is an unknown result, not proof of no consumers. Report the uncertainty instead of silently permitting deletion.

## Execution and component boundary

Implement an execution-time Pod-use checker as a dependency of the storage deletion task, wired with the Kubernetes client in `cmd/server`. Keep the storage task dependent on a narrow checker interface/callback so it does not import the API package. The API-side checker can reuse the existing NFS source/path normalization helpers; inventory's cached `mounted_pods` stays informational, never authoritative. Tests can supply a fake checker without a cluster.

1. Validate task parameters and worker; resolve the LV's path evidence using read-only commands and the task store.
2. Record a `check_pod_usage` task step. If Pods or uncertainty block removal, fail with their identities/reason **before** the first exports/fstab/unmount command.
3. If clear, run the existing unexport, per-target user diagnostic, deepest-first unmount, and `verify_unmounted` steps.
4. Re-query Pod use immediately before `lvremove`, recording `verify_pod_usage`. If a new Pod appeared, retain the LV and report that cleanup may be partial; never proceed to `lvremove` on uncertainty.
5. If LVM still reports “filesystem in use” with no matching Pod, keep the LV and show the existing host-holder guidance. Pod deletion and kubelet mount teardown are asynchronous; the operator can retry after the Pod disappears and references are released.

These checks reduce but cannot eliminate the race with a Pod created by another actor between the last Kubernetes read and `lvremove`. The panel does not control Kubernetes admission for new Pods. A stronger atomic guarantee would require an admission/controller boundary and is out of scope.

## Validation

Use failing tests first, then implement. Cover:

- A non-Notebook Pod using native NFS directly blocks before any SSH mutation.
- Pods using native NFS PV and NFS CSI PV through PVC block, including terminating Pods. After deleting the Pod object, the same LV proceeds when the host is no longer busy.
- A Pod on a different export on the same worker does not block when the target path is known.
- When the path is unknown, zero NFS Pod users on the worker permits removal; a candidate user or uncertain server/PVC/PV blocks it.
- Kubernetes Pod/PVC/PV list failures and a nil client fail closed before mutation.
- A Pod appearing during teardown blocks the final `lvremove` check; no force removal is attempted.
- Existing tests for multiple host mounts, reserved mount protection, and in-use LVM failures remain passing.

Run `go test ./...`, `go vet ./...`, applicable web tests, and `git diff --check`. No destructive test runs against a live worker.

## Rollout

A Git commit alone does not update the running control-panel image or OCI Chart. Build/publish the backend image and deploy it separately after verification. Do not include the locally modified development SQLite database in any release commit.
