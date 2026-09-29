package db

import (
	"context"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
	"crypto/x509"
	"encoding/hex"
	"encoding/pem"
	"errors"
	"sync"
	"sync/atomic"
	"testing"
	"time"

	"golang.org/x/crypto/bcrypt"
)

func setBootstrapPasswordHash(t *testing.T, store *Store) string {
	t.Helper()
	hash, err := bcrypt.GenerateFromPassword([]byte("bootstrap-password-for-test"), bcrypt.MinCost)
	if err != nil {
		t.Fatal(err)
	}
	if err := store.UpsertAdminPassword(context.Background(), "admin", string(hash)); err != nil {
		t.Fatal(err)
	}
	return string(hash)
}

func testP256PublicKey(t *testing.T) (string, string) {
	t.Helper()
	privateKey, err := ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	if err != nil {
		t.Fatal(err)
	}
	der, err := x509.MarshalPKIXPublicKey(&privateKey.PublicKey)
	if err != nil {
		t.Fatal(err)
	}
	fingerprint := sha256.Sum256(der)
	return string(pem.EncodeToMemory(&pem.Block{Type: "PUBLIC KEY", Bytes: der})), hex.EncodeToString(fingerprint[:])
}

func TestValidateAdminAuthStateAcceptsPasswordBootstrap(t *testing.T) {
	store := newStore(t)
	setBootstrapPasswordHash(t, store)
	if err := store.ValidateAdminAuthState(context.Background()); err != nil {
		t.Fatalf("valid PASSWORD_BOOTSTRAP state rejected: %v", err)
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != AuthStatePasswordBootstrap || admin.PublicKeyPEM != nil || admin.PublicKeyFingerprint != nil {
		t.Fatalf("unexpected bootstrap admin state: %+v", admin)
	}
}

func TestValidateAdminAuthStateRejectsInconsistentTuples(t *testing.T) {
	publicKey, fingerprint := testP256PublicKey(t)
	validHash, err := bcrypt.GenerateFromPassword([]byte("bootstrap-password-for-test"), bcrypt.MinCost)
	if err != nil {
		t.Fatal(err)
	}
	cases := []struct {
		name        string
		state       string
		password    string
		publicKey   *string
		fingerprint *string
	}{
		{name: "bootstrap with public key", state: string(AuthStatePasswordBootstrap), password: string(validHash), publicKey: &publicKey, fingerprint: &fingerprint},
		{name: "active without public key", state: string(AuthStateKeyActive), password: disabledPasswordHash},
		{name: "active with bcrypt password", state: string(AuthStateKeyActive), password: string(validHash), publicKey: &publicKey, fingerprint: &fingerprint},
		{name: "active fingerprint mismatch", state: string(AuthStateKeyActive), password: disabledPasswordHash, publicKey: &publicKey, fingerprint: ptrStringForDBTest("00")},
		{name: "recovery pending must not serve", state: string(AuthStateRecoveryPending), password: pendingInitHash},
		{name: "unknown state", state: "LOCKED", password: string(validHash)},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			store := newStore(t)
			_, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=?, public_key_pem=?, public_key_fingerprint=? WHERE username='admin'`, tc.state, tc.password, tc.publicKey, tc.fingerprint)
			if err != nil {
				t.Fatal(err)
			}
			if err := store.ValidateAdminAuthState(context.Background()); err == nil {
				t.Fatal("inconsistent admin auth state was accepted")
			}
		})
	}
}

func TestValidateAdminAuthStateAcceptsKeyActive(t *testing.T) {
	store := newStore(t)
	publicKey, fingerprint := testP256PublicKey(t)
	if _, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=?, public_key_pem=?, public_key_fingerprint=? WHERE username='admin'`, AuthStateKeyActive, disabledPasswordHash, publicKey, fingerprint); err != nil {
		t.Fatal(err)
	}
	if err := store.ValidateAdminAuthState(context.Background()); err != nil {
		t.Fatalf("valid KEY_ACTIVE state rejected: %v", err)
	}
}

func TestBootstrapAdminKeyCASReturnsAndPersistsNewVersion(t *testing.T) {
	store := newStore(t)
	setBootstrapPasswordHash(t, store)
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	publicKey, fingerprint := testP256PublicKey(t)
	newVersion, err := store.BootstrapAdminKey(context.Background(), admin.AuthVersion, publicKey, fingerprint)
	if err != nil {
		t.Fatalf("BootstrapAdminKey() error = %v", err)
	}
	if newVersion != admin.AuthVersion+1 {
		t.Fatalf("new version = %d, want %d", newVersion, admin.AuthVersion+1)
	}
	stored, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if stored.AuthVersion != newVersion || stored.AuthState != AuthStateKeyActive || stored.PasswordHash != disabledPasswordHash || stored.PublicKeyPEM == nil || *stored.PublicKeyPEM != publicKey || stored.PublicKeyFingerprint == nil || *stored.PublicKeyFingerprint != fingerprint {
		t.Fatalf("unexpected bootstrapped admin: %+v", stored)
	}
	if _, err := store.BootstrapAdminKey(context.Background(), admin.AuthVersion, publicKey, fingerprint); err == nil {
		t.Fatal("stale bootstrap CAS succeeded")
	}
}

func TestRotateAdminKeyCASReturnsNewVersion(t *testing.T) {
	store := newStore(t)
	currentKey, currentFingerprint := testP256PublicKey(t)
	newKey, newFingerprint := testP256PublicKey(t)
	_, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=?, public_key_pem=?, public_key_fingerprint=? WHERE username='admin'`, AuthStateKeyActive, disabledPasswordHash, currentKey, currentFingerprint)
	if err != nil {
		t.Fatal(err)
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	newVersion, err := store.RotateAdminKey(context.Background(), admin.AuthVersion, currentFingerprint, newKey, newFingerprint)
	if err != nil {
		t.Fatalf("RotateAdminKey() error = %v", err)
	}
	if newVersion != admin.AuthVersion+1 {
		t.Fatalf("new version = %d, want %d", newVersion, admin.AuthVersion+1)
	}
	if _, err := store.RotateAdminKey(context.Background(), admin.AuthVersion, currentFingerprint, currentKey, currentFingerprint); err == nil {
		t.Fatal("stale rotation CAS succeeded")
	}
}

func TestInitializeAdminAuthSeedsNewDatabase(t *testing.T) {
	store := newStore(t)
	hash, err := bcrypt.GenerateFromPassword([]byte("new-admin-bootstrap"), bcrypt.MinCost)
	if err != nil {
		t.Fatal(err)
	}
	if err := store.InitializeAdminAuth(context.Background(), string(hash)); err != nil {
		t.Fatalf("InitializeAdminAuth() error = %v", err)
	}
	if err := store.ValidateAdminAuthState(context.Background()); err != nil {
		t.Fatalf("seeded bootstrap state invalid: %v", err)
	}
	admin, err := store.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if admin.AuthState != AuthStatePasswordBootstrap || admin.PasswordHash != string(hash) {
		t.Fatalf("unexpected seeded admin: %+v", admin)
	}
}

func TestInitializeAdminAuthCompletesRecoveryAndAudits(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	challenge := testAuthChallenge("stale-recovery-challenge", "10.0.0.5", time.Now().UTC())
	if err := store.CreateAuthChallenge(ctx, challenge, 5, 100); err != nil {
		t.Fatal(err)
	}
	if _, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=?, public_key_pem=NULL, public_key_fingerprint=NULL, auth_version=auth_version+1 WHERE username='admin'`, AuthStateRecoveryPending, pendingInitHash); err != nil {
		t.Fatal(err)
	}
	adminBefore, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	hash, err := bcrypt.GenerateFromPassword([]byte("recovered-admin-bootstrap"), bcrypt.MinCost)
	if err != nil {
		t.Fatal(err)
	}
	if err := store.InitializeAdminAuth(ctx, string(hash)); err != nil {
		t.Fatalf("InitializeAdminAuth() recovery error = %v", err)
	}
	if err := store.ValidateAdminAuthState(ctx); err != nil {
		t.Fatalf("recovered bootstrap state invalid: %v", err)
	}
	adminAfter, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	if adminAfter.AuthVersion != adminBefore.AuthVersion || adminAfter.PasswordHash != string(hash) {
		t.Fatalf("recovery changed unexpected fields: before=%+v after=%+v", adminBefore, adminAfter)
	}
	var challenges int
	if err := store.db.QueryRow("SELECT COUNT(*) FROM auth_challenges").Scan(&challenges); err != nil {
		t.Fatal(err)
	}
	if challenges != 0 {
		t.Fatalf("recovery left %d stale challenges", challenges)
	}
	audits, err := store.ListAudit(ctx, 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(audits) != 1 || audits[0].Action != "auth.recovery_bootstrap" || audits[0].Result != "success" {
		t.Fatalf("unexpected recovery audit entries: %+v", audits)
	}
}

func TestInitializeAdminAuthRejectsInvalidStateTuple(t *testing.T) {
	store := newStore(t)
	hash, err := bcrypt.GenerateFromPassword([]byte("valid-test-password"), bcrypt.MinCost)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=? WHERE username='admin'`, AuthStateKeyActive, pendingInitHash); err != nil {
		t.Fatal(err)
	}
	if err := store.InitializeAdminAuth(context.Background(), string(hash)); err == nil {
		t.Fatal("inconsistent KEY_ACTIVE state must not be reseeded")
	}
}

func TestConcurrentBootstrapAdminKeyCASOnlyOneSucceeds(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	setBootstrapPasswordHash(t, store)
	admin, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	firstKey, firstFingerprint := testP256PublicKey(t)
	secondKey, secondFingerprint := testP256PublicKey(t)
	type result struct {
		version int64
		err     error
		fp      string
	}
	results := make(chan result, 2)
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		version, err := store.BootstrapAdminKey(ctx, admin.AuthVersion, firstKey, firstFingerprint)
		results <- result{version: version, err: err, fp: firstFingerprint}
	}()
	go func() {
		defer wg.Done()
		version, err := store.BootstrapAdminKey(ctx, admin.AuthVersion, secondKey, secondFingerprint)
		results <- result{version: version, err: err, fp: secondFingerprint}
	}()
	wg.Wait()
	close(results)
	var successes, conflicts atomic.Int32
	var winner result
	for res := range results {
		if res.err == nil {
			successes.Add(1)
			winner = res
		} else if errors.Is(res.err, ErrAuthStateConflict) {
			conflicts.Add(1)
		} else {
			t.Fatalf("unexpected bootstrap error: %v", res.err)
		}
	}
	if successes.Load() != 1 || conflicts.Load() != 1 {
		t.Fatalf("bootstrap successes=%d conflicts=%d, want one each", successes.Load(), conflicts.Load())
	}
	stored, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	if stored.AuthVersion != admin.AuthVersion+1 || stored.AuthState != AuthStateKeyActive || stored.PublicKeyFingerprint == nil || *stored.PublicKeyFingerprint != winner.fp || winner.version != stored.AuthVersion {
		t.Fatalf("bootstrap CAS winner/version mismatch: winner=%+v stored=%+v", winner, stored)
	}
}

func TestConcurrentRotateAdminKeyCASOnlyOneSucceeds(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	currentKey, currentFingerprint := testP256PublicKey(t)
	firstNewKey, firstNewFingerprint := testP256PublicKey(t)
	secondNewKey, secondNewFingerprint := testP256PublicKey(t)
	if _, err := store.db.Exec(`UPDATE admin SET auth_state=?, password_hash=?, public_key_pem=?, public_key_fingerprint=? WHERE username='admin'`, AuthStateKeyActive, disabledPasswordHash, currentKey, currentFingerprint); err != nil {
		t.Fatal(err)
	}
	admin, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	type result struct {
		version int64
		err     error
		fp      string
	}
	results := make(chan result, 2)
	var wg sync.WaitGroup
	wg.Add(2)
	go func() {
		defer wg.Done()
		version, err := store.RotateAdminKey(ctx, admin.AuthVersion, currentFingerprint, firstNewKey, firstNewFingerprint)
		results <- result{version: version, err: err, fp: firstNewFingerprint}
	}()
	go func() {
		defer wg.Done()
		version, err := store.RotateAdminKey(ctx, admin.AuthVersion, currentFingerprint, secondNewKey, secondNewFingerprint)
		results <- result{version: version, err: err, fp: secondNewFingerprint}
	}()
	wg.Wait()
	close(results)
	var successes, conflicts atomic.Int32
	var winner result
	for res := range results {
		if res.err == nil {
			successes.Add(1)
			winner = res
		} else if errors.Is(res.err, ErrAuthStateConflict) {
			conflicts.Add(1)
		} else {
			t.Fatalf("unexpected rotation error: %v", res.err)
		}
	}
	if successes.Load() != 1 || conflicts.Load() != 1 {
		t.Fatalf("rotation successes=%d conflicts=%d, want one each", successes.Load(), conflicts.Load())
	}
	stored, err := store.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	if stored.AuthVersion != admin.AuthVersion+1 || stored.PublicKeyFingerprint == nil || *stored.PublicKeyFingerprint != winner.fp || winner.version != stored.AuthVersion {
		t.Fatalf("CAS winner/version mismatch: winner=%+v stored=%+v", winner, stored)
	}
}

func ptrStringForDBTest(value string) *string { return &value }
