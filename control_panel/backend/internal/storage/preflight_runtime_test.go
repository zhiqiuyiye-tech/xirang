package storage

import (
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"sort"
	"strconv"
	"strings"
	"testing"
	"time"
)

const preflightDeviceMarker = "@DEVICE@"

type preflightCommandResult struct {
	output string
	status int
}

type preflightRuntimeFixture struct {
	name     string
	lsblk    map[string]preflightCommandResult
	findmnt  map[string]preflightCommandResult
	wantSafe bool
}

func TestPreflightDeviceFullCommandWithFixtures(t *testing.T) {
	cases := []preflightRuntimeFixture{
		{
			name:     "unused whole disk is safe",
			lsblk:    unusedDiskPreflightFixture(),
			findmnt:  noFindmntMatches(preflightDeviceMarker, "/dev/sdb", "/dev/sdb1"),
			wantSafe: true,
		},
		{
			name:     "unused spare partition with proven disk parent is safe",
			lsblk:    unusedPartitionPreflightFixture(),
			findmnt:  noFindmntMatches(preflightDeviceMarker),
			wantSafe: true,
		},
		{
			name: "system mount on partition ancestor is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["MOUNTPOINT|/dev/sda"] = preflightCommandResult{output: "/\n"}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "selected type query failure is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["TYPE|"+preflightDeviceMarker] = preflightCommandResult{output: "part\n", status: 2}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "ambiguous selected type is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["TYPE|"+preflightDeviceMarker] = preflightCommandResult{output: "part\ndisk\n"}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "partition parent query failure is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["PKNAME|"+preflightDeviceMarker] = preflightCommandResult{status: 2}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "multiple partition parents are rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["PKNAME|"+preflightDeviceMarker] = preflightCommandResult{output: "sda\nsdb\n"}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "partition without a parent is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["PKNAME|"+preflightDeviceMarker] = preflightCommandResult{}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "ancestor type query failure is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["TYPE|/dev/sda"] = preflightCommandResult{status: 2}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "cyclic ancestry is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["TYPE|/dev/sda"] = preflightCommandResult{output: "part\n"}
				fixture["PKNAME|/dev/sda"] = preflightCommandResult{output: "sdb\n"}
				fixture["TYPE|/dev/sdb"] = preflightCommandResult{output: "part\n"}
				fixture["PKNAME|/dev/sdb"] = preflightCommandResult{output: "sda\n"}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "ancestor mountpoint query failure is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedPartitionPreflightFixture()
				fixture["MOUNTPOINT|/dev/sda"] = preflightCommandResult{status: 2}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name:     "device findmnt exit one with no output means unmounted",
			lsblk:    unusedPartitionPreflightFixture(),
			findmnt:  noFindmntMatches(preflightDeviceMarker),
			wantSafe: true,
		},
		{
			name:    "device findmnt empty exit zero is rejected",
			lsblk:   unusedPartitionPreflightFixture(),
			findmnt: map[string]preflightCommandResult{preflightDeviceMarker: {}},
		},
		{
			name:    "device findmnt unexpected status is rejected",
			lsblk:   unusedPartitionPreflightFixture(),
			findmnt: map[string]preflightCommandResult{preflightDeviceMarker: {status: 2}},
		},
		{
			name:    "device findmnt exit one with output is rejected",
			lsblk:   unusedPartitionPreflightFixture(),
			findmnt: map[string]preflightCommandResult{preflightDeviceMarker: {output: "/data02\n", status: 1}},
		},
		{
			name:    "mounted device is rejected",
			lsblk:   unusedPartitionPreflightFixture(),
			findmnt: map[string]preflightCommandResult{preflightDeviceMarker: {output: "/data02\n"}},
		},
		{
			name: "disk child query failure is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedDiskPreflightFixture()
				fixture["NAME|"+preflightDeviceMarker] = preflightCommandResult{status: 2}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "empty successful disk child query is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedDiskPreflightFixture()
				fixture["NAME|"+preflightDeviceMarker] = preflightCommandResult{}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name: "malformed disk child name is rejected",
			lsblk: func() map[string]preflightCommandResult {
				fixture := unusedDiskPreflightFixture()
				fixture["NAME|"+preflightDeviceMarker] = preflightCommandResult{output: "sdb\n../sda\n"}
				return fixture
			}(),
			findmnt: noFindmntMatches(preflightDeviceMarker),
		},
		{
			name:  "disk child findmnt failure is rejected",
			lsblk: unusedDiskPreflightFixture(),
			findmnt: map[string]preflightCommandResult{
				preflightDeviceMarker: {status: 1},
				"/dev/sdb":            {status: 1},
				"/dev/sdb1":           {status: 2},
			},
		},
	}

	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			output, runErr, sentinel := runPreflightRuntimeFixture(t, tc)
			if tc.wantSafe {
				if runErr != nil {
					t.Fatalf("healthy unused-device fixture rejected: %v; output: %s", runErr, output)
				}
				if !strings.Contains(output, "SAFE") || sentinel != "untouched\nproduction-change\n" {
					t.Fatalf("safe preflight did not proceed exactly once: output=%q sentinel=%q", output, sentinel)
				}
				return
			}
			if errors.Is(runErr, context.DeadlineExceeded) {
				t.Fatalf("preflight did not terminate promptly: %s", output)
			}
			if runErr == nil || strings.Contains(output, "SAFE") {
				t.Fatalf("unsafe or inconclusive fixture reached production change: output=%q sentinel=%q", output, sentinel)
			}
			if sentinel != "untouched\n" {
				t.Fatalf("preflight failure changed production sentinel: %q", sentinel)
			}
		})
	}
}

