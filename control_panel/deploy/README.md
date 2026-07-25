# Control Panel - Kubernetes Deployment

This directory contains Kubernetes manifests and an install script for deploying
the control panel into a cluster.

## Contents

| File | Purpose |
|------|---------|
| `rbac.yaml` | Namespace, ServiceAccount, ClusterRole (least privilege), ClusterRoleBinding |
| `pvc.yaml` | PersistentVolumeClaim (1Gi) for the SQLite database |
| `deployment.yaml` | Deployment: single pod, env from Secret, PVC mount, probes, resources |
| `service.yaml` | Service: NodePort 30180 exposing :8080 |
| `secret.yaml.template` | Placeholder Secret template (real `secret.yaml` is git-ignored) |
| `install.sh` | Interactive installer: generates secrets, applies all manifests |
| `README.md` | This file |

## Prerequisites

1. **Target Kubernetes cluster** with:
   - A default `StorageClass` that can provision a 1Gi PVC (or edit `pvc.yaml`).
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
latest pushed image. The cluster nodes must be able to reach the registry
(`registry-xirang.jxslpt.cn:30443`) - if they need credentials, create an
`imagePullSecret` and add `imagePullSecrets:` to the deployment spec.

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

The script is **idempotent**: re-running regenerates the Secret. If a Secret
already exists in the cluster you will be warned and asked to confirm the
overwrite (which rotates `AES_KEY` and `JWT_SECRET`, invalidating existing
encrypted per-worker SSH private keys and all login sessions).

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

- **Secret management**: `AES_KEY`, `JWT_SECRET`, and `ADMIN_INIT_PASSWORD` are
  delivered to the pod via a Kubernetes Secret (`control-panel-secrets`) and
  consumed as env vars (`secretKeyRef`). The generated `secret.yaml` is
  git-ignored; only `secret.yaml.template` (with placeholder values) is
  committed.
- **RBAC least privilege**: the control panel's ServiceAccount can only manage
  `services` and `networkpolicies` (full CRUD) and read `pods` (get/list/watch
  for ownerReferences UID lookup). It has **no** access to `secrets`,
  `configmaps`, or other sensitive resources.
- **Per-worker SSH private keys are NOT mounted as a file.** The backend stores
  them AES-encrypted in SQLite; operators upload each worker's private key
  through the web UI (SetPrivateKey API) after first login. There is no
  `/app/ssh_keys/id_rsa` volume mount in the Deployment - the original spec's
  SSH-key Secret mount was omitted because the backend does not read from the
  filesystem. See `internal/ssh` for the decryption path.
- **Internal-only exposure**: NodePort 30180 is intended for internal-network
  access. Use an Ingress with TLS for any production exposure.
- **Pod security**: the Deployment sets `seccompProfile: RuntimeDefault`. The
  container currently runs as root (required to write to the PVC-mounted
  `/data` without a chown init container); this is a known hardening item - a
  future revision should run as a non-root user with proper volume ownership.

## RBAC Permissions Reference

| Resource | API Group | Verbs |
|----------|-----------|-------|
| `services` | `""` (core) | get, list, watch, create, update, delete |
| `networkpolicies` | `networking.k8s.io` | get, list, watch, create, update, delete |
| `pods` | `""` (core) | get, list, watch (read-only) |

No `secrets`, `configmaps`, `pods/exec`, or `pods/portforward` permissions are
granted.

## Troubleshooting

- **Pod fails to start with `config: AES_KEY env var is required`**: the Secret
  was not applied, or the key is missing. Check:
  `kubectl -n control-panel get secret control-panel-secrets -o yaml`.
- **Pod fails with `AES_KEY must decode to 32 bytes`**: the `AES_KEY` value is
  not a base64 encoding of 32 bytes. Re-run `install.sh` to regenerate.
- **K8s API calls return 403 Forbidden**: the ServiceAccount's ClusterRole is
  not applied, or the ClusterRoleBinding is missing. Check:
  `kubectl -n control-panel describe serviceaccount control-panel`.
- **PVC stuck Pending**: no StorageClass can provision a volume, or the node is
  out of space. Check: `kubectl -n control-panel describe pvc control-panel-data`.
- **NodePort 30180 not reachable**: check node firewalls and that the port
  range allows 30180 (default NodePort range is 30000-32767).
