package workers

import (
	"context"
	"encoding/csv"
	"errors"
	"fmt"
	"regexp"
	"sort"
	"strings"
	"time"

	"xirang/control_panel/internal/db"
)

// AcceleratorModel counts physical cards, not chips, processes or utilization.
type AcceleratorModel struct {
	Model string `json:"model"`
	Count int64  `json:"count"`
}

type AcceleratorInfo struct {
	Status    string             `json:"status"`
	Devices   []AcceleratorModel `json:"devices"`
	Total     *int64             `json:"total"`
	Source    string             `json:"source,omitempty"`
	Error     string             `json:"error,omitempty"`
	CheckedAt time.Time          `json:"checked_at"`
}

// These read-only commands are fixed strings; no user input enters the shell.
// Include the usual driver locations for non-interactive SSH sessions.
const acceleratorProbeCommand = `export LC_ALL=C
PATH="$PATH:/usr/local/sbin:/usr/sbin:/usr/local/Ascend/driver/tools:/usr/local/Ascend/driver/bin"
export PATH
found=0
failed=0
if command -v npu-smi >/dev/null 2>&1; then
 found=1
 printf '__NPU__\n'
 npu-smi info || failed=1
fi
if command -v nvidia-smi >/dev/null 2>&1; then
 found=1
 printf '__NVIDIA__\n'
 nvidia-smi --query-gpu=uuid,name --format=csv,noheader,nounits || failed=1
fi
if [ "$found" = 0 ]; then printf '__UNSUPPORTED__\n'; fi
exit "$failed"`

func (s *Service) DiscoverAccelerators(parent context.Context, w db.WorkerNode) AcceleratorInfo {
	info := AcceleratorInfo{Status: "unknown", Devices: []AcceleratorModel{}, CheckedAt: time.Now().UTC()}
	ctx, cancel := context.WithTimeout(parent, 8*time.Second)
	defer cancel()
	stdout, _, code, err := s.sshm.Run(ctx, w, acceleratorProbeCommand)
	if err != nil {
		info.Error = "SSH 设备采集失败"
		return info
	}
	if code != 0 {
		info.Error = "设备查询命令执行失败，请检查驱动和权限"
		return info
	}
	var source string
	var section strings.Builder
	var sources []string
	flush := func() error {
		if source == "" {
			return nil
		}
		var devices []AcceleratorModel
		var parseErr error
		if source == "npu-smi" {
			devices, parseErr = parseNPUCards(section.String())
		} else {
			devices, parseErr = parseNVIDIACards(section.String())
		}
		if parseErr != nil {
			return parseErr
		}
		info.Devices = append(info.Devices, devices...)
		sources = append(sources, source)
		section.Reset()
		return nil
	}
	for _, line := range strings.Split(stdout, "\n") {
		line = strings.TrimSpace(line)
		if line == "__NPU__" || line == "__NVIDIA__" {
			if err := flush(); err != nil {
				info.Error = "无法识别设备查询结果"
				info.Devices = []AcceleratorModel{}
				return info
			}
			if line == "__NPU__" {
				source = "npu-smi"
			} else {
				source = "nvidia-smi"
			}
		} else if source != "" {
			section.WriteString(line + "\n")
		}
	}
	if err := flush(); err != nil {
		info.Error = "无法识别设备查询结果"
		info.Devices = []AcceleratorModel{}
		return info
	}
	if len(sources) == 0 {
		info.Error = "未找到 npu-smi 或 nvidia-smi"
		return info
	}
	var total int64
	for _, device := range info.Devices {
		total += device.Count
	}
	info.Status = "available"
	info.Total = &total
	info.Source = strings.Join(sources, ", ")
	return info
}

var npuCardRow = regexp.MustCompile(`^(\d+)\s+([A-Za-z0-9][A-Za-z0-9 _.-]*)$`)

func parseNPUCards(output string) ([]AcceleratorModel, error) {
	cards := map[string]string{}
	for _, line := range strings.Split(output, "\n") {
		columns := strings.Split(line, "|")
		if len(columns) < 4 {
			continue
		}
		match := npuCardRow.FindStringSubmatch(strings.TrimSpace(columns[1]))
		if len(match) != 3 {
			continue
		}
		model := strings.TrimSpace(match[2])
		// Card rows have a health field. Chip continuation rows have a bus
		// address here, and process rows have a process name. This also allows
		// older numeric card models such as 310/910 without counting chip IDs.
		health := strings.ToLower(strings.TrimSpace(columns[2]))
		if health != "ok" && health != "warning" && health != "alarm" && health != "critical" && health != "unknown" && health != "error" {
			continue
		}
		if !strings.HasPrefix(strings.ToLower(model), "ascend") {
			model = "Ascend " + model
		}
		cards[match[1]] = model
	}
	if len(cards) == 0 {
		return nil, errors.New("no recognized NPU cards")
	}
	return groupAcceleratorModels(cards), nil
}

func parseNVIDIACards(output string) ([]AcceleratorModel, error) {
	rows, err := csv.NewReader(strings.NewReader(output)).ReadAll()
	if err != nil {
		return nil, err
	}
	cards := map[string]string{}
	for _, row := range rows {
		if len(row) != 2 || !strings.HasPrefix(strings.TrimSpace(row[0]), "GPU-") || strings.TrimSpace(row[1]) == "" {
			return nil, fmt.Errorf("invalid GPU row")
		}
		cards[strings.TrimSpace(row[0])] = strings.TrimSpace(row[1])
	}
	// A successful empty NVIDIA query explicitly reports zero visible cards.
	return groupAcceleratorModels(cards), nil
}

func groupAcceleratorModels(cards map[string]string) []AcceleratorModel {
	counts := map[string]int64{}
	for _, model := range cards {
		counts[model]++
	}
	models := make([]string, 0, len(counts))
	for model := range counts {
		models = append(models, model)
	}
	sort.Strings(models)
	devices := make([]AcceleratorModel, 0, len(models))
	for _, model := range models {
		devices = append(devices, AcceleratorModel{Model: model, Count: counts[model]})
	}
	return devices
}
