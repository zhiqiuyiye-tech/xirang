package workers

import (
	"context"
	"testing"
)

func TestConnectionWithoutCredentialsRemainsUnknown(t *testing.T) {
	svc := setup(t)
	id, err := svc.Create(context.Background(), CreateReq{Name: "w", Host: "127.0.0.1"})
	if err != nil {
		t.Fatal(err)
	}
	if err := svc.TestConnection(context.Background(), id); err == nil {
		t.Fatal("expected missing credentials error")
	}
	w, err := svc.Get(context.Background(), id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "unknown" || w.HealthFailures != 0 || w.StatusError == nil {
		t.Fatalf("missing credentials incorrectly declared offline: %+v", w)
	}
}
