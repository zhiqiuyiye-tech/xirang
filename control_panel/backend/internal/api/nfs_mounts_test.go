package api

import (
	"testing"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	"xirang/control_panel/internal/storage"
)

func TestTracePodPVCReferencesKeepsPendingAndNFSOnlyRelations(t *testing.T) {
	pod := corev1.Pod{
		ObjectMeta: metav1.ObjectMeta{Name: "notebook-test", Namespace: "ns1", UID: "uid-1"},
		Spec: corev1.PodSpec{
			Volumes: []corev1.Volume{
				{Name: "pending", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "pending-claim"}}},
				{Name: "missing", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "gone"}}},
				{Name: "namespace-isolation", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "same-claim"}}},
				{Name: "orphan", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "orphan-claim"}}},
				{Name: "shared-a", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "nfs-claim"}}},
				{Name: "shared-b", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "nfs-claim"}}},
				{Name: "local", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "local-claim"}}},
				{Name: "unknown-csi", VolumeSource: corev1.VolumeSource{PersistentVolumeClaim: &corev1.PersistentVolumeClaimVolumeSource{ClaimName: "unknown-csi-claim"}}},
			},
			Containers: []corev1.Container{{Name: "notebook", VolumeMounts: []corev1.VolumeMount{
				{Name: "shared-a", MountPath: "/workspace/one", ReadOnly: true},
				{Name: "shared-b", MountPath: "/workspace/two"},
			}}},
			InitContainers: []corev1.Container{{Name: "init-data", VolumeMounts: []corev1.VolumeMount{
				{Name: "shared-b", MountPath: "/init/workspace"},
			}}},
		},
	}
	pvcs := map[string]corev1.PersistentVolumeClaim{
		namespacedKey("ns1", "pending-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "pending-claim", Namespace: "ns1"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimPending},
		},
		namespacedKey("ns2", "same-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "same-claim", Namespace: "ns2"},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: "pv-nfs"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		},
		namespacedKey("ns1", "orphan-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "orphan-claim", Namespace: "ns1"},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: "pv-gone"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		},
		namespacedKey("ns1", "nfs-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "nfs-claim", Namespace: "ns1"},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: "pv-nfs"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		},
		namespacedKey("ns1", "local-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "local-claim", Namespace: "ns1"},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: "pv-local"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		},
		namespacedKey("ns1", "unknown-csi-claim"): {
			ObjectMeta: metav1.ObjectMeta{Name: "unknown-csi-claim", Namespace: "ns1"},
			Spec:       corev1.PersistentVolumeClaimSpec{VolumeName: "pv-unknown-csi"},
			Status:     corev1.PersistentVolumeClaimStatus{Phase: corev1.ClaimBound},
		},
	}
	pvs := map[string]corev1.PersistentVolume{
		"pv-nfs": {
			ObjectMeta: metav1.ObjectMeta{Name: "pv-nfs"},
			Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
				NFS: &corev1.NFSVolumeSource{Server: "WORKER-A.EXAMPLE.", Path: "/exports/./users"},
			}},
		},
		"pv-local": {
			ObjectMeta: metav1.ObjectMeta{Name: "pv-local"},
			Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
				HostPath: &corev1.HostPathVolumeSource{Path: "/var/lib/data"},
			}},
		},
		"pv-unknown-csi": {
			ObjectMeta: metav1.ObjectMeta{Name: "pv-unknown-csi"},
			Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
				CSI: &corev1.CSIPersistentVolumeSource{Driver: "vendor.example/nfs", VolumeAttributes: map[string]string{"server": "worker-a", "share": "/exports"}},
			}},
		},
	}

	mounts := tracePodPVCReferences(pod, pvcs, pvs)
	byPVC := make(map[string]podNFSMount, len(mounts))
	for _, mount := range mounts {
		byPVC[mount.PVCName] = mount
	}
	if len(mounts) != 5 {
		t.Fatalf("expected pending, missing claims, missing PV, and confirmed NFS only; got %+v", mounts)
	}
	if mount := byPVC["pending-claim"]; mount.Status != "pending" || mount.Reason != "pvc_not_bound" || mount.NFSSourceConfirmed {
		t.Fatalf("pending PVC was not represented safely: %+v", mount)
	}
	if mount := byPVC["gone"]; mount.Status != "missing_claim" || mount.Reason != "pvc_not_found" {
		t.Fatalf("missing PVC was not represented: %+v", mount)
	}
	if mount := byPVC["same-claim"]; mount.Status != "missing_claim" || mount.Reason != "pvc_not_found" {
		t.Fatalf("a PVC with the same name in another namespace must not resolve: %+v", mount)
	}
	if mount := byPVC["orphan-claim"]; mount.Status != "missing_pv" || mount.Reason != "pv_not_found" || mount.PVName != "pv-gone" {
		t.Fatalf("missing PV reference was not represented: %+v", mount)
	}
	nfsMount, ok := byPVC["nfs-claim"]
	if !ok || nfsMount.Status != "unmatched" || !nfsMount.NFSSourceConfirmed || nfsMount.PVName != "pv-nfs" {
		t.Fatalf("standard NFS PV was not retained: %+v", nfsMount)
	}
	if nfsMount.nfsServer != "worker-a.example" || nfsMount.nfsPath != "/exports/users" {
		t.Fatalf("NFS source was not normalized: server=%q path=%q", nfsMount.nfsServer, nfsMount.nfsPath)
	}
	if len(nfsMount.ContainerMounts) != 3 {
		t.Fatalf("two volume names and an init container should merge into three paths: %+v", nfsMount.ContainerMounts)
	}
}

