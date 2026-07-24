package db

import (
	"context"
	"testing"
)

func TestInsertAndListAudit(t *testing.T) {
	s := newStore(t)
	if err := s.InsertAudit(context.Background(), AuditLog{
		Actor: "admin", Action: "worker.create", Result: "success",
	}); err != nil {
		t.Fatal(err)
	}
	logs, err := s.ListAudit(context.Background(), 10)
	if err != nil {
		t.Fatal(err)
	}
	if len(logs) != 1 || logs[0].Action != "worker.create" {
		t.Fatalf("audit=%+v", logs)
	}
}
