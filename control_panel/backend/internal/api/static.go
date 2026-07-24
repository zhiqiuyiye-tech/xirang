package api

import (
	"embed"
	"io/fs"
	"net/http"

	"github.com/gin-gonic/gin"
)

// webFS embeds the static frontend files (index.html, app.js, styles.css).
// The //go:embed directive requires the web/ directory to exist relative to
// this source file - the files live at internal/api/web/.
//
//go:embed web/*
var webFS embed.FS

// registerStaticRoutes serves the embedded SPA. GET / returns index.html;
// GET /static/* serves app.js, styles.css, and any other web assets. The SPA
// uses hash-based routing so a single index.html is sufficient - no
// server-side fallback routes are needed.
func registerStaticRoutes(r *gin.Engine) {
	sub, _ := fs.Sub(webFS, "web")
	r.GET("/", func(c *gin.Context) {
		c.Data(http.StatusOK, "text/html; charset=utf-8", readStatic(sub, "index.html"))
	})
	r.StaticFS("/static", http.FS(sub))
}

func readStatic(fsys fs.FS, name string) []byte {
	b, _ := fs.ReadFile(fsys, name)
	return b
}
