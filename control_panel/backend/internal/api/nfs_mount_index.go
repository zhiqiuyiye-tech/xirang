package api

import corev1 "k8s.io/api/core/v1"

// indexReferencedClaimsAndVolumes keeps request-local lookup maps limited to
// claims referenced by the selected Pods and the volumes bound to those claims.
// Missing/pending references remain absent or pending, preserving lookup states.
func indexReferencedClaimsAndVolumes(pods []corev1.Pod, claims []corev1.PersistentVolumeClaim, volumes []corev1.PersistentVolume) (map[string]corev1.PersistentVolumeClaim, map[string]corev1.PersistentVolume) {
	wantedClaims := make(map[string]struct{})
	for _, pod := range pods {
		for _, volume := range pod.Spec.Volumes {
			if volume.PersistentVolumeClaim != nil && volume.PersistentVolumeClaim.ClaimName != "" {
				wantedClaims[namespacedKey(pod.Namespace, volume.PersistentVolumeClaim.ClaimName)] = struct{}{}
			}
		}
	}
	selectedClaims := make(map[string]corev1.PersistentVolumeClaim, len(wantedClaims))
	wantedVolumes := make(map[string]struct{}, len(wantedClaims))
	for _, claim := range claims {
		key := namespacedKey(claim.Namespace, claim.Name)
		if _, wanted := wantedClaims[key]; !wanted {
			continue
		}
		selectedClaims[key] = claim
		if claim.Status.Phase == corev1.ClaimBound && claim.Spec.VolumeName != "" {
			wantedVolumes[claim.Spec.VolumeName] = struct{}{}
		}
	}
	selectedVolumes := make(map[string]corev1.PersistentVolume, len(wantedVolumes))
	for _, volume := range volumes {
		if _, wanted := wantedVolumes[volume.Name]; wanted {
			selectedVolumes[volume.Name] = volume
		}
	}
	return selectedClaims, selectedVolumes
}
