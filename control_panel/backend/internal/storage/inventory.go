package storage

import (
	"context"
	"fmt"
	"regexp"
	"strconv"
	"strings"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
)

// LVInfo is a logical volume on a worker node, with its size, mount point, and
// filesystem type. Includes LVs NOT created by the control panel so the admin
// can see and manage all existing LVM capacity.
type LVInfo struct {
	VGName     string  `json:"vg_name"`
	Name       string  `json:"name"`
	SizeGB     float64 `json:"size_gb"`
	Path       string  `json:"path"`        // /dev/<vg>/<lv> (lv_path)
	MountPoint string  `json:"mount_point"` // from lsblk join; empty if unmounted
	FSType     string  `json:"fs_type"`     // from lsblk (reads superblock, works unmounted)
}

// DiskInfo is an unused whole disk discovered on the worker - not mounted, has
// no filesystem, no partitions, and is not already a PV. These are candidates
// for pvcreate+vgcreate into a VG pool.
type DiskInfo struct {
	Name   string  `json:"name"` // /dev/sdb
	SizeGB float64 `json:"size_gb"`
}

// InventoryInfo is the full LVM/block-device picture of a worker, returned by
// the inventory endpoint so the storage UI can render VGs, LVs (editable),
// and unused disks (creatable into a VG pool) in one round trip.
type InventoryInfo struct {
	VGs         []VGInfo   `json:"vgs"`
	LVs         []LVInfo    `json:"lvs"`
	UnusedDisks []DiskInfo `json:"unused_disks"`
}

// inventoryCmd runs every LVM/block probe in a single SSH round trip, with
// section markers so the output can be split in Go. Every subcommand suppresses
// its own stderr so a missing dep (lvm2 not installed yet) yields an empty
// section rather than aborting the whole probe; lsblk (util-linux, always
// present) runs last so the overall exit code reflects it.
const inventoryCmd = "echo '###VGS###'; vgs --units g --noheadings --nosuffix --separator , -o vg_name,vg_size,vg_free 2>/dev/null; " +
	"echo '###LVS###'; lvs --units g --noheadings --nosuffix --separator , -o vg_name,lv_name,lv_size,lv_path 2>/dev/null; " +
	"echo '###PVS###'; pvs --noheadings --nosuffix --separator , -o pv_name,vg_name 2>/dev/null; " +
	"echo '###LSBLK###'; lsblk -b -P -n -o NAME,TYPE,SIZE,MOUNTPOINT,FSTYPE,PKNAME 2>/dev/null"

// lsblkRow is one parsed lsblk -P line.
type lsblkRow struct {
	Name       string
	Type       string
	SizeBytes  int64
	Mountpoint string
	Fstype     string
	Pkname     string
}

// ListInventory SSHes to the worker once and returns its VGs, LVs (with mount
// point + filesystem), and unused disks. Safe to call before lvm2 is installed:
// the LVM sections will be empty and only lsblk (disks) is populated.
func ListInventory(ctx context.Context, runner ssh.Runner, w db.WorkerNode) (*InventoryInfo, error) {
	out, stderr, code, err := runner.Run(ctx, w, inventoryCmd)
	if err != nil {
		return nil, fmt.Errorf("inventory: %w (stderr: %s)", err, stderr)
	}
	if code != 0 {
		return nil, fmt.Errorf("inventory exited %d: %s", code, stderr)
	}
	return parseInventory(out), nil
}

