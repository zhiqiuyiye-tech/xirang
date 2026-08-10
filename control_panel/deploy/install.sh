#!/usr/bin/env bash
#
# install.sh - Install the control panel into a Kubernetes cluster.
#
# This script:
#   1. Validates that kubectl is available and connected to a cluster.
#   2. If the Secret 'control-panel-secrets' already exists: REUSES its values
#      (AES_KEY/JWT_SECRET/ADMIN_INIT_PASSWORD) unchanged, so the admin password
#      and encrypted worker credentials keep working across upgrades. Only
#      re-renders secret.yaml (a no-op on the cluster) and re-applies the other
#      manifests (picking up any image/deployment changes).
#   3. On first install (or with --reset-secrets): generates fresh AES_KEY and
#      JWT_SECRET via openssl and prompts for the initial admin password.
#   4. Renders the Secret into secret.yaml (git-ignored).
#   5. Applies all manifests in this directory to the cluster.
#   6. Prints the NodePort access URL.
#
# Idempotent and upgrade-safe: re-running to pick up a new image preserves the
# existing Secret by default. Use --reset-secrets to force regeneration (this
# invalidates existing encrypted worker credentials and the retrievable admin
# password - back up first).
#
# Usage:
#   ./install.sh [--reset-secrets]
#
# Prerequisites:
#   - kubectl installed and configured to talk to the target cluster.
#   - The control panel image built and pushed to the private registry:
#       docker build -t registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest control_panel/backend
#       docker push registry-xirang.jxslpt.cn:30443/tai-dev/control-panel:latest
#     The cluster nodes must be able to pull from that registry (imagePullPolicy: Always).
#     See README.md for self-signed/insecure-registry handling.

set -euo pipefail

# --- constants -------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRET_FILE="${SCRIPT_DIR}/secret.yaml"
SECRET_NAME="control-panel-secrets"
NAMESPACE="control-panel"

# --- helpers ---------------------------------------------------------------

log() {
    printf '\033[1;34m[install]\033[0m %s\n' "$*"
}

warn() {
    printf '\033[1;33m[warn]\033[0m %s\n' "$*" >&2
}

die() {
    printf '\033[1;31m[error]\033[0m %s\n' "$*" >&2
    exit 1
}

# --- preflight -------------------------------------------------------------

command -v kubectl >/dev/null 2>&1 || die "kubectl not found on PATH. Install kubectl and configure it to talk to your cluster."

if ! kubectl cluster-info >/dev/null 2>&1; then
    die "kubectl cannot reach the cluster. Check your kubeconfig / context."
fi

command -v openssl >/dev/null 2>&1 || die "openssl not found on PATH. Install openssl."

# --- flag parsing ---------------------------------------------------------

RESET_SECRETS=0
for arg in "$@"; do
    case "${arg}" in
        --reset-secrets) RESET_SECRETS=1 ;;
        --help|-h)
            cat <<'EOF'
Usage: ./install.sh [--reset-secrets]

Installs or upgrades the control panel. By default, if the Secret
'control-panel-secrets' already exists, its values (AES_KEY, JWT_SECRET,
ADMIN_INIT_PASSWORD) are REUSED unchanged so the admin password and encrypted
worker credentials keep working across image upgrades.

  --reset-secrets   Force regeneration of AES_KEY/JWT_SECRET/admin password.
                    Invalidates existing encrypted worker credentials and the
                    retrievable admin password - back up first.
EOF
            exit 0 ;;
        *) die "unknown argument: ${arg} (see --help)" ;;
    esac
done

# --- secret values: reuse existing, or generate on first install ----------

SECRET_EXISTS=0
if kubectl get secret "${SECRET_NAME}" -n "${NAMESPACE}" >/dev/null 2>&1; then
    SECRET_EXISTS=1
fi

# read_secret_key echoes the existing base64 value for a Secret data key
# (empty if the secret or key is absent). Called only when SECRET_EXISTS=1.
read_secret_key() {
    kubectl get secret "${SECRET_NAME}" -n "${NAMESPACE}" \
        -o "jsonpath={.data.$1}" 2>/dev/null || true
}

if [ "${SECRET_EXISTS}" = "1" ] && [ "${RESET_SECRETS}" = "0" ]; then
    # Upgrade / re-run: reuse the existing Secret values verbatim. The admin
    # password is bcrypt-hashed in the SQLite DB (on the PVC) and the per-worker
    # SSH credentials are AES-encrypted with AES_KEY in the same DB - reusing
    # these values keeps both working. Re-rendering secret.yaml with identical
    # values is a no-op on the cluster; re-applying picks up image/deployment
    # changes only.
    log "Secret '${SECRET_NAME}' exists - reusing its values (passwords unchanged)."
    AES_KEY="$(read_secret_key AES_KEY)"
    JWT_SECRET="$(read_secret_key JWT_SECRET)"
    ADMIN_INIT_PASSWORD_B64="$(read_secret_key ADMIN_INIT_PASSWORD)"
    if [ -z "${AES_KEY}" ] || [ -z "${JWT_SECRET}" ] || [ -z "${ADMIN_INIT_PASSWORD_B64}" ]; then
        die "existing Secret is missing AES_KEY/JWT_SECRET/ADMIN_INIT_PASSWORD; re-run with --reset-secrets to regenerate."
    fi
