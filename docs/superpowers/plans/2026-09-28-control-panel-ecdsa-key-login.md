# Control Panel ECDSA Key Login Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the single admin password login with a P-256 challenge-signature flow using a shared downloadable private-key file, while preserving the approved HTTP-only deployment constraints.

**Architecture:** Keep the existing single `admin` row and JWT/CSRF cookie session model. Add P-256 protocol helpers, explicit auth states, durable one-use SQLite challenges, version-bound/CAS session issuance, source-based throttling, and a local bundled browser crypto module. The web application remains cookie-authenticated; bootstrap, rotation, local logout, and global logout have separate state transitions.

**Tech Stack:** Go 1.26, Gin, `crypto/ecdsa`, `crypto/x509`, SQLite via `modernc.org/sqlite`, embedded HTML/CSS/JavaScript, Node.js 24 for a reproducible browser-crypto bundle.

**Spec:** `docs/superpowers/specs/2026-09-28-control-panel-ecdsa-key-login-design.md`

## Global Constraints

- One `admin` account and one shared unencrypted PKCS#8 P-256 key file; no user/role schema.
- HTTP only, one service process/replica, local persistent SQLite; no claim of protection against active HTTP MITM.
- Challenge ID = 16 bytes, nonce = 32 bytes, 2-minute lifetime; canonical base64url without padding.
- Signature = 64-byte `r || s`; sign one SHA-256 digest of the exact domain-separated UTF-8/LF message.
- Login Session `auth_version` equals its consumed challenge version; bootstrap/rotation Session version comes only from the CAS transaction result.
- Auth states are `PASSWORD_BOOTSTRAP`, `KEY_ACTIVE`, `RECOVERY_PENDING`; invalid field combinations fail before the HTTP listener starts.
- Atomic challenge consumption and atomic pending-count/insert; check SQLite runtime `>= 3.35.0` before migrations. Verified current runtime: `3.53.3`.
- JWT TTL defaults to 30 minutes; startup rejects values above 30 minutes. Cookies use `HttpOnly`, `SameSite=Strict`, and `Secure=false` only for the required HTTP deployment.
- A normal logout clears only the current browser; `logout-all` increments the global auth version. Signature failures only throttle the resolved source IP in process memory; no persisted account-wide lock.
- Trust no forwarded IP headers unless their proxy CIDR is explicitly configured; `client_ip` is for rate/pending accounting and audit only, never authentication binding.
- Browser crypto uses pinned `@noble/curves@2.4.0`, `asn1js@3.0.10`, and build-only `esbuild@0.28.2`; require `crypto.getRandomValues()`, deterministic ECDSA, no CDN, no `Math.random()` fallback.
- Keep all private-key contents out of requests, logs, DOM, URL, local storage, and IndexedDB. Best-effort memory cleanup must not be described as secure erasure.

---

### Task 1: Add protocol crypto primitives with fixed Go tests

**Files:**
- Create: `control_panel/backend/internal/auth/key_protocol.go`
- Test: `control_panel/backend/internal/auth/key_protocol_test.go`

**Interfaces:**
- Produce `ChallengeContext{ID, Nonce, Purpose, AuthVersion, KeyFingerprint, NewKeyFingerprint}` and `ProofKind` constants for login, bootstrap, current-key rotation authorization, and new-key proof.
- Produce `CanonicalizeP256PublicKeyPEM(pemText) -> (*ecdsa.PublicKey, canonicalPEM, fingerprint, error)`.
- Produce `BuildChallengeMessage(context, proofKind) -> []byte` and `DecodeCanonicalRawSignature(encoded) -> ([64]byte, error)`.
- Produce `VerifyP256DigestSignature(publicKey, digest, rawSignature) -> bool`, rejecting `r` or `s` outside `[1,N-1]`.

