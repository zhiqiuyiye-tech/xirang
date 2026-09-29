package api

import (
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"net/http"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

const unauthenticatedFailureAuditLimit = 60
const unauthenticatedFailureAuditWindow = time.Minute

type unauthenticatedFailureAuditBudget struct {
	mu          sync.Mutex
	windowStart time.Time
	writes      int
}

func (budget *unauthenticatedFailureAuditBudget) allow() bool {
	budget.mu.Lock()
	defer budget.mu.Unlock()

	now := time.Now()
	if budget.windowStart.IsZero() || now.Sub(budget.windowStart) >= unauthenticatedFailureAuditWindow {
		budget.windowStart = now
		budget.writes = 0
	}
	if budget.writes >= unauthenticatedFailureAuditLimit {
		return false
	}
	budget.writes++
	return true
}

type AuthHandlerConfig struct {
	Store                       *db.Store
	Tokens                      *auth.Tokens
	Limiter                     *auth.RateLimiter
	CookieName                  string
	CookieSecure                bool
	CookieSameSite              string
	CSRFCookieName              string
	TokenTTL                    time.Duration
	ChallengeRateLimitPerMinute int
	ChallengeMaxPendingPerIP    int
	ChallengeMaxPendingGlobal   int
}

type authHandlers struct {
	store                       *db.Store
	tk                          *auth.Tokens
	limiter                     *auth.RateLimiter
	cookieName                  string
	cookieSecure                bool
	cookieSameSite              string
	csrfCookieName              string
	tokenTTL                    time.Duration
	challengeRateLimitPerMinute int
	challengeMaxPendingPerIP    int
	challengeMaxPendingGlobal   int
	failureAuditBudget          *unauthenticatedFailureAuditBudget
}

func newAuthHandlers(cfg AuthHandlerConfig) *authHandlers {
	cName := cfg.CookieName
	if cName == "" {
		cName = "cp_session"
	}
	csrfName := cfg.CSRFCookieName
	if csrfName == "" {
		csrfName = "cp_csrf"
	}
	ttl := cfg.TokenTTL
	if ttl <= 0 {
		ttl = 30 * time.Minute
	}
	sameSite := cfg.CookieSameSite
	if sameSite == "" {
		sameSite = "Strict"
	}
	challengeRateLimit := cfg.ChallengeRateLimitPerMinute
	if challengeRateLimit <= 0 {
		challengeRateLimit = 10
	}
	challengePendingPerIP := cfg.ChallengeMaxPendingPerIP
	if challengePendingPerIP <= 0 {
		challengePendingPerIP = 5
	}
	challengePendingGlobal := cfg.ChallengeMaxPendingGlobal
	if challengePendingGlobal <= 0 {
		challengePendingGlobal = 1000
	}

	return &authHandlers{
		store:                       cfg.Store,
		tk:                          cfg.Tokens,
		limiter:                     cfg.Limiter,
		cookieName:                  cName,
		cookieSecure:                cfg.CookieSecure,
		cookieSameSite:              sameSite,
		csrfCookieName:              csrfName,
		tokenTTL:                    ttl,
		challengeRateLimitPerMinute: challengeRateLimit,
		challengeMaxPendingPerIP:    challengePendingPerIP,
		challengeMaxPendingGlobal:   challengePendingGlobal,
		failureAuditBudget:          &unauthenticatedFailureAuditBudget{},
	}
}

func parseSameSite(s string) http.SameSite {
	switch strings.ToLower(s) {
	case "strict":
		return http.SameSiteStrictMode
	case "none":
		return http.SameSiteNoneMode
	default:
		return http.SameSiteLaxMode
	}
}

func generateRandomToken(n int) (string, error) {
	b := make([]byte, n)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}

func generateRandomBase64URL(n int) (string, error) {
	b := make([]byte, n)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return base64.RawURLEncoding.EncodeToString(b), nil
}

func bindAuthJSON(c *gin.Context, target any) bool {
	c.Request.Body = http.MaxBytesReader(c.Writer, c.Request.Body, 8*1024)
	if err := c.ShouldBindJSON(target); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "invalid authentication request"})
		return false
	}
	return true
}

