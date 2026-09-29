# Control Panel - Kubernetes Deployment

> **One-command install (recommended):** use the Helm chart at
> `control_panel/charts/control-panel/`. It auto-generates all secrets
> `AES_KEY`, `JWT_SECRET`, and the one-time bootstrap/recovery password are
> generated automatically; no manual Secret creation is needed. The first browser
> visit still requires key enrollment:
> ```bash
> helm install control-panel ./control_panel/charts/control-panel --create-namespace -n control-panel
> ```
> See `control_panel/charts/control-panel/README.md` for details.
>
> This `deploy/` directory holds the raw kubectl manifests + `install.sh` as an
> alternative (non-Helm) path.

This directory contains Kubernetes manifests and an install script for deploying
the control panel into a cluster.

## Contents

| File | Purpose |
|------|---------|
| `rbac.yaml` | Namespace, ServiceAccount, ClusterRole (least privilege), ClusterRoleBinding |
| `pvc.yaml` | PersistentVolumeClaim (1Gi) for the SQLite database |
| `deployment.yaml` | Deployment: single pod, root execution supported, PVC mount, probes, resources |
| `service.yaml` | Service: NodePort 30180 exposing :8080 |
| `secret.yaml.template` | Placeholder Secret template (real `secret.yaml` is git-ignored) |
| `install.sh` | Interactive installer: generates secrets, applies all manifests |
| `sqlite-maintenance-pod.yaml` | One-off PVC-mounted SQLite maintenance pod; use only after stopping the app replica |
| `README.md` | This file |

## Critical Storage Requirements (SQLite)

> **CRITICAL**: The PVC backing `/data` **MUST** use a block-based storage class or local storage (e.g. `local-path`, `hostPath`, Ceph RBD, Longhorn).
> **DO NOT USE REGULAR NFS FOR THE CONTROL PANEL PVC.**
> The backend SQLite database operates in WAL (Write-Ahead Logging) mode, which relies on POSIX shared-memory primitives (`.db-shm`). Network file systems (such as NFS) do not reliably support POSIX locking and shared memory, which can lead to `database is locked` errors or database corruption. The service supports a single process/replica and checks for SQLite runtime `>= 3.35.0` before migrations (the current Go driver reports `3.53.3`).

## Prerequisites

1. **Target Kubernetes cluster** with:
   - A default block/local `StorageClass` that can provision a 1Gi PVC (or edit `pvc.yaml`).
   - Nodes reachable on the NodePort range (default 30180).

2. **Worker nodes** where storage/LVM operations run must have:
   - `lvm2` and `nfs-utils` (or `nfs-common`) installed. These can be installed
     automatically from the control panel UI: add the worker, set its SSH
     credentials, then click "安装依赖" (Install Deps) to auto-detect the distro
     (yum/dnf/apt) and install `lvm2` + `nfs-utils`.
   - A volume group (VG) configured for LVM provisioning. The control panel's
     storage task handlers run `lvcreate`/`lvremove` and mount NFS exports on the
     target pods' nodes via SSH + the per-worker private key.

3. **kubectl** installed and configured to talk to the target cluster.

4. **Docker** (or compatible builder) to build and push the control panel image.

5. **Private container registry** (`registry-xirang.jxslpt.cn:30443`) reachable
   from the cluster. If the registry uses a self-signed or HTTP-only cert, the
   cluster nodes must trust it (configure `insecure-registries` or install the
   CA on each node), or create an `imagePullSecret` and reference it in
   `deployment.yaml`.

## Build and Push the Image

The deployment pulls `registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest`
from the private registry. On a host with docker, build and push it once
(repeat after any backend change):

```bash
# From the repo root:
docker build -t registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest ./control_panel/backend
docker push registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest
```

The committed `internal/api/web/p256.bundle.js` is embedded by the Go build. If
its browser crypto source changes, rebuild and test it first:

```bash
cd control_panel/backend/web-build
npm ci
npm test
npm run build
cd ../../..
```

Then build and push the container as shown above.

If `docker push` fails with a certificate error, log in first and/or configure
the registry as a trusted (insecure) registry on the build host:

```bash
docker login registry-xirang.jxslpt.cn:30443
# or add "registry-xirang.jxslpt.cn:30443" to /etc/docker/daemon.json insecure-registries
# and restart docker, then retry the push.
```

`deployment.yaml` uses `imagePullPolicy: Always`, so each pod restart pulls the
latest pushed image.

## Install

