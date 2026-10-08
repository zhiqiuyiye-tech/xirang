package workers

import (
	"context"
	"errors"
	"strings"
	"testing"

	"xirang/control_panel/internal/db"
)

const npuSample = `+----------------------------------------------------------------------------------+
| npu-smi 24.1.0                    Version: 24.1.0                                |
| NPU     Name                     | Health                | Power(W)              |
| Chip    Device                   | Bus-Id                | AICore(%)             |
| 0       910B4                    | OK                    | 90.1                  |
| 0       0                        | 0000:81:00.0          | 0                     |
| 1       910B4                    | OK                    | 90.2                  |
| 0       1                        | 0000:82:00.0          | 0                     |
+----------------------------------------------------------------------------------+
| NPU     Chip       Process id    | Process name          | Process memory(MB)    |
| 0       0          12345         | python                | 1000                  |
| 1       0          67890         | python                | 1000                  |
+----------------------------------------------------------------------------------+`

type acceleratorSSHStub struct {
	workerSSHStub
	output string
	code   int
	err    error
	calls  int
}

func (s *acceleratorSSHStub) Run(ctx context.Context, w db.WorkerNode, cmd string) (string, string, int, error) {
	s.calls++
	if !strings.Contains(cmd, "npu-smi info") || !strings.Contains(cmd, "nvidia-smi") {
		return "", "", 1, errors.New("missing device discovery commands")
	}
	return s.output, "", s.code, s.err
}

func TestParseNPUCards(t *testing.T) {
	devices, err := parseNPUCards(npuSample)
	if err != nil || len(devices) != 1 || devices[0].Model != "Ascend 910B4" || devices[0].Count != 2 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}
func TestNPUCountsPhysicalCardsOnceAcrossChips(t *testing.T) {
	devices, err := parseNPUCards(npuSample + "\n| 0 910B4 | OK | 90 |\n| 1 910B4 | OK | 90 |\n| 2 Ascend 310P | OK | 20 |")
	if err != nil || len(devices) != 2 || devices[0].Model != "Ascend 310P" || devices[0].Count != 1 || devices[1].Model != "Ascend 910B4" || devices[1].Count != 2 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}
func TestNPUNumericModelAndChipContinuation(t *testing.T) {
	devices, err := parseNPUCards("| 0 910 | OK | 90 |\n| 0 0 | 0000:81:00.0 | 0 |\n| 1 310 | Warning | 20 |\n| 0 1 | 0000:82:00.0 | 0 |")
	if err != nil || len(devices) != 2 || devices[0].Model != "Ascend 310" || devices[0].Count != 1 || devices[1].Model != "Ascend 910" || devices[1].Count != 1 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
}

func TestNPUUnrecognizedOutputIsUnknown(t *testing.T) {
	for _, output := range []string{"", "npu-smi: driver unavailable", "| 0 0 123 | python | 1024 |"} {
		if _, err := parseNPUCards(output); err == nil {
			t.Fatalf("accepted invalid output %q", output)
		}
	}
}
func TestParseNVIDIACards(t *testing.T) {
	devices, err := parseNVIDIACards("GPU-a, NVIDIA A100-SXM4-80GB\nGPU-b, NVIDIA A100-SXM4-80GB\nGPU-c, NVIDIA H100 PCIe\n")
	if err != nil || len(devices) != 2 || devices[0].Count != 2 || devices[1].Count != 1 {
		t.Fatalf("devices=%+v err=%v", devices, err)
	}
	if _, err := parseNVIDIACards("driver failed"); err == nil {
		t.Fatal("accepted invalid output")
	}
}
func TestDiscoverAccelerators(t *testing.T) {
	cases := []struct {
		name, output string
		code         int
		sshErr       error
		status       string
		total        int64
	}{
		{name: "npu", output: "__NPU__\n" + npuSample, status: "available", total: 2},
		{name: "nvidia", output: "__NVIDIA__\nGPU-a, NVIDIA A100\n", status: "available", total: 1},
		{name: "zero cards", output: "__NVIDIA__\n", status: "available", total: 0},
		{name: "both", output: "__NPU__\n" + npuSample + "\n__NVIDIA__\nGPU-a, NVIDIA A100\n", status: "available", total: 3},
		{name: "unsupported", output: "__UNSUPPORTED__\n", status: "unknown"},
		{name: "driver failure", output: "__NPU__\ndriver unavailable", code: 1, status: "unknown"},
		{name: "ssh failure", sshErr: errors.New("connection failed"), status: "unknown"},
	}
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			svc := setup(t)
			stub := &acceleratorSSHStub{output: tc.output, code: tc.code, err: tc.sshErr}
			svc.sshm = stub
			got := svc.DiscoverAccelerators(context.Background(), db.WorkerNode{ID: 1})
			if got.Status != tc.status {
				t.Fatalf("got %+v", got)
			}
			if tc.status == "available" && (got.Total == nil || *got.Total != tc.total) {
				t.Fatalf("got %+v", got)
			}
			if tc.status == "unknown" && (got.Total != nil || got.Error == "") {
				t.Fatalf("failure should have unknown count: %+v", got)
			}
		})
	}
}
