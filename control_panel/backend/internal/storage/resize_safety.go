package storage

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"path"
	"strings"
)

type lvResizeSafetyState struct {
	MountTargets    []string `json:"mount_targets"`
	FstabTargets    []string `json:"fstab_targets"`
	SwapActive      bool     `json:"swap_active"`
	DeviceOpenCount int      `json:"device_open_count"`
}

// buildLVResizeSafetyCommand returns a read-only remote probe for an LV. An
// invalid path produces a fixed failing command, so untrusted input is never
// interpolated into the shell script.
func buildLVResizeSafetyCommand(lvDev string) string {
	parts := strings.Split(lvDev, "/")
	if len(parts) != 4 || parts[0] != "" || parts[1] != "dev" ||
		ValidateLVComponent(parts[2]) != nil || ValidateLVComponent(parts[3]) != nil {
		return `printf '%s\n' 'invalid logical volume device path' >&2; exit 1`
	}

	return "device=" + shellLiteral(lvDev) + `
LC_ALL=C
export LC_ALL

fail() {
  printf '%s\n' "$1" >&2
  exit 1
}

targets_to_json() {
  first=1
  printf '['
  while IFS= read -r target || [ -n "$target" ]; do
    [ -n "$target" ] || fail 'empty target in safety probe output'
    case "$target" in
      /*) ;;
      *) fail 'invalid target in safety probe output' ;;
    esac
    case "$target" in
      *[!A-Za-z0-9_/-]*) fail 'unrepresentable target in safety probe output' ;;
    esac
    if [ "$first" -eq 0 ]; then printf ','; fi
    printf '"%s"' "$target"
    first=0
  done
  printf ']'
}

fstab_targets_for_device() {
  printf '%s\n' "$1" | while IFS=' 	' read -r fstab_source fstab_target fstab_extra; do
    if [ -z "$fstab_source" ] && [ -z "$fstab_target" ] && [ -z "$fstab_extra" ]; then continue; fi
    [ -n "$fstab_source" ] && [ -n "$fstab_target" ] && [ -z "$fstab_extra" ] || fail 'fstab source and target data is malformed'
    case "$fstab_source" in
      /dev/*)
        fstab_resolved=$(readlink -f -- "$fstab_source" 2>/dev/null) || fail 'cannot resolve fstab device source'
        [ -n "$fstab_resolved" ] || fail 'resolved fstab device source is empty'
        if [ "$fstab_resolved" = "$resolved" ]; then printf '%s\n' "$fstab_target"; fi
        ;;
      UUID=*|LABEL=*|PARTUUID=*|PARTLABEL=*|uuid=*|label=*|partuuid=*|partlabel=*)
        fail 'fstab device source could not be evaluated'
        ;;
    esac
  done
}

resolved=$(readlink -f -- "$device" 2>/dev/null) || fail 'cannot resolve logical volume device'
[ -n "$resolved" ] || fail 'resolved logical volume device is empty'
[ -b "$resolved" ] || fail 'resolved logical volume is not a block device'

mount_raw=$(findmnt --raw --noheadings --output TARGET --source "$resolved" 2>/dev/null)
mount_status=$?
case "$mount_status" in
  0) [ -n "$mount_raw" ] || fail 'live mount probe returned no target data' ;;
  1) [ -z "$mount_raw" ] || fail 'live mount probe returned inconclusive target data' ;;
  *) fail 'live mount probe failed' ;;
esac
mount_targets=$(printf '%s' "$mount_raw" | targets_to_json) || fail 'cannot encode live mount targets'

[ -r /etc/fstab ] || fail 'fstab is unreadable'
fstab_raw=$(findmnt --fstab --evaluate --raw --noheadings --output SOURCE,TARGET 2>/dev/null)
fstab_status=$?
case "$fstab_status" in
  0) ;;
  1) [ -z "$fstab_raw" ] || fail 'fstab probe returned inconclusive data' ;;
  *) fail 'fstab probe failed' ;;
esac
fstab_candidates=$(fstab_targets_for_device "$fstab_raw") || fail 'cannot inspect evaluated fstab sources'
fstab_targets=$(printf '%s' "$fstab_candidates" | targets_to_json) || fail 'cannot encode fstab targets'

[ -r /proc/swaps ] || fail 'swap state is unreadable'
swap_active=false
{
  IFS=' 	' read -r header_name header_type header_size header_used header_priority || fail 'swap state has no header'
  [ "$header_name" = 'Filename' ] && [ "$header_type" = 'Type' ] &&
    [ "$header_size" = 'Size' ] && [ "$header_used" = 'Used' ] &&
    [ "$header_priority" = 'Priority' ] || fail 'swap state header is malformed'
  while IFS=' 	' read -r swap_source swap_type swap_size swap_used swap_priority; do
    [ -n "$swap_source" ] && [ -n "$swap_type" ] && [ -n "$swap_size" ] &&
      [ -n "$swap_used" ] && [ -n "$swap_priority" ] || fail 'swap state row is malformed'
    case "$swap_source" in
      /dev/*)
        swap_resolved=$(readlink -f -- "$swap_source" 2>/dev/null) || fail 'cannot resolve active swap device'
        [ -n "$swap_resolved" ] || fail 'resolved active swap device is empty'
        if [ "$swap_resolved" = "$resolved" ]; then swap_active=true; fi
        ;;
    esac
  done
} < /proc/swaps

open_raw=$(dmsetup info --noheadings --columns --options open "$resolved" 2>/dev/null) || fail 'cannot inspect device-mapper open count'
open_count=$(printf '%s\n' "$open_raw" | awk '
  NF == 0 { next }
  NF == 1 && $1 ~ /^[0-9]+$/ && !found { value = $1; found = 1; next }
  { exit 1 }
  END { if (!found) exit 1; print value }
') || fail 'device-mapper open count is malformed'

printf '{"mount_targets":%s,"fstab_targets":%s,"swap_active":%s,"device_open_count":%s}\n' \
  "$mount_targets" "$fstab_targets" "$swap_active" "$open_count"
`
}

