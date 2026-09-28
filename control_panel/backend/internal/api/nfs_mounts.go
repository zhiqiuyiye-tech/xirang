package api

import (
	"context"
	"encoding/json"
	"math"
	"net"
	"path"
	"sort"
	"strconv"
	"strings"
	"time"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"

	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/storage"
)

type containerMountInfo struct {
	ContainerName string `json:"container_name"`
	MountPath     string `json:"mount_path"`
	ReadOnly      bool   `json:"read_only"`
}

type nfsVolumeCapacity struct {
	LVSizeGB         *float64   `json:"lv_size_gb"`
	FilesystemUsedGB *float64   `json:"filesystem_used_gb"`
	FilesystemFreeGB *float64   `json:"filesystem_free_gb"`
	FilesystemUsePct *string    `json:"filesystem_use_pct"`
	Known            bool       `json:"known"`
	CollectedAt      *time.Time `json:"collected_at"`
	Stale            bool       `json:"stale"`
	Scope            string     `json:"scope"`
}

type podNFSMount struct {
	Status             string               `json:"status"`
	Reason             string               `json:"reason"`
	NFSSourceConfirmed bool                 `json:"nfs_source_confirmed"`
	PVCName            string               `json:"pvc_name"`
	PVName             string               `json:"pv_name"`
	WorkerID           *int64               `json:"worker_id,omitempty"`
	WorkerName         string               `json:"worker_name,omitempty"`
	VGName             string               `json:"vg_name,omitempty"`
	LVName             string               `json:"lv_name,omitempty"`
	ExportPath         string               `json:"export_path"`
	ContainerMounts    []containerMountInfo `json:"container_mounts"`
	Capacity           *nfsVolumeCapacity   `json:"capacity"`
	nfsServer          string               `json:"-"`
	nfsPath            string               `json:"-"`
}

type notebookPodMountResponse struct {
	k8s.PodInfo
	NFSMounts       []podNFSMount `json:"nfs_mounts"`
	NFSMountsStatus string        `json:"nfs_mounts_status"`
	NFSMountsError  string        `json:"nfs_mounts_error,omitempty"`
}

type mountedPodInfo struct {
	Namespace       string               `json:"namespace"`
	PodName         string               `json:"pod_name"`
	PodUID          string               `json:"pod_uid"`
	OwnerName       string               `json:"owner_name"`
	Note            string               `json:"note"`
	PVCName         string               `json:"pvc_name"`
	PVName          string               `json:"pv_name"`
	ExportPath      string               `json:"export_path"`
	ContainerMounts []containerMountInfo `json:"container_mounts"`
}

type unmatchedNFSMountInfo struct {
	WorkerID        int64  `json:"worker_id"`
	WorkerName      string `json:"worker_name"`
	Namespace       string `json:"namespace"`
	PodName         string `json:"pod_name"`
	PodUID          string `json:"pod_uid"`
	OwnerName       string `json:"owner_name"`
	Note            string `json:"note"`
	PVCName         string `json:"pvc_name"`
	PVName          string `json:"pv_name"`
	NFSServer       string `json:"nfs_server"`
	NFSPath         string `json:"nfs_path"`
	Status          string `json:"status"`
	SourceStatus    string `json:"source_status,omitempty"`
	Reason          string `json:"reason"`
	CandidateWorker bool   `json:"candidate_worker,omitempty"`
}

type lvWithMountedPods struct {
	storage.LVInfo
	MountedPods []mountedPodInfo `json:"mounted_pods"`
}

type inventoryWithMountAssociation struct {
	NFS                    storage.NFSStatusInfo      `json:"nfs"`
	VGs                    []storage.VGInfo           `json:"vgs"`
	LVs                    []lvWithMountedPods        `json:"lvs"`
	PhysicalDisks          []storage.PhysicalDiskInfo `json:"physical_disks"`
	UnusedDisks            []storage.DiskInfo         `json:"unused_disks"`
	MountAssociationStatus string                     `json:"mount_association_status"`
	MountAssociationError  string                     `json:"mount_association_error,omitempty"`
	UnmatchedMounts        []unmatchedNFSMountInfo    `json:"unmatched_mounts"`
}

type nfsWorkerInventory struct {
	inventory   storage.InventoryInfo
	collectedAt *time.Time
	hasSnapshot bool
}