```bash
cd control_panel/deploy
./install.sh
```

`install.sh` will:

1. Validate that `kubectl` is reachable.
2. Generate `AES_KEY` (32 random bytes, base64) via `openssl rand 32 | base64`.
3. Generate `JWT_SECRET` (32 random bytes, base64) the same way.
4. Prompt for the bootstrap/recovery password (min 8 chars, input hidden).
5. Render the real `secret.yaml` (git-ignored) with the base64-encoded values.
6. `kubectl apply` all manifests (`rbac.yaml`, `pvc.yaml`, `secret.yaml`,
   `deployment.yaml`, `service.yaml`).
7. Print the NodePort access URL.

The script is **idempotent and upgrade-safe**: re-running it when the Secret
`control-panel-secrets` already exists **reuses** its values
(`AES_KEY`/`JWT_SECRET`/`ADMIN_INIT_PASSWORD`) unchanged.

## Upgrade (after a new image push)

```bash
# 1. Build and push the new image (see "Build and Push the Image" above).
docker build -t registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest ./control_panel/backend
docker push registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest

# 2. Re-run install.sh - it reuses the existing Secret and only re-applies the
#    manifests (imagePullPolicy: Always makes the pod pull the new image).
cd control_panel/deploy
./install.sh
```

Or, to update the image without touching the Secret at all:

```bash
kubectl -n control-panel set image deployment/control-panel \
    control-panel=registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:<new-tag>
```

## Access

Once the pod is `Ready`:

```bash
kubectl -n control-panel rollout status deployment/control-panel
```

For a fresh database or an operator recovery, retrieve the bootstrap password
from the Secret:

```bash
kubectl -n control-panel get secret control-panel-secrets \
  -o jsonpath='{.data.ADMIN_INIT_PASSWORD}' | base64 -d ; echo
```

`ADMIN_INIT_PASSWORD` is the first-install/recovery secret. When upgrading an
existing installation, use the currently working administrator password from
the old version; the migration preserves its bcrypt hash and does not replace it
with the Secret value.

The web UI is exposed on **NodePort 30180**:

```
http://<any-node-ip>:30180/
```

The only account is `admin`. On first access, enter the applicable bootstrap
password (the current working password when upgrading, or `ADMIN_INIT_PASSWORD`
for a fresh install/recovery). The browser generates and downloads an unencrypted
P-256 PKCS#8 PEM file; re-select that exact file to prove it is readable before
the public key is registered. Distribute the same private-key file to all
authorized operators over a controlled channel. Subsequent logins use only that
file; the password is retained as an offline recovery secret, not a login
fallback.

> **HTTP risk acceptance.** This deployment uses plain HTTP because HTTPS is not
> available in the environment. Apply the existing source-IP whitelist/firewall
> restrictions and allow access only from the trusted internal network. A passive
> listener can steal active Session Cookies and the first bootstrap password; if
> present during enrollment it can race to register its own key. An active
> man-in-the-middle can replace JavaScript and exfiltrate the private-key file
> when selected. The P-256 challenge prevents simple replay but does not protect
> HTTP sessions or resist active page replacement.

## Back up and recover the shared key

The service supports one SQLite process/replica. For a consistent backup or a
lost-key recovery, first restrict network access to the maintenance operator and
stop the application deployment. The included maintenance pod mounts the same
`control-panel-data` PVC and uses the SQLite CLI included in the image:

```bash
kubectl -n control-panel scale deployment/control-panel --replicas=0
kubectl apply -f control_panel/deploy/sqlite-maintenance-pod.yaml
kubectl -n control-panel wait --for=condition=Ready pod/control-panel-sqlite-maintenance --timeout=120s

# Create a consistent SQLite backup and copy it off the cluster.
kubectl -n control-panel exec control-panel-sqlite-maintenance -- \
  sqlite3 /data/control_panel.db ".backup '/tmp/control_panel.db.backup'"
kubectl -n control-panel cp control-panel-sqlite-maintenance:/tmp/control_panel.db.backup ./control_panel.db.backup
kubectl -n control-panel delete pod control-panel-sqlite-maintenance
kubectl -n control-panel scale deployment/control-panel --replicas=1
```

To recover after every shared private-key copy is lost, restrict access again,
scale the app to zero, re-create the maintenance pod and wait for it to become
Ready, then run this transaction:

```bash
kubectl -n control-panel scale deployment/control-panel --replicas=0
kubectl apply -f control_panel/deploy/sqlite-maintenance-pod.yaml
kubectl -n control-panel wait --for=condition=Ready pod/control-panel-sqlite-maintenance --timeout=120s
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

Verify the update changed exactly one row, then remove the maintenance pod and
restart the application:

```bash
kubectl -n control-panel delete pod control-panel-sqlite-maintenance
kubectl -n control-panel scale deployment/control-panel --replicas=1
kubectl -n control-panel rollout status deployment/control-panel
```

Startup uses the retained `ADMIN_INIT_PASSWORD` Secret to re-enter
`PASSWORD_BOOTSTRAP` and records an `auth.recovery_bootstrap` audit event. The
operator then enrolls and distributes a new shared P-256 private-key file. Do
not run multiple application replicas or mount this WAL database over NFS.

## Uninstall

```bash
kubectl delete -f control_panel/deploy/service.yaml
kubectl delete -f control_panel/deploy/deployment.yaml
kubectl delete secret control-panel-secrets -n control-panel
kubectl delete -f control_panel/deploy/pvc.yaml   # WARNING: deletes SQLite data
kubectl delete -f control_panel/deploy/rbac.yaml   # deletes Namespace last, which removes everything in it
```

The PVC deletion is permanent - the SQLite database (including the admin
account, audit log, worker registrations, and encrypted per-worker SSH private
keys) will be lost. Back up `/data/control_panel.db` first if you need to
preserve it.

## Security Notes

- **Pod Deployment & Permissions**: The container runs as root by default to ensure complete compatibility with host storage permissions (e.g. `local-path` / `hostPath` volumes owned by root:root) and arbitrary persistent volume mount points. Can be restricted via `securityContext` if desired.
- **HttpOnly Cookies & CSRF Protection**: Browser sessions authenticate via `HttpOnly` same-origin cookies and double-submit CSRF tokens. Sensitive tokens are never stored in browser `localStorage` or transmitted via URL query parameters.
- **Session and logout semantics**: sessions use `HttpOnly`, `SameSite=Strict` cookies and a JWT TTL capped at 30 minutes. Key rotation and “退出所有会话” bump `auth_version`; “退出此浏览器” only clears that browser's cookie. Failed signatures use per-source in-memory throttling; there is no persistent global account lock.
- **Shared identity**: all operators use the same `admin` account and private key. The audit log cannot attribute an action to an individual key holder; rotating the key requires redistributing the replacement file to everyone.
- **Secret management**: `AES_KEY`, `JWT_SECRET`, and `ADMIN_INIT_PASSWORD` are delivered via the Kubernetes Secret. Keep `ADMIN_INIT_PASSWORD` as the offline recovery secret even after password login is disabled.
- **SQLite runtime**: the bundled driver currently reports `3.53.3`; startup rejects SQLite versions older than `3.35.0` because challenge consumption uses `UPDATE ... RETURNING`.
- **RBAC least privilege**: the control panel's ServiceAccount only manages `services` and `networkpolicies` (full CRUD) and reads `pods` and `nodes` (read-only). It has **no** access to `secrets`, `configmaps`, or `pods/exec`.
- **Per-worker SSH credentials**: stored AES-encrypted in SQLite; operators upload credentials through the web UI after first login.
- **SSH Host Key Policy**: Currently uses `InsecureIgnoreHostKey()` for trusted internal network deployment. In production environments, verify that SSH connections from the control panel Pod to worker nodes route through a dedicated, trusted management network.

## Pre-flight Checklist

- [ ] **Pod egress to Kubernetes API**: Pod must be able to reach Kubernetes API (TCP 443 / 6443).
- [ ] **Pod egress to Worker Nodes on TCP 22**: Verify node firewalls (`iptables` / `firewalld`) do not block traffic from the Pod CIDR to worker nodes on port 22.
- [ ] **StorageClass**: Verify StorageClass is local or block-based (not NFS).
- [ ] **Ingress Network Restriction**: If exposed to corporate LAN, configure source IP range restrictions or NetworkPolicy.

## RBAC Permissions Reference

| Resource | API Group | Verbs |
|----------|-----------|-------|
| `services` | `""` (core) | get, list, watch, create, update, delete |
| `networkpolicies` | `networking.k8s.io` | get, list, watch, create, update, delete |
| `pods` | `""` (core) | get, list, watch (read-only) |
| `nodes` | `""` (core) | get, list, watch (read-only) |

No `secrets`, `configmaps`, `pods/exec`, or `pods/portforward` permissions are
granted.