- [ ] **Step 1: Add failing tests** for P-256 PEM canonicalization/fingerprint, rejected malformed and non-P-256 keys, exact four domain-separated messages, canonical 16/32-byte base64url values, 86-character raw signatures, invalid `r/s`, and Go-generated signature verification.
- [ ] **Step 2: Run the focused test** from `control_panel/backend`: `go test ./internal/auth -run 'Test(CanonicalizeP256|BuildChallengeMessage|DecodeCanonicalRawSignature|VerifyP256)' -count=1`; confirm the missing functions/tests fail.
- [ ] **Step 3: Implement the helpers** using only Go standard-library P-256, PEM, X.509 and ECDSA APIs; compute fingerprints from canonical SPKI DER and hash each signed message exactly once.
- [ ] **Step 4: Re-run the focused tests** and add fixed message/digest/signature fixtures usable by the browser test suite.

### Task 2: Add SQLite runtime guard, schema migration and atomic auth storage

**Files:**
- Modify: `control_panel/backend/internal/db/db.go`
- Modify: `control_panel/backend/internal/db/migrations.go`
- Modify: `control_panel/backend/internal/db/models.go`
- Modify: `control_panel/backend/internal/db/admins.go`
- Create: `control_panel/backend/internal/db/auth_challenges.go`
- Create: `control_panel/backend/internal/db/auth_state.go`
- Test: `control_panel/backend/internal/db/db_test.go`
- Test: `control_panel/backend/internal/db/admins_test.go`
- Create: `control_panel/backend/internal/db/auth_challenges_test.go`

**Interfaces:**
- `db.Open` validates `SELECT sqlite_version()` against `3.35.0` before `runMigrations`.
- `Admin` exposes typed `AuthState`, optional canonical public key PEM, and fingerprint; password/private fields remain JSON-hidden.
- Store methods provide validated admin-auth reads, startup state validation/recovery, `BootstrapAdminKey(expectedVersion, keyPEM, fingerprint) -> newVersion`, `RotateAdminKey(expectedVersion, currentFingerprint, keyPEM, newFingerprint) -> newVersion`, current/global session revocation, atomic challenge create and atomic one-use challenge consume.
- Challenge creation receives purpose, version, current/candidate fingerprints, source IP, expiry and pending caps; source IP is persisted only for throttling/accounting/audit.

- [ ] **Step 1: Add failing schema/runtime tests** for a v3-to-new migration preserving the existing password hash, a single migration-time `auth_version` bump, all new fields/tables/indexes, and SQLite version parsing below/at/above `3.35.0`.
- [ ] **Step 2: Run the focused tests**: `go test ./internal/db -run 'Test(Open|Upgrade|SQLiteVersion|AdminAuthState)' -count=1`; confirm failures before implementation.
- [ ] **Step 3: Add the migration and startup DB checks**; set old records to `PASSWORD_BOOTSTRAP`, add canonical-key/state columns, create challenge storage, and bump old session versions once.
- [ ] **Step 4: Add failing tests** for strict state invariants, `RECOVERY_PENDING` re-seeding, bootstrap/rotation CAS return versions, duplicate challenge rejection, expiry/purpose checks, and 100 concurrent challenge consumers with exactly one success.
- [ ] **Step 5: Implement auth-store transactions**. Consume with conditional `UPDATE ... RETURNING`; create challenges, clean old rows, count source/global pending rows, and insert within one serialized SQLite write transaction; bootstrap/rotation use conditional updates and return the exact incremented version.
- [ ] **Step 6: Add a concurrency test** that starts 100 goroutines creating challenges from one IP and proves per-IP/global limits are never exceeded; run `go test -race ./internal/db` when a CGo compiler is available.

### Task 3: Enforce startup invariants, TTL, proxy trust and source-only throttling

**Files:**
- Modify: `control_panel/backend/internal/config/config.go`
- Test: `control_panel/backend/internal/config/config_test.go`
- Modify: `control_panel/backend/internal/auth/ratelimit.go`
- Test: `control_panel/backend/internal/auth/ratelimit_test.go`
- Modify: `control_panel/backend/internal/api/router.go`
- Test: `control_panel/backend/internal/api/health_test.go`
- Create: `control_panel/backend/internal/api/router_security_test.go`
- Modify: `control_panel/backend/cmd/server/main.go`

