package storage

import (
	"context"
	"fmt"
	"path"
	"regexp"
	"sort"
	"strconv"
	"strings"
	"sync"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/ssh"
)

// LVInfo is a logical volume on a worker node, with its size, mount point,
// filesystem type, disk space usage, and NFS export status.
type LVInfo struct {
	VGName        string   `json:"vg_name"`
	Name          string   `json:"name"`
	SizeGB        float64  `json:"size_gb"`
	UsedGB        float64  `json:"used_gb"`        // used space in GB (from df); 0 if unmounted
	FreeGB        float64  `json:"free_gb"`        // remaining free space in GB (from df)
	UsePct        string   `json:"use_pct"`        // usage percentage, e.g. "5%"
	Path          string   `json:"path"`           // /dev/<vg>/<lv> (lv_path)
	MountPoint    string   `json:"mount_point"`    // from lsblk join; empty if unmounted
	FSType        string   `json:"fs_type"`        // from lsblk (reads superblock, works unmounted)
	IsNFSExport   bool     `json:"is_nfs_export"`  // true if exported via NFS
	NFSExportOpt  string   `json:"nfs_export_opt"` // export options e.g. "*(rw,sync)"
	PVs           []string `json:"pvs"`
	PhysicalDisks []string `json:"physical_disks"`
	FreeKnown     bool     `json:"free_known"`
}

// DiskInfo is an unused whole disk discovered on the worker - not mounted, has
// no filesystem, no partitions, and is not already a PV. These are candidates
// for pvcreate+vgcreate into a VG pool.
type DiskInfo struct {
	Name       string  `json:"name"` // /dev/sdb or /dev/sdb1
	SizeGB     float64 `json:"size_gb"`
	Type       string  `json:"type"`        // disk | part
	ParentDisk string  `json:"parent_disk"` // top-level physical disk
}

// PhysicalDiskInfo represents a physical hard drive on the worker node,
// with its total capacity, remaining allocatable capacity, and role.
type PhysicalDiskInfo struct {
	Name        string   `json:"name"`    // /dev/sda, /dev/sdb
	SizeGB      float64  `json:"size_gb"` // total capacity in GB
	FreeGB      float64  `json:"free_gb"` // remaining capacity in GB
	FreeKind    string   `json:"free_kind"`
	Role        string   `json:"role"`    // lvm, unused, data, reserved, system
	VGName      string   `json:"vg_name"` // VG name if role is "lvm"
	IsSystem    bool     `json:"is_system"`
	IsReserved  bool     `json:"is_reserved"`
	MountPoints []string `json:"mount_points"`
}

// NFSStatusInfo represents the state of NFS services and exported shares on a worker.
type NFSStatusInfo struct {
	Active  bool     `json:"active"`  // true if NFS server is active or has active exports
	Exports []string `json:"exports"` // active exported directory paths
}

// InventoryInfo is the full LVM/block-device and NFS picture of a worker, returned
// by the inventory endpoint so the storage UI can render VGs, LVs (with usage and
// NFS status), physical disks, and unused disks in one round trip.
type InventoryInfo struct {
	NFS           NFSStatusInfo      `json:"nfs"`
	VGs           []VGInfo           `json:"vgs"`
	LVs           []LVInfo           `json:"lvs"`
	PhysicalDisks []PhysicalDiskInfo `json:"physical_disks"`
	UnusedDisks   []DiskInfo         `json:"unused_disks"`
}

// inventoryCmd runs every LVM/block/NFS probe in a single SSH round trip, with
// section markers so the output can be split in Go. Every subcommand suppresses
// its own stderr so a missing dep yields an empty section rather than aborting
// the whole probe; lsblk (util-linux, always present) runs last so the overall
// exit code reflects it.
const inventoryCmd = "echo '###VGS###'; vgs --units g --noheadings --nosuffix --separator , -o vg_name,vg_size,vg_free 2>/dev/null; " +
	"echo '###LVS###'; lvs --segments --units g --noheadings --nosuffix --separator , -o vg_name,lv_name,lv_size,lv_path,devices 2>/dev/null; " +
	"echo '###PVS###'; pvs --units g --noheadings --nosuffix --separator , -o pv_name,pv_size,pv_free,vg_name 2>/dev/null; " +
	"echo '###DF###'; df -B1 -P 2>/dev/null; " +
	"echo '###NFS###'; (systemctl is-active nfs-server 2>/dev/null || systemctl is-active nfs-kernel-server 2>/dev/null || echo inactive); " +
	"echo '###EXPORTS###'; (exportfs -v 2>/dev/null || cat /etc/exports 2>/dev/null); " +
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
	return ListInventoryWithReserved(ctx, runner, w, []string{"/data01"})
}

