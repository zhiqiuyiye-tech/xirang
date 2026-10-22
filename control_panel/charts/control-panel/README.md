# control-panel Helm Chart

One-command deployment of the Agentless K8s + storage control panel. AES/JWT and
the bootstrap/recovery secret are auto-generated; an operator still completes
the one-time browser key enrollment after the pod is Ready.

## Architecture & Security Highlights

- **Pod Deployment & Permissions**: Runs as root by default to ensure complete compatibility with host storage permissions (e.g. `local-path` / `hostPath` volumes owned by root:root) and arbitrary persistent volume mount points. Can be restricted via `podSecurityContext` if desired.
- **HttpOnly Cookie & CSRF**: Web UI authenticates via same-origin `HttpOnly` session cookies and double-submit CSRF tokens. Sensitive tokens are not exposed in browser `localStorage` or URL query strings.
- **ECDSA P-256 key login**: One `admin` account uses one shared PKCS#8 private-key file. `ADMIN_INIT_PASSWORD` is only for first key enrollment and offline recovery; after enrollment the bcrypt password hash is disabled. The system cannot attribute actions to individual holders of the shared file.
- **Session and source limits**: Browser sessions use HttpOnly, SameSite=Strict cookies with a 30-minute maximum JWT lifetime. Key rotation and “退出所有会话” increment `auth_version`; “退出此浏览器” clears only that browser. Failed proofs are throttled per resolved source IP and never persist a global admin lock.
- **HTTP-only internal deployment**: NodePort is plain HTTP. A passive network observer can steal active Session cookies and the first bootstrap password (and can race first enrollment to register its own key); an active man-in-the-middle can replace JavaScript and steal a selected key file. Use only on a restricted internal network; IP allowlists do not provide TLS-equivalent protection.
- **Health Probes**: Dedicated `/health/live` (process health) and `/health/ready` (SQLite & Kubernetes API readiness) endpoints.

## Critical Storage Requirements (SQLite)

> **CRITICAL**: The PVC backing `/data` **MUST** use a block-based storage class or local storage (e.g. `local-path`, `hostPath`, Ceph RBD, Longhorn).
> **DO NOT USE REGULAR NFS FOR THE CONTROL PANEL PVC.**
> The SQLite database uses WAL and POSIX shared-memory/locking files (`.db-shm`);
> NFS is unsupported and can cause locking failures or corruption. The service
> supports one replica only. Startup checks the SQLite runtime is at least 3.35.0
> (the pinned Go driver currently reports 3.53.3) before applying migrations.

## NFS namespace recovery

Deletion and reclaim follow the operator handbook: revoke the target exports,
ordinary host unmount, an ordinary `umount` inside each remaining holder's mount
namespace via `nsenter`, LV removal, then fstab cleanup. There is no process
identity pinning and no Open Count pre-check: a volume that is still in use is
reported by `lvremove` itself and retained. The backend does not
scan Kubernetes Pod/PVC references or require maintenance-mode switches or a
workload allowlist for this flow. Operators must first stop business use and
confirm the target volume's data can be permanently discarded.

`config.namespaceCleanupTimeout` defaults to `60s`, and
`config.namespaceUnmountTimeout` to `10s`. A worker requires Python 3, GNU
`timeout`, LVM/device-mapper and ordinary mount/export tools, and privileged
access for the trusted executor. Linux 5.10 does not require newer namespace
enumeration ioctls. Old maintenance/allowlist values remain accepted only for
configuration compatibility, not as deletion prerequisites. Resize retains its
own workload checks. See [the operator guide](../../docs/nfs-namespace-recovery.md)
for physical protections, uncertainty markers, and isolated Linux validation.

## Prerequisites

