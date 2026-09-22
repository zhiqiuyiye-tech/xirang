package api

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/crypto/bcrypt"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

// dummyBcryptHash is a precomputed bcrypt hash of a random placeholder
// string. When the username does not exist, CheckPassword still burns one
// bcrypt comparison against it so the "unknown user" and "wrong password"
// paths take the same time - otherwise response latency difference would let
// an attacker enumerate valid usernames.
const dummyBcryptHash = "$2a$10$mrJ4Z8L0aAN5BUrf6QSqp.rjEGBVlYsrju0FGe/RL7JYURXBVBivC"

type AuthHandlerConfig struct {
	Store          *db.Store
	Tokens         *auth.Tokens
	Limiter        *auth.RateLimiter
	CookieName     string
	CookieSecure   bool
	CookieSameSite string
	CSRFCookieName string
	TokenTTL       time.Duration
}

type authHandlers struct {
	store          *db.Store
	tk             *auth.Tokens
	limiter        *auth.RateLimiter
	cookieName     string
	cookieSecure   bool
	cookieSameSite string
	csrfCookieName string
	tokenTTL       time.Duration
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
		ttl = 4 * time.Hour
	}
	sameSite := cfg.CookieSameSite
	if sameSite == "" {
		sameSite = "Lax"
	}

	return &authHandlers{
		store:          cfg.Store,
		tk:             cfg.Tokens,
		limiter:        cfg.Limiter,
		cookieName:     cName,
		cookieSecure:   cfg.CookieSecure,
		cookieSameSite: sameSite,
		csrfCookieName: csrfName,
		tokenTTL:       ttl,
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

func (h *authHandlers) login(c *gin.Context) {
	var req struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	normUser := strings.TrimSpace(strings.ToLower(req.Username))
	rateLimitKey := normUser + ":" + c.ClientIP()

	// Check rate limit
	if h.limiter != nil {
		if locked, remaining := h.limiter.Check(rateLimitKey); locked {
			_ = h.store.InsertAudit(c, db.AuditLog{
				Actor:  req.Username,
				Action: "auth.login_rate_limited",
				Target: &req.Username,
				Result: "blocked",
			})
			c.Header("Retry-After", strconv.Itoa(int(remaining.Seconds())+1))
			c.JSON(http.StatusTooManyRequests, gin.H{
				"error": fmt.Sprintf("too many failed login attempts, please try again in %d seconds", int(remaining.Seconds())+1),
			})
			return
		}
	}

	a, err := h.store.GetAdminByUsername(c, req.Username)
	if err != nil {
		// Timing equalizer
		_ = bcrypt.CompareHashAndPassword([]byte(dummyBcryptHash), []byte(req.Password))
		if h.limiter != nil {
			if locked, dur := h.limiter.RecordFailure(rateLimitKey); locked {
				c.Header("Retry-After", strconv.Itoa(int(dur.Seconds())+1))
				c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many failed login attempts, account temporarily locked"})
				return
			}
		}
		_ = h.store.InsertAudit(c, db.AuditLog{Actor: req.Username, Action: "auth.login", Target: &req.Username, Result: "failed"})
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
		return
	}

	if !auth.CheckPassword(a.PasswordHash, req.Password) {
		if h.limiter != nil {
			if locked, dur := h.limiter.RecordFailure(rateLimitKey); locked {
				c.Header("Retry-After", strconv.Itoa(int(dur.Seconds())+1))
				c.JSON(http.StatusTooManyRequests, gin.H{"error": "too many failed login attempts, account temporarily locked"})
				return
			}
		}
		_ = h.store.InsertAudit(c, db.AuditLog{Actor: req.Username, Action: "auth.login", Target: &req.Username, Result: "failed"})
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
		return
	}

	if h.limiter != nil {
		h.limiter.RecordSuccess(rateLimitKey)
	}

	tok, err := h.tk.Issue(a.ID, a.Username, a.AuthVersion)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Set HttpOnly session cookie
	c.SetSameSite(parseSameSite(h.cookieSameSite))
	c.SetCookie(h.cookieName, tok, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, true)

	// Set CSRF cookie readable by frontend scripts
	csrfToken, _ := generateRandomToken(32)
	c.SetCookie(h.csrfCookieName, csrfToken, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, false)

	_ = h.store.InsertAudit(c, db.AuditLog{Actor: a.Username, Action: "auth.login", Target: &req.Username, Result: "success"})
	c.JSON(http.StatusOK, gin.H{
		"token":      tok,
		"csrf_token": csrfToken,
	})
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

func (h *authHandlers) changePassword(c *gin.Context) {
	cl, ok := auth.ClaimsFrom(c)
	if !ok {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "unauthorized"})
		return
	}

	var req struct {
		OldPassword string `json:"old_password"`
		NewPassword string `json:"new_password"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	if len(req.NewPassword) < 12 || len(req.NewPassword) > 72 {
		c.JSON(http.StatusBadRequest, gin.H{"error": "new password must be between 12 and 72 characters"})
		return
	}

	a, err := h.store.GetAdminByUsername(c, cl.Username)
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "admin not found"})
		return
	}

	if !auth.CheckPassword(a.PasswordHash, req.OldPassword) {
		_ = h.store.InsertAudit(c, db.AuditLog{
			Actor:  cl.Username,
			Action: "auth.change_password",
			Target: &cl.Username,
			Result: "failed",
		})
		c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid old password"})
		return
	}

	newHash, err := auth.HashPassword(req.NewPassword)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	newVer, err := h.store.UpdateAdminPasswordAndBumpVersion(c, cl.Username, newHash)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	newTok, err := h.tk.Issue(a.ID, a.Username, newVer)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	// Update session cookie with new token
	c.SetSameSite(parseSameSite(h.cookieSameSite))
	c.SetCookie(h.cookieName, newTok, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, true)

	// Refresh CSRF cookie
	csrfToken, _ := generateRandomToken(32)
	c.SetCookie(h.csrfCookieName, csrfToken, int(h.tokenTTL.Seconds()), "/", "", h.cookieSecure, false)

	_ = h.store.InsertAudit(c, db.AuditLog{
		Actor:  cl.Username,
		Action: "auth.change_password",
		Target: &cl.Username,
		Result: "success",
	})

	c.JSON(http.StatusOK, gin.H{
		"status":     "ok",
		"token":      newTok,
		"csrf_token": csrfToken,
	})
}

func (h *authHandlers) logout(c *gin.Context) {
	cl, ok := auth.ClaimsFrom(c)
	if ok {
		_, _ = h.store.RevokeAdminSessions(c, cl.Username)
		_ = h.store.InsertAudit(c, db.AuditLog{
			Actor:  cl.Username,
			Action: "auth.logout",
			Target: &cl.Username,
			Result: "success",
		})
	}

	// Clear session & CSRF cookies
	c.SetSameSite(parseSameSite(h.cookieSameSite))
	c.SetCookie(h.cookieName, "", -1, "/", "", h.cookieSecure, true)
	c.SetCookie(h.csrfCookieName, "", -1, "/", "", h.cookieSecure, false)

	c.JSON(http.StatusOK, gin.H{"status": "ok"})
}

// loginHandler is a compatibility wrapper for existing tests.
func loginHandler(store *db.Store, tk *auth.Tokens) gin.HandlerFunc {
	h := newAuthHandlers(AuthHandlerConfig{
		Store:  store,
		Tokens: tk,
	})
	return h.login
}