**Interfaces:**
- Config defaults `JWT_TTL=30m`, `COOKIE_SAMESITE=Strict`, and rejects JWT TTL above 30m and malformed trusted proxy CIDRs.
- Router setup explicitly disables forwarded-header trust when the trusted proxy list is empty; router creation returns an error for invalid proxy configuration.
- Source throttling keys only on the safely resolved client IP, is process-local and bounded, and never changes persisted auth state or `auth_version`.
- Startup order validates SQLite, runs migrations/seeding, validates the complete admin auth-state tuple, then constructs the router/listener; absent `ADMIN_INIT_PASSWORD` or invalid state exits before HTTP starts.

- [ ] **Step 1: Add failing config tests** for 30-minute default, exactly-30-minute acceptance, over-limit rejection, Strict default, invalid proxy CIDRs, and missing/empty `ADMIN_INIT_PASSWORD`.
- [ ] **Step 2: Add failing router tests** proving spoofed `X-Forwarded-For` is ignored with no trusted proxies and used only for configured trusted proxy CIDRs.
- [ ] **Step 3: Add limiter tests** proving signature failures throttle only their source, use bounded in-memory backoff, and do not lock another source or persist lock state.
- [ ] **Step 4: Implement config/router/limiter changes** and update `NewRouter` call sites in `cmd/server/main.go`, `handlers_k8s_test.go`, `handlers_workers_test.go`, and `health_test.go` for its error return.
- [ ] **Step 5: Implement startup validation** after seed/recovery and before router/listener creation; on `RECOVERY_PENDING`, re-hash the configured secret, clear stale challenges, transition to `PASSWORD_BOOTSTRAP`, and insert one `auth.recovery_bootstrap` audit event. Test every valid state tuple, representative invalid combinations, and recovery audit behavior.
- [ ] **Step 6: Run** `go test ./internal/config ./internal/auth ./internal/api ./internal/db -run 'Test(Load|RateLimiter|TrustedProxy|StartupAuthState)' -count=1`.

### Task 4: Implement challenge, bootstrap, login, rotation and logout APIs

**Files:**
- Modify: `control_panel/backend/internal/api/handlers_auth.go`
- Modify: `control_panel/backend/internal/api/router.go`
- Test: `control_panel/backend/internal/api/handlers_auth_key_test.go`
- Modify: `control_panel/backend/internal/auth/middleware.go` only if needed to preserve per-request version checking.

**Interfaces:**
- Public routes: `GET /auth/status`, `POST /auth/challenges/login`, `POST /auth/login`, `POST /auth/challenges/bootstrap`, `POST /auth/bootstrap`.
- CSRF-protected routes: `POST /auth/challenges/rotate`, `PUT /auth/key`, `POST /auth/logout`, and `POST /auth/logout-all`.
- Login signs a Session with the consumed challenge's `auth_version` only. Bootstrap/rotation sign with the version returned from the successful DB transaction only; no “read current latest version” after verification/commit.
- Auth success sets cookie values only; response JSON never echoes JWT or CSRF tokens. Every auth response sets `Cache-Control: no-store`.

- [ ] **Step 1: Replace password-path tests with failing API tests** for status states, challenge issue/expiry/rate limit, successful signature login, JSON token absence, one-time password bootstrap + PoP, key rotation requiring both signatures, replay rejection, and audit records containing no password/private key/nonce/signature.
- [ ] **Step 2: Add failure/concurrency tests** for version changes between challenge and login, bootstrap race, rotation CAS race, wrong-purpose challenge, oversized input, invalid canonical base64url, and a failed signature from one IP not locking another.
- [ ] **Step 3: Add logout tests** proving ordinary logout clears only the request browser's cookies without changing `auth_version`, while logout-all bumps it and rejects every prior session.
- [ ] **Step 4: Implement handler flows** using the protocol helpers from Task 1 and atomic store methods from Task 2; keep failure logging credential-free and rate-limited.
- [ ] **Step 5: Wire routes and CSRF policies**; remove `/auth/password`, ensure key challenge endpoints have explicit purposes, enforce 8-KiB auth request bodies, and attach no-store headers.
- [ ] **Step 6: Run** `go test ./internal/api -run 'Test(Auth|Challenge|Bootstrap|Rotate|Logout)' -count=1` and run `go test -race ./internal/api ./internal/db` when a CGo compiler is available.

