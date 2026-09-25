# control-panel Helm Chart

One-command deployment of the Agentless K8s + storage control panel. All
secrets (AES_KEY, JWT_SECRET, ADMIN_INIT_PASSWORD) are auto-generated on install
- no manual setup.

## Architecture & Security Highlights

- **Pod Security Hardening**: Runs as non-root user (`UID:GID 10001:10001`), read-only root filesystem, `allowPrivilegeEscalation: false`, all Linux capabilities dropped (`drop: ["ALL"]`), seccomp profile `RuntimeDefault`.
- **HttpOnly Cookie & CSRF**: Web UI authenticates via same-origin `HttpOnly` session cookies and double-submit CSRF tokens. Sensitive tokens are not exposed in browser `localStorage` or URL query strings.
- **Session Revocation & Rate Limiting**: Administrative password change automatically increments `auth_version` and invalidates all previous sessions. Login attempts are rate-limited (default 5 failed attempts triggers 15-minute temporary lockout).
- **Health Probes**: Dedicated `/health/live` (process health) and `/health/ready` (SQLite & Kubernetes API readiness) endpoints.

## Critical Storage Requirements (SQLite)

> **CRITICAL**: The PVC backing `/data` **MUST** use a block-based storage class or local storage (e.g. `local-path`, `hostPath`, Ceph RBD, Longhorn).
> **DO NOT USE REGULAR NFS FOR THE CONTROL PANEL PVC.**
> The backend SQLite database operates in WAL (Write-Ahead Logging) mode, which relies on POSIX shared-memory primitives (`.db-shm`). Network file systems (such as NFS) do not reliably support POSIX locking and shared memory, which can lead to `database is locked` errors or database corruption.

## Prerequisites

1. **Private registry image pushed** (the master must be able to pull it):
   ```bash
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
helm push /tmp/control-panel-0.7.3.tgz oci://registry-xirang.jxslpt.cn:30443/tai-dev
```

The chart then lives at `oci://registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:0.7.3`.

## Install

### 1. Standard Internal Deployment (NodePort)

```bash
helm install control-panel ./control_panel/charts/control-panel \
  --create-namespace -n control-panel
```

Retrieve the initial admin password:

```bash
kubectl -n control-panel get secret control-panel-secrets \
  -o jsonpath='{.data.ADMIN_INIT_PASSWORD}' | base64 -d ; echo
```

Access the web UI (NodePort 30180 by default):

```
http://<node-ip>:30180/
```

### 2. Production Deployment (HTTPS Ingress + ClusterIP)

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
- **`ADMIN_INIT_PASSWORD`**: Seeded into the SQLite database **only on the very first boot**. Once the admin logs in and updates their password via the web UI ("修改密码"), the new bcrypt hash in SQLite is authoritative.

## Backup, Restore & Rollback

### Backup

Before performing major upgrades:

```bash
# 1. Backup Kubernetes secrets
kubectl -n control-panel get secret control-panel-secrets -o yaml > control-panel-secrets-backup.yaml

# 2. Backup SQLite database safely using SQLite online backup
kubectl -n control-panel exec -it deployment/control-panel -- cp /data/control_panel.db /tmp/control_panel_backup.db
kubectl -n control-panel cp control-panel-xxxx:/tmp/control_panel_backup.db ./control_panel_backup.db
```

### Rollback

```bash
helm rollback control-panel -n control-panel
```

The database schema migrations are backwards-compatible, so rolling back to the previous image version remains supported.

## Pre-flight Checklist

- [ ] **Pod egress to Kubernetes API**: Pod must be able to contact Kubernetes API (TCP 443 / 6443).
- [ ] **Pod egress to Worker Nodes on TCP 22**: Worker management & LVM/NFS automation require the Pod to establish SSH connections to worker nodes on port 22. Verify node firewalls (`iptables` / `firewalld`) do not block traffic from the Pod CIDR.
- [ ] **StorageClass**: Ensure StorageClass is `local-path`, `hostPath`, or a block CSI (not NFS).
- [ ] **Ingress Network Restriction**: If exposed to corporate LAN, configure `whitelist-source-range` on Ingress or enable `networkPolicy`.

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
| `config.cookieSecure` | `false` | Set `Secure` on cookies (set `true` with HTTPS) |
| `config.rateLimitMaxFailures` | `5` | Failed logins before temporary lockout |
| `config.rateLimitLockoutDuration` | `15m` | Duration of login lockout |
| `podSecurityContext.runAsNonRoot` | `true` | Enforce non-root execution |
| `podSecurityContext.runAsUser` | `10001` | Non-root UID |
| `persistence.enabled` | `true` | PVC for SQLite database |
| `persistence.storageClassName` | `"local-path"` | StorageClass (must be block or local) |
| `secrets.aesKey` | `""` (auto) | Pin AES_KEY (base64 32-byte) |
| `secrets.jwtSecret` | `""` (auto) | Pin JWT_SECRET (base64) |
| `secrets.adminPassword` | `""` (auto) | Pin initial admin password |
