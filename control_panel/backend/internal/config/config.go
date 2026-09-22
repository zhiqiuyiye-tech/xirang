package config

import (
	"encoding/base64"
	"fmt"
	"os"
	"strings"
	"time"
)

type Config struct {
	AESKey                   []byte
	JWTSecret                string
	AdminInitPassword        string
	DBPath                   string
	ListenAddr               string
	SSHPoolSize              int
	SSHIdleTimeout           time.Duration
	JWTTTL                   time.Duration
	JWTIssuer                string
	JWTAudience              string
	TaskTimeout              time.Duration
	CookieName               string
	CookieSecure             bool
	CookieSameSite           string
	CSRFCookieName           string
	CSRFHeaderName           string
	TrustedProxies           []string
	RateLimitMaxFailures     int
	RateLimitLockoutDuration time.Duration
	RateLimitWindow          time.Duration
	RequireK8s               bool
}

func Load() (Config, error) {
	var c Config
	b64, ok := os.LookupEnv("AES_KEY")
	if !ok {
		return c, fmt.Errorf("AES_KEY env var is required")
	}
	key, err := base64.StdEncoding.DecodeString(b64)
	if err != nil {
		return c, fmt.Errorf("AES_KEY is not valid base64: %w", err)
	}
	if len(key) != 32 {
		return c, fmt.Errorf("AES_KEY must decode to 32 bytes, got %d", len(key))
	}
	c.AESKey = key
	c.JWTSecret = os.Getenv("JWT_SECRET")
	if c.JWTSecret == "" {
		return c, fmt.Errorf("JWT_SECRET env var is required")
	}
	c.AdminInitPassword = os.Getenv("ADMIN_INIT_PASSWORD")
	if c.AdminInitPassword == "" {
		return c, fmt.Errorf("ADMIN_INIT_PASSWORD env var is required")
	}
	c.DBPath = envOr("DB_PATH", "/data/control_panel.db")
	c.ListenAddr = envOr("LISTEN_ADDR", ":8080")
	c.SSHPoolSize = envIntOr("SSH_POOL_SIZE", 3)
	if c.SSHPoolSize <= 0 {
		return c, fmt.Errorf("SSH_POOL_SIZE must be > 0")
	}
	c.SSHIdleTimeout = envDurOr("SSH_IDLE_TIMEOUT", 5*time.Minute)
	c.JWTTTL = envDurOr("JWT_TTL", 4*time.Hour)
	if c.JWTTTL <= 0 {
		return c, fmt.Errorf("JWT_TTL must be > 0")
	}
	c.JWTIssuer = envOr("JWT_ISSUER", "xirang-control-panel")
	c.JWTAudience = envOr("JWT_AUDIENCE", "xirang-control-panel-api")
	// TaskTimeout bounds a single task run (a wedged SSH command must not
	// hold the task - and its per-worker slot - open forever).
	c.TaskTimeout = envDurOr("TASK_TIMEOUT", 30*time.Minute)
	if c.TaskTimeout <= 0 {
		return c, fmt.Errorf("TASK_TIMEOUT must be > 0")
	}

	c.CookieName = envOr("COOKIE_NAME", "cp_session")
	c.CookieSecure = envBoolOr("COOKIE_SECURE", false)
	sameSite := strings.ToLower(envOr("COOKIE_SAMESITE", "Lax"))
	switch sameSite {
	case "lax":
		c.CookieSameSite = "Lax"
	case "strict":
		c.CookieSameSite = "Strict"
	case "none":
		c.CookieSameSite = "None"
	default:
		return c, fmt.Errorf("COOKIE_SAMESITE must be Lax, Strict, or None, got %q", sameSite)
	}

	c.CSRFCookieName = envOr("CSRF_COOKIE_NAME", "cp_csrf")
	c.CSRFHeaderName = envOr("CSRF_HEADER_NAME", "X-CSRF-Token")
	c.TrustedProxies = envSliceOr("TRUSTED_PROXIES", nil)

	c.RateLimitMaxFailures = envIntOr("LOGIN_RATE_LIMIT_MAX_FAILURES", 5)
	if c.RateLimitMaxFailures <= 0 {
		return c, fmt.Errorf("LOGIN_RATE_LIMIT_MAX_FAILURES must be > 0")
	}
	c.RateLimitLockoutDuration = envDurOr("LOGIN_RATE_LIMIT_LOCKOUT_DURATION", 15*time.Minute)
	if c.RateLimitLockoutDuration <= 0 {
		return c, fmt.Errorf("LOGIN_RATE_LIMIT_LOCKOUT_DURATION must be > 0")
	}
	c.RateLimitWindow = envDurOr("LOGIN_RATE_LIMIT_WINDOW", 15*time.Minute)
	if c.RateLimitWindow <= 0 {
		return c, fmt.Errorf("LOGIN_RATE_LIMIT_WINDOW must be > 0")
	}

	c.RequireK8s = envBoolOr("REQUIRE_K8S", false)

	return c, nil
}

func envOr(k, def string) string {
	if v := os.Getenv(k); v != "" {
		return v
	}
	return def
}

func envIntOr(k string, def int) int {
	if v := os.Getenv(k); v != "" {
		var n int
		if _, err := fmt.Sscanf(v, "%d", &n); err == nil {
			return n
		}
	}
	return def
}

func envDurOr(k string, def time.Duration) time.Duration {
	if v := os.Getenv(k); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			return d
		}
	}
	return def
}

func envBoolOr(k string, def bool) bool {
	if v := os.Getenv(k); v != "" {
		v = strings.TrimSpace(strings.ToLower(v))
		return v == "1" || v == "true" || v == "yes" || v == "on"
	}
	return def
}

func envSliceOr(k string, def []string) []string {
	v := os.Getenv(k)
	if v == "" {
		return def
	}
	parts := strings.Split(v, ",")
	res := make([]string, 0, len(parts))
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p != "" {
			res = append(res, p)
		}
	}
	if len(res) == 0 {
		return def
	}
	return res
}
