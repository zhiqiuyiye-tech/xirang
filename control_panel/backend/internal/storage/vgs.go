package storage

import (
	"context"
	"fmt"
	"strconv"
	"strings"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
)

// VGInfo is a volume group on a worker node, with its total and free space.
type VGInfo struct {
	Name   string `json:"name"`
	VSize  string `json:"vsize"`  // e.g. "3.50g"
	VFree  string `json:"vfree"`  // e.g. "2.30g"
	FreeGB float64 `json:"free_gb"` // numeric free in GB for UI sizing
}

// vgsCmd outputs VG/VSize/VFree as CSV (gigabyte units, no headers).
// Example row: vg_data,3.50g,2.30g
const vgsCmd = "vgs --units g --noheadings --nosuffix --separator , -o vg_name,vg_size,vg_free 2>/dev/null"

// ListVGs SSHes to the worker and returns its volume groups with free space.
func ListVGs(ctx context.Context, runner ssh.Runner, w db.WorkerNode) ([]VGInfo, error) {
	out, stderr, code, err := runner.Run(ctx, w, vgsCmd)
	if err != nil {
		return nil, fmt.Errorf("vgs: %w (stderr: %s)", err, stderr)
	}
	if code != 0 {
		return nil, fmt.Errorf("vgs exited %d: %s", code, stderr)
	}
	var vgs []VGInfo
	for _, line := range strings.Split(out, "\n") {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		parts := strings.Split(line, ",")
		if len(parts) < 3 {
			continue
		}
		name := strings.TrimSpace(parts[0])
		vsize := strings.TrimSpace(parts[1])
		vfree := strings.TrimSpace(parts[2])
		freeGB, _ := strconv.ParseFloat(strings.TrimSuffix(strings.TrimSpace(vfree), "g"), 64)
		vgs = append(vgs, VGInfo{Name: name, VSize: vsize, VFree: vfree, FreeGB: freeGB})
	}
	return vgs, nil
}