type workerMountAssociation struct {
	status             string
	errorCode          string
	unmatchedMounts    []unmatchedNFSMountInfo
	mountedPodsByLV    map[string][]mountedPodInfo
	hasServerCandidate bool
	hasIssue           bool
	matchedCount       int
}

type nfsAssociationResult struct {
	pods          []notebookPodMountResponse
	workers       map[int64]*workerMountAssociation
	errorCode     string
	podListFailed bool
}

type podClaimUse struct {
	claimName string
	mounts    []containerMountInfo
}

type nfsPVSource struct {
	confirmed bool
	server    string
	path      string
	reason    string
}

func queryNFSAssociations(
	ctx context.Context,
	client kubernetes.Interface,
	store *db.Store,
	workers []db.WorkerNode,
	inventories map[int64]nfsWorkerInventory,
	staleAfter time.Duration,
	preflightErrorCode string,
) nfsAssociationResult {
	result := newNFSAssociationResult(workers)
	if client == nil {
		result.fail("k8s_client_unavailable")
		return result
	}

	pods, err := k8s.ListNotebookPodObjects(ctx, client)
	if err != nil {
		result.podListFailed = true
		result.fail("pod_list_failed")
		return result
	}
	podInfos := make([]k8s.PodInfo, 0, len(pods))
	for _, pod := range pods {
		podInfos = append(podInfos, k8s.NotebookPodInfo(pod))
	}
	joinNotebookMetadata(ctx, store, podInfos)
	result.pods = make([]notebookPodMountResponse, len(podInfos))
	for i := range podInfos {
		result.pods[i] = notebookPodMountResponse{
			PodInfo: podInfos[i], NFSMounts: []podNFSMount{}, NFSMountsStatus: "none",
		}
	}

	pvcList, err := client.CoreV1().PersistentVolumeClaims("").List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		result.fail("pvc_list_failed")
		return result
	}
	pvList, err := client.CoreV1().PersistentVolumes().List(ctx, metav1.ListOptions{ResourceVersion: "0"})
	if err != nil {
		result.fail("pv_list_failed")
		return result
	}
	if preflightErrorCode != "" {
		result.fail(preflightErrorCode)
		return result
	}

	pvcs := make(map[string]corev1.PersistentVolumeClaim, len(pvcList.Items))
	for i := range pvcList.Items {
		pvc := pvcList.Items[i]
		pvcs[namespacedKey(pvc.Namespace, pvc.Name)] = pvc
	}
	pvs := make(map[string]corev1.PersistentVolume, len(pvList.Items))
	for i := range pvList.Items {
		pv := pvList.Items[i]
		pvs[pv.Name] = pv
	}
	workersByServer := indexWorkersByServer(workers)

	for i := range pods {
		podMounts := tracePodPVCReferences(pods[i], pvcs, pvs)
		for j := range podMounts {
			resolvePodNFSMount(&podMounts[j], result.pods[i].PodInfo, workersByServer, inventories, result.workers, staleAfter)
		}
		result.pods[i].NFSMounts = podMounts
		result.pods[i].NFSMountsStatus = summarizePodNFSMounts(podMounts)
	}
	for _, state := range result.workers {
		state.unmatchedMounts = nonNilUnmatched(state.unmatchedMounts)
		sort.Slice(state.unmatchedMounts, func(i, j int) bool {
			if state.unmatchedMounts[i].Namespace != state.unmatchedMounts[j].Namespace {
				return state.unmatchedMounts[i].Namespace < state.unmatchedMounts[j].Namespace
			}
			if state.unmatchedMounts[i].PodName != state.unmatchedMounts[j].PodName {
				return state.unmatchedMounts[i].PodName < state.unmatchedMounts[j].PodName
			}
			return state.unmatchedMounts[i].PVCName < state.unmatchedMounts[j].PVCName
		})
		for key := range state.mountedPodsByLV {
			mounted := state.mountedPodsByLV[key]
			sort.Slice(mounted, func(i, j int) bool {
				if mounted[i].Namespace != mounted[j].Namespace {
					return mounted[i].Namespace < mounted[j].Namespace
				}
				if mounted[i].PodName != mounted[j].PodName {
					return mounted[i].PodName < mounted[j].PodName
				}
				if mounted[i].PVCName != mounted[j].PVCName {
					return mounted[i].PVCName < mounted[j].PVCName
				}
				return mounted[i].PVName < mounted[j].PVName
			})
			state.mountedPodsByLV[key] = mounted
		}
		state.status = summarizeWorkerMounts(state)
	}
	return result
}

