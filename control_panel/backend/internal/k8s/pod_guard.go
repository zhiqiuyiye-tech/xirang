package k8s

import (
	"context"
	"fmt"
	"net"
	"path"
	"strings"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
)

// CheckNFSPodUsage uses fresh reads, including Pending and Terminating pods.
// Unknown references stop reclamation. Parent hostPath mounts are intentionally
// left to AuthorizeNamespaceCleanup; directly mounted target/child paths block.
func CheckNFSPodUsage(ctx context.Context, client kubernetes.Interface, workerHost, exportPath string) (bool, []string, error) {
	if client == nil {
		return false, nil, fmt.Errorf("kubernetes client is unavailable")
	}
	nodes, err := loadWorkerNodes(ctx, client, workerHost)
	if err != nil {
		return false, nil, err
	}
	target := ""
	if exportPath != "" {
		var ok bool
		target, ok = normalizePath(exportPath)
		if !ok {
			return false, nil, fmt.Errorf("invalid export path: %q", exportPath)
		}
	}
	pods, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pods: %w", err)
	}
	claims, err := client.CoreV1().PersistentVolumeClaims("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pvcs: %w", err)
	}
	volumes, err := client.CoreV1().PersistentVolumes().List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pvs: %w", err)
	}
	pvcs := map[string]corev1.PersistentVolumeClaim{}
	pvs := map[string]corev1.PersistentVolume{}
	for _, pvc := range claims.Items {
		pvcs[pvc.Namespace+"/"+pvc.Name] = pvc
	}
	for _, pv := range volumes.Items {
		pvs[pv.Name] = pv
	}
	var blockers []string
	for _, pod := range pods.Items {
		podID := pod.Namespace + "/" + pod.Name
		for _, vol := range pod.Spec.Volumes {
			source := vol.VolumeSource
			reason := ""
			if source.NFS != nil {
				reason = "direct nfs"
			}
			if source.CSI != nil {
				reason = "direct csi nfs"
			}
			claimName := ""
			if source.PersistentVolumeClaim != nil {
				claimName = source.PersistentVolumeClaim.ClaimName
				if claimName == "" {
					return false, nil, fmt.Errorf("%s: empty PVC reference", podID)
				}
			}
			if source.Ephemeral != nil {
				claimName = pod.Name + "-" + vol.Name
			}
			if claimName != "" {
				pvc, ok := pvcs[pod.Namespace+"/"+claimName]
				if !ok || pvc.Spec.VolumeName == "" {
					return false, nil, fmt.Errorf("%s: unresolved PVC %q", podID, claimName)
				}
				pv, ok := pvs[pvc.Spec.VolumeName]
				if !ok {
					return false, nil, fmt.Errorf("%s: unresolved PV %q", podID, pvc.Spec.VolumeName)
				}
				srv, p, isNFS := extractPVNFSInfo(pv)
				if isNFS {
					source = corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: srv, Path: p}}
				} else if pv.Spec.CSI != nil {
					return false, nil, fmt.Errorf("%s: cannot exclude NFS for CSI PV %s", podID, pv.Name)
				} else if pv.Spec.HostPath != nil {
					source = corev1.VolumeSource{HostPath: pv.Spec.HostPath}
				} else if pv.Spec.Local != nil {
					source = corev1.VolumeSource{HostPath: &corev1.HostPathVolumeSource{Path: pv.Spec.Local.Path}}
				} else if pv.Spec.PersistentVolumeSource == (corev1.PersistentVolumeSource{}) {
					return false, nil, fmt.Errorf("%s: unknown PV source %s", podID, pv.Name)
				} else {
					continue
				}
				reason = fmt.Sprintf("pvc: %s, pv: %s", pvc.Name, pv.Name)
			}
			if source.CSI != nil {
				if source.CSI.Driver != "nfs.csi.k8s.io" {
					return false, nil, fmt.Errorf("%s: cannot exclude NFS for inline CSI %q", podID, source.CSI.Driver)
				}
				source = corev1.VolumeSource{NFS: &corev1.NFSVolumeSource{Server: source.CSI.VolumeAttributes["server"], Path: source.CSI.VolumeAttributes["share"]}}
			}
			if source.NFS != nil {
				relevant, err := nodes.nfsRelevant(source.NFS.Server, source.NFS.Path, target)
				if err != nil {
					return false, nil, fmt.Errorf("%s: %w", podID, err)
				}
				if relevant {
					blockers = append(blockers, fmt.Sprintf("%s (%s)", podID, reason))
					break
				}
			}
			if source.HostPath != nil {
				blocked, err := hostPathBlocks(pod, vol.Name, source.HostPath.Path, target, nodes)
				if err != nil {
					return false, nil, fmt.Errorf("%s: %w", podID, err)
				}
				if blocked {
					blockers = append(blockers, podID+" (hostPath)")
					break
				}
			}
		}
	}
	return len(blockers) > 0, blockers, nil
}

// workerNodes retains all address types, unlike the UI's ListNodes helper,
// which deliberately returns only the first InternalIP. ResourceVersion is
// empty: a reclaim decision must not request an arbitrarily stale cache read.
type workerNodes struct {
	targetName string
	targetUID  string
	aliases    map[string]string
	worker     string
}

