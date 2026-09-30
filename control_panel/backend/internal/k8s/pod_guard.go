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

// CheckNFSPodUsage scans all Kubernetes pods in all namespaces to determine if any pod
// is mounting or referencing the specified NFS export on the target worker node.
// If exportPath is empty, it evaluates conservatively: any NFS mount pointing to workerHost blocks.
func CheckNFSPodUsage(
	ctx context.Context,
	client kubernetes.Interface,
	workerHost string,
	exportPath string,
) (bool, []string, error) {
	if client == nil {
		return false, nil, fmt.Errorf("kubernetes client is unavailable")
	}

	normWorkerHost, ok := normalizeServerAddress(workerHost)
	if !ok {
		return false, nil, fmt.Errorf("invalid worker host address: %q", workerHost)
	}

	var normExportPath string
	if exportPath != "" {
		p, pok := normalizePath(exportPath)
		if !pok {
			return false, nil, fmt.Errorf("invalid export path: %q", exportPath)
		}
		normExportPath = p
	}

	podList, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pods: %w", err)
	}

	pvcList, err := client.CoreV1().PersistentVolumeClaims("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pvcs: %w", err)
	}

	pvList, err := client.CoreV1().PersistentVolumes().List(ctx, metav1.ListOptions{})
	if err != nil {
		return false, nil, fmt.Errorf("list pvs: %w", err)
	}

	pvcs := make(map[string]corev1.PersistentVolumeClaim, len(pvcList.Items))
	for _, pvc := range pvcList.Items {
		pvcs[pvc.Namespace+"/"+pvc.Name] = pvc
	}

	pvs := make(map[string]corev1.PersistentVolume, len(pvList.Items))
	for _, pv := range pvList.Items {
		pvs[pv.Name] = pv
	}

	var blockers []string

	for _, pod := range podList.Items {
		podID := fmt.Sprintf("%s/%s", pod.Namespace, pod.Name)

		for _, vol := range pod.Spec.Volumes {
			// Case 1: Direct Volume NFS mount
			if vol.NFS != nil {
				srv, sok := normalizeServerAddress(vol.NFS.Server)
				p, pok := normalizePath(vol.NFS.Path)
				if sok && pok && srv == normWorkerHost {
					if normExportPath == "" || isSubpathOrEqual(p, normExportPath) {
						blockers = append(blockers, fmt.Sprintf("%s (direct nfs)", podID))
						break
					}
				}
			}

			// Case 2: PVC reference
			if vol.PersistentVolumeClaim != nil && vol.PersistentVolumeClaim.ClaimName != "" {
				claimKey := pod.Namespace + "/" + vol.PersistentVolumeClaim.ClaimName
				pvc, exists := pvcs[claimKey]
				if !exists || pvc.Spec.VolumeName == "" {
					continue
				}

				pv, pvExists := pvs[pvc.Spec.VolumeName]
				if !pvExists {
					continue
				}

				srv, p, isNFS := extractPVNFSInfo(pv)
				if isNFS {
					normSrv, sok := normalizeServerAddress(srv)
					normP, pok := normalizePath(p)
					if sok && pok && normSrv == normWorkerHost {
						if normExportPath == "" || isSubpathOrEqual(normP, normExportPath) {
							blockers = append(blockers, fmt.Sprintf("%s (pvc: %s, pv: %s)", podID, pvc.Name, pv.Name))
							break
						}
					}
				}
			}
		}
	}

	return len(blockers) > 0, blockers, nil
}

func extractPVNFSInfo(pv corev1.PersistentVolume) (server, exportPath string, ok bool) {
	if pv.Spec.NFS != nil {
		return pv.Spec.NFS.Server, pv.Spec.NFS.Path, true
	}
	if pv.Spec.CSI != nil && pv.Spec.CSI.Driver == "nfs.csi.k8s.io" && pv.Spec.CSI.VolumeAttributes != nil {
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
	return s, s != ""
}

func normalizePath(raw string) (string, bool) {
	trimmed := strings.TrimSpace(raw)
	if trimmed == "" || !strings.HasPrefix(trimmed, "/") {
		return "", false
	}
	return path.Clean(trimmed), true
}

func isSubpathOrEqual(candidate, root string) bool {
	c := path.Clean(candidate)
	r := path.Clean(root)
	if c == r {
		return true
	}
	return strings.HasPrefix(c, strings.TrimRight(r, "/")+"/")
}