func TestExtractNFSPVSourceSupportsOnlyExplicitNFSDrivers(t *testing.T) {
	standard, ok := extractNFSPVSource(corev1.PersistentVolume{
		Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
			NFS: &corev1.NFSVolumeSource{Server: "10.0.0.1", Path: "/exports/work"},
		}},
	})
	if !ok || !standard.confirmed || standard.server != "10.0.0.1" || standard.path != "/exports/work" || standard.reason != "" {
		t.Fatalf("standard NFS source was not extracted: %+v, recognized=%v", standard, ok)
	}

	csi, ok := extractNFSPVSource(corev1.PersistentVolume{
		Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
			CSI: &corev1.CSIPersistentVolumeSource{Driver: "nfs.csi.k8s.io", VolumeAttributes: map[string]string{"server": "worker-a", "share": "/exports/share"}},
		}},
	})
	if !ok || !csi.confirmed || csi.server != "worker-a" || csi.path != "/exports/share" || csi.reason != "" {
		t.Fatalf("supported CSI source was not extracted: %+v, recognized=%v", csi, ok)
	}

	missingShare, ok := extractNFSPVSource(corev1.PersistentVolume{
		Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
			CSI: &corev1.CSIPersistentVolumeSource{Driver: "nfs.csi.k8s.io", VolumeAttributes: map[string]string{"server": "worker-a"}},
		}},
	})
	if !ok || missingShare.reason != "missing_csi_share" || !missingShare.confirmed {
		t.Fatalf("missing CSI share should be a confirmed unsupported NFS source: %+v", missingShare)
	}

	unknown, recognized := extractNFSPVSource(corev1.PersistentVolume{
		Spec: corev1.PersistentVolumeSpec{PersistentVolumeSource: corev1.PersistentVolumeSource{
			CSI: &corev1.CSIPersistentVolumeSource{Driver: "vendor.example/nfs", VolumeAttributes: map[string]string{"server": "worker-a", "share": "/exports"}},
		}},
	})
	if recognized || unknown.confirmed {
		t.Fatalf("unknown CSI driver must not be inferred as NFS: %+v, recognized=%v", unknown, recognized)
	}
}

func TestNFSExportAndLVMatchingUsesPathBoundariesAndMostSpecificMount(t *testing.T) {
	inventory := storage.InventoryInfo{
		NFS: storage.NFSStatusInfo{Exports: []string{"/data", "/data/nfs", "/data/nfs2"}},
		LVs: []storage.LVInfo{
			{Name: "lv-parent", VGName: "vg", MountPoint: "/data"},
			{Name: "lv-nfs", VGName: "vg", MountPoint: "/data/nfs"},
		},
	}
	lv, exportPath, status, reason := matchNFSExportToLV(inventory, "/data/nfs/subdir")
	if status != "matched" || reason != "" || exportPath != "/data/nfs" || lv.Name != "lv-nfs" {
		t.Fatalf("expected deepest export and LV, got lv=%+v export=%q status=%q reason=%q", lv, exportPath, status, reason)
	}
	_, _, status, reason = matchNFSExportToLV(inventory, "/data/nfs2/subdir")
	if status != "matched" || reason != "" {
		t.Fatalf("exact path-segment match to /data/nfs2 should be valid: status=%q reason=%q", status, reason)
	}
	_, _, status, reason = matchNFSExportToLV(storage.InventoryInfo{
		NFS: storage.NFSStatusInfo{Exports: []string{"/share"}},
		LVs: []storage.LVInfo{{Name: "lv-share", MountPoint: "/share"}},
	}, "/share2/user")
	if status != "unmatched" || reason != "export_not_found" {
		t.Fatalf("/share must not match /share2: status=%q reason=%q", status, reason)
	}

	_, _, status, reason = matchNFSExportToLV(storage.InventoryInfo{
		NFS: storage.NFSStatusInfo{Exports: []string{"/exports/user"}},
		LVs: []storage.LVInfo{
			{Name: "lv-a", MountPoint: "/exports"},
			{Name: "lv-b", MountPoint: "/exports"},
		},
	}, "/exports/user")
	if status != "ambiguous" || reason != "multiple_lvs" {
		t.Fatalf("duplicate most-specific LV candidates must remain ambiguous: status=%q reason=%q", status, reason)
	}
}

