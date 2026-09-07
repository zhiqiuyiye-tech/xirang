package config

import (
	"encoding/base64"
	"fmt"
	"os"
	"time"
)

type Config struct {
	AESKey            []byte
	JWTSecret         string
	AdminInitPassword string
	DBPath            string
	ListenAddr        string
	SSHPoolSize       int
	SSHIdleTimeout    time.Duration
	JWTTTL            time.Duration
	TaskTimeout       time.Duration
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
	c.SSHIdleTimeout = envDurOr("SSH_IDLE_TIMEOUT", 5*time.Minute)
	c.JWTTTL = envDurOr("JWT_TTL", 12*time.Hour)
	// TaskTimeout bounds a single task run (a wedged SSH command must not
	// hold the task - and its per-worker slot - open forever).
	c.TaskTimeout = envDurOr("TASK_TIMEOUT", 30*time.Minute)
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
