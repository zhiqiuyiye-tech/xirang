package db

import (
	"context"
	"path/filepath"
	"testing"
	"time"
)

func TestInventorySnapshotKeepsLastGoodDataOnFailedAttempt(t *testing.T) {
	store, err := Open(filepath.Join(t.TempDir(), "snapshots.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()

	workerID, err := store.CreateWorker(context.Background(), WorkerNode{Name: "w1", Host: "10.0.0.1", Port: 22, Username: "root", AuthMode: "key"})
	if err != nil {
		t.Fatal(err)
	}
	collected := time.Date(2026, 9, 25, 1, 2, 3, 0, time.UTC)
	if err := store.SaveInventorySnapshot(context.Background(), InventorySnapshot{
		WorkerID: workerID, SchemaVersion: 1, PayloadJSON: `{"ok":true}`, CollectedAt: &collected, LastAttemptedAt: collected,
	}); err != nil {
		t.Fatal(err)
	}
	attempted := collected.Add(time.Minute)
	if err := store.RecordInventoryFailure(context.Background(), workerID, attempted, "ssh timeout"); err != nil {
		t.Fatal(err)
	}

	got, err := store.GetInventorySnapshot(context.Background(), workerID)
	if err != nil {
		t.Fatal(err)
	}
	if got.PayloadJSON != `{"ok":true}` || got.CollectedAt == nil || !got.CollectedAt.Equal(collected) {
		t.Fatalf("last good snapshot was overwritten: %+v", got)
	}
	if got.LastError == nil || *got.LastError != "ssh timeout" || !got.LastAttemptedAt.Equal(attempted) {
		t.Fatalf("failure metadata not recorded: %+v", got)
	}
}

func TestInventorySnapshotDeletedWithWorker(t *testing.T) {
	store, err := Open(filepath.Join(t.TempDir(), "cascade.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	ctx := context.Background()
	workerID, _ := store.CreateWorker(ctx, WorkerNode{Name: "w1", Host: "10.0.0.1", Port: 22, Username: "root", AuthMode: "key"})
	now := time.Now().UTC()
	if err := store.SaveInventorySnapshot(ctx, InventorySnapshot{WorkerID: workerID, SchemaVersion: 1, PayloadJSON: `{}`, CollectedAt: &now, LastAttemptedAt: now}); err != nil {
		t.Fatal(err)
	}
	if err := store.DeleteWorker(ctx, workerID); err != nil {
		t.Fatal(err)
	}
	if _, err := store.GetInventorySnapshot(ctx, workerID); err != ErrNotFound {
		t.Fatalf("snapshot after worker delete: err=%v, want ErrNotFound", err)
	}
}

func TestNotebookMetadataUpsertLookupAndDelete(t *testing.T) {
	store, err := Open(filepath.Join(t.TempDir(), "metadata.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	ctx := context.Background()
	m := NotebookMetadata{
		StableKey: "v1:namespace:ns:workspace:ws:project:p", KeyKind: "business_labels",
		Namespace: "ns", WorkspaceID: "ws", ProjectID: "p", LastPodUID: "uid-1",
		OwnerName: "Alice", Note: "GPU experiment", UpdatedBy: "admin",
	}
	if err := store.UpsertNotebookMetadata(ctx, m); err != nil {
		t.Fatal(err)
	}
	m.LastPodUID = "uid-2"
	m.Note = "updated"
	if err := store.UpsertNotebookMetadata(ctx, m); err != nil {
		t.Fatal(err)
	}
	got, err := store.GetNotebookMetadata(ctx, m.StableKey)
	if err != nil {
		t.Fatal(err)
	}
	if got.LastPodUID != "uid-2" || got.OwnerName != "Alice" || got.Note != "updated" || got.UpdatedAt.IsZero() {
		t.Fatalf("unexpected metadata: %+v", got)
	}
	byKeys, err := store.GetNotebookMetadataByKeys(ctx, []string{m.StableKey, "missing"})
	if err != nil || len(byKeys) != 1 || byKeys[m.StableKey].Note != "updated" {
		t.Fatalf("batch lookup: map=%+v err=%v", byKeys, err)
	}
	if err := store.DeleteNotebookMetadata(ctx, m.StableKey); err != nil {
		t.Fatal(err)
	}
	if _, err := store.GetNotebookMetadata(ctx, m.StableKey); err != ErrNotFound {
		t.Fatalf("metadata after delete: err=%v, want ErrNotFound", err)
	}
}

func TestRecordWorkerHealthTracksChecksAndFailures(t *testing.T) {
	store, err := Open(filepath.Join(t.TempDir(), "health.db"))
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	ctx := context.Background()
	workerID, _ := store.CreateWorker(ctx, WorkerNode{Name: "w1", Host: "10.0.0.1", Port: 22, Username: "root", AuthMode: "key"})

	checked1 := time.Date(2026, 9, 25, 2, 0, 0, 0, time.UTC)
	if err := store.RecordWorkerHealth(ctx, workerID, false, checked1, "timeout", 2); err != nil {
		t.Fatal(err)
	}
	w, _ := store.GetWorker(ctx, workerID)
	if w.Status != "unknown" || w.HealthFailures != 1 || w.LastCheckedAt == nil || !w.LastCheckedAt.Equal(checked1) {
		t.Fatalf("first failed check wrong: %+v", w)
	}
	checked2 := checked1.Add(time.Minute)
	if err := store.RecordWorkerHealth(ctx, workerID, false, checked2, "timeout", 2); err != nil {
		t.Fatal(err)
	}
	w, _ = store.GetWorker(ctx, workerID)
	if w.Status != "offline" || w.HealthFailures != 2 || w.StatusError == nil {
		t.Fatalf("second failed check wrong: %+v", w)
	}
	checked3 := checked2.Add(time.Minute)
	if err := store.RecordWorkerHealth(ctx, workerID, true, checked3, "", 2); err != nil {
		t.Fatal(err)
	}
	w, _ = store.GetWorker(ctx, workerID)
	if w.Status != "online" || w.HealthFailures != 0 || w.StatusError != nil || w.LastSeenAt == nil || !w.LastSeenAt.Equal(checked3) {
		t.Fatalf("successful check wrong: %+v", w)
	}
}
