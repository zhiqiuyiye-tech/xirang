package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/db"
)

func auditHandler(store *db.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		logs, err := store.ListAudit(c, 200)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, logs)
	}
}
