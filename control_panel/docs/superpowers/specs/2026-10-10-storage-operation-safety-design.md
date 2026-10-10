# Storage Operation Safety Design

## Status

This design covers findings 5 and 7 only. The user approved the behavioral boundaries in chat. This document does not authorize implementation; implementation begins after the user reviews this spec and approves it.

## Goal

Prevent resize operations from changing protected or active logical volumes, keep the supported NFS reclaim flow available, and avoid blocking unrelated NFS reclamation for CSI drivers explicitly confirmed to be non-NFS.

## Context

`resizeLVHandler` currently validates the resize action, names, and positive delta, then runs `lvextend -r` or `lvreduce -y -r` without checking live mount, reserved-path, swap, device-open, or Pod-use state. Deletion already has live mountpoint validation, a Pod usage guard, LV identity checks, and a controlled namespace cleanup path used by reclaim.

`k8s.CheckNFSPodUsage` reads Nodes, Pods, PVCs, and PVs. It recognizes direct NFS and `nfs.csi.k8s.io`, but currently returns an error for any other CSI-backed PV or inline CSI source. That makes an unrelated CSI volume block reclamation because its source cannot be excluded as NFS.

## Approved behavior

### Resize protection (finding 5)

- Both grow and shrink are rejected when the target LV is mounted, active as swap, or has a nonzero device-mapper open count. A mount configured beneath a protected operating-system or reserved path is also protected even when currently unmounted. Online growth is not exempt.
- The handler obtains live read-only evidence immediately before any resize command. It resolves the requested VG/LV to a stable device identity and checks current mount targets, `/etc/fstab` references, system/reserved paths, swap use, and device-mapper open state. When an NFS export path can be resolved, the existing Kubernetes Pod guard also checks that path for consumers.
- Any missing, malformed, ambiguous, or failed safety probe rejects the resize before a mutating command runs.
- The target LV identity is revalidated immediately before mutation so a replaced device path is not acted on.
- Protected operating-system paths continue to use `ValidateMountPoint`; configured paths come from `RESERVED_MOUNT_POINTS` and the existing storage registration options.

### NFS reclaim exception

- Existing NFS reclaim remains supported. A mounted NFS LV may be reclaimed only after the current Pod usage guard confirms there are no consumers and the mount path is neither a protected operating-system path nor a configured reserved path.
- Reclaim continues to remove only the target export/fstab entries, unmount the target paths, verify the device is unmounted, and revalidate LV identity before `lvremove`.
- This exception does not permit resizing a mounted NFS LV and does not bypass unknown-source or Pod-usage checks.

### CSI classification (finding 7)

- `nfs.csi.k8s.io` remains an NFS source. Missing or invalid server/share attributes fail closed.
- A CSI driver is excluded from the NFS guard only when its exact driver name appears in an explicit operator-configured non-NFS list, exposed as `STORAGE_NON_NFS_CSI_DRIVERS` (comma-separated, empty by default).
- CSI drivers absent from that list remain unclassified and fail closed. This keeps the safety default while allowing operators to identify unrelated drivers without changing code.
- The configuration parser trims whitespace, ignores empty entries, and validates each non-empty driver name as a Kubernetes DNS-1123 subdomain. Driver names are compared exactly and case-sensitively, matching Kubernetes CSI identifiers.

## Architecture and affected areas

- `control_panel/backend/internal/storage/handlers.go`: inject reserved paths and the existing Pod guard into resize preflight; reject unsafe grow/shrink requests before SSH mutation.
- `control_panel/backend/internal/storage/commands.go` or a focused storage safety helper: construct read-only preflight commands and parse their structured results. Do not infer safety from stale inventory snapshots.
- `control_panel/backend/internal/storage/delete_recovery.go`: preserve existing deletion checks and confirm the safe NFS reclaim path remains unchanged by resize guards.
- `control_panel/backend/internal/k8s/pod_guard.go`: add explicit non-NFS CSI driver classification while preserving fail-closed behavior for unlisted CSI sources and malformed NFS CSI attributes.
- `control_panel/backend/internal/config/config.go` and its tests: parse `STORAGE_NON_NFS_CSI_DRIVERS`.
- `control_panel/backend/cmd/server/main.go`: pass configured driver names to the Kubernetes Pod guard.
- `control_panel/charts/control-panel/values.yaml`, deployment templates, and deployment docs: expose the optional driver list without weakening the empty-list default.
- Storage and Kubernetes tests: cover every rejection condition, explicit CSI exclusions, unknown CSI fail-closed behavior, and successful NFS reclaim after the Pod guard proves the volume is unused.

## Failure handling

- A failed or inconclusive resize preflight creates a failed task and records which guard failed; no resize command is issued.
- A failed Pod/PVC/PV/Node query remains a hard stop for destructive NFS reclaim.
- An explicitly allowlisted non-NFS CSI PV is ignored only for NFS-source correlation; it is not treated as a successful NFS match.
- A successful safety check does not suppress the existing command-level failure handling or deletion rollback/recovery behavior.

## Non-goals

- Task, step, or audit-log retention and Kubernetes display-query performance work (finding 6).
- User identity, role, namespace authorization, or Kubernetes RBAC redesign (finding 8).
- Credential validity checks, secret revocation, or credential rotation (finding 9); those require the credential owner.
- Automatically adding or changing Kubernetes Pod labels.

## Acceptance criteria

1. Grow and shrink issue no SSH mutation when a target is mounted, configured to mount beneath a protected/reserved path, active as swap, open in device-mapper, or cannot be conclusively inspected.
2. A safe, unused, non-reserved data LV can still be resized using the existing filesystem-aware commands.
3. A configured non-NFS CSI driver does not block unrelated NFS reclaim.
4. An unlisted CSI driver, a failed Kubernetes query, or an NFS CSI source with missing/invalid attributes still blocks reclaim.
5. A valid NFS reclaim with no active Pod consumer can still unexport, unmount, verify identity, and remove the LV through the existing sequence.