else
    # First install, or explicit reset.
    if [ "${SECRET_EXISTS}" = "1" ] && [ "${RESET_SECRETS}" = "1" ]; then
        warn "Secret '${SECRET_NAME}' exists and --reset-secrets was given."
        warn "Re-applying will OVERWRITE the existing values:"
        warn "  - Rotate AES_KEY: existing encrypted per-worker SSH private keys become unreadable (back up the old key first if needed)."
        warn "  - Rotate JWT_SECRET: all current login sessions are invalidated."
        warn "  - Reset ADMIN_INIT_PASSWORD: the retrievable password changes (the DB bcrypt hash is only seeded on first startup, so the old password keeps working until you change it)."
        read -r -p "Overwrite? Type 'yes' to continue: " CONFIRM
        [ "${CONFIRM}" = "yes" ] || die "aborted by user."
    fi

    log "Generating AES_KEY (32 random bytes, base64)..."
    AES_KEY="$(openssl rand 32 | base64 | tr -d '\n')"
    if [ -z "${AES_KEY}" ]; then die "failed to generate AES_KEY"; fi

    log "Generating JWT_SECRET (32 random bytes, base64)..."
    JWT_SECRET="$(openssl rand 32 | base64 | tr -d '\n')"
    if [ -z "${JWT_SECRET}" ]; then die "failed to generate JWT_SECRET"; fi

    log "Prompt for initial admin password (input hidden)..."
    while true; do
        read -r -s -p "  Initial admin password (min 8 chars): " ADMIN_PW
        echo
        if [ "${#ADMIN_PW}" -lt 8 ]; then
            warn "Password must be at least 8 characters. Please try again."
            continue
        fi
        read -r -s -p "  Confirm password: " ADMIN_PW_CONFIRM
        echo
        if [ "${ADMIN_PW}" != "${ADMIN_PW_CONFIRM}" ]; then
            warn "Passwords do not match. Please try again."
            continue
        fi
        break
    done

    ADMIN_INIT_PASSWORD_B64="$(printf '%s' "${ADMIN_PW}" | base64 | tr -d '\n')"
    unset ADMIN_PW ADMIN_PW_CONFIRM
fi

# --- render secret.yaml ----------------------------------------------------

log "Rendering ${SECRET_FILE}..."
cat > "${SECRET_FILE}" <<EOF
# Generated by install.sh on $(date -u '+%Y-%m-%dT%H:%M:%SZ').
# DO NOT COMMIT THIS FILE - it is git-ignored (see .gitignore).
apiVersion: v1
kind: Secret
metadata:
  name: ${SECRET_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: control-panel
type: Opaque
data:
  AES_KEY: ${AES_KEY}
  JWT_SECRET: ${JWT_SECRET}
  ADMIN_INIT_PASSWORD: ${ADMIN_INIT_PASSWORD_B64}
EOF
chmod 600 "${SECRET_FILE}" 2>/dev/null || true
unset AES_KEY JWT_SECRET ADMIN_INIT_PASSWORD_B64

# --- apply manifests -------------------------------------------------------

log "Applying manifests from ${SCRIPT_DIR}..."
kubectl apply -f "${SCRIPT_DIR}/rbac.yaml"
kubectl apply -f "${SCRIPT_DIR}/pvc.yaml"
kubectl apply -f "${SECRET_FILE}"
kubectl apply -f "${SCRIPT_DIR}/deployment.yaml"
kubectl apply -f "${SCRIPT_DIR}/service.yaml"

# --- print access info -----------------------------------------------------

log "Installation complete."
echo
echo "Control panel is deploying to namespace '${NAMESPACE}'."
echo
echo "Wait for the pod to become Ready:"
echo "  kubectl -n ${NAMESPACE} rollout status deployment/control-panel"
echo
echo "Access the web UI via NodePort (30180):"
echo "  http://<any-node-ip>:30180/"
echo
echo "Default admin username: admin"
echo "Login with the password you just set."
echo
echo "Manifests applied:"
echo "  - Namespace, ServiceAccount, ClusterRole, ClusterRoleBinding (rbac.yaml)"
echo "  - PersistentVolumeClaim control-panel-data (pvc.yaml)"
echo "  - Secret control-panel-secrets (secret.yaml, generated)"
echo "  - Deployment control-panel (deployment.yaml)"
echo "  - Service control-panel NodePort 30180 (service.yaml)"
