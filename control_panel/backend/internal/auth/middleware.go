package auth

import (
	"context"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const (
	claimsKey   = "auth_claims"
	authTypeKey = "auth_type"

	AuthTypeBearer = "bearer"
	AuthTypeCookie = "cookie"
)

type VersionStore interface {
	GetAdminAuthVersion(ctx context.Context, id int64) (int64, error)
}

type MiddlewareConfig struct {
	Tokens       *Tokens
	VersionStore VersionStore
	CookieName   string
}

func AuthMiddleware(cfg MiddlewareConfig) gin.HandlerFunc {
	cookieName := cfg.CookieName
	if cookieName == "" {
		cookieName = "cp_session"
	}

	return func(c *gin.Context) {
		tok := ""
		authType := ""

		// 1. Check Authorization header
		h := c.GetHeader("Authorization")
		if strings.HasPrefix(strings.ToLower(h), "bearer ") {
			tok = h[7:]
			authType = AuthTypeBearer
		}

		// 2. Fall back to Cookie if no Bearer header
		if tok == "" {
			if cookieVal, err := c.Cookie(cookieName); err == nil && cookieVal != "" {
				tok = cookieVal
				authType = AuthTypeCookie
			}
		}

		if tok == "" {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing authentication"})
			return
		}

		cl, err := cfg.Tokens.Parse(tok)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}

		// 3. Verify auth_version against database if store is configured
		if cfg.VersionStore != nil {
			curVer, err := cfg.VersionStore.GetAdminAuthVersion(c.Request.Context(), cl.AdminID)
			if err != nil || curVer != cl.AuthVersion {
				c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "session revoked or expired"})
				return
			}
		}

		c.Set(claimsKey, cl)
		c.Set(authTypeKey, authType)
		c.Next()
	}
}

// BearerMiddleware is a backwards-compatible wrapper for callers without a VersionStore.
func BearerMiddleware(tokens *Tokens) gin.HandlerFunc {
	return AuthMiddleware(MiddlewareConfig{Tokens: tokens})
}

func ClaimsFrom(c *gin.Context) (Claims, bool) {
	v, ok := c.Get(claimsKey)
	if !ok {
		return Claims{}, false
	}
	cl, ok := v.(Claims)
	return cl, ok
}

func AuthTypeFrom(c *gin.Context) (string, bool) {
	v, ok := c.Get(authTypeKey)
	if !ok {
		return "", false
	}
	t, ok := v.(string)
	return t, ok
}