func queryNFSAssociationsFromStore(
	ctx context.Context,
	client kubernetes.Interface,
	store *db.Store,
	staleAfter time.Duration,
) nfsAssociationResult {
	if store == nil {
		return queryNFSAssociations(ctx, client, nil, nil, nil, staleAfter, "worker_list_failed")
	}
	workers, err := store.ListWorkers(ctx)
	if err != nil {
		return queryNFSAssociations(ctx, client, store, nil, nil, staleAfter, "worker_list_failed")
	}
	snapshots, err := store.ListInventorySnapshots(ctx)
	if err != nil {
		return queryNFSAssociations(ctx, client, store, workers, nil, staleAfter, "inventory_snapshot_list_failed")
	}
	return queryNFSAssociations(ctx, client, store, workers, parseNFSWorkerInventories(snapshots), staleAfter, "")
}

func newNFSAssociationResult(workers []db.WorkerNode) nfsAssociationResult {
	result := nfsAssociationResult{
		pods:    []notebookPodMountResponse{},
		workers: make(map[int64]*workerMountAssociation, len(workers)),
	}
	for _, worker := range workers {
		result.workers[worker.ID] = &workerMountAssociation{
			unmatchedMounts: []unmatchedNFSMountInfo{},
			mountedPodsByLV: make(map[string][]mountedPodInfo),
		}
	}
	return result
}

func (result *nfsAssociationResult) fail(code string) {
	result.errorCode = code
	for i := range result.pods {
		result.pods[i].NFSMounts = []podNFSMount{}
		result.pods[i].NFSMountsStatus = "lookup_failed"
		result.pods[i].NFSMountsError = code
	}
	for _, state := range result.workers {
		state.status = "lookup_failed"
		state.errorCode = code
		state.unmatchedMounts = []unmatchedNFSMountInfo{}
		state.mountedPodsByLV = make(map[string][]mountedPodInfo)
	}
}

func joinNotebookMetadata(ctx context.Context, store *db.Store, pods []k8s.PodInfo) {
	if store == nil || len(pods) == 0 {
		return
	}
	keys := make([]string, 0, len(pods))
	for _, pod := range pods {
		if pod.StableKey != "" {
			keys = append(keys, pod.StableKey)
		}
	}
	metadata, err := store.GetNotebookMetadataByKeys(ctx, keys)
	if err != nil {
		return
	}
	for i := range pods {
		if entry, ok := metadata[pods[i].StableKey]; ok {
			pods[i].OwnerName = entry.OwnerName
			pods[i].Note = entry.Note
			pods[i].UpdatedBy = entry.UpdatedBy
			updatedAt := entry.UpdatedAt
			pods[i].MetadataUpdatedAt = &updatedAt
		}
	}
}

func tracePodPVCReferences(
	pod corev1.Pod,
	pvcs map[string]corev1.PersistentVolumeClaim,
	pvs map[string]corev1.PersistentVolume,
) []podNFSMount {
	claims := make(map[string]*podClaimUse)
	claimByVolume := make(map[string]string)
	for _, volume := range pod.Spec.Volumes {
		if volume.PersistentVolumeClaim == nil || volume.PersistentVolumeClaim.ClaimName == "" {
			continue
		}
		key := namespacedKey(pod.Namespace, volume.PersistentVolumeClaim.ClaimName)
		use := claims[key]
		if use == nil {
			use = &podClaimUse{claimName: volume.PersistentVolumeClaim.ClaimName, mounts: []containerMountInfo{}}
			claims[key] = use
		}
		claimByVolume[volume.Name] = key
	}

	collectContainerMounts := func(container corev1.Container) {
		for _, volumeMount := range container.VolumeMounts {
			key, ok := claimByVolume[volumeMount.Name]
			if !ok {
				continue
			}
			claims[key].mounts = append(claims[key].mounts, containerMountInfo{
				ContainerName: container.Name,
				MountPath:     volumeMount.MountPath,
				ReadOnly:      volumeMount.ReadOnly,
			})
		}
	}
	for _, container := range pod.Spec.Containers {
		collectContainerMounts(container)
	}
	for _, container := range pod.Spec.InitContainers {
		collectContainerMounts(container)
	}

	keys := make([]string, 0, len(claims))
	for key := range claims {
		keys = append(keys, key)
	}
	sort.Strings(keys)
	out := make([]podNFSMount, 0, len(keys))
	for _, key := range keys {
		use := claims[key]
		mounts := sortedContainerMounts(use.mounts)
		item := podNFSMount{
			PVCName: use.claimName, ContainerMounts: mounts, Capacity: nil,
		}
		pvc, exists := pvcs[key]
		if !exists {
			item.Status, item.Reason = "missing_claim", "pvc_not_found"
			out = append(out, item)
			continue
		}
		if pvc.Status.Phase != corev1.ClaimBound || pvc.Spec.VolumeName == "" {
			item.Status, item.Reason = "pending", "pvc_not_bound"
			out = append(out, item)
			continue
		}
		pvName := pvc.Spec.VolumeName
		item.PVName = pvName
		pv, exists := pvs[pvName]
		if !exists {
			item.Status, item.Reason = "missing_pv", "pv_not_found"
			out = append(out, item)
			continue
		}
		source, isNFS := extractNFSPVSource(pv)
		if !isNFS {
			continue
		}
		item.PVName = pv.Name
		item.NFSSourceConfirmed = source.confirmed
		item.nfsServer = source.server
		item.nfsPath = source.path
		if source.reason != "" {
			item.Status, item.Reason = "unsupported", source.reason
		} else {
			item.Status = "unmatched"
		}
		out = append(out, item)
	}
	return out
}

