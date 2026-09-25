package storage

import (
	"context"
	"io"
	"testing"

	"xirang/control_panel/internal/db"
)

// realisticInventory is a single SSH round-trip's worth of sectioned output from
// inventoryCmd: two LVs (one mounted, one not), an OS disk (sda, mounted
// partitions), a PV disk (sdb, backs vg_data), and one raw unused disk (sdc).
const realisticInventory = "###VGS###\n" +
	"vg_data,3.50g,2.30g\n" +
	"###LVS###\n" +
	"vg_data,lv_nb_1,200.00g,/dev/vg_data/lv_nb_1\n" +
	"vg_data,lv_nb_2,500.00g,/dev/vg_data/lv_nb_2\n" +
	"###PVS###\n" +
	"/dev/sdb,vg_data\n" +
	"###LSBLK###\n" +
	`NAME="sda" TYPE="disk" SIZE="8001563222016" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
	`NAME="sda1" TYPE="part" SIZE="1073741824" MOUNTPOINT="/boot" FSTYPE="ext4" PKNAME="sda"` + "\n" +
	`NAME="sda2" TYPE="part" SIZE="7990000000000" MOUNTPOINT="/" FSTYPE="ext4" PKNAME="sda"` + "\n" +
	`NAME="sdb" TYPE="disk" SIZE="3758096384000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
	`NAME="vg_data-lv_nb_1" TYPE="lvm" SIZE="214748364800" MOUNTPOINT="/data02/nb_1" FSTYPE="ext4" PKNAME="sdb"` + "\n" +
	`NAME="vg_data-lv_nb_2" TYPE="lvm" SIZE="536870912000" MOUNTPOINT="" FSTYPE="ext4" PKNAME="sdb"` + "\n" +
	`NAME="sdc" TYPE="disk" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME=""`

func TestParseInventory(t *testing.T) {
	inv := parseInventory(realisticInventory)

	if len(inv.VGs) != 1 || inv.VGs[0].Name != "vg_data" || inv.VGs[0].FreeGB != 2.30 {
		t.Fatalf("vgs wrong: %+v", inv.VGs)
	}
	if len(inv.LVs) != 2 {
		t.Fatalf("expected 2 lvs, got %d: %+v", len(inv.LVs), inv.LVs)
	}
	lv1 := inv.LVs[0]
	if lv1.Name != "lv_nb_1" || lv1.SizeGB != 200.00 || lv1.Path != "/dev/vg_data/lv_nb_1" {
		t.Fatalf("lv1 base wrong: %+v", lv1)
	}
	if lv1.MountPoint != "/data02/nb_1" || lv1.FSType != "ext4" {
		t.Fatalf("lv1 mount/fstype join wrong: %+v", lv1)
	}
	// Unmounted LV still gets fstype from lsblk (reads superblock).
	lv2 := inv.LVs[1]
	if lv2.MountPoint != "" || lv2.FSType != "ext4" {
		t.Fatalf("lv2 (unmounted) wrong: %+v", lv2)
	}
	// Only sdc is unused: sda excluded (mounted partitions), sdb excluded (PV +
	// has LV children).
	if len(inv.UnusedDisks) != 1 || inv.UnusedDisks[0].Name != "/dev/sdc" {
		t.Fatalf("unused disks wrong: %+v", inv.UnusedDisks)
	}
	if got := inv.UnusedDisks[0].SizeGB; got < 10.73 || got > 10.74 {
		t.Fatalf("sdc size wrong: %v", got)
	}
}

func TestParseInventory_LVMNotInstalled(t *testing.T) {
	// lvm2 missing: vgs/lvs/pvs empty (commands not found, stderr suppressed),
	// only lsblk produces data. The probe must not error and must still report
	// unused disks so the admin can install deps and create a VG.
	const out = "###VGS###\n###LVS###\n###PVS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sda" TYPE="disk" SIZE="8001563222016" MOUNTPOINT="/" FSTYPE="ext4" PKNAME=""`
	inv := parseInventory(out)
	if len(inv.VGs) != 0 || len(inv.LVs) != 0 {
		t.Fatalf("expected empty vgs/lvs, got %+v", inv)
	}
	if len(inv.UnusedDisks) != 1 || inv.UnusedDisks[0].Name != "/dev/sdb" {
		t.Fatalf("unused disks wrong: %+v", inv.UnusedDisks)
	}
	// sda is mounted (/) -> excluded.
	for _, d := range inv.UnusedDisks {
		if d.Name == "/dev/sda" {
			t.Fatal("mounted OS disk should not be unused")
		}
	}
}

func TestParseInventory_BlankPartitionIsCandidate(t *testing.T) {
	// A blank partition is a safe candidate, while its parent whole disk is not
	// offered separately because it has children.
	const out = "###VGS###\n###LVS###\n###PVS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdb1" TYPE="part" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME="sdb"`
	inv := parseInventory(out)
	if len(inv.UnusedDisks) != 1 || inv.UnusedDisks[0].Name != "/dev/sdb1" || inv.UnusedDisks[0].Type != "part" {
		t.Fatalf("blank partition should be the only candidate: %+v", inv.UnusedDisks)
	}
}