// parseInventory splits the sectioned command output and joins LVs with lsblk
// (for mount point + filesystem) and computes unused disks. Exported to tests
// via the package so parseInventory can be unit-tested with fixture output.
func parseInventory(out string) *InventoryInfo {
	inv := &InventoryInfo{VGs: []VGInfo{}, LVs: []LVInfo{}, UnusedDisks: []DiskInfo{}}
	var lsblkRows []lsblkRow
	pvSet := map[string]bool{}
	section := ""
	for _, raw := range strings.Split(out, "\n") {
		line := strings.TrimSpace(raw)
		if line == "" {
			continue
		}
		if strings.HasPrefix(line, "###") && strings.HasSuffix(line, "###") {
			section = strings.ToLower(strings.TrimSuffix(strings.TrimPrefix(line, "###"), "###"))
			continue
		}
		switch section {
		case "vgs":
			if v, ok := parseVGLine(line); ok {
				inv.VGs = append(inv.VGs, v)
			}
		case "lvs":
			if lv, ok := parseLVLine(line); ok {
				inv.LVs = append(inv.LVs, lv)
			}
		case "pvs":
			// pvs -o pv_name,vg_name -> "/dev/sdb,vg_data" (vg may be empty)
			parts := strings.Split(line, ",")
			if len(parts) >= 1 {
				if pv := strings.TrimSpace(parts[0]); pv != "" {
					pvSet[pv] = true
				}
			}
		case "lsblk":
			if r, ok := parseLSBLKLine(line); ok {
				lsblkRows = append(lsblkRows, r)
			}
		}
	}

	// Join LVs with lsblk lvm rows by device-mapper name for mount + fstype.
	// lsblk NAME for an LVM device is the dm name = vg+"-"+lv with every "-" in
	// vg/lv doubled to "--" (LVM escaping). dmName reproduces that so the join
	// matches even when vg or lv contain hyphens.
	lvmByName := map[string]lsblkRow{}
	for _, r := range lsblkRows {
		if r.Type == "lvm" {
			lvmByName[r.Name] = r
		}
	}
	for i := range inv.LVs {
		if r, ok := lvmByName[dmName(inv.LVs[i].VGName, inv.LVs[i].Name)]; ok {
			inv.LVs[i].MountPoint = r.Mountpoint
			inv.LVs[i].FSType = r.Fstype
		}
	}

	// Unused disks: TYPE=disk with no children (no lsblk row has PKNAME==disk),
	// no filesystem, no mountpoint, and not already a PV. This excludes the OS
	// disk (has mounted partitions) and PV disks (have LV children, or are in
	// pvSet for an empty VG). Disks with a partition table are excluded by the
	// "no children" rule so we never wipe a partition table.
	childrenOf := map[string]bool{}
	for _, r := range lsblkRows {
		if r.Pkname != "" {
			childrenOf[r.Pkname] = true
		}
	}
	for _, r := range lsblkRows {
		if r.Type != "disk" {
			continue
		}
		if r.Fstype != "" || r.Mountpoint != "" {
			continue
		}
		if childrenOf[r.Name] {
			continue
		}
		if pvSet["/dev/"+r.Name] {
			continue
		}
		inv.UnusedDisks = append(inv.UnusedDisks, DiskInfo{
			Name:   "/dev/" + r.Name,
			SizeGB: bytesToGB(r.SizeBytes),
		})
	}
	return inv
}

// parseVGLine parses a vgs CSV row "vg_name,vg_size,vg_free" (gigabyte units,
// no suffix). Mirrors ListVGs parsing.
func parseVGLine(line string) (VGInfo, bool) {
	parts := strings.Split(line, ",")
	if len(parts) < 3 {
		return VGInfo{}, false
	}
	name := strings.TrimSpace(parts[0])
	vsize := strings.TrimSpace(parts[1])
	vfree := strings.TrimSpace(parts[2])
	freeGB, _ := strconv.ParseFloat(strings.TrimSuffix(vfree, "g"), 64)
	return VGInfo{Name: name, VSize: vsize, VFree: vfree, FreeGB: freeGB}, true
}

// parseLVLine parses an lvs CSV row "vg_name,lv_name,lv_size,lv_path".
func parseLVLine(line string) (LVInfo, bool) {
	parts := strings.Split(line, ",")
	if len(parts) < 4 {
		return LVInfo{}, false
	}
	vg := strings.TrimSpace(parts[0])
	name := strings.TrimSpace(parts[1])
	sizeStr := strings.TrimSpace(parts[2])
	path := strings.TrimSpace(parts[3])
	sizeGB, _ := strconv.ParseFloat(strings.TrimSuffix(sizeStr, "g"), 64)
	return LVInfo{VGName: vg, Name: name, SizeGB: sizeGB, Path: path}, true
}

// lsblkPairRe matches key="value" pairs in lsblk -P output. Values may contain
// escaped quotes (\"), which the ((?:[^"\\]|\\.)*) group handles.
var lsblkPairRe = regexp.MustCompile(`(\w+)="((?:[^"\\]|\\.)*)"`)

// parseLSBLKLine parses one lsblk -P line into an lsblkRow.
func parseLSBLKLine(line string) (lsblkRow, bool) {
	if !strings.HasPrefix(line, "NAME=") {
		return lsblkRow{}, false
	}
	row := lsblkRow{}
	for _, m := range lsblkPairRe.FindAllStringSubmatch(line, -1) {
		k, v := m[1], m[2]
		switch k {
		case "NAME":
			row.Name = v
		case "TYPE":
			row.Type = v
		case "SIZE":
			row.SizeBytes, _ = strconv.ParseInt(v, 10, 64)
		case "MOUNTPOINT":
			row.Mountpoint = v
		case "FSTYPE":
			row.Fstype = v
		case "PKNAME":
			row.Pkname = v
		}
	}
	if row.Name == "" {
		return lsblkRow{}, false
	}
	return row, true
}

// dmName returns the device-mapper node name for an LV: vg and lv joined by a
// single "-", with every "-" in each doubled to "--" (LVM dm escaping). Used to
// join lvs output to lsblk's NAME for an LVM device.
func dmName(vg, lv string) string {
	double := func(s string) string { return strings.ReplaceAll(s, "-", "--") }
	return double(vg) + "-" + double(lv)
}

// bytesToGB converts lsblk -b byte sizes to decimal GB to match LVM's --units g.
func bytesToGB(b int64) float64 {
	if b <= 0 {
		return 0
	}
	return float64(b) / 1e9
}
