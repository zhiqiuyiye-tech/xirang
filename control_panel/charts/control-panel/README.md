# control-panel Helm Chart

One-command deployment of the Agentless K8s + storage control panel. All
secrets (AES_KEY, JWT_SECRET, ADMIN_INIT_PASSWORD) are auto-generated on install
- no manual setup.

## Prerequisites

1. **Private registry image pushed** (the master must be able to pull it):
   ```bash
   docker build -t registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest ./control_panel/backend
   docker push registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest
   ```
   If the registry needs auth or uses a self-signed cert, configure the cluster
   nodes (insecure-registries / CA) or set `image.imagePullSecrets` in values.

2. **Cluster has a default StorageClass** (for the 1Gi PVC), or set
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
helm push /tmp/control-panel-0.3.0.tgz oci://registry-xirang.jxslpt.cn:30443/tai-dev
```

The chart then lives at `oci://registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:0.3.0`.

## Install

### From the OCI registry (any machine)

```bash
helm install control-panel oci://registry-xirang.jxslpt.cn:30443/tai-dev/control-panel \
  --version 0.3.0 --create-namespace -n control-panel
```

### From a local chart checkout

```bash
helm install control-panel ./control_panel/charts/control-panel \
  --create-namespace -n control-panel
```

That's it. Helm prints the access URL and the command to retrieve the
auto-generated admin password (also see `NOTES.txt`).

Retrieve the admin password:

```bash
kubectl -n control-panel get secret control-panel-secrets \
  -o jsonpath='{.data.ADMIN_INIT_PASSWORD}' | base64 -d ; echo
```

Access the web UI (NodePort 30180 by default):

```
http://<any-node-ip>:30180/
```

Login with username `admin` + the retrieved password.

## Upgrade (after a new image push)

```bash
helm upgrade control-panel ./control_panel/charts/control-panel -n control-panel
# or, to bump just the image tag:
helm upgrade control-panel ./control_panel/charts/control-panel -n control-panel \
  --set image.tag=v2
```

`imagePullPolicy: Always` makes the pod pull the latest image on restart.

Passwords survive the upgrade: the admin login password (bcrypt-hashed in the
SQLite DB on the PVC) and the per-worker SSH credentials (AES-encrypted in the
same DB) are never touched by `helm upgrade`. The Secret values
(`AES_KEY`/`JWT_SECRET`/`ADMIN_INIT_PASSWORD`) are reused from the existing
deployed Secret via the `lookup` function (see `templates/_helpers.tpl`), so the
key that decrypts worker creds and the password retrievable via `kubectl get
secret ... ADMIN_INIT_PASSWORD | base64 -d` both stay stable across upgrades.

## Pin secrets across upgrades

By default the three Secret values are generated once on first install and
reused on every upgrade via `lookup`. To explicitly pin them (e.g. to set your
own admin password or to force a rotation), set them in values or `--set`:

```bash
helm install control-panel ./control_panel/charts/control-panel -n control-panel \
  --create-namespace \
  --set secrets.adminPassword=yourpass \
  --set secrets.aesKey=$(openssl rand 32 | base64) \
  --set secrets.jwtSecret=$(openssl rand 32 | base64)
```

Note: pinning `secrets.aesKey`/`secrets.jwtSecret` on a `helm upgrade` of an
existing release WILL rotate them (pinned values win over `lookup`), which
invalidates existing encrypted worker credentials and login sessions. Only pin
on first install, or when you intend to rotate.

## Uninstall

```bash
helm uninstall control-panel -n control-panel
kubectl delete namespace control-panel   # also removes the PVC (SQLite data)
```

## Configuration

| Key | Default | Description |
|-----|---------|-------------|
| `image.repository` | `registry-xirang.jxslpt.cn:30443/tai-dev/control-panel` | Image repo |
| `image.tag` | `latest` | Image tag |
| `image.pullPolicy` | `Always` | Pull policy |
| `image.imagePullSecrets` | `[]` | Registry auth secrets |
| `namespace` | `control-panel` | Namespace |
| `service.type` | `NodePort` | Service type |
| `service.port` | `8080` | Container/service port |
| `service.nodePort` | `30180` | NodePort |
| `persistence.enabled` | `true` | PVC for SQLite |
| `persistence.size` | `1Gi` | PVC size |
| `persistence.storageClassName` | `""` | StorageClass (default if empty) |
| `secrets.aesKey` | `""` (auto) | Pin AES_KEY (base64 32-byte) |
| `secrets.jwtSecret` | `""` (auto) | Pin JWT_SECRET (base64) |
| `secrets.adminPassword` | `""` (auto) | Pin admin password (plaintext) |
| `resources` | req 100m/128Mi, lim 500m/512Mi | Pod resources |