### Task 5: Bound authenticated SSE lifetime and revocation delay

**Files:**
- Modify: `control_panel/backend/internal/api/handlers_tasks.go`
- Test: `control_panel/backend/internal/api/handlers_tasks_test.go`
- Create: `control_panel/backend/internal/api/handlers_tasks_auth_lifetime_test.go`

**Interfaces:**
- SSE still authenticates with same-origin cookie and checks JWT expiry plus database `auth_version` at connection start.
- A fixed 30-second revalidation ticker closes the stream after global logout/key rotation or JWT expiry; checking on task events may close earlier.

- [ ] **Step 1: Add a failing stream test** that changes the stored auth version while an SSE stream is open and asserts the stream closes within one 30-second revalidation interval using a controllable clock/ticker seam.
- [ ] **Step 2: Add a failing expiry test** and keep current valid-stream, cookie, terminal-task and heartbeat coverage intact.
- [ ] **Step 3: Implement recurring JWT/version validation** without delaying event delivery; close the connection on invalid/expired state.
- [ ] **Step 4: Run** `go test ./internal/api -run 'Test.*Stream' -count=1` and `go test -race ./internal/api`.

### Task 6: Bundle browser crypto and replace login/credential UI

**Files:**
- Create: `control_panel/backend/web-build/package.json`
- Create: `control_panel/backend/web-build/package-lock.json`
- Create: `control_panel/backend/web-build/build.mjs`
- Create: `control_panel/backend/web-build/src/key_crypto.js`
- Create: `control_panel/backend/web-build/test/key_crypto.test.mjs`
- Create: `control_panel/backend/web-build/NOTICE.md`
- Create: `control_panel/backend/internal/api/web/p256.bundle.js` (generated and committed)
- Modify: `control_panel/backend/internal/api/web/index.html`
- Modify: `control_panel/backend/internal/api/web/app.js`
- Create: `control_panel/backend/internal/api/web/key_login.js`
- Modify: `control_panel/backend/internal/api/web/styles.css`
- Modify: `control_panel/backend/internal/api/static.go`
- Modify: `control_panel/backend/internal/api/router.go`

**Interfaces:**
- Bundle `@noble/curves@2.4.0` and `asn1js@3.0.10` with build-only `esbuild@0.28.2`; ship the committed bundle locally, with package locks, hashes and MIT/BSD license notices.
- Browser wrapper exports `generatePrivateKeyPem() -> Promise<string>`, `derivePublicKeyPem(privatePem) -> string`, `fingerprintPublicKeyPem(publicPem) -> Promise<string>`, and `signChallenge(privatePem, ChallengeContext, ProofKind) -> Promise<string>`; signatures are canonical base64url strings of exactly 86 characters.
- Browser key generation calls only `crypto.getRandomValues()` and fails closed when unavailable; no CDN or fallback RNG.
- Login page chooses key login versus one-time password bootstrap from auth status. Bootstrap/rotation generate and download PEM, release generated state, require re-selection, derive the public key from the re-imported key, and submit PoP. The current key must be re-selected for rotation authorization.