func extractNFSPVSource(pv corev1.PersistentVolume) (nfsPVSource, bool) {
	var server, exportPath string
	isCSI := false
	switch {
	case pv.Spec.NFS != nil:
		server, exportPath = pv.Spec.NFS.Server, pv.Spec.NFS.Path
	case pv.Spec.CSI != nil && pv.Spec.CSI.Driver == "nfs.csi.k8s.io":
		isCSI = true
		server = pv.Spec.CSI.VolumeAttributes["server"]
		exportPath = pv.Spec.CSI.VolumeAttributes["share"]
	default:
		return nfsPVSource{}, false
	}

	source := nfsPVSource{confirmed: true}
	normalizedServer, serverOK := normalizeNFSServer(server)
	normalizedPath, pathOK := normalizeNFSPath(exportPath)
	if strings.TrimSpace(server) == "" {
		source.reason = "missing_nfs_server"
	} else if !serverOK {
		source.reason = "unsupported_nfs_format"
	} else {
		source.server = normalizedServer
	}
	if source.reason == "" {
		if strings.TrimSpace(exportPath) == "" {
			if isCSI {
				source.reason = "missing_csi_share"
			} else {
				source.reason = "missing_nfs_path"
			}
		} else if !pathOK {
			source.reason = "unsupported_nfs_format"
		} else {
			source.path = normalizedPath
		}
	}
	return source, true
}

func indexWorkersByServer(workers []db.WorkerNode) map[string][]db.WorkerNode {
	out := make(map[string][]db.WorkerNode, len(workers))
	for _, worker := range workers {
		server, ok := normalizeNFSServer(worker.Host)
		if ok {
			out[server] = append(out[server], worker)
		}
	}
	return out
}

func normalizeNFSServer(value string) (string, bool) {
	server := strings.TrimSpace(value)
	if server == "" {
		return "", false
	}
	if strings.HasPrefix(server, "[") && strings.HasSuffix(server, "]") {
		server = server[1 : len(server)-1]
	}
	if ip := net.ParseIP(server); ip != nil {
		return ip.String(), true
	}
	server = strings.ToLower(strings.TrimSuffix(server, "."))
	if server == "" || len(server) > 253 {
		return "", false
	}
	for _, label := range strings.Split(server, ".") {
		if label == "" || len(label) > 63 || label[0] == '-' || label[len(label)-1] == '-' {
			return "", false
		}
		for _, r := range label {
			if !(r >= 'a' && r <= 'z') && !(r >= '0' && r <= '9') && r != '-' {
				return "", false
			}
		}
	}
	return server, true
}

func normalizeNFSPath(value string) (string, bool) {
	cleaned := strings.TrimSpace(value)
	if cleaned == "" || !strings.HasPrefix(cleaned, "/") || strings.ContainsRune(cleaned, '\x00') {
		return "", false
	}
	return path.Clean(cleaned), true
}

