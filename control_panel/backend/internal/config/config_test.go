package config

import (
	"os"
	"testing"
	"time"
)

const (
	base64_32bytes = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=" // 32 bytes of 0x00, base64-encoded
	base64_16bytes = "AAAAAAAAAAAAAAAAAAAAAA=="                     // 16 bytes of 0x00, base64-encoded
)

func setMinimalEnv() {
	os.Setenv("AES_KEY", base64_32bytes)
	os.Setenv("JWT_SECRET", "s3cret")
	os.Setenv("ADMIN_INIT_PASSWORD", "initpass")
}

func unsetMinimalEnv() {
	os.Unsetenv("AES_KEY")
	os.Unsetenv("JWT_SECRET")
	os.Unsetenv("ADMIN_INIT_PASSWORD")
	os.Unsetenv("DB_PATH")
	os.Unsetenv("LISTEN_ADDR")
	os.Unsetenv("JWT_TTL")
	os.Unsetenv("JWT_ISSUER")
	os.Unsetenv("JWT_AUDIENCE")
	os.Unsetenv("COOKIE_NAME")
	os.Unsetenv("COOKIE_SECURE")
	os.Unsetenv("COOKIE_SAMESITE")
	os.Unsetenv("CSRF_COOKIE_NAME")
	os.Unsetenv("CSRF_HEADER_NAME")
	os.Unsetenv("TRUSTED_PROXIES")
	os.Unsetenv("LOGIN_RATE_LIMIT_MAX_FAILURES")
	os.Unsetenv("LOGIN_RATE_LIMIT_LOCKOUT_DURATION")
	os.Unsetenv("LOGIN_RATE_LIMIT_WINDOW")
	os.Unsetenv("REQUIRE_K8S")
	os.Unsetenv("WORKER_HEARTBEAT_INTERVAL")
	os.Unsetenv("WORKER_HEARTBEAT_TIMEOUT")
	os.Unsetenv("STORAGE_REFRESH_INTERVAL")
	os.Unsetenv("STORAGE_PROBE_TIMEOUT")
	os.Unsetenv("COLLECTOR_CONCURRENCY")
	os.Unsetenv("STORAGE_STALE_AFTER")
	os.Unsetenv("RESERVED_MOUNT_POINTS")
}

func TestLoad_OK(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(cfg.AESKey) != 32 {
		t.Fatalf("AESKey len = %d, want 32", len(cfg.AESKey))
	}
	if cfg.JWTSecret != "s3cret" {
		t.Fatalf("JWTSecret = %q", cfg.JWTSecret)
	}
	if cfg.ListenAddr != ":8080" {
		t.Fatalf("ListenAddr default = %q", cfg.ListenAddr)
	}
	if cfg.JWTTTL != 4*time.Hour {
		t.Fatalf("JWTTTL default = %v, want 4h", cfg.JWTTTL)
	}
	if cfg.JWTIssuer != "xirang-control-panel" {
		t.Fatalf("JWTIssuer default = %q", cfg.JWTIssuer)
	}
	if cfg.JWTAudience != "xirang-control-panel-api" {
		t.Fatalf("JWTAudience default = %q", cfg.JWTAudience)
	}
	if cfg.CookieName != "cp_session" {
		t.Fatalf("CookieName = %q", cfg.CookieName)
	}
	if cfg.CookieSecure != false {
		t.Fatalf("CookieSecure = %v, want false", cfg.CookieSecure)
	}
	if cfg.CookieSameSite != "Lax" {
		t.Fatalf("CookieSameSite = %q, want Lax", cfg.CookieSameSite)
	}
	if cfg.RateLimitMaxFailures != 5 {
		t.Fatalf("RateLimitMaxFailures = %d, want 5", cfg.RateLimitMaxFailures)
	}
	if cfg.RateLimitLockoutDuration != 15*time.Minute {
		t.Fatalf("RateLimitLockoutDuration = %v, want 15m", cfg.RateLimitLockoutDuration)
	}
	if cfg.RequireK8s != false {
		t.Fatalf("RequireK8s = %v, want false", cfg.RequireK8s)
	}
}

func TestLoad_CustomValues(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()

	os.Setenv("COOKIE_SECURE", "true")
	os.Setenv("COOKIE_SAMESITE", "strict")
	os.Setenv("TRUSTED_PROXIES", "10.0.0.0/8, 192.168.1.0/24")
	os.Setenv("LOGIN_RATE_LIMIT_MAX_FAILURES", "3")
	os.Setenv("LOGIN_RATE_LIMIT_LOCKOUT_DURATION", "10m")
	os.Setenv("REQUIRE_K8S", "true")

	cfg, err := Load()
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if !cfg.CookieSecure {
		t.Fatal("expected CookieSecure true")
	}
	if cfg.CookieSameSite != "Strict" {
		t.Fatalf("CookieSameSite = %q, want Strict", cfg.CookieSameSite)
	}
	if len(cfg.TrustedProxies) != 2 || cfg.TrustedProxies[0] != "10.0.0.0/8" || cfg.TrustedProxies[1] != "192.168.1.0/24" {
		t.Fatalf("unexpected TrustedProxies: %+v", cfg.TrustedProxies)
	}
	if cfg.RateLimitMaxFailures != 3 {
		t.Fatalf("RateLimitMaxFailures = %d, want 3", cfg.RateLimitMaxFailures)
	}
	if cfg.RateLimitLockoutDuration != 10*time.Minute {
		t.Fatalf("RateLimitLockoutDuration = %v, want 10m", cfg.RateLimitLockoutDuration)
	}
	if !cfg.RequireK8s {
		t.Fatal("expected RequireK8s true")
	}
}