- [ ] **Step 1: Add Node failing tests** using the fixed Go vectors for PKCS#8 import/export, exact message digest, JS-sign/Go-verify and Go-sign/JS-verify; reject wrong curves, malformed/oversized PEM, and missing `crypto.getRandomValues()`.
- [ ] **Step 2: Run** `npm test` in `control_panel/backend/web-build`; confirm the new crypto tests fail before implementation.
- [ ] **Step 3: Implement browser crypto source** with deterministic ECDSA from the pinned library, strict DER/OID validation and no application-defined ECC arithmetic; run tests.
- [ ] **Step 4: Build and pin the static artifact**: run `npm ci`, then `npm run build`; inspect the output/license bundle and verify no external import or CDN reference.
- [ ] **Step 5: Add UI tests/manual steps** for key-state rendering, bootstrap re-selection, login challenge, key rotation dual proof, current-browser logout, and logout-all.
- [ ] **Step 6: Update CSP/static routes**: `default-src 'self'`, `script-src 'self'`, `object-src 'none'`, `base-uri 'none'`, `frame-ancestors 'none'`, `form-action 'self'`, `connect-src 'self'`, `img-src 'self' data:`, and `style-src 'self' 'unsafe-inline'`; no inline/eval script or third-party URLs; remove the login form's inline handler and `javascript:` action, set no-referrer, and mark login HTML/static signing code no-store.
- [ ] **Step 7: Run separately** from `control_panel/backend/web-build`: `npm test` and `npm run build`; then run `go test ./internal/api` from `control_panel/backend`.

### Task 7: Update deployment configuration, recovery and operator docs

**Files:**
- Modify: `control_panel/backend/Dockerfile`
- Create: `control_panel/backend/.dockerignore`
- Modify: `control_panel/backend/cmd/server/main.go`
- Modify: `control_panel/deploy/deployment.yaml`
- Create: `control_panel/deploy/sqlite-maintenance-pod.yaml`
- Modify: `control_panel/deploy/README.md`
- Modify: `control_panel/charts/control-panel/values.yaml`
- Modify: `control_panel/charts/control-panel/templates/deployment.yaml`
- Modify: `control_panel/charts/control-panel/README.md`

**Interfaces:**
- Raw deployment and Helm remain `replicas: 1`; the runtime image includes the SQLite CLI for online backup and an offline maintenance Pod procedure, while `.dockerignore` excludes `web-build/node_modules` from the Go build context. Expose explicit JWT TTL, Strict SameSite, trusted proxy and challenge rate/pending configuration.
- Document the current `ADMIN_INIT_PASSWORD` as the bootstrap/recovery secret, the state-safe SQLite backup/reset procedure, shared-key non-attribution, file distribution/rotation, HTTP passive/active threat boundaries, current/global logout and 30-second SSE revocation window.

- [ ] **Step 1: Add the runtime SQLite CLI and `.dockerignore`**; verify `sqlite3` exists in the Alpine image while `web-build/node_modules` is excluded from `docker build` context.
- [ ] **Step 2: Update Helm defaults and raw deployment env** to set the frozen values and limits; keep secret generation unchanged.
- [ ] **Step 3: Add the maintenance Pod manifest** for the shared `control-panel-data` PVC; keep the normal application deployment at one replica and document scale-down, consistent `.backup`, offline recovery SQL, cleanup, and restart steps.
- [ ] **Step 4: Update both deployment READMEs** to remove password-login/change-password claims and document bootstrap, private-key backup, rotation, logout choices, offline recovery, SQLite single-replica/version requirement, and HTTP risks.
- [ ] **Step 5: Run** `helm lint ./control_panel/charts/control-panel` and inspect rendered deployment values with `helm template`.

### Task 8: Run full regression and security-boundary verification

**Files:**
- Verify all modified Go, JS, HTML, Helm and documentation files.

- [ ] **Step 1: Run** `go test ./...` from `control_panel/backend`.
- [ ] **Step 2: Run** `go test -race ./internal/auth ./internal/db ./internal/api` when CGo and a C compiler are available; if unavailable, record that limitation and rely on the explicit 100-goroutine concurrency tests.
- [ ] **Step 3: Run separately** from `control_panel/backend/web-build`: `npm ci`, then `npm test`, then `npm run build` (stop if any command exits nonzero).
- [ ] **Step 4: Run** `go vet ./...` from `control_panel/backend`, `helm lint ./control_panel/charts/control-panel`, `helm template control-panel ./control_panel/charts/control-panel -n control-panel`, and `git diff --check`.
- [ ] **Step 5: Review the final diff** against the frozen spec, confirm no private key or token logging, and confirm the worktree contains no unrelated changes.