func resolvePodNFSMount(
	mount *podNFSMount,
	pod k8s.PodInfo,
	workersByServer map[string][]db.WorkerNode,
	inventories map[int64]nfsWorkerInventory,
	workerStates map[int64]*workerMountAssociation,
	staleAfter time.Duration,
) {
	if !mount.NFSSourceConfirmed {
		return
	}
	if mount.Reason != "" {
		mount.Reason = safeMountReason(mount.Reason)
	}
	candidates := workersByServer[mount.nfsServer]
	if mount.Status == "unsupported" {
		if len(candidates) == 1 {
			if state := workerStates[candidates[0].ID]; state != nil {
				state.hasServerCandidate = true
				recordWorkerMountIssue(state, candidates[0], pod, *mount, "unsupported", "unsupported", mount.Reason, false)
			}
		} else if len(candidates) > 1 {
			for _, worker := range candidates {
				if state := workerStates[worker.ID]; state != nil {
					state.hasServerCandidate = true
					recordWorkerMountIssue(state, worker, pod, *mount, "ambiguous", "unsupported", mount.Reason, true)
				}
			}
		}
		return
	}

	if len(candidates) == 0 {
		mount.Status, mount.Reason = "unmatched", "worker_not_found"
		return
	}
	if len(candidates) > 1 {
		mount.Status, mount.Reason = "ambiguous", "multiple_workers"
		for _, worker := range candidates {
			if state := workerStates[worker.ID]; state != nil {
				state.hasServerCandidate = true
				recordWorkerMountIssue(state, worker, pod, *mount, "ambiguous", "", mount.Reason, true)
			}
		}
		return
	}

	worker := candidates[0]
	state := workerStates[worker.ID]
	if state != nil {
		state.hasServerCandidate = true
	}
	inventory := inventories[worker.ID]
	lv, exportPath, status, reason := matchNFSExportToLV(inventory.inventory, mount.nfsPath)
	if status != "matched" {
		mount.Status, mount.Reason = status, safeMountReason(reason)
		if state != nil {
			state.hasIssue = true
			recordWorkerMountIssue(state, worker, pod, *mount, status, "", mount.Reason, false)
		}
		return
	}

	workerID := worker.ID
	mount.Status = "matched"
	mount.Reason = ""
	mount.WorkerID = &workerID
	mount.WorkerName = worker.Name
	mount.VGName = lv.VGName
	mount.LVName = lv.Name
	mount.ExportPath = exportPath
	mount.Capacity = buildNFSVolumeCapacity(lv, inventory, staleAfter)
	if state != nil {
		state.matchedCount++
		key := lvAssociationKey(lv.VGName, lv.Name)
		state.mountedPodsByLV[key] = append(state.mountedPodsByLV[key], mountedPodInfo{
			Namespace: pod.Namespace, PodName: pod.Name, PodUID: pod.UID,
			OwnerName: pod.OwnerName, Note: pod.Note,
			PVCName: mount.PVCName, PVName: mount.PVName, ExportPath: exportPath,
			ContainerMounts: mount.ContainerMounts,
		})
	}
}

func recordWorkerMountIssue(
	state *workerMountAssociation,
	worker db.WorkerNode,
	pod k8s.PodInfo,
	mount podNFSMount,
	status, sourceStatus, reason string,
	candidate bool,
) {
	state.hasIssue = true
	state.unmatchedMounts = append(state.unmatchedMounts, unmatchedNFSMountInfo{
		WorkerID: worker.ID, WorkerName: worker.Name,
		Namespace: pod.Namespace, PodName: pod.Name, PodUID: pod.UID,
		OwnerName: pod.OwnerName, Note: pod.Note,
		PVCName: mount.PVCName, PVName: mount.PVName,
		NFSServer: mount.nfsServer, NFSPath: mount.nfsPath,
		Status: status, SourceStatus: sourceStatus,
		Reason: safeMountReason(reason), CandidateWorker: candidate,
	})
}

