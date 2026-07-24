package auth

import (
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

const claimsKey = "auth_claims"

func BearerMiddleware(tokens *Tokens) gin.HandlerFunc {
	return func(c *gin.Context) {
		h := c.GetHeader("Authorization")
		// RFC 7235: the auth scheme is case-insensitive. Match on the
		// lowercased header but slice the ORIGINAL value to preserve the
		// token's exact casing.
		if !strings.HasPrefix(strings.ToLower(h), "bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing bearer token"})
			return
		}
		tok := h[7:]
		cl, err := tokens.Parse(tok)
		if err != nil {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "invalid token"})
			return
		}
		c.Set(claimsKey, cl)
		c.Next()
	}
}

func ClaimsFrom(c *gin.Context) (Claims, bool) {
	v, ok := c.Get(claimsKey)
	if !ok {
		return Claims{}, false
	}
	cl, ok := v.(Claims)
	return cl, ok
}
