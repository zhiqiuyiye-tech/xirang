# Storage Operation Safety Design

## Status

This design covers findings 5 and 7 only. The user approved the behavioral boundaries in chat. This document does not authorize implementation; implementation begins after the user reviews this spec and approves it. The 2026-10-21 amendment at the end of this document revises the resize boundary for grow, on the authority of section 9 of the operator handbook; everything else below still stands.

## Goal

Prevent resize operations from changing protected or active logical volumes, keep the supported NFS reclaim flow available, and avoid blocking unrelated NFS reclamation for CSI drivers explicitly confirmed to be non-NFS.

## Context

`resizeLVHandler` currently validates the resize action, names, and positive delta, then runs `lvextend -r` or `lvreduce -y -r` without checking live mount, reserved-path, swap, device-open, or Pod-use state. Deletion already has live mountpoint validation, a Pod usage guard, LV identity checks, and a controlled namespace cleanup path used by reclaim.

`k8s.CheckNFSPodUsage` reads Nodes, Pods, PVCs, and PVs. It recognizes direct NFS and `nfs.csi.k8s.io`, but currently returns an error for any other CSI-backed PV or inline CSI source. That makes an unrelated CSI volume block reclamation because its source cannot be excluded as NFS.

## Approved behavior

### Resize protection (finding 5)

- Shrink is rejected when the target LV is mounted, active as swap, or has a nonzero device-mapper open count. A mount configured beneath a protected operating-system or reserved path is also protected even when currently unmounted, for grow and shrink alike.
- Grow follows section 9 of the operator handbook and runs online on a mounted volume. An LV that is active as swap or that is configured to mount beneath a protected or reserved path is still refused; the device-mapper open count and the Kubernetes Pod guard no longer gate grow. See the 2026-10-21 amendment at the end of this document.
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

1. Shrink issues no SSH mutation when a target is mounted, configured to mount beneath a protected/reserved path, active as swap, open in device-mapper, or cannot be conclusively inspected. Grow issues no SSH mutation when a target is active as swap, configured to mount beneath a protected/reserved path, backed by a filesystem the handbook flow does not cover, or cannot be conclusively inspected.
2. A safe, unused, non-reserved data LV can still be resized using the existing filesystem-aware commands, and an in-service mounted ext or XFS LV can be grown online by the handbook sequence.
3. A configured non-NFS CSI driver does not block unrelated NFS reclaim.
4. An unlisted CSI driver, a failed Kubernetes query, or an NFS CSI source with missing/invalid attributes still blocks reclaim.
5. A valid NFS reclaim with no active Pod consumer can still unexport, unmount, verify identity, and remove the LV through the existing sequence.

## Amendment 2026-10-21: online grow for an in-service logical volume

`control_panel/docs/NFS创建流程.md` section 9 states the grow procedure the panel
must follow: `lvextend -r` extends the logical volume and its filesystem in one
operation, `resize2fs` completes it for ext and `xfs_growfs <mount target>`
completes it for a mounted XFS. Section 7 mounts every volume and exports it over
NFS while it is in use, so the earlier rule that refused a mounted target for
grow and shrink alike made grow unusable on every volume the panel serves: the
only resizable volume was one nothing was using.

The handbook is the authority for this flow, so the resize boundary now reads:

- Grow runs online on a mounted volume. The swap check, the protected and
  reserved path checks on `/etc/fstab` targets, the pinned LV identity and the
  probed filesystem type still apply, before the task and again inside the
  same SSH execution that mutates the volume.
- The device-mapper open count and the Kubernetes Pod guard gate shrink only.
  `lvextend` needs no exclusive access to the volume, and the filesystem grow is
  the kernel's own online operation, so an open, exported or Pod-used volume is
  not a reason to refuse a grow.
- Shrink keeps the stricter boundary: it refuses a mounted, open, swap-active or
  Pod-used volume, and it is ext-only, because XFS cannot shrink and ext cannot
  shrink while mounted. The refusal names the filesystem rather than reporting a
  generic unsupported workflow.
- Grow completes the filesystem inside the guarded command and treats a failed
  `lvextend` as fatal, so a filesystem-only success is never reported as a
  finished resize. XFS is no longer refused outright: an XFS volume that cannot
  be shrunk is still a grow target.
- The handbook's follow-up filesystem command is the fallback, not a second
  unconditional resize. On a mounted ext volume `lvextend -r` performs the online
  grow and the kernel writes the enlarged superblock asynchronously, so a
  `resize2fs` issued immediately afterwards can read that superblock mid-update
  and refuse to open the filesystem (`Superblock checksum does not match
  superblock`), failing a task whose volume and filesystem both grew. The step
  compares the size the kernel reports for the mount (`stat -f`) with the
  enlarged device (`blockdev --getsize64`) and runs `resize2fs` only when the
  filesystem still lags, or when the mount can no longer be measured. An
  unmounted ext volume runs the handbook command directly, and a mounted XFS
  keeps `xfs_growfs`, which is idempotent.
- The resize flow reads the LV identity through the identity-only operation the
  deletion flow uses (`inspect_lv`: LVM UUID and kernel `major:minor`, from the
  ordinary active writable linear volume check). It no longer runs the retired
  conservative inspection, which additionally demanded mount-propagation proof
  and refused every resize on a worker whose mounts the analysis cannot prove
  local (`target/direct-parent propagation not proven local`) before any safety
  decision was reached. That operation is removed rather than left unreferenced.
- The protected and reserved path guarantee stays: the resize safety probe's
  live mount targets are now validated with `ValidateMountPoint` as well as the
  `/etc/fstab` targets, for grow and shrink alike, so a volume mounted at an
  operating-system path or a reserved mount point is still refused.
- What a mounted grow does not do: it does not re-read the volume's size on the
  NFS clients. A client that cached the share size sees the new capacity after
  remounting, which is an operational step, not a panel guarantee.
