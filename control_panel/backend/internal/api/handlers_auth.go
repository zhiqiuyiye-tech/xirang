package api

import (
	"net/http"

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

func loginHandler(store *db.Store, tk *auth.Tokens) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req struct {
			Username string `json:"username"`
			Password string `json:"password"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		a, err := store.GetAdminByUsername(c, req.Username)
		if err != nil {
			// Timing equalizer: spend the same ~100ms bcrypt comparison as the
			// wrong-password path below.
			_ = bcrypt.CompareHashAndPassword([]byte(dummyBcryptHash), []byte(req.Password))
			c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
			return
		}
		if !auth.CheckPassword(a.PasswordHash, req.Password) {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "invalid credentials"})
			return
		}
		tok, err := tk.Issue(a.ID, a.Username)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		_ = store.InsertAudit(c, db.AuditLog{Actor: a.Username, Action: "auth.login", Target: &req.Username, Result: "success"})
		c.JSON(http.StatusOK, gin.H{"token": tok})
	}
}
