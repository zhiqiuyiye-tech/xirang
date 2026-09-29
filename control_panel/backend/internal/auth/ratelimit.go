package auth

import (
	"container/list"
	"sync"
	"time"
)

const maxTrackedRateLimitEntries = 4096

type rateLimitEntry struct {
	failures    int
	firstFailAt time.Time
	lockedUntil time.Time
	lruElement  *list.Element
}

type requestRateEntry struct {
	windowStarted time.Time
	window        time.Duration
	requests      int
	lruElement    *list.Element
}

type RateLimiter struct {
	mu              sync.Mutex
	maxFailures     int
	lockoutDuration time.Duration
	window          time.Duration
	entries         map[string]*rateLimitEntry
	entriesLRU      list.List
	requestEntries  map[string]*requestRateEntry
	requestsLRU     list.List
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
		requestEntries:  make(map[string]*requestRateEntry),
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
	for key, entry := range rl.entries {
		// Entry has expired if not locked and window passed, or if lockout has passed.
		if (!entry.lockedUntil.IsZero() && now.After(entry.lockedUntil)) ||
			(entry.lockedUntil.IsZero() && now.Sub(entry.firstFailAt) > rl.window) {
			rl.removeFailureEntry(key)
		}
	}
	for key, entry := range rl.requestEntries {
		if now.Sub(entry.windowStarted) >= entry.window {
			rl.removeRequestEntry(key)
		}
	}
}

func (rl *RateLimiter) removeFailureEntry(key string) {
	entry, ok := rl.entries[key]
	if !ok {
		return
	}
	delete(rl.entries, key)
	if entry.lruElement != nil {
		rl.entriesLRU.Remove(entry.lruElement)
		entry.lruElement = nil
	}
}

func (rl *RateLimiter) addFailureEntry(key string, entry *rateLimitEntry) {
	if len(rl.entries) >= maxTrackedRateLimitEntries {
		if oldest := rl.entriesLRU.Back(); oldest != nil {
			rl.removeFailureEntry(oldest.Value.(string))
		}
	}
	entry.lruElement = rl.entriesLRU.PushFront(key)
	rl.entries[key] = entry
}

func (rl *RateLimiter) touchFailureEntry(entry *rateLimitEntry) {
	if entry.lruElement != nil {
		rl.entriesLRU.MoveToFront(entry.lruElement)
	}
}

func (rl *RateLimiter) removeRequestEntry(key string) {
	entry, ok := rl.requestEntries[key]
	if !ok {
		return
	}
	delete(rl.requestEntries, key)
	if entry.lruElement != nil {
		rl.requestsLRU.Remove(entry.lruElement)
		entry.lruElement = nil
	}
}

func (rl *RateLimiter) addRequestEntry(key string, entry *requestRateEntry) {
	if len(rl.requestEntries) >= maxTrackedRateLimitEntries {
		if oldest := rl.requestsLRU.Back(); oldest != nil {
			rl.removeRequestEntry(oldest.Value.(string))
		}
	}
	entry.lruElement = rl.requestsLRU.PushFront(key)
	rl.requestEntries[key] = entry
}

func (rl *RateLimiter) touchRequestEntry(entry *requestRateEntry) {
	if entry.lruElement != nil {
		rl.requestsLRU.MoveToFront(entry.lruElement)
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
	rl.touchFailureEntry(e)
	now := time.Now()
	if !e.lockedUntil.IsZero() {
		if now.Before(e.lockedUntil) {
			return true, e.lockedUntil.Sub(now)
		}
		// Lockout expired, reset
		rl.removeFailureEntry(key)
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
		rl.addFailureEntry(key, e)
		return false, 0
	}
	rl.touchFailureEntry(e)

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
	rl.removeFailureEntry(key)
}

// AllowRequest limits request creation by a caller-controlled source key. It
// keeps counters in process memory and never creates account-wide persisted
// lock state.
func (rl *RateLimiter) AllowRequest(key string, maxRequests int, window time.Duration) (bool, time.Duration) {
	if key == "" || maxRequests <= 0 || window <= 0 {
		return false, window
	}
	now := time.Now()
	rl.mu.Lock()
	defer rl.mu.Unlock()

	entry, ok := rl.requestEntries[key]
	if !ok {
		entry = &requestRateEntry{windowStarted: now, window: window, requests: 1}
		rl.addRequestEntry(key, entry)
		return true, 0
	}
	rl.touchRequestEntry(entry)
	if entry.window != window || now.Sub(entry.windowStarted) >= window {
		entry.windowStarted = now
		entry.window = window
		entry.requests = 1
		return true, 0
	}
	if entry.requests >= maxRequests {
		return false, window - now.Sub(entry.windowStarted)
	}
	entry.requests++
	return true, 0
}
