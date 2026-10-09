package k8s

import (
	"context"
	"fmt"
	"path"
	"regexp"
	"strconv"
	"strings"

	corev1 "k8s.io/api/core/v1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"xirang/control_panel/internal/storage"
)

var (
	cleanupUIDPattern       = regexp.MustCompile(`^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$`)
	cleanupIDPattern        = regexp.MustCompile(`^[0-9a-f]{64}$`)
	cleanupPodSlicePattern  = regexp.MustCompile(`^kubepods(?:-(?:burstable|besteffort))?-pod([0-9a-f_]{36})\.slice$`)
	cleanupScopePattern     = regexp.MustCompile(`^(cri-containerd|crio|docker)-([0-9a-f]{64})\.scope$`)
	cleanupNamespacePattern = regexp.MustCompile(`^mnt:\[[0-9]+\]$`)
)

// AuthorizeNamespaceCleanup is a read-only authorization gate. A successful
// result does not replace remote process/root/mount revalidation immediately
// before ordinary unmount. Every member of every supplied namespace must be
// identified and permitted; the default empty allowlist always denies cleanup.
func AuthorizeNamespaceCleanup(ctx context.Context, client kubernetes.Interface, workerHost string, exportPath string, holders []storage.NamespaceHolder, allowlist []string) error {
	if err := ctx.Err(); err != nil {
		return err
	}
	if client == nil {
		return fmt.Errorf("kubernetes client is unavailable")
	}
	allowed := map[string]bool{}
	for _, entry := range allowlist {
		parts := strings.Split(entry, "/")
		if len(parts) != 3 || parts[0] == "" || parts[1] == "" || parts[2] == "" || strings.TrimSpace(entry) != entry || strings.ContainsAny(entry, "* \t\r\n") {
			return fmt.Errorf("invalid namespace cleanup allowlist entry %q", entry)
		}
		allowed[entry] = true
	}
	if len(allowed) == 0 {
		return fmt.Errorf("namespace cleanup is disabled: allowlist is empty")
	}
	target, ok := normalizePath(exportPath)
	if !ok || target == "/" {
		return fmt.Errorf("namespace cleanup requires a known non-root export path")
	}
	if len(holders) == 0 {
		return fmt.Errorf("no namespace holders to authorize")
	}
	nodes, err := loadWorkerNodes(ctx, client, workerHost)
	if err != nil {
		return err
	}
	if nodes.targetName == "" || nodes.targetUID == "" {
		return fmt.Errorf("cannot establish worker node identity")
	}
	pods, err := client.CoreV1().Pods("").List(ctx, metav1.ListOptions{})
	if err != nil {
		return fmt.Errorf("list pods for namespace authorization: %w", err)
	}

	roots := map[string]string{}
	seenProcesses := map[int]string{}
	for _, holder := range holders {
		if holder.PID <= 0 || !positiveDecimal(holder.StartTime) || !cleanupNamespacePattern.MatchString(holder.Namespace) || holder.RootDev == 0 || holder.RootIno == 0 || len(holder.Mounts) == 0 || len(holder.Members) == 0 {
			return fmt.Errorf("namespace %q has incomplete process/root/mount evidence", holder.Namespace)
		}
		rootIdentity := fmt.Sprintf("%d:%d", holder.RootDev, holder.RootIno)
		if old, exists := roots[holder.Namespace]; exists && old != rootIdentity {
			return fmt.Errorf("namespace %s has inconsistent roots", holder.Namespace)
		}
		roots[holder.Namespace] = rootIdentity
		representative := false
		for _, member := range holder.Members {
			if member.PID <= 0 || !positiveDecimal(member.StartTime) {
				return fmt.Errorf("namespace %s has invalid member identity", holder.Namespace)
			}
			processIdentity := holder.Namespace + "/" + member.StartTime + "/" + member.Cgroup
			if old, exists := seenProcesses[member.PID]; exists && old != processIdentity {
				return fmt.Errorf("PID %d has conflicting evidence", member.PID)
			}
			seenProcesses[member.PID] = processIdentity
			if member.PID == holder.PID {
				if member.StartTime != holder.StartTime || member.Cgroup != holder.Cgroup {
					return fmt.Errorf("namespace %s representative identity changed", holder.Namespace)
				}
				representative = true
			}
			identity, err := parseCleanupCgroup(member.Cgroup)
			if err != nil {
				return fmt.Errorf("namespace %s PID %d: %w", holder.Namespace, member.PID, err)
			}
			var candidate *corev1.Pod
			for i := range pods.Items {
				if string(pods.Items[i].UID) == identity.podUID {
					if candidate != nil {
						return fmt.Errorf("ambiguous Pod UID %s", identity.podUID)
					}
					candidate = &pods.Items[i]
				}
			}
			if candidate == nil {
				return fmt.Errorf("namespace %s PID %d has no known Pod UID", holder.Namespace, member.PID)
			}
			fresh, err := client.CoreV1().Pods(candidate.Namespace).Get(ctx, candidate.Name, metav1.GetOptions{})
			if err != nil {
				return fmt.Errorf("get holder pod: %w", err)
			}
			if string(fresh.UID) != identity.podUID || fresh.Spec.NodeName != nodes.targetName || fresh.Spec.HostPID {
				return fmt.Errorf("holder Pod UID/node/host identity does not match")
			}
			container, err := cleanupContainer(*fresh, identity)
			if err != nil {
				return err
			}
			var owner *metav1.OwnerReference
			for i := range fresh.OwnerReferences {
				ref := &fresh.OwnerReferences[i]
				if ref.Controller != nil && *ref.Controller {
					if owner != nil {
						return fmt.Errorf("holder Pod has multiple controller owners")
					}
					owner = ref
				}
			}
			if owner == nil || owner.APIVersion != "apps/v1" || owner.Kind != "DaemonSet" || owner.Name == "" || owner.UID == "" {
				return fmt.Errorf("holder Pod lacks a precise DaemonSet controller identity")
			}
			entry := fresh.Namespace + "/" + owner.Name + "/" + container.Name
			if !allowed[entry] {
				return fmt.Errorf("container %s is not permitted for namespace cleanup", entry)
			}
			ds, err := client.AppsV1().DaemonSets(fresh.Namespace).Get(ctx, owner.Name, metav1.GetOptions{})
			if err != nil {
				return fmt.Errorf("get holder DaemonSet: %w", err)
			}
			if ds.UID != owner.UID || ds.DeletionTimestamp != nil {
				return fmt.Errorf("holder DaemonSet identity changed or is terminating")
			}
			if err := verifyParentHostPath(*fresh, container, target, holder.Mounts); err != nil {
				return fmt.Errorf("%s: %w", entry, err)
			}
		}
		if !representative {
			return fmt.Errorf("namespace %s representative is absent from member evidence", holder.Namespace)
		}
	}
	// Repeat the node identity read and the business usage guard after all
	// holders are authorized. Kubernetes/remote state is still not transactional.
	node, err := client.CoreV1().Nodes().Get(ctx, nodes.targetName, metav1.GetOptions{})
	if err != nil {
		return fmt.Errorf("verify worker node: %w", err)
	}
	if string(node.UID) != nodes.targetUID {
		return fmt.Errorf("worker node UID changed")
	}
	aliases := []string{node.Name}
	for _, a := range node.Status.Addresses {
		aliases = append(aliases, a.Address)
	}
	workerMatches := false
	for _, a := range aliases {
		if normalized, ok := normalizeServerAddress(a); ok && normalized == nodes.worker {
			workerMatches = true
		}
	}
	if !workerMatches {
		return fmt.Errorf("worker node address changed")
	}
	inUse, blockers, err := CheckNFSPodUsage(ctx, client, workerHost, target)
	if err != nil {
		return fmt.Errorf("verify business Pod usage: %w", err)
	}
	if inUse {
		return fmt.Errorf("business Pod usage blocks namespace cleanup: %s", strings.Join(blockers, ", "))
	}
	return nil
}

