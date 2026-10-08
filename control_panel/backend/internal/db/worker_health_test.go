package db

import (
	"context"
	"testing"
	"time"
)

func TestWorkerHealthRejectsOutOfOrderChecks(t *testing.T) {
	for _, latestOnline := range []bool{true, false} {
		t.Run(map[bool]string{true: "newer_success", false: "newer_failure"}[latestOnline], func(t *testing.T) {
			s := newStore(t)
			ctx := context.Background()
			id, err := s.CreateWorker(ctx, WorkerNode{Name: "w", Host: "h", Port: 22, Username: "root"})
			if err != nil {
				t.Fatal(err)
			}
			// Sub-millisecond precision matters when inventory and heartbeat run together.
			old := time.Date(2026, 10, 8, 0, 0, 0, 100, time.UTC)
			latest := old.Add(time.Nanosecond)
			if err := s.RecordWorkerHealth(ctx, id, latestOnline, latest, "newer failure", 1); err != nil {
				t.Fatal(err)
			}
			before, err := s.GetWorker(ctx, id)
			if err != nil {
				t.Fatal(err)
			}
			for _, at := range []time.Time{old, old.In(time.FixedZone("offset", 8*60*60))} {
				if err := s.RecordWorkerHealth(ctx, id, !latestOnline, at, "stale result", 1); err != nil {
					t.Fatal(err)
				}
				after, err := s.GetWorker(ctx, id)
				if err != nil {
					t.Fatal(err)
				}
				if after.Status != before.Status || after.HealthFailures != before.HealthFailures || !after.LastCheckedAt.Equal(*before.LastCheckedAt) || !after.UpdatedAt.Equal(before.UpdatedAt) {
					t.Fatalf("stale health check overwrote latest state: before=%+v after=%+v", before, after)
				}
			}
		})
	}
}

func TestWorkerHealthSameTimestampCountsDistinctChecks(t *testing.T) {
	s := newStore(t)
	ctx := context.Background()
	id, err := s.CreateWorker(ctx, WorkerNode{Name: "w", Host: "h", Port: 22, Username: "root"})
	if err != nil {
		t.Fatal(err)
	}
	at := time.Now().UTC()
	// time.Now can repeat on Windows; separate probes must still reach the threshold.
	for i := 0; i < 2; i++ {
		if err := s.RecordWorkerHealth(ctx, id, false, at, "refused", 2); err != nil {
			t.Fatal(err)
		}
	}
	w, err := s.GetWorker(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "offline" || w.HealthFailures != 2 {
		t.Fatalf("equal-timestamp checks failed to reach threshold: %+v", w)
	}
	if err := s.RecordWorkerHealth(ctx, id, true, at, "", 2); err != nil {
		t.Fatal(err)
	}
	w, err = s.GetWorker(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "online" || w.HealthFailures != 0 {
		t.Fatalf("equal-timestamp recovery ignored: %+v", w)
	}
}

func TestWorkerHealthFailureThresholdAndRecovery(t *testing.T) {
	s := newStore(t)
	ctx := context.Background()
	id, err := s.CreateWorker(ctx, WorkerNode{Name: "w", Host: "h", Port: 22, Username: "root"})
	if err != nil {
		t.Fatal(err)
	}
	at := time.Now().UTC()
	if err := s.RecordWorkerHealth(ctx, id, true, at, "", 2); err != nil {
		t.Fatal(err)
	}
	for failures := 1; failures <= 2; failures++ {
		if err := s.RecordWorkerHealth(ctx, id, false, at.Add(time.Duration(failures)*time.Second), "connection refused", 2); err != nil {
			t.Fatal(err)
		}
		w, err := s.GetWorker(ctx, id)
		if err != nil {
			t.Fatal(err)
		}
		want := "online"
		if failures == 2 {
			want = "offline"
		}
		if w.Status != want || w.HealthFailures != failures || !w.LastSeenAt.Equal(at) {
			t.Fatalf("threshold violated: %+v", w)
		}
	}
	if err := s.RecordWorkerHealth(ctx, id, true, at.Add(3*time.Second), "", 2); err != nil {
		t.Fatal(err)
	}
	w, err := s.GetWorker(ctx, id)
	if err != nil {
		t.Fatal(err)
	}
	if w.Status != "online" || w.HealthFailures != 0 || w.StatusError != nil {
		t.Fatalf("success did not reset failures: %+v", w)
	}
}