func TestBuildNFSVolumeCapacityKeepsPartialValuesAndSeparatesStaleness(t *testing.T) {
	collectedAt := time.Now().UTC().Add(-11 * time.Minute)
	completeLV := storage.LVInfo{
		SizeGB: 200, SizeKnown: true, CapacityValidityKnown: true,
		UsedGB: 0, UsedKnown: true, FreeGB: 120, FreeKnown: true,
		UsePct: "0%", UsePctKnown: true,
	}
	complete := buildNFSVolumeCapacity(completeLV, nfsWorkerInventory{
		inventory: storage.InventoryInfo{}, collectedAt: &collectedAt, hasSnapshot: true,
	}, 10*time.Minute)
	if !complete.Known || !complete.Stale || complete.LVSizeGB == nil || *complete.LVSizeGB != 200 ||
		complete.FilesystemUsedGB == nil || *complete.FilesystemUsedGB != 0 || complete.FilesystemFreeGB == nil ||
		*complete.FilesystemFreeGB != 120 || complete.FilesystemUsePct == nil || *complete.FilesystemUsePct != "0%" {
		t.Fatalf("complete but stale capacity should retain collected values: %+v", complete)
	}

	partialLV := completeLV
	partialLV.UsedKnown = false
	partialLV.UsePctKnown = false
	partial := buildNFSVolumeCapacity(partialLV, nfsWorkerInventory{
		inventory: storage.InventoryInfo{}, collectedAt: &collectedAt, hasSnapshot: true,
	}, 10*time.Minute)
	if partial.Known || partial.LVSizeGB == nil || partial.FilesystemFreeGB == nil ||
		partial.FilesystemUsedGB != nil || partial.FilesystemUsePct != nil {
		t.Fatalf("partial capacity must retain only independently valid values: %+v", partial)
	}

	unknown := buildNFSVolumeCapacity(completeLV, nfsWorkerInventory{}, 10*time.Minute)
	if unknown.Known || !unknown.Stale || unknown.CollectedAt != nil || unknown.LVSizeGB != nil ||
		unknown.FilesystemUsedGB != nil || unknown.FilesystemFreeGB != nil || unknown.FilesystemUsePct != nil {
		t.Fatalf("missing snapshot must be stale and entirely unknown: %+v", unknown)
	}
}

func TestMountAssociationStatusSummaries(t *testing.T) {
	cases := []struct {
		name   string
		mounts []podNFSMount
		want   string
	}{
		{name: "none", mounts: []podNFSMount{}, want: "none"},
		{name: "only pending", mounts: []podNFSMount{{Status: "pending"}}, want: "pending"},
		{name: "all matched", mounts: []podNFSMount{{Status: "matched"}, {Status: "matched"}}, want: "available"},
		{name: "matched with pending", mounts: []podNFSMount{{Status: "matched"}, {Status: "pending"}}, want: "partial"},
		{name: "unresolved", mounts: []podNFSMount{{Status: "missing_pv"}}, want: "partial"},
	}
	for _, test := range cases {
		t.Run(test.name, func(t *testing.T) {
			if got := summarizePodNFSMounts(test.mounts); got != test.want {
				t.Fatalf("status=%q, want %q", got, test.want)
			}
		})
	}

	workerCases := []struct {
		name  string
		state workerMountAssociation
		want  string
	}{
		{name: "none", state: workerMountAssociation{}, want: "none"},
		{name: "matched only", state: workerMountAssociation{hasServerCandidate: true, matchedCount: 1}, want: "available"},
		{name: "candidate issue", state: workerMountAssociation{hasServerCandidate: true, hasIssue: true}, want: "partial"},
		{name: "lookup failed", state: workerMountAssociation{errorCode: "pv_list_failed"}, want: "lookup_failed"},
	}
	for _, test := range workerCases {
		t.Run("worker "+test.name, func(t *testing.T) {
			if got := summarizeWorkerMounts(&test.state); got != test.want {
				t.Fatalf("status=%q, want %q", got, test.want)
			}
		})
	}
}