func ListInventoryWithReserved(ctx context.Context, runner ssh.Runner, w db.WorkerNode, reservedMounts []string) (*InventoryInfo, error) {
	out, stderr, code, err := runner.Run(ctx, w, inventoryCmd)
	if err != nil {
		return nil, fmt.Errorf("inventory: %w (stderr: %s)", err, stderr)
	}
	if code != 0 {
		return nil, fmt.Errorf("inventory exited %d: %s", code, stderr)
	}
	return parseInventoryWithReserved(out, reservedMounts), nil
}

type pvDetail struct {
	SizeGB float64
	FreeGB float64
	VGName string
}

type dfDetail struct {
	UsedBytes  int64
	AvailBytes int64
	Capacity   string
}

// NFSHostStatus represents an overall summary of a worker host running NFS,
// detailing its physical disks, remaining capacities, allocated virtual disks,
// their mount points and space utilization, and NFS export configuration.
type NFSHostStatus struct {
	WorkerID      int64              `json:"worker_id"`
	WorkerName    string             `json:"worker_name"`
	Host          string             `json:"host"`
	Port          int                `json:"port"`
	Status        string             `json:"status"`
	NFSActive     bool               `json:"nfs_active"`
	TotalDisks    int                `json:"total_disks"`
	PhysicalDisks []PhysicalDiskInfo `json:"physical_disks"`
	VirtualDisks  []LVInfo           `json:"virtual_disks"`
	NFSExports    []string           `json:"nfs_exports"`
	ErrorMessage  string             `json:"error_message,omitempty"`
}

// ListNFSHosts probes workers and returns the NFS host status. If nfsOnly is true,
// it filters only nodes where NFS is active or has NFS exports; if false, it returns
// all accessible worker nodes with their NFS and disk status.
func ListNFSHosts(ctx context.Context, runner ssh.Runner, workers []db.WorkerNode, nfsOnly bool) ([]NFSHostStatus, error) {
	results := make([]NFSHostStatus, len(workers))
	var wg sync.WaitGroup

	for i, w := range workers {
		wg.Add(1)
		go func(idx int, node db.WorkerNode) {
			defer wg.Done()
			st := NFSHostStatus{
				WorkerID:      node.ID,
				WorkerName:    node.Name,
				Host:          node.Host,
				Port:          node.Port,
				Status:        node.Status,
				PhysicalDisks: []PhysicalDiskInfo{},
				VirtualDisks:  []LVInfo{},
				NFSExports:    []string{},
			}
			inv, err := ListInventory(ctx, runner, node)
			if err != nil {
				st.ErrorMessage = err.Error()
				results[idx] = st
				return
			}
			st.NFSActive = inv.NFS.Active
			st.PhysicalDisks = inv.PhysicalDisks
			st.TotalDisks = len(inv.PhysicalDisks)
			st.VirtualDisks = inv.LVs
			st.NFSExports = inv.NFS.Exports
			results[idx] = st
		}(i, w)
	}
	wg.Wait()

	if !nfsOnly {
		return results, nil
	}

	var filtered []NFSHostStatus
	for _, res := range results {
		hasExportedLV := false
		for _, lv := range res.VirtualDisks {
			if lv.IsNFSExport {
				hasExportedLV = true
				break
			}
		}
		if res.NFSActive || len(res.NFSExports) > 0 || hasExportedLV {
			filtered = append(filtered, res)
		}
	}
	return filtered, nil
}

// parseInventory splits the sectioned command output and joins LVs with lsblk
// (for mount point + filesystem), df (for space usage), exports (for NFS status),
// and computes physical disks and unused disks. Exported to tests via the package
// so parseInventory can be unit-tested with fixture output.
func parseInventory(out string) *InventoryInfo {
	return parseInventoryWithReserved(out, []string{"/data01"})
}

