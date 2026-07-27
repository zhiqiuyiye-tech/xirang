#!/usr/bin/env bash
#
# push-chart.sh - Package and push the control-panel Helm chart to an OCI registry.
#
# Prerequisites: helm >= 3.8 (OCI support enabled by default since 3.8).
#
# Usage:
#   ./push-chart.sh
#
# Environment overrides:
#   OCI_REGISTRY  (default: registry-xirang.jxslpt.cn:30443)
#   OCI_REPO      (default: tai-dev)
#   CHART_VERSION (default: read from Chart.yaml)
#
# After pushing, install on any machine with:
#   helm install control-panel oci://<OCI_REGISTRY>/<OCI_REPO>/control-panel \
#     --version <CHART_VERSION> --create-namespace -n control-panel

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART_DIR="${SCRIPT_DIR}/../charts/control-panel"

OCI_REGISTRY="${OCI_REGISTRY:-registry-xirang.jxslpt.cn:30443}"
OCI_REPO="${OCI_REPO:-tai-dev}"
CHART_NAME="control-panel"

command -v helm >/dev/null 2>&1 || { echo "helm not found (need >= 3.8 for OCI)"; exit 1; }

# Extract version from Chart.yaml (no yq dependency).
CHART_VERSION="${CHART_VERSION:-$(awk '/^version:/{print $2}' "${CHART_DIR}/Chart.yaml")}"
[ -n "${CHART_VERSION}" ] || { echo "could not read version from Chart.yaml"; exit 1; }

OCI_REF="${OCI_REGISTRY}/${OCI_REPO}/${CHART_NAME}"

echo "==> Packaging chart ${CHART_NAME}-${CHART_VERSION} from ${CHART_DIR}"
PKG="$(helm package "${CHART_DIR}" --version "${CHART_VERSION}" --destination "${SCRIPT_DIR}" | awk '/Saved/{print $NF}')"
[ -n "${PKG}" ] || PKG="${SCRIPT_DIR}/${CHART_NAME}-${CHART_VERSION}.tgz"
echo "    packaged: ${PKG}"

echo "==> Logging in to OCI registry ${OCI_REGISTRY}"
helm registry login "${OCI_REGISTRY}"

echo "==> Pushing ${PKG} to oci://${OCI_REF}"
helm push "${PKG}" "oci://${OCI_REGISTRY}/${OCI_REPO}"

echo
echo "Done. Chart pushed as:"
echo "  oci://${OCI_REF}:${CHART_VERSION}"
echo
echo "Install on any machine:"
echo "  helm install control-panel oci://${OCI_REF} \\"
echo "    --version ${CHART_VERSION} --create-namespace -n control-panel"
echo
echo "Pull/install without specifying version (latest):"
echo "  helm install control-panel oci://${OCI_REF} --create-namespace -n control-panel"