1. **Private registry image pushed** (the master must be able to pull it):
   ```bash
   # If changing browser crypto assets, run this first:
   cd ./control_panel/backend/web-build && npm ci && npm test && npm run build
   cd ../../..
   docker build -t registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest ./control_panel/backend
   docker push registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest
   ```
   If the registry needs auth or uses a self-signed cert, configure the cluster
   nodes (insecure-registries / CA) or set `image.imagePullSecrets` in values.

2. **Cluster has a block/local StorageClass** (for the 1Gi PVC), e.g. `local-path` or set
   `persistence.storageClassName`.

3. **Helm >= 3.8** installed on the master (OCI support), and `kubectl` configured.

## Publish the Chart to the OCI Registry (once, from a machine with the source)

To install from any machine (not just the one with the source), publish the
chart as an OCI artifact to the same registry as the image:

```bash
# From repo root. Packages the chart and pushes it as an OCI artifact.
./control_panel/deploy/push-chart.sh
```

Or manually:

```bash
helm package ./control_panel/charts/control-panel --destination /tmp
helm registry login registry-xirang.jxslpt.cn:30443
helm push /tmp/control-panel-1.0.25.tgz oci://registry-xirang.jxslpt.cn:30443/tai-dev
```

The chart then lives at `oci://registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:1.0.25`.

## Install

### 1. Standard Internal Deployment (NodePort)

```bash
helm install control-panel ./control_panel/charts/control-panel \
  --create-namespace -n control-panel
```

For a fresh install or operator recovery, retrieve the bootstrap password from
the Secret:

```bash
kubectl -n control-panel get secret control-panel-secrets \
  -o jsonpath='{.data.ADMIN_INIT_PASSWORD}' | base64 -d ; echo
```

`ADMIN_INIT_PASSWORD` is the first-install/recovery secret. When upgrading an
existing installation, use the currently working administrator password from
the old version; the database migration preserves its bcrypt hash.

On first access, enter the applicable password to initialize the shared P-256
login key. The browser downloads an unencrypted PKCS#8 PEM file; re-select the
downloaded file to verify it before enrollment completes. Distribute that same
file to all authorized operators over a controlled channel and keep a protected
backup. Normal logins use only the private-key file, not the bootstrap password.
Access the web UI (NodePort 30180 by default):

```
http://<node-ip>:30180/
```

### 2. Optional future deployment (only if HTTPS becomes available)

The current environment uses the HTTP-only NodePort above. Keep this example for
future environments that permit TLS; it is not required for the approved
internal HTTP deployment.

Create a custom `values-prod.yaml`:

```yaml
service:
  type: ClusterIP
  port: 8080

config:
  cookieSecure: true # enforces Secure flag on session cookies

ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTP"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
    nginx.ingress.kubernetes.io/whitelist-source-range: "10.0.0.0/8,192.168.0.0/16"
  hosts:
    - host: control-panel.internal.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: control-panel-tls
      hosts:
        - control-panel.internal.example.com
```

Deploy with:

```bash
helm install control-panel ./control_panel/charts/control-panel \
  --create-namespace -n control-panel -f values-prod.yaml
```

## Secrets Lifecycle

- **`AES_KEY`**: Master encryption key (AES-256-GCM) for worker SSH passwords and private keys stored in SQLite. **Must remain unchanged across upgrades**; regenerating it makes stored worker credentials unreadable.
- **`JWT_SECRET`**: HS256 signing secret for session tokens.
- **`ADMIN_INIT_PASSWORD`**: Required at startup as the bootstrap/recovery secret. It seeds the bcrypt hash on first boot and is used again only after the documented offline recovery process. Successful key enrollment replaces the database password hash with a disabled marker; changing this Secret alone does not affect an active key installation.

## Backup, Restore & Rollback

### Backup

Before major upgrades, back up the Secret and SQLite database.

