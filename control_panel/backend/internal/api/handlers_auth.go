package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/auth"
	"xirang/control_panel/internal/db"
)

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