type cleanupCgroupIdentity struct{ podUID, containerID, runtime string }

func parseCleanupCgroup(raw string) (cleanupCgroupIdentity, error) {
	var identity cleanupCgroupIdentity
	lines := strings.Split(strings.TrimSpace(raw), "\n")
	for _, line := range lines {
		fields := strings.SplitN(line, ":", 3)
		if len(fields) != 3 || fields[0] == "" || fields[2] == "" || !strings.HasPrefix(fields[2], "/") {
			return identity, fmt.Errorf("unrecognized cgroup evidence")
		}
		if _, err := strconv.ParseUint(fields[0], 10, 64); err != nil {
			return identity, fmt.Errorf("invalid cgroup hierarchy")
		}
		components := strings.Split(strings.TrimPrefix(fields[2], "/"), "/")
		if len(components) < 3 || len(components) > 4 || (components[0] != "kubepods" && components[0] != "kubepods.slice") {
			return identity, fmt.Errorf("cgroup is not a recognized Kubernetes hierarchy")
		}
		if len(components) == 4 {
			qos := components[1]
			if components[0] == "kubepods" && qos != "burstable" && qos != "besteffort" {
				return identity, fmt.Errorf("unrecognized cgroupfs QoS hierarchy")
			}
			if components[0] == "kubepods.slice" && qos != "kubepods-burstable.slice" && qos != "kubepods-besteffort.slice" {
				return identity, fmt.Errorf("unrecognized systemd QoS hierarchy")
			}
		}
		var found cleanupCgroupIdentity
		for _, component := range components[len(components)-2:] {
			podUID := ""
			if strings.HasPrefix(component, "pod") {
				podUID = strings.TrimPrefix(component, "pod")
			} else if match := cleanupPodSlicePattern.FindStringSubmatch(component); match != nil {
				podUID = strings.ReplaceAll(match[1], "_", "-")
			}
			if cleanupUIDPattern.MatchString(podUID) {
				if found.podUID != "" {
					return identity, fmt.Errorf("ambiguous cgroup Pod identity")
				}
				found.podUID = podUID
				continue
			}
			containerID, runtime := "", ""
			if match := cleanupScopePattern.FindStringSubmatch(component); match != nil {
				containerID = match[2]
				runtime = map[string]string{"cri-containerd": "containerd", "crio": "cri-o", "docker": "docker"}[match[1]]
			} else if cleanupIDPattern.MatchString(component) {
				containerID = component
			}
			if containerID != "" {
				if found.podUID == "" || found.containerID != "" {
					return identity, fmt.Errorf("ambiguous cgroup container identity")
				}
				found.containerID = containerID
				found.runtime = runtime
			}
		}
		if found.podUID == "" || found.containerID == "" {
			return identity, fmt.Errorf("cgroup does not identify a complete Pod UID/container ID")
		}
		if identity.podUID != "" && identity != found {
			return identity, fmt.Errorf("conflicting cgroup controller identities")
		}
		identity = found
	}
	return identity, nil
}
func cleanupContainer(pod corev1.Pod, identity cleanupCgroupIdentity) (corev1.Container, error) {
	name := ""
	for _, status := range pod.Status.ContainerStatuses {
		parts := strings.Split(status.ContainerID, "://")
		if len(parts) != 2 || !cleanupIDPattern.MatchString(parts[1]) {
			continue
		}
		if parts[0] != "containerd" && parts[0] != "cri-o" && parts[0] != "docker" {
			continue
		}
		if parts[1] != identity.containerID || (identity.runtime != "" && identity.runtime != parts[0]) {
			continue
		}
		if status.State.Running == nil || status.State.Terminated != nil || status.State.Waiting != nil || name != "" {
			return corev1.Container{}, fmt.Errorf("holder container runtime identity is ambiguous or not running")
		}
		name = status.Name
	}
	if name != "" {
		for _, container := range pod.Spec.Containers {
			if container.Name == name {
				return container, nil
			}
		}
	}
	return corev1.Container{}, fmt.Errorf("holder full runtime container ID does not match a regular Pod container")
}
func verifyParentHostPath(pod corev1.Pod, container corev1.Container, target string, mounts []storage.NamespaceMount) error {
	var inheritedTargets []string
	for _, vm := range container.VolumeMounts {
		for _, vol := range pod.Spec.Volumes {
			if vol.Name != vm.Name || vol.HostPath == nil {
				continue
			}
			hp, ok := normalizePath(vol.HostPath.Path)
			if !ok {
				return fmt.Errorf("invalid parent hostPath")
			}
			if !pathsOverlap(hp, target) {
				continue
			}
			if vm.SubPathExpr != "" {
				return fmt.Errorf("unresolved parent hostPath subPathExpr")
			}
			effective := path.Join(hp, vm.SubPath)
			if !isSubpathOrEqual(effective, hp) {
				return fmt.Errorf("parent hostPath subPath escapes parent")
			}
			if isSubpathOrEqual(effective, target) {
				return fmt.Errorf("target or child hostPath is a business mount")
			}
			if !isSubpathOrEqual(target, effective) {
				continue
			}
			containerPath, ok := normalizePath(vm.MountPath)
			if !ok || containerPath == "/" {
				return fmt.Errorf("invalid or root-replacing container parent mount path")
			}
			if vm.MountPropagation != nil && *vm.MountPropagation != corev1.MountPropagationNone {
				return fmt.Errorf("parent hostPath propagation is not private")
			}
			relative := strings.TrimPrefix(strings.TrimPrefix(target, effective), "/")
			inherited := path.Join(containerPath, relative)
			for _, other := range container.VolumeMounts {
				if other.Name == vm.Name && other.MountPath == vm.MountPath {
					continue
				}
				otherPath, valid := normalizePath(other.MountPath)
				if !valid || pathsOverlap(otherPath, inherited) {
					return fmt.Errorf("another container volume obscures parent hostPath inheritance")
				}
			}
			inheritedTargets = append(inheritedTargets, inherited)
		}
	}
	if len(inheritedTargets) == 0 {
		return fmt.Errorf("no strict-parent hostPath inheritance evidence")
	}
	for _, mount := range mounts {
		mountPath, ok := normalizePath(mount.Path)
		if !ok || mountPath == "/" || mount.ID <= 0 || mount.ParentID < 0 {
			return fmt.Errorf("invalid inherited mount evidence")
		}
		root, ok := normalizePath(mount.Root)
		if !ok {
			return fmt.Errorf("invalid inherited filesystem root")
		}
		for _, optional := range mount.Optional {
			if strings.HasPrefix(optional, "shared:") || strings.HasPrefix(optional, "master:") || strings.HasPrefix(optional, "propagate_from:") {
				return fmt.Errorf("inherited mount has unsafe propagation")
			}
		}
		matched := false
		for _, inherited := range inheritedTargets {
			if mountPath == path.Join(inherited, strings.TrimPrefix(root, "/")) {
				matched = true
			}
		}
		if !matched {
			return fmt.Errorf("mount %q root %q does not match parent hostPath inheritance", mount.Path, mount.Root)
		}
	}
	return nil
}
func positiveDecimal(value string) bool {
	n, err := strconv.ParseUint(value, 10, 64)
	return err == nil && n > 0
}
