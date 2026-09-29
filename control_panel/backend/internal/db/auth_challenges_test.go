package db

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

func testAuthChallenge(id, clientIP string, now time.Time) AuthChallenge {
	return AuthChallenge{
		ChallengeID:    id,
		Nonce:          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
		Purpose:        AuthChallengeLogin,
		AuthVersion:    7,
		KeyFingerprint: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
		ClientIP:       clientIP,
		CreatedAt:      now,
		ExpiresAt:      now.Add(2 * time.Minute),
	}
}

func TestCreateAndConsumeAuthChallengeOnce(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	now := time.Now().UTC().Truncate(time.Microsecond)
	challenge := testAuthChallenge("challenge-one", "10.0.0.1", now)
	if err := store.CreateAuthChallenge(ctx, challenge, 5, 100); err != nil {
		t.Fatalf("CreateAuthChallenge() error = %v", err)
	}

	consumed, err := store.ConsumeAuthChallenge(ctx, challenge.ChallengeID, AuthChallengeLogin, now.Add(time.Second))
	if err != nil {
		t.Fatalf("ConsumeAuthChallenge() error = %v", err)
	}
	if consumed.ChallengeID != challenge.ChallengeID || consumed.Nonce != challenge.Nonce || consumed.AuthVersion != challenge.AuthVersion || consumed.KeyFingerprint != challenge.KeyFingerprint || consumed.ClientIP != challenge.ClientIP || consumed.ConsumedAt == nil {
		t.Fatalf("unexpected consumed challenge: %+v", consumed)
	}
	if _, err := store.ConsumeAuthChallenge(ctx, challenge.ChallengeID, AuthChallengeLogin, now.Add(2*time.Second)); !errors.Is(err, ErrChallengeUnavailable) {
		t.Fatalf("second consume error = %v, want ErrChallengeUnavailable", err)
	}
}

func TestConsumeAuthChallengeRequiresPurposeAndUnexpiredTime(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	now := time.Now().UTC()
	challenge := testAuthChallenge("challenge-expiry", "10.0.0.2", now)
	if err := store.CreateAuthChallenge(ctx, challenge, 5, 100); err != nil {
		t.Fatal(err)
	}
	if _, err := store.ConsumeAuthChallenge(ctx, challenge.ChallengeID, AuthChallengeBootstrap, now.Add(time.Second)); !errors.Is(err, ErrChallengeUnavailable) {
		t.Fatalf("wrong-purpose consume error = %v, want ErrChallengeUnavailable", err)
	}
	if _, err := store.ConsumeAuthChallenge(ctx, challenge.ChallengeID, AuthChallengeLogin, challenge.ExpiresAt); !errors.Is(err, ErrChallengeUnavailable) {
		t.Fatalf("expired consume error = %v, want ErrChallengeUnavailable", err)
	}
}

func TestCreateAuthChallengeEnforcesGlobalPendingLimit(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	now := time.Now().UTC()
	for i := 0; i < 3; i++ {
		challenge := testAuthChallenge(fmt.Sprintf("global-%d", i), fmt.Sprintf("10.0.1.%d", i+1), now)
		if err := store.CreateAuthChallenge(ctx, challenge, 10, 3); err != nil {
			t.Fatalf("create challenge %d: %v", i, err)
		}
	}
	extra := testAuthChallenge("global-overflow", "10.0.1.9", now)
	if err := store.CreateAuthChallenge(ctx, extra, 10, 3); !errors.Is(err, ErrChallengeLimitExceeded) {
		t.Fatalf("global overflow error = %v, want ErrChallengeLimitExceeded", err)
	}
}

func TestCreateAuthChallengePendingLimitsAreAtomic(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	now := time.Now().UTC()
	const workers = 100
	const pendingPerIP = 5
	var accepted atomic.Int32
	var rejected atomic.Int32
	var unexpected atomic.Int32
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			challenge := testAuthChallenge(fmt.Sprintf("challenge-%03d", i), "10.0.0.3", now)
			err := store.CreateAuthChallenge(ctx, challenge, pendingPerIP, 1000)
			switch {
			case err == nil:
				accepted.Add(1)
			case errors.Is(err, ErrChallengeLimitExceeded):
				rejected.Add(1)
			default:
				unexpected.Add(1)
			}
		}(i)
	}
	wg.Wait()
	if unexpected.Load() != 0 {
		t.Fatalf("unexpected challenge creation errors: %d", unexpected.Load())
	}
	if accepted.Load() != pendingPerIP || rejected.Load() != workers-pendingPerIP {
		t.Fatalf("accepted=%d rejected=%d, want accepted=%d rejected=%d", accepted.Load(), rejected.Load(), pendingPerIP, workers-pendingPerIP)
	}
	var pending int
	if err := store.db.QueryRow(`SELECT COUNT(*) FROM auth_challenges WHERE client_ip=? AND consumed_at IS NULL AND expires_at>?`, "10.0.0.3", now).Scan(&pending); err != nil {
		t.Fatal(err)
	}
	if pending != pendingPerIP {
		t.Fatalf("pending challenges = %d, want %d", pending, pendingPerIP)
	}
}

func TestConsumeAuthChallengeConcurrentRequestsOnlyOneSucceeds(t *testing.T) {
	store := newStore(t)
	ctx := context.Background()
	now := time.Now().UTC()
	challenge := testAuthChallenge("concurrent-consume", "10.0.0.4", now)
	if err := store.CreateAuthChallenge(ctx, challenge, 5, 100); err != nil {
		t.Fatal(err)
	}

	const callers = 100
	var succeeded atomic.Int32
	var unavailable atomic.Int32
	var unexpected atomic.Int32
	var wg sync.WaitGroup
	for i := 0; i < callers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			_, err := store.ConsumeAuthChallenge(ctx, challenge.ChallengeID, AuthChallengeLogin, now.Add(time.Second))
			switch {
			case err == nil:
				succeeded.Add(1)
			case errors.Is(err, ErrChallengeUnavailable):
				unavailable.Add(1)
			default:
				unexpected.Add(1)
			}
		}()
	}
	wg.Wait()
	if succeeded.Load() != 1 || unavailable.Load() != callers-1 || unexpected.Load() != 0 {
		t.Fatalf("success=%d unavailable=%d unexpected=%d", succeeded.Load(), unavailable.Load(), unexpected.Load())
	}
}