func unusedDiskPreflightFixture() map[string]preflightCommandResult {
	return map[string]preflightCommandResult{
		"TYPE|" + preflightDeviceMarker:       {output: "disk\n"},
		"PKNAME|" + preflightDeviceMarker:     {},
		"MOUNTPOINT|" + preflightDeviceMarker: {output: "\n"},
		"NAME|" + preflightDeviceMarker:       {output: "sdb\nsdb1\n"},
	}
}

func unusedPartitionPreflightFixture() map[string]preflightCommandResult {
	return map[string]preflightCommandResult{
		"TYPE|" + preflightDeviceMarker:   {output: "part\n"},
		"PKNAME|" + preflightDeviceMarker: {output: "sda\n"},
		"TYPE|/dev/sda":                   {output: "disk\n"},
		"PKNAME|/dev/sda":                 {},
		"MOUNTPOINT|/dev/sda":             {output: "\n"},
	}
}

func noFindmntMatches(devices ...string) map[string]preflightCommandResult {
	results := make(map[string]preflightCommandResult, len(devices))
	for _, device := range devices {
		results[device] = preflightCommandResult{status: 1}
	}
	return results
}

func runPreflightRuntimeFixture(t *testing.T, fixture preflightRuntimeFixture) (string, error, string) {
	t.Helper()
	shell := findPOSIXShell(t)
	_ = runtime.GOOS
	dir := t.TempDir()
	devicePath := filepath.ToSlash(filepath.Join(dir, "fixture-device"))
	sentinelPath := filepath.ToSlash(filepath.Join(dir, "production-sentinel"))
	if err := os.WriteFile(devicePath, []byte("block-device stand-in"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(sentinelPath, []byte("untouched\n"), 0600); err != nil {
		t.Fatal(err)
	}

	command := PreflightDeviceCmd("/dev/sdb", []string{"/data01"})
	const blockCheck = `test -b "$device"`
	if !strings.Contains(command, `device='/dev/sdb'`) || !strings.Contains(command, blockCheck) {
		t.Fatal("preflight device identity or block check changed; update explicit fixture substitution")
	}
	command = strings.Replace(command, `device='/dev/sdb'`, "device="+shellLiteral(devicePath), 1)
	command = strings.Replace(command, blockCheck, `[ -f "$device" ]`, 1)

	mockScript := preflightFixtureMocks(devicePath, fixture)
	script := mockScript + "\n" + command + "\nstatus=$?\n" +
		"if [ \"$status\" -eq 0 ]; then printf '%s\\n' 'production-change' >> " + shellLiteral(sentinelPath) + "; fi\n" +
		"exit \"$status\"\n"
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	output, runErr := exec.CommandContext(ctx, shell, "-c", script).CombinedOutput()
	if errors.Is(ctx.Err(), context.DeadlineExceeded) {
		runErr = context.DeadlineExceeded
	}
	sentinel, err := os.ReadFile(sentinelPath)
	if err != nil {
		t.Fatal(err)
	}
	return string(output), runErr, string(sentinel)
}

func preflightFixtureMocks(devicePath string, fixture preflightRuntimeFixture) string {
	var script strings.Builder
	script.WriteString(`lsblk() {
  column=
  target=
  while [ "$#" -gt 0 ]; do
    case "$1" in
      -o) shift; column=$1 ;;
      -*) ;;
      *) target=$1 ;;
    esac
    shift
  done
  case "$column|$target" in
`)
	lsblkKeys := make([]string, 0, len(fixture.lsblk))
	for key := range fixture.lsblk {
		lsblkKeys = append(lsblkKeys, strings.ReplaceAll(key, preflightDeviceMarker, devicePath))
	}
	sort.Strings(lsblkKeys)
	lsblkResults := make(map[string]preflightCommandResult, len(fixture.lsblk))
	for key, result := range fixture.lsblk {
		lsblkResults[strings.ReplaceAll(key, preflightDeviceMarker, devicePath)] = result
	}
	for _, key := range lsblkKeys {
		result := lsblkResults[key]
		fmt.Fprintf(&script, "    %s) printf '%%s' %s; return %s ;;\n", shellLiteral(key), shellLiteral(result.output), strconv.Itoa(result.status))
	}
	script.WriteString(`    *) printf 'unexpected lsblk probe: %s\n' "$column|$target" >&2; return 97 ;;
  esac
}
`)

	script.WriteString(`findmnt() {
  target=
  for arg do target=$arg; done
  case "$target" in
`)
	findmntKeys := make([]string, 0, len(fixture.findmnt))
	for key := range fixture.findmnt {
		findmntKeys = append(findmntKeys, strings.ReplaceAll(key, preflightDeviceMarker, devicePath))
	}
	sort.Strings(findmntKeys)
	findmntResults := make(map[string]preflightCommandResult, len(fixture.findmnt))
	for key, result := range fixture.findmnt {
		findmntResults[strings.ReplaceAll(key, preflightDeviceMarker, devicePath)] = result
	}
	for _, key := range findmntKeys {
		result := findmntResults[key]
		fmt.Fprintf(&script, "    %s) printf '%%s' %s; return %s ;;\n", shellLiteral(key), shellLiteral(result.output), strconv.Itoa(result.status))
	}
	script.WriteString(`    *) printf 'unexpected findmnt probe: %s\n' "$target" >&2; return 97 ;;
  esac
}
`)
	script.WriteString("wipefs() { return 0; }\n")
	script.WriteString("head() { IFS= read -r first || :; printf '%s\\n' \"$first\"; return 0; }\n")
	return script.String()
}
