package auth

import (
	"sync"
	"time"
)

type rateLimitEntry struct {
	failures    int
	firstFailAt time.Time
	lockedUntil time.Time
}

type RateLimiter struct {
	mu              sync.Mutex
	maxFailures     int
	lockoutDuration time.Duration
	window          time.Duration
	entries         map[string]*rateLimitEntry
	stopCh          chan struct{}
	stopOnce        sync.Once
}

func NewRateLimiter(maxFailures int, lockoutDuration, window time.Duration) *RateLimiter {
	if maxFailures <= 0 {
		maxFailures = 5
	}
	if lockoutDuration <= 0 {
		lockoutDuration = 15 * time.Minute
	}
	if window <= 0 {
		window = 15 * time.Minute
	}
	rl := &RateLimiter{
		maxFailures:     maxFailures,
		lockoutDuration: lockoutDuration,
		window:          window,
		entries:         make(map[string]*rateLimitEntry),
		stopCh:          make(chan struct{}),
	}
	go rl.cleanupLoop()
	return rl
}

func (rl *RateLimiter) Close() {
	rl.stopOnce.Do(func() {
		close(rl.stopCh)
	})
}

func (rl *RateLimiter) cleanupLoop() {
	ticker := time.NewTicker(5 * time.Minute)
	defer ticker.Stop()
	for {
		select {
		case <-rl.stopCh:
			return
		case now := <-ticker.C:
			rl.cleanup(now)
		}
	}
}

func (rl *RateLimiter) cleanup(now time.Time) {
	rl.mu.Lock()
	defer rl.mu.Unlock()
	for k, e := range rl.entries {
		// Entry has expired if not locked and window passed, or if lockout has passed
		if !e.lockedUntil.IsZero() {
			if now.After(e.lockedUntil) {
				delete(rl.entries, k)
			}
		} else if now.Sub(e.firstFailAt) > rl.window {
			delete(rl.entries, k)
		}
	}
}

// Check checks whether the key is currently locked out.
func (rl *RateLimiter) Check(key string) (bool, time.Duration) {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	e, ok := rl.entries[key]
	if !ok {
		return false, 0
	}
	now := time.Now()
	if !e.lockedUntil.IsZero() {
		if now.Before(e.lockedUntil) {
			return true, e.lockedUntil.Sub(now)
		}
		// Lockout expired, reset
		delete(rl.entries, key)
		return false, 0
	}
	return false, 0
}

// RecordFailure records a failed login attempt. Returns whether the key is now locked out.
func (rl *RateLimiter) RecordFailure(key string) (bool, time.Duration) {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	now := time.Now()
	e, ok := rl.entries[key]
	if !ok {
		e = &rateLimitEntry{
			failures:    1,
			firstFailAt: now,
		}
		rl.entries[key] = e
		return false, 0
	}

	// Check if already locked
	if !e.lockedUntil.IsZero() {
		if now.Before(e.lockedUntil) {
			return true, e.lockedUntil.Sub(now)
		}
		// Previous lockout expired, reset with 1 failure
		e.failures = 1
		e.firstFailAt = now
		e.lockedUntil = time.Time{}
		return false, 0
	}

	// If window expired since first failure, reset counter
	if now.Sub(e.firstFailAt) > rl.window {
		e.failures = 1
		e.firstFailAt = now
		return false, 0
	}

	e.failures++
	if e.failures >= rl.maxFailures {
		e.lockedUntil = now.Add(rl.lockoutDuration)
		return true, rl.lockoutDuration
	}

	return false, 0
}

// RecordSuccess clears any failure records for the key upon successful login.
func (rl *RateLimiter) RecordSuccess(key string) {
	rl.mu.Lock()
	defer rl.mu.Unlock()
	delete(rl.entries, key)
}