func TestParseInventory_EmptyPVExcludesDisk(t *testing.T) {
	// sdb is a PV in an empty VG (no LVs) - lsblk shows no lvm children, so the
	// only thing keeping it out of UnusedDisks is the pvs section.
	const out = "###VGS###\nvg_empty,1.00g,1.00g\n###LVS###\n###PVS###\n/dev/sdb,vg_empty\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME=""`
	inv := parseInventory(out)
	if len(inv.UnusedDisks) != 0 {
		t.Fatalf("empty-VG PV disk must not be unused: %+v", inv.UnusedDisks)
	}
}

func TestDmNameEscaping(t *testing.T) {
	// vg/lv with hyphens: LVM doubles them in the dm name.
	if got := dmName("vg-data", "lv-x"); got != "vg--data-lv--x" {
		t.Fatalf("dmName escaping wrong: %q", got)
	}
	if got := dmName("vg_data", "lv_x"); got != "vg_data-lv_x" {
		t.Fatalf("dmName no-hyphen wrong: %q", got)
	}
}

func TestParseInventory_HyphenNamesJoin(t *testing.T) {
	// VG name with a hyphen: the lvm dm name is escaped (vg--data), and the
	// join must still find the mount point.
	const out = "###VGS###\nvg-data,1.00g,1.00g\n###LVS###\nvg-data,lv_x,100.00g,/dev/vg-data/lv_x\n###PVS###\n###LSBLK###\n" +
		`NAME="vg--data-lv_x" TYPE="lvm" SIZE="107374182400" MOUNTPOINT="/data02/x" FSTYPE="xfs" PKNAME=""`
	inv := parseInventory(out)
	if len(inv.LVs) != 1 {
		t.Fatalf("expected 1 lv, got %d", len(inv.LVs))
	}
	if inv.LVs[0].MountPoint != "/data02/x" || inv.LVs[0].FSType != "xfs" {
		t.Fatalf("hyphen-name join wrong: %+v", inv.LVs[0])
	}
}

func TestParseInventory_NFS_DF_PhysicalDisks(t *testing.T) {
	const out = "###VGS###\n" +
		"vg_data,3500.00g,2300.00g\n" +
		"###LVS###\n" +
		"vg_data,lv_notebook_200g,200.00g,/dev/vg_data/lv_notebook_200g\n" +
		"###PVS###\n" +
		"/dev/sdb,3500.00g,2300.00g,vg_data\n" +
		"###DF###\n" +
		"Filesystem 1024-blocks Used Available Capacity Mounted on\n" +
		"/dev/mapper/vg_data-lv_notebook_200g 214748364800 10737418240 204010946560 5% /data02/notebook_a_200g\n" +
		"###NFS###\n" +
		"active\n" +
		"###EXPORTS###\n" +
		"/data02/notebook_a_200g *(rw,sync,no_root_squash,no_subtree_check)\n" +
		"###LSBLK###\n" +
		`NAME="sda" TYPE="disk" SIZE="858993459200" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sda1" TYPE="part" SIZE="1073741824" MOUNTPOINT="/boot" FSTYPE="ext4" PKNAME="sda"` + "\n" +
		`NAME="sda2" TYPE="part" SIZE="751619276800" MOUNTPOINT="/" FSTYPE="ext4" PKNAME="sda"` + "\n" +
		`NAME="sdb" TYPE="disk" SIZE="3758096384000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="vg_data-lv_notebook_200g" TYPE="lvm" SIZE="214748364800" MOUNTPOINT="/data02/notebook_a_200g" FSTYPE="ext4" PKNAME="sdb"` + "\n" +
		`NAME="sdc" TYPE="disk" SIZE="1073741824000" MOUNTPOINT="" FSTYPE="" PKNAME=""`

	inv := parseInventory(out)

	// Check NFS
	if !inv.NFS.Active {
		t.Fatal("expected NFS to be active")
	}
	if len(inv.NFS.Exports) != 1 || inv.NFS.Exports[0] != "/data02/notebook_a_200g" {
		t.Fatalf("unexpected exports: %+v", inv.NFS.Exports)
	}

	// Check Physical Disks
	if len(inv.PhysicalDisks) != 3 {
		t.Fatalf("expected 3 physical disks (sda, sdb, sdc), got %d: %+v", len(inv.PhysicalDisks), inv.PhysicalDisks)
	}
	sda := inv.PhysicalDisks[0]
	if sda.Name != "/dev/sda" || sda.Role != "system" {
		t.Fatalf("sda wrong: %+v", sda)
	}
	sdb := inv.PhysicalDisks[1]
	if sdb.Name != "/dev/sdb" || sdb.Role != "lvm" || sdb.FreeGB != 2300.00 || sdb.VGName != "vg_data" {
		t.Fatalf("sdb wrong: %+v", sdb)
	}
	sdc := inv.PhysicalDisks[2]
	if sdc.Name != "/dev/sdc" || sdc.Role != "unused" || sdc.FreeGB < 1073.0 {
		t.Fatalf("sdc wrong: %+v", sdc)
	}

	// Check Virtual Disk (LV)
	if len(inv.LVs) != 1 {
		t.Fatalf("expected 1 lv, got %d", len(inv.LVs))
	}
	lv := inv.LVs[0]
	if lv.Name != "lv_notebook_200g" || lv.MountPoint != "/data02/notebook_a_200g" {
		t.Fatalf("lv metadata wrong: %+v", lv)
	}
	if !lv.IsNFSExport {
		t.Fatal("expected LV to be flagged as NFS export")
	}
	if lv.UsedGB < 10.73 || lv.UsedGB > 10.75 {
		t.Fatalf("lv used gb wrong: %v", lv.UsedGB)
	}
	if lv.FreeGB < 204.0 || lv.FreeGB > 204.1 {
		t.Fatalf("lv free gb wrong: %v", lv.FreeGB)
	}
	if lv.UsePct != "5%" {
		t.Fatalf("lv use pct wrong: %v", lv.UsePct)
	}
}

