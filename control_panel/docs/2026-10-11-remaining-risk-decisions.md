# Remaining risk decisions and credential exposure review

Date: 2026-10-11

## Administrator and namespace scope (item 8)

The operator explicitly chose to keep one shared `admin` account/key and the
existing cross-namespace Kubernetes management privileges. No personal accounts,
OIDC integration, per-person audit identity, or namespace write allowlist were
introduced. These are accepted design limitations, not security issues that this
change claims to have eliminated.

Audits can attribute an action to the shared administrator, not reliably to an
individual key holder. A Kubernetes ClusterRole still permits Service and
NetworkPolicy management across namespaces; it is not a namespace isolation
boundary. Existing protected-namespace checks, Pod/Service/NetworkPolicy identity
checks, single-Pod selector checks and fresh destructive storage guards remain.
Read-only Pod/PVC/PV/Node/DaemonSet access is retained for discovery and safe
storage usage decisions; Secret, ConfigMap and Pod exec access is not added.

## Redacted credential exposure checks (item 9)

Pinned Gitleaks v8.24.3 ran locally with full redaction against all reachable
local Git refs and the current working tree. Coverage: 3 local refs, 100 distinct
reachable commits, plus modified/untracked project files. Dependency directories,
local caches, Git internals and ignored scanner artifacts were excluded from the
working-tree pass. No repository content or scan report was uploaded.

Both initial passes reported the same 7 matches. A final working-tree rescan on
2026-10-12 reported the same 7 locations and no new findings:

| Location | Type/count | Owner confirmation |
|---|---|---|
| `control_panel/backend/internal/auth/testdata/p256-login-vector.json` | 2 private-key matches | Synthetic test vectors, never deployed or reused |
| `control_panel/backend/web-build/test/key_crypto.test.mjs` | 1 private-key and 1 generic-api-key match | Test/vector material, never deployed or reused |
| `control_panel/deploy/secret.yaml.template` | 3 generic-api-key matches | Template examples, never deployed or reused |

The operator confirmed that all these materials have never been used as real
credentials. No credential rotation is required for these confirmed fixtures.
No new operational credential match was reported in the covered local data.
This is not proof that credentials in other repositories, copies, unfetched
remote refs, unreachable objects, or deployed systems are absent or rotated.
Scanner pattern coverage is finite and can miss unsupported formats.

No credential validity check, external revocation or production rotation was
performed. No Git history was rewritten. Secret values and matched source lines
are deliberately omitted from this document and the metadata summary.

## Credential-owner procedure if operational reuse is later discovered

1. Identify the credential owner and affected provider/system without sending
   credential values through chat or committing them.
2. Revoke/rotate at that provider and update deployment/worker configuration;
   changing documentation or source literals does not invalidate a real secret.
3. Coordinate JWT signing-secret changes with session invalidation and service
   restart. Use the documented admin-key/recovery process for administrator
   secrets and redistribute a shared replacement key only to authorized holders.
4. Preserve a database backup and the old encryption key during an AES key
   migration. Existing encrypted Worker credentials must be re-encrypted or
   re-uploaded through a verified migration; simply replacing `AES_KEY` can make
   those stored credentials unreadable.
5. Verify deployment behavior and new credential access, then verify old-secret
   revocation through the provider with owner authorization.
6. Consider history/copy remediation only after revocation, with repository-owner
   approval; history rewriting cannot recall other people's clones or backups.

## Performance measurement (remaining item 6)

Local synthetic scale measurements and any behavior-preserving optimization are
recorded separately in `Kubernetes-display-performance.md`. They do not measure
production Kubernetes API-server, network or etcd latency. No live cluster is
accessed by this review or the local benchmark.
