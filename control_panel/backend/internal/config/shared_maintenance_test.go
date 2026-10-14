package config

import "testing"

func TestSharedHostMaintenanceIsExplicitAndDisabledByDefault(t *testing.T) {
	setMinimalEnv()
	defer unsetMinimalEnv()
	t.Setenv("SHARED_HOST_MAINTENANCE_ENABLED", "")
	cfg, err := Load()
	if err != nil || cfg.SharedHostMaintenance {
		t.Fatalf("maintenance must default off: enabled=%v err=%v", cfg.SharedHostMaintenance, err)
	}
	t.Setenv("SHARED_HOST_MAINTENANCE_ENABLED", "true")
	cfg, err = Load()
	if err != nil || !cfg.SharedHostMaintenance {
		t.Fatalf("explicit enable not applied: enabled=%v err=%v", cfg.SharedHostMaintenance, err)
	}
	for _, value := range []string{"yes", "1", "tru", "invalid"} {
		t.Setenv("SHARED_HOST_MAINTENANCE_ENABLED", value)
		if _, err := Load(); err == nil {
			t.Fatalf("invalid security setting accepted: %q", value)
		}
	}
}