func parseInventoryWithReserved(out string, reservedMounts []string) *InventoryInfo {
	inv := &InventoryInfo{
		NFS:           NFSStatusInfo{Active: false, Exports: []string{}},
		VGs:           []VGInfo{},
		LVs:           []LVInfo{},
		PhysicalDisks: []PhysicalDiskInfo{},
		UnusedDisks:   []DiskInfo{},
	}
	var lsblkRows []lsblkRow
	pvSet := map[string]bool{}
	pvMap := map[string]pvDetail{}
	dfMap := map[string]dfDetail{}
	exportsMap := map[string]string{}
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
			// pvs -o pv_name,pv_size,pv_free,vg_name
			// e.g. "/dev/sdb,3500.00g,2300.00g,vg_data" or "/dev/sdb,vg_data"
			parts := strings.Split(line, ",")
			if len(parts) >= 1 {
				pv := strings.TrimSpace(parts[0])
				if pv != "" {
					pvSet[pv] = true
					d := pvDetail{}
					if len(parts) >= 4 {
						sGB, _ := strconv.ParseFloat(strings.TrimSuffix(strings.TrimSpace(parts[1]), "g"), 64)
						fGB, _ := strconv.ParseFloat(strings.TrimSuffix(strings.TrimSpace(parts[2]), "g"), 64)
						d.SizeGB = sGB
						d.FreeGB = fGB
						d.VGName = strings.TrimSpace(parts[3])
					} else if len(parts) >= 2 {
						d.VGName = strings.TrimSpace(parts[1])
					}
					pvMap[pv] = d
				}
			}
		case "df":
			// df -B1 -P output: Filesystem 1024-blocks Used Available Capacity Mounted on
			fields := strings.Fields(line)
			if len(fields) >= 6 && fields[0] != "Filesystem" {
				usedB, _ := strconv.ParseInt(fields[2], 10, 64)
				availB, _ := strconv.ParseInt(fields[3], 10, 64)
				cap := fields[4]
				mp := strings.Join(fields[5:], " ")
				dfMap[mp] = dfDetail{UsedBytes: usedB, AvailBytes: availB, Capacity: cap}
			}
		case "nfs":
			lower := strings.ToLower(line)
			if strings.Contains(lower, "active") && !strings.Contains(lower, "inactive") {
				inv.NFS.Active = true
			}
		case "exports":
			if !strings.HasPrefix(line, "#") {
				fields := strings.Fields(line)
				if len(fields) >= 1 && strings.HasPrefix(fields[0], "/") {
					expPath := fields[0]
					opts := ""
					if len(fields) > 1 {
						opts = strings.Join(fields[1:], " ")
					}
					exportsMap[expPath] = opts
					inv.NFS.Exports = append(inv.NFS.Exports, expPath)
					inv.NFS.Active = true
				}
			}
		case "lsblk":
			if r, ok := parseLSBLKLine(line); ok {
				lsblkRows = append(lsblkRows, r)
			}
		}
	}

	// lvs --segments may return one row per segment. Merge rows by VG/LV and
	// keep the union of backing PV devices.
	mergedLVs := make([]LVInfo, 0, len(inv.LVs))
	lvIndex := map[string]int{}
	for _, lv := range inv.LVs {
		key := lv.VGName + "\x00" + lv.Name
		if idx, ok := lvIndex[key]; ok {
			mergedLVs[idx].PVs = appendUnique(mergedLVs[idx].PVs, lv.PVs...)
			continue
		}
		lv.PVs = sortedUnique(lv.PVs)
		lvIndex[key] = len(mergedLVs)
		mergedLVs = append(mergedLVs, lv)
	}
	inv.LVs = mergedLVs

	rowsByName := make(map[string]lsblkRow, len(lsblkRows))
	childrenOf := map[string]bool{}
	for _, row := range lsblkRows {
		rowsByName[row.Name] = row
		if row.Pkname != "" {
			childrenOf[row.Pkname] = true
		}
	}

	// Join LVs with lsblk lvm rows and map each LV's segment devices to the
	// top-level physical disks. If devices are unavailable, fall back to all PVs
	// in the same VG so the UI still reports a conservative relationship.
	lvmByName := map[string]lsblkRow{}
	for _, row := range lsblkRows {
		if row.Type == "lvm" {
			lvmByName[row.Name] = row
		}
	}
	for i := range inv.LVs {
		lv := &inv.LVs[i]
		if row, ok := lvmByName[dmName(lv.VGName, lv.Name)]; ok {
			lv.MountPoint = row.Mountpoint
			lv.FSType = row.Fstype
		}
		if len(lv.PVs) == 0 {
			for pvName, detail := range pvMap {
				if detail.VGName == lv.VGName {
					lv.PVs = append(lv.PVs, pvName)
				}
			}
		}
		for _, pvName := range lv.PVs {
			if disk := physicalDiskFor(pvName, rowsByName); disk != "" {
				lv.PhysicalDisks = append(lv.PhysicalDisks, disk)
			}
		}
		lv.PVs = sortedUnique(lv.PVs)
		lv.PhysicalDisks = sortedUnique(lv.PhysicalDisks)
		if lv.MountPoint != "" {
			if detail, ok := dfMap[lv.MountPoint]; ok {
				lv.UsedGB = bytesToGB(detail.UsedBytes)
				lv.FreeGB = bytesToGB(detail.AvailBytes)
				lv.UsePct = detail.Capacity
				lv.FreeKnown = true
			}
			if opt, ok := exportsMap[lv.MountPoint]; ok {
				lv.IsNFSExport = true
				lv.NFSExportOpt = opt
			}
		}
	}

	systemDisks := map[string]bool{}
	reservedDisks := map[string]bool{}
	diskMounts := map[string][]string{}
	diskFilesystemFree := map[string]float64{}
	markMount := func(device, mountPoint string) {
		if mountPoint == "" {
			return
		}
		disk := physicalDiskFor(device, rowsByName)
		if disk == "" {
			return
		}
		diskMounts[disk] = appendUnique(diskMounts[disk], mountPoint)
		if mountPoint == "/" || mountPoint == "/boot" || mountPoint == "/boot/efi" {
			systemDisks[disk] = true
		}
		if isReservedMountpoint(mountPoint, reservedMounts) {
			reservedDisks[disk] = true
		}
		if detail, ok := dfMap[mountPoint]; ok {
			diskFilesystemFree[disk] += bytesToGB(detail.AvailBytes)
		}
	}
	for _, row := range lsblkRows {
		markMount("/dev/"+row.Name, row.Mountpoint)
	}
	// LVM rows do not always expose PKNAME. Use the segment mapping to mark
	// every physical disk behind mounted LVs.
	for _, lv := range inv.LVs {
		for _, disk := range lv.PhysicalDisks {
			if lv.MountPoint == "" {
				continue
			}
			diskMounts[disk] = appendUnique(diskMounts[disk], lv.MountPoint)
			if lv.MountPoint == "/" || lv.MountPoint == "/boot" || lv.MountPoint == "/boot/efi" {
				systemDisks[disk] = true
			}
			if isReservedMountpoint(lv.MountPoint, reservedMounts) {
				reservedDisks[disk] = true
			}
		}
	}

	pvFreeByDisk := map[string]float64{}
	vgNamesByDisk := map[string][]string{}
	for pvName, detail := range pvMap {
		if disk := physicalDiskFor(pvName, rowsByName); disk != "" {
			pvFreeByDisk[disk] += detail.FreeGB
			if detail.VGName != "" {
				vgNamesByDisk[disk] = appendUnique(vgNamesByDisk[disk], detail.VGName)
			}
		}
	}

	// Safe initialization candidates may be unmounted whole disks or unmounted
	// partitions. A candidate is rejected if its physical ancestor is a system
	// disk or reserved disk (/data01), if it is currently mounted, if it has
	// child devices (partitions), or if it already belongs to an active volume group.
	// Devices with stale unmounted filesystems or unassigned PVs are valid candidates
	// because create_vg will wipe them prior to initialization.
	candidateBytesByDisk := map[string]int64{}
	unusedMap := map[string]bool{}
	for _, row := range lsblkRows {
		if row.Type != "disk" && row.Type != "part" {
			continue
		}
		device := "/dev/" + row.Name
		physical := physicalDiskFor(device, rowsByName)
		if physical == "" || systemDisks[physical] || reservedDisks[physical] {
			continue
		}
		// A mounted device or a device with child devices (partitions) cannot be
		// directly initialized. For partitioned disks, child partitions will be evaluated.
		if row.Mountpoint != "" || childrenOf[row.Name] {
			continue
		}
		// Devices belonging to an active Volume Group must not be wiped.
		// Free PVs without an active VG are safe to reuse/initialize.
		if detail, ok := pvMap[device]; ok && detail.VGName != "" {
			continue
		}
		inv.UnusedDisks = append(inv.UnusedDisks, DiskInfo{
			Name: device, SizeGB: bytesToGB(row.SizeBytes), Type: row.Type, ParentDisk: physical,
		})
		unusedMap[device] = true
		candidateBytesByDisk[physical] += row.SizeBytes
	}
	sort.Slice(inv.UnusedDisks, func(i, j int) bool { return inv.UnusedDisks[i].Name < inv.UnusedDisks[j].Name })

	for _, row := range lsblkRows {
		if row.Type != "disk" || isVirtualDiskName(row.Name) {
			continue
		}
		device := "/dev/" + row.Name
		disk := PhysicalDiskInfo{
			Name: device, SizeGB: bytesToGB(row.SizeBytes), IsSystem: systemDisks[device],
			IsReserved: reservedDisks[device], MountPoints: sortedUnique(diskMounts[device]),
		}
		switch {
		case disk.IsReserved:
			disk.Role = "reserved"
		case disk.IsSystem:
			disk.Role = "system"
		case len(vgNamesByDisk[device]) > 0:
			disk.Role = "lvm"
		case unusedMap[device] || (candidateBytesByDisk[device] > 0 && len(disk.MountPoints) == 0):
			disk.Role = "unused"
		default:
			disk.Role = "data"
		}
		disk.VGName = strings.Join(sortedUnique(vgNamesByDisk[device]), ",")
		if len(vgNamesByDisk[device]) > 0 {
			disk.FreeGB = pvFreeByDisk[device]
			disk.FreeKind = "pv_allocatable"
		} else {
			disk.FreeGB = diskFilesystemFree[device] + bytesToGB(candidateBytesByDisk[device])
			if candidateBytesByDisk[device] > 0 && diskFilesystemFree[device] > 0 {
				disk.FreeKind = "filesystem_and_candidate"
			} else if candidateBytesByDisk[device] > 0 {
				disk.FreeKind = "candidate"
			} else if len(disk.MountPoints) > 0 {
				disk.FreeKind = "filesystem_available"
			}
		}
		inv.PhysicalDisks = append(inv.PhysicalDisks, disk)
	}
	sort.Slice(inv.PhysicalDisks, func(i, j int) bool { return inv.PhysicalDisks[i].Name < inv.PhysicalDisks[j].Name })
	return inv
}

