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

func TestParseInventory_DiskWithPartitionsExcluded(t *testing.T) {
	// sdb has an unused partition sdb1 (no mount, no fstype). We must NOT offer
	// sdb as unused - wiping it would destroy the partition table.
	const out = "###VGS###\n###LVS###\n###PVS###\n###LSBLK###\n" +
		`NAME="sdb" TYPE="disk" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME=""` + "\n" +
		`NAME="sdb1" TYPE="part" SIZE="10737418240" MOUNTPOINT="" FSTYPE="" PKNAME="sdb"`
	inv := parseInventory(out)
	if len(inv.UnusedDisks) != 0 {
		t.Fatalf("disk with partitions must not be unused: %+v", inv.UnusedDisks)
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
