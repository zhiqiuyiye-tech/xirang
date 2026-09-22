package db

import (
	"context"
	"path/filepath"
	"testing"
)

func newStore(t *testing.T) *Store {
	t.Helper()
	s, err := Open(filepath.Join(t.TempDir(), "t.db"))
	if err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() { s.Close() })
	return s
}

func TestIsAdminSeeded_PendingInit(t *testing.T) {
	s := newStore(t)
	seeded, err := s.IsAdminSeeded(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if seeded {
		t.Fatal("expected not seeded while hash is __PENDING_INIT__")
	}
}

func TestUpsertAdminPasswordThenSeeded(t *testing.T) {
	s := newStore(t)
	if err := s.UpsertAdminPassword(context.Background(), "admin", "$2a$hash"); err != nil {
		t.Fatal(err)
	}
	seeded, _ := s.IsAdminSeeded(context.Background())
	if !seeded {
		t.Fatal("expected seeded after upsert")
	}
	a, err := s.GetAdminByUsername(context.Background(), "admin")
	if err != nil {
		t.Fatal(err)
	}
	if a.PasswordHash != "$2a$hash" {
		t.Fatalf("hash = %q", a.PasswordHash)
	}
	if a.AuthVersion != 1 {
		t.Fatalf("auth_version = %d, want 1", a.AuthVersion)
	}
}

func TestUpdateAdminPasswordAndBumpVersion(t *testing.T) {
	s := newStore(t)
	ctx := context.Background()

	ver1, err := s.GetAdminAuthVersion(ctx, 1)
	if err != nil {
		t.Fatal(err)
	}
	if ver1 != 1 {
		t.Fatalf("initial auth_version = %d, want 1", ver1)
	}

	newVer, err := s.UpdateAdminPasswordAndBumpVersion(ctx, "admin", "$2a$newhash")
	if err != nil {
		t.Fatal(err)
	}
	if newVer != 2 {
		t.Fatalf("expected newVer 2, got %d", newVer)
	}

	a, err := s.GetAdminByUsername(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	if a.PasswordHash != "$2a$newhash" {
		t.Fatalf("unexpected hash: %q", a.PasswordHash)
	}
	if a.AuthVersion != 2 {
		t.Fatalf("unexpected auth_version: %d", a.AuthVersion)
	}
}

func TestRevokeAdminSessions(t *testing.T) {
	s := newStore(t)
	ctx := context.Background()

	newVer, err := s.RevokeAdminSessions(ctx, "admin")
	if err != nil {
		t.Fatal(err)
	}
	if newVer != 2 {
		t.Fatalf("expected newVer 2, got %d", newVer)
	}

	ver, err := s.GetAdminAuthVersion(ctx, 1)
	if err != nil {
		t.Fatal(err)
	}
	if ver != 2 {
		t.Fatalf("expected ver 2, got %d", ver)
	}
}

func TestGetAdminByUsername_NotFound(t *testing.T) {
	s := newStore(t)
	_, err := s.GetAdminByUsername(context.Background(), "nobody")
	if err == nil {
		t.Fatal("expected error for missing user")
	}
}
