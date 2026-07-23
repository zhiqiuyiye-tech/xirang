package config

import (
	"os"
	"testing"
)

const (
	base64_32bytes = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=" // 32 bytes of 0x00, base64-encoded
	base64_16bytes = "AAAAAAAAAAAAAAAAAAAAAA=="                    // 16 bytes of 0x00, base64-encoded
)

func TestLoad_OK(t *testing.T) {
	os.Setenv("AES_KEY", base64_32bytes)
	os.Setenv("JWT_SECRET", "s3cret")
	os.Setenv("ADMIN_INIT_PASSWORD", "initpass")
	defer func() {
		os.Unsetenv("AES_KEY")
		os.Unsetenv("JWT_SECRET")
		os.Unsetenv("ADMIN_INIT_PASSWORD")
	}()
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
}

func TestLoad_MissingAESKey(t *testing.T) {
	os.Unsetenv("AES_KEY")
	os.Setenv("JWT_SECRET", "s")
	os.Setenv("ADMIN_INIT_PASSWORD", "p")
	_, err := Load()
	if err == nil {
		t.Fatal("expected error for missing AES_KEY")
	}
}

func TestLoad_BadAESKeyLength(t *testing.T) {
	os.Setenv("AES_KEY", base64_16bytes)
	os.Setenv("JWT_SECRET", "s")
	os.Setenv("ADMIN_INIT_PASSWORD", "p")
	defer os.Unsetenv("AES_KEY")
	_, err := Load()
	if err == nil {
		t.Fatal("expected error for bad AES_KEY length")
	}
}