func matchNFSExportToLV(inventory storage.InventoryInfo, nfsPath string) (storage.LVInfo, string, string, string) {
	exports := make(map[string]struct{}, len(inventory.NFS.Exports))
	for _, rawExport := range inventory.NFS.Exports {
		if exportPath, ok := normalizeNFSPath(rawExport); ok {
			exports[exportPath] = struct{}{}
		}
	}
	var matchingExports []string
	longestExport := -1
	for exportPath := range exports {
		if !pathWithin(nfsPath, exportPath) {
			continue
		}
		if len(exportPath) > longestExport {
			matchingExports = []string{exportPath}
			longestExport = len(exportPath)
		} else if len(exportPath) == longestExport {
			matchingExports = append(matchingExports, exportPath)
		}
	}
	if len(matchingExports) == 0 {
		return storage.LVInfo{}, "", "unmatched", "export_not_found"
	}
	if len(matchingExports) > 1 {
		return storage.LVInfo{}, "", "ambiguous", "multiple_exports"
	}
	exportPath := matchingExports[0]

	var matchingLVs []storage.LVInfo
	longestMount := -1
	for _, lv := range inventory.LVs {
		mountPoint, ok := normalizeNFSPath(lv.MountPoint)
		if !ok || !pathWithin(exportPath, mountPoint) {
			continue
		}
		if len(mountPoint) > longestMount {
			matchingLVs = []storage.LVInfo{lv}
			longestMount = len(mountPoint)
		} else if len(mountPoint) == longestMount {
			matchingLVs = append(matchingLVs, lv)
		}
	}
	if len(matchingLVs) == 0 {
		return storage.LVInfo{}, "", "unmatched", "lv_not_found"
	}
	if len(matchingLVs) > 1 {
		return storage.LVInfo{}, "", "ambiguous", "multiple_lvs"
	}
	return matchingLVs[0], exportPath, "matched", ""
}

func summarizePodNFSMounts(mounts []podNFSMount) string {
	if len(mounts) == 0 {
		return "none"
	}
	matched, pending := 0, 0
	for _, mount := range mounts {
		switch mount.Status {
		case "matched":
			matched++
		case "pending":
			pending++
		default:
			return "partial"
		}
	}
	if pending > 0 {
		if matched == 0 && pending == len(mounts) {
			return "pending"
		}
		return "partial"
	}
	if matched == len(mounts) {
		return "available"
	}
	return "partial"
}

func summarizeWorkerMounts(state *workerMountAssociation) string {
	if state.errorCode != "" {
		return "lookup_failed"
	}
	if !state.hasServerCandidate {
		return "none"
	}
	if state.hasIssue || state.matchedCount == 0 {
		return "partial"
	}
	return "available"
}

func buildNFSVolumeCapacity(lv storage.LVInfo, inventory nfsWorkerInventory, staleAfter time.Duration) *nfsVolumeCapacity {
	capacity := &nfsVolumeCapacity{
		CollectedAt: inventory.collectedAt,
		Stale:       inventory.collectedAt == nil || (staleAfter > 0 && time.Since(*inventory.collectedAt) > staleAfter),
		Scope:       "volume",
	}
	if !inventory.hasSnapshot || inventory.collectedAt == nil {
		capacity.Stale = true
		return capacity
	}

	sizeKnown := lv.SizeKnown
	usedKnown := lv.UsedKnown
	freeKnown := lv.FreeKnown
	usePctKnown := lv.UsePctKnown
	if !lv.CapacityValidityKnown {
		// Older cached inventory payloads predate the per-field markers. Preserve
		// values from those snapshots using the previous FreeKnown contract.
		sizeKnown = lv.SizeGB > 0
		usedKnown = lv.FreeKnown
		freeKnown = lv.FreeKnown
		usePctKnown = lv.FreeKnown && parseNFSPercent(lv.UsePct)
	}
	if sizeKnown && lv.SizeGB > 0 && !math.IsNaN(lv.SizeGB) && !math.IsInf(lv.SizeGB, 0) {
		value := lv.SizeGB
		capacity.LVSizeGB = &value
	}
	if usedKnown && lv.UsedGB >= 0 && !math.IsNaN(lv.UsedGB) && !math.IsInf(lv.UsedGB, 0) {
		value := lv.UsedGB
		capacity.FilesystemUsedGB = &value
	}
	if freeKnown && lv.FreeGB >= 0 && !math.IsNaN(lv.FreeGB) && !math.IsInf(lv.FreeGB, 0) {
		value := lv.FreeGB
		capacity.FilesystemFreeGB = &value
	}
	if usePctKnown && strings.TrimSpace(lv.UsePct) != "" {
		value := lv.UsePct
		capacity.FilesystemUsePct = &value
	}
	capacity.Known = capacity.LVSizeGB != nil && capacity.FilesystemUsedGB != nil &&
		capacity.FilesystemFreeGB != nil && capacity.FilesystemUsePct != nil
	return capacity
}

