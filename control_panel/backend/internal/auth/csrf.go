package auth

import (
	"net/http"
	"net/url"
	"strings"

	"github.com/gin-gonic/gin"
)

type CSRFConfig struct {
	CookieName string
	HeaderName string
}

func CSRFMiddleware(cfg CSRFConfig) gin.HandlerFunc {
	cookieName := cfg.CookieName
	if cookieName == "" {
		cookieName = "cp_csrf"
	}
	headerName := cfg.HeaderName
	if headerName == "" {
		headerName = "X-CSRF-Token"
	}

	return func(c *gin.Context) {
		switch c.Request.Method {
		case http.MethodPost, http.MethodPut, http.MethodDelete, http.MethodPatch:
			authType, _ := AuthTypeFrom(c)
			// Only requests authenticated by browser cookies require CSRF protection
			if authType != AuthTypeCookie {
				c.Next()
				return
			}

			// Origin check if present
			if origin := c.GetHeader("Origin"); origin != "" {
				u, err := url.Parse(origin)
				if err == nil && u.Host != "" {
					reqHost := c.Request.Host
					if !strings.EqualFold(u.Host, reqHost) {
						c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "cross-origin request forbidden"})
						return
					}
				}
			}

			cookieVal, err := c.Cookie(cookieName)
			headerVal := c.GetHeader(headerName)

			if err != nil || cookieVal == "" || headerVal == "" || cookieVal != headerVal {
				c.AbortWithStatusJSON(http.StatusForbidden, gin.H{"error": "invalid or missing CSRF token"})
				return
			}
		}

		c.Next()
	}
}
