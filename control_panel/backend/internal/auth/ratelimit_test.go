package auth

import (
	"strconv"
	"testing"
	"time"
)

func TestRateLimiter_SourceRequestLimitIsIndependentAndExpires(t *testing.T) {
	rl := NewRateLimiter(3, 100*time.Millisecond, 200*time.Millisecond)
	defer rl.Close()

	for i := 0; i < 2; i++ {
		allowed, _ := rl.AllowRequest("10.0.0.1", 2, 40*time.Millisecond)
		if !allowed {
			t.Fatalf("request %d from first source unexpectedly denied", i+1)
		}
	}
	allowed, retryAfter := rl.AllowRequest("10.0.0.1", 2, 40*time.Millisecond)
	if allowed || retryAfter <= 0 {
		t.Fatalf("third request from first source: allowed=%v retryAfter=%v", allowed, retryAfter)
	}
	allowed, _ = rl.AllowRequest("10.0.0.2", 2, 40*time.Millisecond)
	if !allowed {
		t.Fatal("rate limiting one source must not block another source")
	}
	time.Sleep(50 * time.Millisecond)
	allowed, _ = rl.AllowRequest("10.0.0.1", 2, 40*time.Millisecond)
	if !allowed {
		t.Fatal("source limit did not expire with its fixed window")
	}
}

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

func TestRateLimiter_BoundsBothSourceMapsAndEvictsOldEntries(t *testing.T) {
	// The fixed 4096-source ceiling bounds memory. Eviction intentionally
	// trades protection for forgotten inactive sources: a source whose entry
	// was evicted starts with a fresh failure/request window when it returns.
	const maxTrackedSources = maxTrackedRateLimitEntries

	rl := NewRateLimiter(5, time.Minute, 15*time.Minute)
	defer rl.Close()

	for i := 0; i <= maxTrackedSources; i++ {
		suffix := strconv.Itoa(i)
		rl.RecordFailure("proof-source-" + suffix)
		if allowed, _ := rl.AllowRequest("challenge-source-"+suffix, 1, time.Minute); !allowed {
			t.Fatalf("first request for source %s was unexpectedly denied", suffix)
		}
	}

	rl.mu.Lock()
	proofCount := len(rl.entries)
	requestCount := len(rl.requestEntries)
	_, oldestProofRetained := rl.entries["proof-source-0"]
	_, oldestRequestRetained := rl.requestEntries["challenge-source-0"]
	rl.mu.Unlock()

	if proofCount > maxTrackedSources || requestCount > maxTrackedSources {
		t.Fatalf("source maps exceeded fixed capacity: proof=%d requests=%d limit=%d", proofCount, requestCount, maxTrackedSources)
	}
	if oldestProofRetained || oldestRequestRetained {
		t.Fatalf("least-recently-used source entries were not evicted: proof=%v requests=%v", oldestProofRetained, oldestRequestRetained)
	}
}