// parseLVResizeSafetyState strictly validates the structured evidence returned
// by buildLVResizeSafetyCommand. Ambiguous JSON and unsafe or invalid targets
// are errors so callers can fail closed.
func parseLVResizeSafetyState(output string) (lvResizeSafetyState, error) {
	var state lvResizeSafetyState
	decoder := json.NewDecoder(strings.NewReader(output))
	token, err := decoder.Token()
	if err != nil {
		return state, fmt.Errorf("decode safety state object: %w", err)
	}
	if delim, ok := token.(json.Delim); !ok || delim != '{' {
		return state, fmt.Errorf("safety state must be a JSON object")
	}

	fields := make(map[string]json.RawMessage, 4)
	for decoder.More() {
		keyToken, err := decoder.Token()
		if err != nil {
			return state, fmt.Errorf("decode safety state field name: %w", err)
		}
		key, ok := keyToken.(string)
		if !ok {
			return state, fmt.Errorf("safety state field name is not a string")
		}
		switch key {
		case "mount_targets", "fstab_targets", "swap_active", "device_open_count":
		default:
			return state, fmt.Errorf("unknown safety state field %q", key)
		}
		if _, exists := fields[key]; exists {
			return state, fmt.Errorf("duplicate safety state field %q", key)
		}
		var value json.RawMessage
		if err := decoder.Decode(&value); err != nil {
			return state, fmt.Errorf("decode safety state field %q: %w", key, err)
		}
		fields[key] = value
	}
	closing, err := decoder.Token()
	if err != nil {
		return state, fmt.Errorf("close safety state object: %w", err)
	}
	if delim, ok := closing.(json.Delim); !ok || delim != '}' {
		return state, fmt.Errorf("safety state object is not closed")
	}
	if _, err := decoder.Token(); err != io.EOF {
		if err == nil {
			return state, fmt.Errorf("trailing data after safety state object")
		}
		return state, fmt.Errorf("trailing data after safety state object: %w", err)
	}

	for _, required := range []string{"mount_targets", "fstab_targets", "swap_active", "device_open_count"} {
		if _, ok := fields[required]; !ok {
			return state, fmt.Errorf("safety state is missing %q", required)
		}
		if bytes.Equal(bytes.TrimSpace(fields[required]), []byte("null")) {
			return state, fmt.Errorf("safety state field %q is null", required)
		}
	}

	var mountTargets []string
	if err := json.Unmarshal(fields["mount_targets"], &mountTargets); err != nil {
		return state, fmt.Errorf("invalid mount_targets: %w", err)
	}
	if mountTargets == nil {
		return state, fmt.Errorf("mount_targets must be an array")
	}
	state.MountTargets, err = normalizeLVResizeSafetyTargets("mount_targets", mountTargets)
	if err != nil {
		return state, err
	}

	var fstabTargets []string
	if err := json.Unmarshal(fields["fstab_targets"], &fstabTargets); err != nil {
		return state, fmt.Errorf("invalid fstab_targets: %w", err)
	}
	if fstabTargets == nil {
		return state, fmt.Errorf("fstab_targets must be an array")
	}
	state.FstabTargets, err = normalizeLVResizeSafetyTargets("fstab_targets", fstabTargets)
	if err != nil {
		return state, err
	}

	if err := json.Unmarshal(fields["swap_active"], &state.SwapActive); err != nil {
		return state, fmt.Errorf("invalid swap_active: %w", err)
	}
	if err := json.Unmarshal(fields["device_open_count"], &state.DeviceOpenCount); err != nil {
		return state, fmt.Errorf("invalid device_open_count: %w", err)
	}
	if state.DeviceOpenCount < 0 {
		return state, fmt.Errorf("device_open_count cannot be negative")
	}
	return state, nil
}

func normalizeLVResizeSafetyTargets(field string, targets []string) ([]string, error) {
	normalized := make([]string, 0, len(targets))
	for _, target := range targets {
		if err := ValidateMountPoint(target, nil); err != nil {
			return nil, fmt.Errorf("invalid %s target %q: %w", field, target, err)
		}
		normalized = append(normalized, path.Clean(target))
	}
	unique := sortedUnique(normalized)
	if unique == nil {
		return []string{}, nil
	}
	return unique, nil
}