func appendUnique(values []string, additions ...string) []string {
	seen := make(map[string]struct{}, len(values)+len(additions))
	for _, value := range values {
		seen[value] = struct{}{}
	}
	for _, value := range additions {
		if value == "" {
			continue
		}
		if _, ok := seen[value]; ok {
			continue
		}
		seen[value] = struct{}{}
		values = append(values, value)
	}
	return values
}

func sortedUnique(values []string) []string {
	values = appendUnique(nil, values...)
	sort.Strings(values)
	return values
}

func physicalDiskFor(device string, rows map[string]lsblkRow) string {
	name := strings.TrimPrefix(strings.TrimSpace(device), "/dev/")
	seen := map[string]bool{}
	for name != "" && !seen[name] {
		seen[name] = true
		row, ok := rows[name]
		if !ok {
			return ""
		}
		if row.Type == "disk" {
			return "/dev/" + row.Name
		}
		name = strings.TrimPrefix(row.Pkname, "/dev/")
	}
	return ""
}

func isReservedMountpoint(mountPoint string, reservedRoots []string) bool {
	for _, reservedRoot := range reservedRoots {
		if reservedRoot != "" && isMountWithin(mountPoint, reservedRoot) {
			return true
		}
	}
	return false
}

func isMountWithin(mountPoint, reservedRoot string) bool {
	mountPoint = path.Clean(mountPoint)
	reservedRoot = path.Clean(reservedRoot)
	return mountPoint == reservedRoot || strings.HasPrefix(mountPoint, reservedRoot+"/")
}