func withMountedPods(lvs []storage.LVInfo, state *workerMountAssociation) []lvWithMountedPods {
	out := make([]lvWithMountedPods, len(lvs))
	for i, lv := range lvs {
		var mounted []mountedPodInfo
		if state != nil {
			mounted = state.mountedPodsByLV[lvAssociationKey(lv.VGName, lv.Name)]
		}
		if mounted == nil {
			mounted = []mountedPodInfo{}
		}
		out[i] = lvWithMountedPods{LVInfo: lv, MountedPods: mounted}
	}
	return out
}

func lvAssociationKey(vgName, lvName string) string {
	return vgName + "\x00" + lvName
}

func namespacedKey(namespace, name string) string {
	return namespace + "\x00" + name
}

func pathWithin(candidate, root string) bool {
	if candidate == root {
		return true
	}
	if root == "/" {
		return strings.HasPrefix(candidate, "/")
	}
	return strings.HasPrefix(candidate, strings.TrimSuffix(root, "/")+"/")
}

func nonNilUnmatched(values []unmatchedNFSMountInfo) []unmatchedNFSMountInfo {
	if values == nil {
		return []unmatchedNFSMountInfo{}
	}
	return values
}

func sortedContainerMounts(mounts []containerMountInfo) []containerMountInfo {
	if len(mounts) == 0 {
		return []containerMountInfo{}
	}
	sort.Slice(mounts, func(i, j int) bool {
		if mounts[i].ContainerName != mounts[j].ContainerName {
			return mounts[i].ContainerName < mounts[j].ContainerName
		}
		if mounts[i].MountPath != mounts[j].MountPath {
			return mounts[i].MountPath < mounts[j].MountPath
		}
		return !mounts[i].ReadOnly && mounts[j].ReadOnly
	})
	unique := mounts[:0]
	for _, mount := range mounts {
		if len(unique) > 0 && unique[len(unique)-1] == mount {
			continue
		}
		unique = append(unique, mount)
	}
	return unique
}

func parseNFSWorkerInventories(snapshots []db.InventorySnapshot) map[int64]nfsWorkerInventory {
	out := make(map[int64]nfsWorkerInventory, len(snapshots))
	for _, snapshot := range snapshots {
		entry := nfsWorkerInventory{collectedAt: snapshot.CollectedAt, hasSnapshot: snapshot.PayloadJSON != ""}
		if snapshot.PayloadJSON != "" {
			_ = json.Unmarshal([]byte(snapshot.PayloadJSON), &entry.inventory)
		}
		out[snapshot.WorkerID] = entry
	}
	return out
}

func inventoryResponseWithMounts(inventory storage.InventoryInfo, state *workerMountAssociation) inventoryWithMountAssociation {
	response := inventoryWithMountAssociation{
		NFS: inventory.NFS, VGs: inventory.VGs,
		LVs:           withMountedPods(inventory.LVs, state),
		PhysicalDisks: inventory.PhysicalDisks, UnusedDisks: inventory.UnusedDisks,
		UnmatchedMounts: []unmatchedNFSMountInfo{},
	}
	if state != nil {
		response.MountAssociationStatus = state.status
		response.MountAssociationError = state.errorCode
		response.UnmatchedMounts = nonNilUnmatched(state.unmatchedMounts)
	} else {
		response.MountAssociationStatus = "none"
	}
	return response
}

func safeMountReason(reason string) string {
	// Reasons are created from this fixed vocabulary; unknown input must not
	// leak a raw Kubernetes object or API error into the response.
	switch reason {
	case "pvc_not_found", "pv_not_found", "pvc_not_bound", "worker_not_found",
		"export_not_found", "lv_not_found", "multiple_workers", "multiple_exports",
		"multiple_lvs", "missing_nfs_server", "missing_nfs_path", "missing_csi_share",
		"unsupported_nfs_format":
		return reason
	default:
		return "unsupported_nfs_format"
	}
}

func parseNFSPercent(value string) bool {
	if !strings.HasSuffix(value, "%") {
		return false
	}
	pct, err := strconv.ParseFloat(strings.TrimSuffix(value, "%"), 64)
	return err == nil && pct >= 0 && !math.IsNaN(pct) && !math.IsInf(pct, 0)
}
