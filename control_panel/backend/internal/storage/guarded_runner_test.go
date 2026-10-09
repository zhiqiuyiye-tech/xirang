package storage

import (
	"context"
	"io"
	"strings"
	"testing"

	"xirang/control_panel/internal/db"
)

type gateRecordingRunner struct {
	cmd   string
	input string
}

func (g *gateRecordingRunner) Run(_ context.Context, _ db.WorkerNode, cmd string) (string, string, int, error) {
	g.cmd = cmd
	return "out", "err", 75, nil
}
func (g *gateRecordingRunner) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, in io.Reader) (string, string, int, error) {
	data, _ := io.ReadAll(in)
	g.input = string(data)
	return g.Run(ctx, w, cmd)
}
func TestGuardedRunnerLocallyBlocksUnknownExecutorState(t *testing.T) {
	raw := &gateRecordingRunner{}
	guard := &guardedStorageRunner{Runner: raw}
	guard.BlockWorker(9, "executor termination unconfirmed")
	if _, _, _, err := guard.Run(context.Background(), db.WorkerNode{ID: 9}, "lvremove -f /dev/vg/lv"); err == nil {
		t.Fatal("unknown executor state permitted a new command")
	}
	if raw.cmd != "" {
		t.Fatal("blocked command reached SSH")
	}
}

func TestGuardedStorageRunnerChecksUncertainMarkerBeforeCommands(t *testing.T) {
	raw := &gateRecordingRunner{}
	guard := &guardedStorageRunner{Runner: raw}
	out, stderr, code, err := guard.Run(context.Background(), db.WorkerNode{}, "lvremove -f /dev/vg/lv")
	if !strings.HasPrefix(raw.cmd, "# cp-storage-recovery-gate\n") || !strings.Contains(raw.cmd, "/run/control-panel-storage-recovery.uncertain") || strings.Index(raw.cmd, "exit 75") > strings.Index(raw.cmd, "lvremove") {
		t.Fatalf("missing gate: %s", raw.cmd)
	}
	if out != "out" || stderr != "err" || code != 75 || err != nil {
		t.Fatal("result not preserved")
	}
	_, _, _, _ = guard.RunWithStdin(context.Background(), db.WorkerNode{}, "remote-helper", strings.NewReader("payload"))
	if raw.input != "payload" || !strings.Contains(raw.cmd, "exit 75") {
		t.Fatal("stdin command bypassed gate")
	}
}