func (h *authHandlers) auditAuthFailure(c *gin.Context, action, result string) {
	if h.failureAuditBudget == nil || !h.failureAuditBudget.allow() {
		return
	}
	// Failure audits use fixed metadata only; request passwords, keys, nonces,
	// and signatures are never passed to persistent storage.
	_ = h.store.InsertAudit(c, db.AuditLog{Actor: "admin", Action: action, Result: result})
}

func (h *authHandlers) allowChallengeCreation(c *gin.Context) bool {
	if h.limiter == nil {
		return true
	}
	allowed, retryAfter := h.limiter.AllowRequest("challenge:"+c.ClientIP(), h.challengeRateLimitPerMinute, time.Minute)
	if allowed {
		return true
	}
	seconds := int(retryAfter.Seconds()) + 1
	c.Header("Retry-After", strconv.Itoa(seconds))
	c.Header("Cache-Control", "no-store")
	h.auditAuthFailure(c, "auth.challenge_rate_limited", "blocked")
	c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many authentication requests"})
	return false
}

func (h *authHandlers) setSessionCookies(c *gin.Context, token string) error {
	csrfToken, err := generateRandomToken(32)
	if err != nil {
		return err
	}
	c.SetSameSite(parseSameSite(h.cookieSameSite))
	c.SetCookie(h.cookieName, token, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, true)
	c.SetCookie(h.csrfCookieName, csrfToken, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, false)
	return nil
}

func (h *authHandlers) clearSessionCookies(c *gin.Context) {
	c.SetSameSite(parseSameSite(h.cookieSameSite))
	c.SetCookie(h.cookieName, "", -1, "/", "", h.cookieSecure, true)
	c.SetCookie(h.csrfCookieName, "", -1, "/", "", h.cookieSecure, false)
}

func (h *authHandlers) status(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	admin, err := h.store.GetAdminByUsername(c, "admin")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "authentication status unavailable"})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"auth_state":      admin.AuthState,
		"key_fingerprint": admin.PublicKeyFingerprint,
	})
}

func (h *authHandlers) checkAuthSourceLocked(c *gin.Context) bool {
	if h.limiter == nil {
		return false
	}
	locked, remaining := h.limiter.Check("auth:" + c.ClientIP())
	if !locked {
		return false
	}
	c.Header("Retry-After", strconv.Itoa(int(remaining.Seconds())+1))
	c.Header("Cache-Control", "no-store")
	c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many failed authentication attempts"})
	return true
}

func (h *authHandlers) rejectAuthAttempt(c *gin.Context, action, result string) {
	h.auditAuthFailure(c, action, result)
	if h.limiter != nil {
		if locked, remaining := h.limiter.RecordFailure("auth:" + c.ClientIP()); locked {
			c.Header("Retry-After", strconv.Itoa(int(remaining.Seconds())+1))
			c.Header("Cache-Control", "no-store")
			c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many failed authentication attempts"})
			return
		}
	}
	c.Header("Cache-Control", "no-store")
	c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid authentication proof"})
}

func (h *authHandlers) me(c *gin.Context) {
	cl, ok := auth.ClaimsFrom(c)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"id":           cl.AdminID,
		"username":     cl.Username,
		"auth_version": cl.AuthVersion,
	})
}

func (h *authHandlers) logout(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	cl, ok := auth.ClaimsFrom(c)
	if ok {
		_ = h.store.InsertAudit(c, db.AuditLog{
			Actor:  cl.Username,
			Action: "auth.logout_current",
			Target: &cl.Username,
			Result: "success",
		})
	}
	h.clearSessionCookies(c)
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

func (h *authHandlers) logoutAll(c *gin.Context) {
	c.Header("Cache-Control", "no-store")
	cl, ok := auth.ClaimsFrom(c)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}
	if _, err := h.store.RevokeAdminSessions(c, cl.Username); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "could not revoke sessions"})
		return
	}
	_ = h.store.InsertAudit(c, db.AuditLog{
		Actor:  cl.Username,
		Action: "auth.logout_all",
		Target: &cl.Username,
		Result: "success",
	})
	h.clearSessionCookies(c)
	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}
