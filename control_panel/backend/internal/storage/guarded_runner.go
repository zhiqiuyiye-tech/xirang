package storage

import (
	"context"
	"fmt"
	"io"
	"sync"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
)

// The remote marker outlives the executor when termination is unconfirmed.
// The local quarantine also covers loss of SSH before marker creation is known.
const recoveryWorkerGate = `# cp-storage-recovery-gate
if [ -e /run/control-panel-storage-recovery.uncertain ]; then
  echo "storage recovery state is uncertain; verify the remote executor and mounts before removing /run/control-panel-storage-recovery.uncertain" >&2
  exit 75
fi
`

type guardedStorageRunner struct {
	ssh.Runner
	uncertain sync.Map
}

func (g *guardedStorageRunner) BlockWorker(workerID int64, reason string) {
	g.uncertain.Store(workerID, reason)
}
func (g *guardedStorageRunner) checkWorker(w db.WorkerNode) error {
	if reason, ok := g.uncertain.Load(w.ID); ok {
		return fmt.Errorf("worker storage operations blocked pending verification of remote executor: %v; verify the worker and restart the backend only after confirmed termination", reason)
	}
	return nil
}
func (g *guardedStorageRunner) Run(ctx context.Context, w db.WorkerNode, cmd string) (string, string, int, error) {
	if err := g.checkWorker(w); err != nil {
		return "", "", -1, err
	}
	return g.Runner.Run(ctx, w, recoveryWorkerGate+cmd)
}
func (g *guardedStorageRunner) RunWithStdin(ctx context.Context, w db.WorkerNode, cmd string, in io.Reader) (string, string, int, error) {
	if err := g.checkWorker(w); err != nil {
		return "", "", -1, err
	}
	return g.Runner.RunWithStdin(ctx, w, recoveryWorkerGate+cmd, in)
}
