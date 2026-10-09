package config

import (
	"testing"
	"time"
)

func TestNamespaceCleanupDefaultsAndValidation(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()
	t.Setenv("NAMESPACE_CLEANUP_ALLOWLIST", "")
	t.Setenv("NAMESPACE_CLEANUP_TIMEOUT", "60s")
	t.Setenv("NAMESPACE_UNMOUNT_TIMEOUT", "10s")
	cfg, err := Load()
	if err != nil {
		t.Fatal(err)
	}
	if len(cfg.NamespaceCleanupAllowlist) != 0 || cfg.NamespaceCleanupTimeout != time.Minute || cfg.NamespaceUnmountTimeout != 10*time.Second {
		t.Fatalf("unsafe defaults: %+v", cfg)
	}
	t.Setenv("NAMESPACE_CLEANUP_ALLOWLIST", "monitoring/promtail/promtail,logging/log-agent/collector")
	cfg, err = Load()
	if err != nil || len(cfg.NamespaceCleanupAllowlist) != 2 {
		t.Fatalf("allowlist=%v err=%v", cfg.NamespaceCleanupAllowlist, err)
	}
	for _, value := range []string{"promtail", "monitoring/*/promtail", "Monitoring/promtail/promtail", "monitoring/promtail/", "monitoring/promtail/promtail,", "monitoring/../promtail"} {
		t.Setenv("NAMESPACE_CLEANUP_ALLOWLIST", value)
		if _, err := Load(); err == nil {
			t.Errorf("accepted malformed allowlist %q", value)
		}
	}
	t.Setenv("NAMESPACE_CLEANUP_ALLOWLIST", "")
	for _, setting := range []string{"NAMESPACE_CLEANUP_TIMEOUT", "NAMESPACE_UNMOUNT_TIMEOUT"} {
		for _, value := range []string{"0s", "-1s", "garbage", "1h"} {
			t.Setenv(setting, value)
			if _, err := Load(); err == nil {
				t.Errorf("accepted %s=%s", setting, value)
			}
		}
		t.Setenv(setting, "10s")
	}
	t.Setenv("NAMESPACE_CLEANUP_TIMEOUT", "60s")
	t.Setenv("NAMESPACE_UNMOUNT_TIMEOUT", "11s")
	if _, err := Load(); err == nil {
		t.Error("accepted unsupported unmount deadline above 10s")
	}
	t.Setenv("NAMESPACE_CLEANUP_TIMEOUT", "5s")
	t.Setenv("NAMESPACE_UNMOUNT_TIMEOUT", "10s")
	if _, err := Load(); err == nil {
		t.Error("accepted unmount timeout exceeding recovery budget")
	}
}