```bash
# 1. Back up the Kubernetes Secret.
kubectl -n control-panel get secret control-panel-secrets -o yaml > control-panel-secrets-backup.yaml

# 2. Stop the single application replica before mounting its ReadWriteOnce PVC.
kubectl -n control-panel scale deployment/control-panel --replicas=0
kubectl apply -f ./control_panel/deploy/sqlite-maintenance-pod.yaml
kubectl -n control-panel wait --for=condition=Ready pod/control-panel-sqlite-maintenance --timeout=120s

# 3. Use SQLite's online backup API through the sqlite3 CLI; do not cp a live .db file.
kubectl -n control-panel exec control-panel-sqlite-maintenance -- \
  sqlite3 /data/control_panel.db ".backup '/tmp/control_panel_backup.db'"
kubectl -n control-panel cp control-panel-sqlite-maintenance:/tmp/control_panel_backup.db ./control_panel_backup.db

# 4. Remove the maintenance pod and restore the application replica.
kubectl -n control-panel delete pod control-panel-sqlite-maintenance
kubectl -n control-panel scale deployment/control-panel --replicas=1
```

For a Helm release in a namespace other than `control-panel`, update the
maintenance pod manifest's namespace before applying it.

### Recovering a lost shared private key

If every copy of the private key is lost, restrict the panel to a maintenance
window and complete the consistent backup above. Then scale the application to
zero again, start the maintenance pod, and run this transaction:

```bash
kubectl -n control-panel scale deployment/control-panel --replicas=0
kubectl apply -f ./control_panel/deploy/sqlite-maintenance-pod.yaml
kubectl -n control-panel wait --for=condition=Ready pod/control-panel-sqlite-maintenance --timeout=120s
```

```bash
kubectl -n control-panel exec -i control-panel-sqlite-maintenance -- \
  sqlite3 /data/control_panel.db <<'SQL'
BEGIN IMMEDIATE;
UPDATE admin
   SET auth_state='RECOVERY_PENDING',
       password_hash='__PENDING_INIT__',
       public_key_pem=NULL,
       public_key_fingerprint=NULL,
       auth_version=auth_version+1
 WHERE username='admin' AND auth_state='KEY_ACTIVE';
SELECT changes();
DELETE FROM auth_challenges;
COMMIT;
SQL
```

Confirm `SELECT changes()` reports `1`, delete the maintenance pod, and restore
the application replica. Startup uses the retained `ADMIN_INIT_PASSWORD` Secret
to return to `PASSWORD_BOOTSTRAP` and writes an `auth.recovery_bootstrap` audit
event. Re-enroll a new shared key and distribute its downloaded PEM. Clearing
only `public_key_pem` is not a recovery procedure and does not re-enable password
login.

## Rollback

```bash
helm rollback control-panel -n control-panel
```

A pre-key-login image is not authentication-compatible after the v4 auth-state
migration. Roll back only together with a matching pre-upgrade SQLite backup; do
not expect the old password-login binary to operate on a `KEY_ACTIVE` database.

## Pre-flight Checklist

- [ ] **Pod egress to Kubernetes API**: Pod must be able to contact Kubernetes API (TCP 443 / 6443).
- [ ] **Pod egress to Worker Nodes on TCP 22**: Worker management & LVM/NFS automation require the Pod to establish SSH connections to worker nodes on port 22. Verify node firewalls (`iptables` / `firewalld`) do not block traffic from the Pod CIDR.
- [ ] **StorageClass**: Ensure StorageClass is `local-path`, `hostPath`, or a block CSI (not NFS).
- [ ] **Ingress Network Restriction**: If exposed to corporate LAN, configure `whitelist-source-range` on Ingress or enable `networkPolicy`.

## Worker SSH heartbeat timeouts

Worker status is based on an authenticated SSH session executing `true`, not
Kubernetes Node Ready or simply opening a TCP port. The default total heartbeat
budget is 30 seconds, matching the manual connection test. Versions that used
5 or 15 seconds can mark a reachable worker offline when its authenticated
non-interactive session takes longer than that budget (a successful 16.6-second
session has been observed).

For an existing installation, the environment variable is already supported:

