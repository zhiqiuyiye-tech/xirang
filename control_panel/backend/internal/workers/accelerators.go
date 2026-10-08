package workers

import (
	"context"
	"encoding/csv"
	"errors"
	"fmt"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"time"

	"xirang/control_panel/internal/db"
)

// AcceleratorModel counts physical cards, not chips, processes or utilization.
type AcceleratorModel struct {
	Model       string `json:"model"`
	Count       int64  `json:"count"`
	DeviceCount int64  `json:"device_count"`
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
// Nodes normally have one accelerator vendor. Stop after a successful query;
// only fall back to NVIDIA when Ascend is absent or failed. Include the usual
// driver locations for non-interactive SSH sessions.
const acceleratorProbeCommand = `export LC_ALL=C
PATH="$PATH:/usr/local/sbin:/usr/sbin:/usr/local/Ascend/driver/tools:/usr/local/Ascend/driver/bin"
export PATH
found=0
failed=0
if command -v npu-smi >/dev/null 2>&1; then
 found=1
 printf '__NPU__\n'
 npu-smi info 2>&1
 code=$?
 printf '\n__NPU_EXIT__=%s\n' "$code"
 if [ "$code" = 0 ]; then printf '__SELECTED__=npu-smi\n'; exit 0; fi
 if [ "$code" != 0 ]; then printf 'npu-smi info failed (exit=%s)\n' "$code" >&2; failed=1; fi
fi
if command -v nvidia-smi >/dev/null 2>&1; then
 found=1
 printf '__NVIDIA__\n'
 nvidia-smi --query-gpu=uuid,name --format=csv,noheader,nounits 2>&1
 code=$?
 printf '\n__NVIDIA_EXIT__=%s\n' "$code"
 if [ "$code" = 0 ]; then printf '__SELECTED__=nvidia-smi\n'; exit 0; fi
 if [ "$code" != 0 ]; then printf 'nvidia-smi query failed (exit=%s)\n' "$code" >&2; failed=1; fi
fi
if [ "$found" = 0 ]; then printf '__UNSUPPORTED__\n'; fi
exit "$failed"`

func (s *Service) DiscoverAccelerators(parent context.Context, w db.WorkerNode) AcceleratorInfo {
	info := AcceleratorInfo{Status: "unknown", Devices: []AcceleratorModel{}, CheckedAt: time.Now().UTC()}
	ctx, cancel := context.WithTimeout(parent, s.acceleratorTimeout)
	defer cancel()
	stdout, stderr, code, err := s.sshm.Run(ctx, w, acceleratorProbeCommand)
	if err != nil {
		if errors.Is(err, context.DeadlineExceeded) {
			info.Error = fmt.Sprintf("SSH 设备采集超时（总预算 %s，WORKER_ACCELERATOR_TIMEOUT）: %s", s.acceleratorTimeout, acceleratorDiagnostic(err.Error()))
		} else {
			info.Error = "SSH 设备采集失败: " + acceleratorDiagnostic(err.Error())
		}
		return info
	}
	if code != 0 && !strings.Contains(stdout, "__NPU_EXIT__=") && !strings.Contains(stdout, "__NVIDIA_EXIT__=") {
		info.Error = fmt.Sprintf("设备查询命令执行失败（exit=%d）", code)
		if detail := acceleratorDiagnostic(stderr); detail != "" {
			info.Error += ": " + detail
		}
		// Some driver tools print failures to stdout, so retaining stderr
		// alone would still hide the actual cause. Never return unbounded output.
		if detail := acceleratorDiagnostic(stdout); detail != "" {
			info.Error += "；stdout: " + detail
		}
		return info
	}
	var source, selectedSource string
	var section strings.Builder
	var sources, warnings []string
	sectionExit := 0
	flush := func() {
		if source == "" {
			return
		}
		output := section.String()
		section.Reset()
		if sectionExit != 0 {
			warnings = append(warnings, fmt.Sprintf("%s 查询失败（exit=%d）: %s", source, sectionExit, acceleratorDiagnostic(output)))
			return
		}
		var devices []AcceleratorModel
		var parseErr error
		if source == "npu-smi" {
			devices, parseErr = parseNPUCards(output)
		} else {
			devices, parseErr = parseNVIDIACards(output)
		}
		if parseErr != nil {
			warnings = append(warnings, source+" 查询结果无法识别: "+acceleratorDiagnostic(output))
			return
		}
		info.Devices = append(info.Devices, devices...)
		sources = append(sources, source)
	}
	for _, line := range strings.Split(stdout, "\n") {
		line = strings.TrimSpace(line)
		if line == "__NPU__" || line == "__NVIDIA__" {
			flush()
			sectionExit = 0
			if line == "__NPU__" {
				source = "npu-smi"
			} else {
				source = "nvidia-smi"
			}
		} else if strings.HasPrefix(line, "__SELECTED__=") {
			selectedSource = strings.TrimPrefix(line, "__SELECTED__=")
		} else if (source == "npu-smi" && strings.HasPrefix(line, "__NPU_EXIT__=")) || (source == "nvidia-smi" && strings.HasPrefix(line, "__NVIDIA_EXIT__=")) {
			value := strings.SplitN(line, "=", 2)[1]
			parsed, parseErr := strconv.Atoi(value)
			if parseErr != nil {
				sectionExit = -1
			} else {
				sectionExit = parsed
			}
		} else if source != "" {
			section.WriteString(line + "\n")
		}
	}
	flush()
	// Under the single-vendor policy, confirmed cards from the selected tool
	// make failures of the other vendor irrelevant. An empty or unrecognized
	// fallback must still retain the original failure rather than claiming zero.
	if len(sources) == 1 && sources[0] == selectedSource && len(info.Devices) > 0 {
		warnings = nil
	}
	info.Error = strings.Join(warnings, "；")
	info.Source = strings.Join(sources, ", ")
	if len(sources) == 0 {
		if info.Error == "" {
			info.Error = "未找到 npu-smi 或 nvidia-smi"
		}
		return info
	}
	// A failure of one installed tool must not discard another tool's valid
	// models. Keep the complete physical total unknown when a vendor failed.
	if len(warnings) > 0 {
		info.Status = "partial"
		return info
	}
	var total int64
	for _, device := range info.Devices {
		total += device.Count
	}
	info.Status = "available"
	info.Total = &total
	return info
}

// acceleratorDiagnostic bounds each diagnostic by characters, preserving UTF-8.
// The fixed read-only probe does not interpolate credentials into command output.
func acceleratorDiagnostic(message string) string {
	message = strings.Join(strings.Fields(message), " ")
	chars := []rune(message)
	if len(chars) > 512 {
		return string(chars[:512]) + "…"
	}
	return message
}

var npuCardRow = regexp.MustCompile(`^(\d+)\s+([A-Za-z0-9][A-Za-z0-9 _.-]*)$`)
var npuChipRow = regexp.MustCompile(`^(\d+)\s+(\d+)$`)
var pciBusID = regexp.MustCompile(`^[0-9A-Fa-f]{4}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}\.[0-7]$`)

func parseNPUCards(output string) ([]AcceleratorModel, error) {
	cards := map[string]string{}
	physicalDevices := map[string]string{}
	currentModel := ""
	for _, line := range strings.Split(output, "\n") {
		columns := strings.Split(line, "|")
		if len(columns) < 4 {
			continue
		}
		if currentModel != "" && pciBusID.MatchString(strings.TrimSpace(columns[2])) {
			if chip := npuChipRow.FindStringSubmatch(strings.TrimSpace(columns[1])); len(chip) == 3 {
				physicalDevices[chip[2]] = currentModel
			}
			continue
		}
		if strings.Contains(columns[1], "NPU") {
			currentModel = ""
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
		currentModel = model
	}
	if len(cards) == 0 {
		return nil, errors.New("no recognized NPU cards")
	}
	devices := groupAcceleratorModels(cards)
	chipCounts := map[string]int64{}
	for _, model := range physicalDevices {
		chipCounts[model]++
	}
	for i := range devices {
		devices[i].DeviceCount = chipCounts[devices[i].Model]
	}
	return devices, nil
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
		devices = append(devices, AcceleratorModel{Model: model, Count: counts[model], DeviceCount: counts[model]})
	}
	return devices
}
