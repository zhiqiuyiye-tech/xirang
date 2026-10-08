package collector

import (
	"context"
	"errors"
	"testing"
	"time"

	"xirang/control_panel/internal/crypto"
	"xirang/control_panel/internal/ssh"
)

func TestSuccessfulInventoryRecoversWorkerHealth(t *testing.T) {
	store, id := newTestStore(t)
	ctx := context.Background()
	if err := store.RecordWorkerHealth(ctx, id, false, time.Now().UTC().Add(-time.Minute), "old timeout", 1); err != nil {
		t.Fatal(err)
	}
	c := New(store, &fakeRunner{out: "###LSBLK###\n"}, Config{})
	if err := c.collectInventory(ctx, id); err != nil {
		t.Fatal(err)
	}
	w, err := store.GetWorker(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "online" || w.HealthFailures != 0 || w.StatusError != nil || w.LastSeenAt == nil {
		t.Fatalf("successful remote inventory left worker unhealthy: %+v", w)
	}
}

func TestFailedInventoryDoesNotDeclareWorkerOnline(t *testing.T) {
	store, id := newTestStore(t)
	ctx := context.Background()
	if err := store.RecordWorkerHealth(ctx, id, false, time.Now().UTC(), "heartbeat failed", 1); err != nil {
		t.Fatal(err)
	}
	c := New(store, &fakeRunner{code: 1, stderr: "lsblk failed"}, Config{})
	if err := c.collectInventory(ctx, id); err == nil {
		t.Fatal("expected inventory error")
	}
	w, err := store.GetWorker(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "offline" || w.LastSeenAt != nil {
		t.Fatalf("failed inventory marked healthy: %+v", w)
	}
}

func TestHeartbeatWithoutCredentialsRemainsUnknown(t *testing.T) {
	store, id := newTestStore(t)
	cipher, err := crypto.New(make([]byte, 32))
	if err != nil {
		t.Fatal(err)
	}
	manager := ssh.NewManager(cipher, 1, 0)
	defer manager.Close()
	c := New(store, manager, Config{HeartbeatTimeout: time.Second, OfflineThreshold: 2})
	for i := 0; i < 3; i++ {
		if err := c.checkHeartbeat(context.Background(), id); err == nil {
			t.Fatal("expected missing credentials error")
		}
	}
	w, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "unknown" || w.HealthFailures != 0 || w.StatusError == nil {
		t.Fatalf("local missing credentials incorrectly declared offline: %+v", w)
	}
}

func TestHeartbeatAuthenticationFailuresReachThreshold(t *testing.T) {
	store, id := newTestStore(t)
	c := New(store, &fakeRunner{code: -1, err: errors.New("ssh: unable to authenticate")}, Config{OfflineThreshold: 2})
	for i := 0; i < 2; i++ {
		_ = c.checkHeartbeat(context.Background(), id)
	}
	w, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "offline" || w.HealthFailures != 2 || w.LastSeenAt != nil {
		t.Fatalf("authentication failure incorrectly treated as healthy: %+v", w)
	}
}

func TestHeartbeatCallerCancellationDoesNotCountAsFailure(t *testing.T) {
	store, id := newTestStore(t)
	c := New(store, &fakeRunner{code: -1, err: context.Canceled}, Config{OfflineThreshold: 1})
	// A runner may report canceled even before the caller's context is visible to the store.
	if err := c.checkHeartbeat(context.Background(), id); !errors.Is(err, context.Canceled) {
		t.Fatalf("err=%v", err)
	}
	w, err := store.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "unknown" || w.HealthFailures != 0 {
		t.Fatalf("canceled check counted as node failure: %+v", w)
	}
}
