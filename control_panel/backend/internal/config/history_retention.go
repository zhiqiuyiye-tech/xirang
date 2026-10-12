package config

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

func strictPositiveIntEnv(key string, fallback int) (int, error) {
	raw := strings.TrimSpace(os.Getenv(key))
	if raw == "" {
		return fallback, nil
	}
	value, err := strconv.Atoi(raw)
	if err != nil || value <= 0 {
		return 0, fmt.Errorf("%s must be a positive integer, got %q", key, raw)
	}
	return value, nil
}

func retentionDaysEnv(key string, fallback int) (time.Duration, error) {
	days, err := strictPositiveIntEnv(key, fallback)
	if err != nil {
		return 0, err
	}
	const day = 24 * time.Hour
	const maxDurationDays = int64((1<<63 - 1) / day)
	if int64(days) > maxDurationDays {
		return 0, fmt.Errorf("%s exceeds the supported duration range", key)
	}
	return time.Duration(days) * day, nil
}