func TestParseInventory_ClassifiesDataReservedAndPartitionCandidates(t *testing.T) {
	const out = "###VGS###\n###LVS###\n###PVS###\n###DF###\n" +
		"Filesystem 1024-blocks Used Available Capacity Mounted on\n" +
		"/dev/sdb1 100000000000 10000000000 90000000000 10% /data02\n" +
		"/dev/sdc1 100000000000 20000000000 80000000000 20% /data01\n" +
		"###NFS###\ninactive\n###EXPORTS###\n###LSBLK###\n" +
		`NAME="sda" TYPE="disk" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sda1" TYPE="part" SIZE="100000000000" MOUNTPOINT="/" FSTYPE="xfs" PKNAME="sda"` + "\n" +
		`NAME="sdb" TYPE="disk" SIZE="200000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdb1" TYPE="part" SIZE="100000000000" MOUNTPOINT="/data02" FSTYPE="xfs" PKNAME="sdb"` + "\n" +
		`NAME="sdb2" TYPE="part" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME="sdb"` + "\n" +
		`NAME="sdc" TYPE="disk" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdc1" TYPE="part" SIZE="100000000000" MOUNTPOINT="/data01" FSTYPE="xfs" PKNAME="sdc"`

	inv := parseInventory(out)
	byName := map[string]PhysicalDiskInfo{}
	for _, disk := range inv.PhysicalDisks {
		byName[disk.Name] = disk
	}
	if byName["/dev/sda"].Role != "system" || !byName["/dev/sda"].IsSystem {
		t.Fatalf("system disk wrong: %+v", byName["/dev/sda"])
	}
	if byName["/dev/sdb"].Role != "data" || byName["/dev/sdb"].FreeGB < 189 {
		t.Fatalf("ordinary data disk wrong: %+v", byName["/dev/sdb"])
	}
	if byName["/dev/sdc"].Role != "reserved" || !byName["/dev/sdc"].IsReserved {
		t.Fatalf("reserved disk wrong: %+v", byName["/dev/sdc"])
	}
	if len(inv.UnusedDisks) != 1 || inv.UnusedDisks[0].Name != "/dev/sdb2" || inv.UnusedDisks[0].Type != "part" || inv.UnusedDisks[0].ParentDisk != "/dev/sdb" {
		t.Fatalf("partition candidates wrong: %+v", inv.UnusedDisks)
	}
}