func isVirtualDiskName(name string) bool {
	for _, prefix := range []string{"loop", "ram", "zram", "sr"} {
		if strings.HasPrefix(name, prefix) {
			return true
		}
	}
	return false
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

// parseLVLine parses an lvs CSV row
// "vg_name,lv_name,lv_size,lv_path,devices...".
func parseLVLine(line string) (LVInfo, bool) {
	parts := strings.Split(line, ",")
	if len(parts) < 4 {
		return LVInfo{}, false
	}
	vg := strings.TrimSpace(parts[0])
	name := strings.TrimSpace(parts[1])
	sizeStr := strings.TrimSpace(parts[2])
	lvPath := strings.TrimSpace(parts[3])
	sizeGB, _ := strconv.ParseFloat(strings.TrimSuffix(sizeStr, "g"), 64)
	pvs := make([]string, 0)
	for _, rawDevice := range parts[4:] {
		device := strings.TrimSpace(rawDevice)
		if idx := strings.IndexByte(device, '('); idx >= 0 {
			device = device[:idx]
		}
		if strings.HasPrefix(device, "/dev/") {
			pvs = append(pvs, device)
		}
	}
	return LVInfo{VGName: vg, Name: name, SizeGB: sizeGB, Path: lvPath, PVs: sortedUnique(pvs)}, true
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
