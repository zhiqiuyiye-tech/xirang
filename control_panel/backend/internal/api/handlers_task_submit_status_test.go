package api

import (
	"errors"
	"net/http"
	"testing"

	"xirang/control_panel/internal/tasks"
)

func TestTaskSubmitStatusMapsQueueFullToServiceUnavailable(t *testing.T) {
	if got := taskSubmitStatus(&tasks.QueueFullError{}, http.StatusInternalServerError); got != http.StatusServiceUnavailable {
		t.Fatalf("queue-full status=%d, want %d", got, http.StatusServiceUnavailable)
	}
	if got := taskSubmitStatus(errors.New("database unavailable"), http.StatusBadRequest); got != http.StatusBadRequest {
		t.Fatalf("fallback status=%d, want %d", got, http.StatusBadRequest)
	}
}
