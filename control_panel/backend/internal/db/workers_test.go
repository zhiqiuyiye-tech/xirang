package db

import (
	"context"
	"testing"
)

func TestCreateAndGetWorker(t *testing.T) {
	s := newStore(t)
	id, err := s.CreateWorker(context.Background(), WorkerNode{
		Name: "w1", Host: "10.0.0.1", Port: 22, Username: "root", AuthMode: "key",
	})
	if err != nil {
		t.Fatal(err)
	}
	got, err := s.GetWorker(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if got.Name != "w1" || got.Status != "unknown" {
		t.Fatalf("unexpected worker %+v", got)
	}
}

func TestListWorkers(t *testing.T) {
	s := newStore(t)
	s.CreateWorker(context.Background(), WorkerNode{Name: "a", Host: "1", Port: 22, Username: "root", AuthMode: "key"})
	s.CreateWorker(context.Background(), WorkerNode{Name: "b", Host: "2", Port: 22, Username: "root", AuthMode: "key"})
	ws, err := s.ListWorkers(context.Background())
	if err != nil {
		t.Fatal(err)
	}
	if len(ws) != 2 {
		t.Fatalf("len = %d", len(ws))
	}
}

func TestSetWorkerCredentials(t *testing.T) {
	s := newStore(t)
	id, _ := s.CreateWorker(context.Background(), WorkerNode{Name: "w", Host: "h", Port: 22, Username: "root", AuthMode: "key"})
	pw := "enc"
	if err := s.SetWorkerCredentials(context.Background(), id, &pw, nil, "password"); err != nil {
		t.Fatal(err)
	}
	got, _ := s.GetWorker(context.Background(), id)
	if got.AuthMode != "password" || *got.EncPassword != "enc" {
		t.Fatalf("creds not set: %+v", got)
	}
}

func TestDeleteWorker(t *testing.T) {
	s := newStore(t)
	id, _ := s.CreateWorker(context.Background(), WorkerNode{Name: "w", Host: "h", Port: 22, Username: "root", AuthMode: "key"})
	if err := s.DeleteWorker(context.Background(), id); err != nil {
		t.Fatal(err)
	}
	if _, err := s.GetWorker(context.Background(), id); err == nil {
		t.Fatal("expected not found after delete")
	}
}