func loadWorkerNodes(ctx context.Context, client kubernetes.Interface, workerHost string) (workerNodes, error) {
	worker, ok := normalizeServerAddress(workerHost)
	if !ok {
		return workerNodes{}, fmt.Errorf("invalid worker host address: %q", workerHost)
	}
	list, err := client.CoreV1().Nodes().List(ctx, metav1.ListOptions{})
	if err != nil {
		return workerNodes{}, fmt.Errorf("list nodes: %w", err)
	}
	out := workerNodes{aliases: map[string]string{}, worker: worker}
	for _, node := range list.Items {
		aliases := []string{node.Name}
		for _, a := range node.Status.Addresses {
			aliases = append(aliases, a.Address)
		}
		for _, a := range aliases {
			norm, ok := normalizeServerAddress(a)
			if !ok {
				continue
			}
			if previous, found := out.aliases[norm]; found && previous != node.Name {
				return workerNodes{}, fmt.Errorf("ambiguous node address %q", norm)
			}
			out.aliases[norm] = node.Name
			if norm == worker {
				out.targetName = node.Name
				out.targetUID = string(node.UID)
			}
		}
	}
	return out, nil
}
func (n workerNodes) nfsRelevant(server, share, target string) (bool, error) {
	srv, ok := normalizeServerAddress(server)
	if !ok {
		return false, fmt.Errorf("invalid NFS server %q", server)
	}
	p, ok := normalizePath(share)
	if !ok {
		return false, fmt.Errorf("invalid NFS share %q", share)
	}
	same := srv == n.worker || (n.targetName != "" && n.aliases[srv] == n.targetName)
	if !same && net.ParseIP(srv) == nil && n.aliases[srv] == "" {
		return false, fmt.Errorf("unresolved NFS server identity %q", server)
	}
	return same && (target == "" || pathsOverlap(p, target)), nil
}
func hostPathBlocks(pod corev1.Pod, volumeName, raw, target string, nodes workerNodes) (bool, error) {
	hp, ok := normalizePath(raw)
	if !ok {
		return false, fmt.Errorf("invalid hostPath %q", raw)
	}
	if target != "" && !pathsOverlap(hp, target) {
		return false, nil
	}
	nodeName, known := nodes.aliases[pod.Spec.NodeName]
	if !known || nodes.targetName == "" {
		return false, fmt.Errorf("cannot resolve node for potentially related hostPath %q", raw)
	}
	if nodeName != nodes.targetName {
		return false, nil
	}
	for _, mount := range podVolumeMounts(pod) {
		if mount.Name != volumeName {
			continue
		}
		effective := hp
		if mount.SubPathExpr != "" {
			return false, fmt.Errorf("unresolved hostPath subPathExpr")
		}
		if mount.SubPath != "" {
			effective = path.Join(hp, mount.SubPath)
			if !isSubpathOrEqual(effective, hp) {
				return false, fmt.Errorf("hostPath subPath escapes parent")
			}
		}
		if target == "" || isSubpathOrEqual(effective, target) {
			return true, nil
		}
	}
	return false, nil
}
func podVolumeMounts(pod corev1.Pod) []corev1.VolumeMount {
	var mounts []corev1.VolumeMount
	for _, c := range pod.Spec.Containers {
		mounts = append(mounts, c.VolumeMounts...)
	}
	for _, c := range pod.Spec.InitContainers {
		mounts = append(mounts, c.VolumeMounts...)
	}
	for _, c := range pod.Spec.EphemeralContainers {
		mounts = append(mounts, c.VolumeMounts...)
	}
	return mounts
}
func extractPVNFSInfo(pv corev1.PersistentVolume) (server, exportPath string, ok bool) {
	if pv.Spec.NFS != nil {
		return pv.Spec.NFS.Server, pv.Spec.NFS.Path, true
	}
	if pv.Spec.CSI != nil && pv.Spec.CSI.Driver == "nfs.csi.k8s.io" {
		return pv.Spec.CSI.VolumeAttributes["server"], pv.Spec.CSI.VolumeAttributes["share"], true
	}
	return "", "", false
}
func normalizeServerAddress(addr string) (string, bool) {
	s := strings.TrimSpace(addr)
	if s == "" {
		return "", false
	}
	if strings.HasPrefix(s, "[") && strings.HasSuffix(s, "]") {
		s = s[1 : len(s)-1]
	}
	if ip := net.ParseIP(s); ip != nil {
		return ip.String(), true
	}
	s = strings.ToLower(strings.TrimSuffix(s, "."))
	if strings.ContainsAny(s, " /\\:\t\r\n") {
		return "", false
	}
	return s, s != ""
}
func normalizePath(raw string) (string, bool) {
	trimmed := strings.TrimSpace(raw)
	if trimmed == "" || !strings.HasPrefix(trimmed, "/") || strings.ContainsAny(trimmed, "\x00\r\n") {
		return "", false
	}
	return path.Clean(trimmed), true
}
func isSubpathOrEqual(candidate, root string) bool {
	c, r := path.Clean(candidate), path.Clean(root)
	return c == r || strings.HasPrefix(c, strings.TrimRight(r, "/")+"/")
}
func pathsOverlap(a, b string) bool { return isSubpathOrEqual(a, b) || isSubpathOrEqual(b, a) }