```bash
kubectl -n control-panel set env deployment/control-panel WORKER_HEARTBEAT_TIMEOUT=30s
kubectl -n control-panel rollout status deployment/control-panel
```

This restarts the panel Pod. Check the worker again after the next heartbeat
(default interval: one minute), or use the panel's connection-test button. To
persist a larger total budget with the updated chart, set
`config.workerHeartbeatTimeout: "30s"` in your values file. Explicit environment
values override the application default; existing `5s` or `15s` overrides must be
changed separately.

New timeout diagnostics name the SSH stage: `tcp connect`,
`handshake/authentication`, `session open`, `exec start`, or
`wait for command completion`. Handshake/authentication also has its own 10-second
limit; increasing the total heartbeat budget does not remove that limit. For a
handshake timeout, inspect server authentication, DNS/PAM and the network path
from the panel Pod, rather than only increasing the heartbeat budget. For
session/exec/wait timeouts, inspect node load and non-interactive shell startup.
Repeated failed checks still use the offline threshold; timeouts are never
converted into successful checks.

## Worker GPU / NPU collection

Device collection has a separate total SSH and tool-query budget of 45 seconds:
`config.workerAcceleratorTimeout` / `WORKER_ACCELERATOR_TIMEOUT`. This includes
connection acquisition and non-interactive shell startup. The environment option
requires version 1.0.10 or later; setting it on the original 1.0.9 binary
will not change that binary's hard-coded eight-second budget.

Starting with version 1.0.11, nodes are probed as single-vendor systems. The panel tries `npu-smi` first
and stops after a successful query, so an Ascend node is not affected by an
unrelated, non-executable `nvidia-smi`. NVIDIA is tried only when the Ascend tool
is absent or fails. When the fallback confirms NVIDIA cards, errors from the
irrelevant Ascend tool are not displayed. Both-tool failures and empty or
unrecognized fallback results still retain diagnostics; driver permissions are
never changed by the panel. This default does not aggregate mixed-vendor nodes.

Physical cards and allocatable devices are separate units. An Ascend910 system
with NPU IDs 0–7 and Phy-IDs 0–15 has eight physical cards and sixteen devices.
The worker's used / total ratio now compares Kubernetes allocated devices with
Kubernetes allocatable devices. Notebook counts use the same device unit.

## Administrator and Kubernetes Management Scope

The deployment owner explicitly chose to retain one shared `admin` account/key
and the current cross-namespace Service/NetworkPolicy management permissions.
Audits cannot reliably identify an individual key holder, and the ClusterRole
is not a namespace isolation boundary. Existing protected-namespace, object
identity and destructive-operation checks remain. No personal-account model,
namespace write allowlist, Secret access or Pod exec access is added. See the
[risk decisions and redacted credential review](../../docs/2026-10-11-remaining-risk-decisions.md)
for the confirmed limitations and local scan coverage.

## History Retention

Before upgrading, back up the SQLite database if historical task output or audits
must be archived. Cleanup runs at startup and every hour by default. Ordinary
terminal tasks (`succeeded`, `failed`, `cancelled`) expire 90 days after
`finished_at`; audits expire 365 days after their event time. Running/pending
and other nonterminal tasks, missing or unrecognized finish timestamps, and
records exactly at the cutoff are retained.

All successful `storage_provision_nfs` task rows and their registration/reclaim
parameters are retained as resource snapshots, even after their old step logs
expire. This deliberately retains snapshots whose resource lifetime is not yet
tracked separately; it keeps existing task-ID-based NFS registration/reclaim
working. It is not an archive of all historical command output.

Each transaction deletes at most 500 rows per table by default. Old steps are
removed first; an ordinary task is deleted only after it has no remaining steps,
so foreign-key cascades cannot silently remove an unlimited step set. Sweeps
are limited to 30 seconds; a backlog continues on the next scheduled sweep.
Failed batches roll back, and cleanup stops before SQLite is closed on shutdown.
The database reuses freed pages; this cleanup does not run `VACUUM` or promise
an immediate reduction of the database file size.

