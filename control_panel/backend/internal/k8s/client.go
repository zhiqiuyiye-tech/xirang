package k8s

import (
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
)

// NewClient returns an in-cluster kubernetes clientset. It will fail outside
// a pod (no service-account token mounted); callers in tests should use a
// fake clientset instead.
func NewClient() (kubernetes.Interface, error) {
	cfg, err := rest.InClusterConfig()
	if err != nil {
		return nil, err
	}
	return kubernetes.NewForConfig(cfg)
}
