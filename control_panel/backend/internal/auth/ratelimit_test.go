package auth

import (
	"testing"
	"time"
)

func TestRateLimiter_LockoutAndSuccessReset(t *testing.T) {
	rl := NewRateLimiter(3, 100*time.Millisecond, 200*time.Millisecond)
	defer rl.Close()

	key := "admin:192.168.1.100"

	// 1st failure -> not locked
	locked, _ := rl.RecordFailure(key)
	if locked {
		t.Fatal("should not be locked after 1 failure")
	}

	// 2nd failure -> not locked
	locked, _ = rl.RecordFailure(key)
	if locked {
		t.Fatal("should not be locked after 2 failures")
	}

	// 3rd failure -> locked!
	locked, dur := rl.RecordFailure(key)
	if !locked || dur <= 0 {
		t.Fatalf("expected locked after 3 failures, got locked=%v dur=%v", locked, dur)
	}

	// Check should report locked
	isLocked, remaining := rl.Check(key)
	if !isLocked || remaining <= 0 {
		t.Fatalf("Check: expected locked, got %v", isLocked)
	}

	// Wait for lockout to expire
	time.Sleep(120 * time.Millisecond)
	isLocked, _ = rl.Check(key)
	if isLocked {
		t.Fatal("expected lockout to have expired")
	}

	// Record success resets everything
	rl.RecordFailure(key)
	rl.RecordSuccess(key)
	isLocked, _ = rl.Check(key)
	if isLocked {
		t.Fatal("should not be locked after RecordSuccess")
	}
}