func TestLoad_InvalidOptions(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()

	os.Setenv("COOKIE_SAMESITE", "invalid")
	if _, err := Load(); err == nil {
		t.Fatal("expected error for invalid COOKIE_SAMESITE")
	}

	os.Setenv("COOKIE_SAMESITE", "Lax")
	os.Setenv("LOGIN_RATE_LIMIT_MAX_FAILURES", "0")
	if _, err := Load(); err == nil {
		t.Fatal("expected error for 0 max failures")
	}

	os.Setenv("LOGIN_RATE_LIMIT_MAX_FAILURES", "5")
	os.Setenv("JWT_TTL", "-1m")
	if _, err := Load(); err == nil {
		t.Fatal("expected error for negative JWT_TTL")
	}
}

func TestLoad_CollectorDefaultsAndCustomValues(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()

	cfg, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	if cfg.WorkerHeartbeatInterval != time.Minute || cfg.WorkerHeartbeatTimeout != 5*time.Second {
		t.Fatalf("heartbeat defaults: interval=%v timeout=%v", cfg.WorkerHeartbeatInterval, cfg.WorkerHeartbeatTimeout)
	}
	if cfg.StorageRefreshInterval != 5*time.Minute || cfg.StorageProbeTimeout != 45*time.Second {
		t.Fatalf("storage defaults: interval=%v timeout=%v", cfg.StorageRefreshInterval, cfg.StorageProbeTimeout)
	}
	if cfg.CollectorConcurrency != 8 || cfg.StorageStaleAfter != 10*time.Minute {
		t.Fatalf("collector defaults: concurrency=%d stale=%v", cfg.CollectorConcurrency, cfg.StorageStaleAfter)
	}
	if len(cfg.ReservedMountPoints) != 1 || cfg.ReservedMountPoints[0] != "/data01" {
		t.Fatalf("reserved mount defaults: %+v", cfg.ReservedMountPoints)
	}

	os.Setenv("WORKER_HEARTBEAT_INTERVAL", "30s")
	os.Setenv("WORKER_HEARTBEAT_TIMEOUT", "3s")
	os.Setenv("STORAGE_REFRESH_INTERVAL", "2m")
	os.Setenv("STORAGE_PROBE_TIMEOUT", "1m")
	os.Setenv("COLLECTOR_CONCURRENCY", "4")
	os.Setenv("STORAGE_STALE_AFTER", "7m")
	os.Setenv("RESERVED_MOUNT_POINTS", "/data01,/var/lib/kubelet")
	cfg, err = Load()
	if err != nil {
		t.Fatal(err)
	}
	if cfg.WorkerHeartbeatInterval != 30*time.Second || cfg.WorkerHeartbeatTimeout != 3*time.Second || cfg.StorageRefreshInterval != 2*time.Minute || cfg.StorageProbeTimeout != time.Minute {
		t.Fatalf("custom durations not loaded: %+v", cfg)
	}
	if cfg.CollectorConcurrency != 4 || cfg.StorageStaleAfter != 7*time.Minute || len(cfg.ReservedMountPoints) != 2 {
		t.Fatalf("custom collector config not loaded: %+v", cfg)
	}
}

func TestLoad_InvalidCollectorOptions(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()

	for key, value := range map[string]string{
		"WORKER_HEARTBEAT_INTERVAL": "0s",
		"WORKER_HEARTBEAT_TIMEOUT":  "not-a-duration",
		"STORAGE_REFRESH_INTERVAL":  "-1m",
		"STORAGE_PROBE_TIMEOUT":     "0s",
		"COLLECTOR_CONCURRENCY":     "0",
		"STORAGE_STALE_AFTER":       "bad",
	} {
		unsetMinimalEnv()
		setMinimalEnv()
		os.Setenv(key, value)
		if _, err := Load(); err == nil {
			t.Fatalf("expected error for %s=%q", key, value)
		}
	}
}

func TestLoad_MissingAESKey(t *testing.T) {
	os.Unsetenv("AES_KEY")
	os.Setenv("JWT_SECRET", "s")
	os.Setenv("ADMIN_INIT_PASSWORD", "p")
	defer unsetMinimalEnv()
	_, err := Load()
	if err == nil {
		t.Fatal("expected error for missing AES_KEY")
	}
}

func TestLoad_BadAESKeyLength(t *testing.T) {
	os.Setenv("AES_KEY", base64_16bytes)
	os.Setenv("JWT_SECRET", "s")
	os.Setenv("ADMIN_INIT_PASSWORD", "p")
	defer unsetMinimalEnv()
	_, err := Load()
	if err == nil {
		t.Fatal("expected error for bad AES_KEY length")
	}
}