The four settings below map to `TASK_RETENTION_DAYS`, `AUDIT_RETENTION_DAYS`,
`HISTORY_CLEANUP_INTERVAL`, and `HISTORY_CLEANUP_BATCH_SIZE`. All must be positive;
the cleanup interval must be at least `1m` to prevent continuous sweeps. Invalid
values fail startup rather than silently disabling cleanup.

## Configuration Reference

| Key | Default | Description |
|-----|---------|-------------|
| `image.repository` | `registry-xirang.jxslpt.cn:30443/tai-dev/control-panel` | Image repo |
| `image.tag` | `latest` | Image tag |
| `image.pullPolicy` | `Always` | Pull policy |
| `namespace` | `control-panel` | Namespace |
| `service.type` | `NodePort` | Service type (`NodePort` or `ClusterIP`) |
| `service.port` | `8080` | Container port |
| `service.nodePort` | `30180` | NodePort (when type is NodePort) |
| `ingress.enabled` | `false` | Enable Ingress resource |
| `config.requireK8s` | `true` | Fail fast on pod start if k8s client fails |
| `config.nonNfsCsiDrivers` | `[]` | Exact names of confirmed non-NFS CSI drivers; empty preserves fail-closed behavior, and unlisted CSI drivers still block NFS reclaim |
| `config.taskRetentionDays` | `90` | Age of terminal task history/step logs measured from finish time; successful NFS supply snapshot rows remain |
| `config.auditRetentionDays` | `365` | Age of audit events before history cleanup |
| `config.historyCleanupInterval` | `1h` | Interval between bounded cleanup sweeps; startup also performs a sweep |
| `config.historyCleanupBatchSize` | `500` | Maximum deleted rows per table and transaction |
| `config.cookieSecure` | `false` | Session cookies cannot use `Secure` in the required HTTP deployment |
| `config.cookieSameSite` | `Strict` | Required SameSite policy for the shared admin session |
| `config.jwtTTL` | `30m` | Session lifetime; values over 30 minutes fail startup |
| `config.workerHeartbeatTimeout` | `30s` | Total SSH heartbeat budget (`WORKER_HEARTBEAT_TIMEOUT`); increase for slow worker authentication/session startup |
| `config.workerAcceleratorTimeout` | `45s` | Total SSH and device-tool collection budget (`WORKER_ACCELERATOR_TIMEOUT`) |
| `config.trustedProxies` | `[]` | CIDRs allowed to supply forwarded client IP headers; empty means use `RemoteAddr` |
| `config.rateLimitMaxFailures` | `5` | Failed proofs per resolved source before temporary source-only backoff |
| `config.rateLimitLockoutDuration` | `15m` | Maximum source-only in-memory backoff; no account-wide persistent lock |
| `config.challengeRateLimitPerMinute` | `10` | Challenge-creation requests allowed per source per minute |
| `config.challengeMaxPendingPerIP` | `5` | Maximum unconsumed challenges per source |
| `config.challengeMaxPendingGlobal` | `1000` | Maximum unconsumed challenges across this single replica |
| `podSecurityContext` | `{}` | Pod security context (empty allows root deployment) |
| `securityContext` | `{}` | Container security context |
| `persistence.enabled` | `true` | PVC for SQLite database |
| `persistence.storageClassName` | `"local-path"` | StorageClass (must be block or local) |
| `secrets.aesKey` | `""` (auto) | Pin the AES_KEY environment value (base64 text for 32 raw key bytes); the chart encodes the Kubernetes Secret data layer |
| `secrets.jwtSecret` | `""` (auto) | Pin JWT_SECRET (base64) |
| `secrets.adminPassword` | `""` (auto) | Pin bootstrap/recovery secret |