func TestParseInventory_MapsLVToPhysicalDisks(t *testing.T) {
	const out = "###VGS###\nvg_cross,200.00g,100.00g\n" +
		"###LVS###\nvg_cross,lv_a,100.00g,/dev/vg_cross/lv_a,/dev/sdb1(0),/dev/nvme1n1p1(0)\n" +
		"###PVS###\n/dev/sdb1,100.00g,50.00g,vg_cross\n/dev/nvme1n1p1,100.00g,50.00g,vg_cross\n" +
		"###DF###\n###NFS###\ninactive\n###EXPORTS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdb1" TYPE="part" SIZE="100000000000" MOUNTPOINT="" FSTYPE="LVM2_member" PKNAME="sdb"` + "\n" +
		`NAME="nvme1n1" TYPE="disk" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="nvme1n1p1" TYPE="part" SIZE="100000000000" MOUNTPOINT="" FSTYPE="LVM2_member" PKNAME="nvme1n1"`
	inv := parseInventory(out)
	if len(inv.LVs) != 1 || len(inv.LVs[0].PhysicalDisks) != 2 {
		t.Fatalf("LV physical mapping wrong: %+v", inv.LVs)
	}
	if inv.LVs[0].PhysicalDisks[0] != "/dev/nvme1n1" || inv.LVs[0].PhysicalDisks[1] != "/dev/sdb" {
		t.Fatalf("LV physical disks should be stable sorted: %+v", inv.LVs[0].PhysicalDisks)
	}
}

func TestParseInventory_UnmountedFilesystemIsCandidate(t *testing.T) {
	// A disk or partition with a preexisting unmounted filesystem (e.g. ext4 or xfs)
	// that is not mounted, not system, and not reserved must be recognized as an
	// unused initialization candidate so the panel can format it into a VG.
	const out = "###VGS###\n###LVS###\n###PVS###\n###DF###\n" +
		"Filesystem 1024-blocks Used Available Capacity Mounted on\n" +
		"/dev/sda1 100000000000 10000000000 90000000000 10% /\n" +
		"###NFS###\ninactive\n###EXPORTS###\n###LSBLK###\n" +
		`NAME="sda" TYPE="disk" SIZE="100000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sda1" TYPE="part" SIZE="100000000000" MOUNTPOINT="/" FSTYPE="ext4" PKNAME="sda"` + "\n" +
		`NAME="sdb" TYPE="disk" SIZE="200000000000" MOUNTPOINT="" FSTYPE="ext4" PKNAME=""` + "\n" +
		`NAME="sdc" TYPE="disk" SIZE="200000000000" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdc1" TYPE="part" SIZE="200000000000" MOUNTPOINT="" FSTYPE="xfs" PKNAME="sdc"`

	inv := parseInventory(out)
	if len(inv.UnusedDisks) != 2 {
		t.Fatalf("expected 2 unused disks, got %d: %+v", len(inv.UnusedDisks), inv.UnusedDisks)
	}
	names := []string{inv.UnusedDisks[0].Name, inv.UnusedDisks[1].Name}
	if names[0] != "/dev/sdb" || names[1] != "/dev/sdc1" {
		t.Fatalf("expected /dev/sdb and /dev/sdc1 as candidates, got %v", names)
	}

	byName := map[string]PhysicalDiskInfo{}
	for _, disk := range inv.PhysicalDisks {
		byName[disk.Name] = disk
	}
	if byName["/dev/sdb"].Role != "unused" {
		t.Fatalf("expected sdb role to be unused, got %s", byName["/dev/sdb"].Role)
	}
	if byName["/dev/sdc"].Role != "unused" {
		t.Fatalf("expected sdc role to be unused, got %s", byName["/dev/sdc"].Role)
	}
}

func TestParseInventory_OrphanedPVIsCandidate(t *testing.T) {
	// A device that was previously initialized with pvcreate but does not belong
	// to any active VG must be recognized as an unused candidate.
	const out = "###VGS###\n###LVS###\n###PVS###\n/dev/sdb,100.00g,100.00g,\n###DF###\n" +
		"###NFS###\ninactive\n###EXPORTS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="107374182400" MOUNTPOINT="" FSTYPE="LVM2_member" PKNAME=""`

	inv := parseInventory(out)
	if len(inv.UnusedDisks) != 1 || inv.UnusedDisks[0].Name != "/dev/sdb" {
		t.Fatalf("expected orphaned PV to be unused candidate: %+v", inv.UnusedDisks)
	}
}

// TestListInventory_Run verifies the SSH round-trip: the runner's output is fed
// to parseInventory unchanged.
func TestListInventory_Run(t *testing.T) {
	r := &fakeRunner{out: realisticInventory}
	inv, err := ListInventory(context.Background(), r, db.WorkerNode{})
	if err != nil {
		t.Fatal(err)
	}
	if len(inv.VGs) != 1 || len(inv.LVs) != 2 || len(inv.UnusedDisks) != 1 {
		t.Fatalf("inventory counts wrong: %+v", inv)
	}
}

func TestListInventory_Error(t *testing.T) {
	// A non-zero exit code from the probe must surface as an error.
	r := &errRunner{}
	if _, err := ListInventory(context.Background(), r, db.WorkerNode{}); err == nil {
		t.Fatal("expected error on non-zero exit")
	}
}

// errRunner returns exit code 1 to simulate a probe failure.
type errRunner struct{}

func (e *errRunner) Run(_ context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	return "", "boom", 1, nil
}
func (e *errRunner) RunWithStdin(_ context.Context, _ db.WorkerNode, _ string, _ io.Reader) (string, string, int, error) {
	return "", "", 1, nil
}
