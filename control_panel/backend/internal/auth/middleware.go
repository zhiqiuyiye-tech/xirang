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
		if !strings.HasPrefix(h, "Bearer ") {
			c.AbortWithStatusJSON(http.StatusUnauthorized, gin.H{"error": "missing bearer token"})
			return
		}
		tok := strings.TrimPrefix(h, "Bearer ")
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
