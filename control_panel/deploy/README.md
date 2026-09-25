# Control Panel - Kubernetes Deployment

> **One-command install (recommended):** use the Helm chart at
> `control_panel/charts/control-panel/`. It auto-generates all secrets
> (AES_KEY/JWT_SECRET/admin password) so a single `helm install` brings up a
> working pod with zero manual steps:
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
| `README.md` | This file |

## Critical Storage Requirements (SQLite)

> **CRITICAL**: The PVC backing `/data` **MUST** use a block-based storage class or local storage (e.g. `local-path`, `hostPath`, Ceph RBD, Longhorn).
> **DO NOT USE REGULAR NFS FOR THE CONTROL PANEL PVC.**
> The backend SQLite database operates in WAL (Write-Ahead Logging) mode, which relies on POSIX shared-memory primitives (`.db-shm`). Network file systems (such as NFS) do not reliably support POSIX locking and shared memory, which can lead to `database is locked` errors or database corruption.

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
4. Prompt for the initial admin password (min 8 chars, input hidden).
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

The web UI is exposed on **NodePort 30180**:

```
http://<any-node-ip>:30180/
```

Default admin username: `admin`. Log in with the password you set during
`install.sh`.

> **Internal exposure only.** The NodePort is intended for internal-network
> access. Restrict it at the cluster level (NetworkPolicy, firewall, or an
> external load balancer) as appropriate for your environment. For production
> with TLS, replace the NodePort Service with a ClusterIP Service + an Ingress
> resource backed by a certificate (e.g. cert-manager).

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
- **Session Revocation & Rate Limiting**: Administrative password changes automatically bump `auth_version` in the database, immediately invalidating any older active sessions and tokens. Login attempts are rate-limited to prevent brute-force attacks.
- **Secret management**: `AES_KEY`, `JWT_SECRET`, and `ADMIN_INIT_PASSWORD` are delivered to the pod via Kubernetes Secret (`control-panel-secrets`).
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
