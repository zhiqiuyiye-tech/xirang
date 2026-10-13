package k8s

import (
	"context"
	"fmt"
	"sync"

	corev1 "k8s.io/api/core/v1"
	coreinformers "k8s.io/client-go/informers/core/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/cache"
)

// AcceleratorAllocationCache is display-only. Pod/Node watches invalidate its
// snapshot; opening the Worker page does not list the cluster again. It must
// never be used as evidence for deletion, storage reclamation or authorization.
type AcceleratorAllocationCache struct {
	nodes    cache.SharedIndexInformer
	pods     cache.SharedIndexInformer
	done     <-chan struct{}
	mu       sync.Mutex
	dirty    bool
	snapshot []NodeAcceleratorAllocation
}

func NewAcceleratorAllocationCache(ctx context.Context, client kubernetes.Interface) *AcceleratorAllocationCache {
	c := &AcceleratorAllocationCache{
		nodes: coreinformers.NewNodeInformer(client, 0, cache.Indexers{}),
		pods:  coreinformers.NewPodInformer(client, "", 0, cache.Indexers{}),
		done:  ctx.Done(),
		dirty: true,
	}
	invalidate := func() { c.mu.Lock(); c.dirty = true; c.mu.Unlock() }
	events := cache.ResourceEventHandlerFuncs{
		AddFunc:    func(any) { invalidate() },
		UpdateFunc: func(any, any) { invalidate() },
		DeleteFunc: func(any) { invalidate() },
	}
	_, _ = c.nodes.AddEventHandler(events)
	_, _ = c.pods.AddEventHandler(events)
	go c.nodes.Run(ctx.Done())
	go c.pods.Run(ctx.Done())
	return c
}

func (c *AcceleratorAllocationCache) Snapshot(ctx context.Context) ([]NodeAcceleratorAllocation, error) {
	if err := ctx.Err(); err != nil {
		return nil, err
	}
	select {
	case <-c.done:
		return nil, fmt.Errorf("accelerator allocation cache stopped")
	default:
	}
	if !cache.WaitForCacheSync(ctx.Done(), c.nodes.HasSynced, c.pods.HasSynced) {
		return nil, fmt.Errorf("accelerator allocation cache not synchronized")
	}
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.dirty {
		nodeObjects, podObjects := c.nodes.GetStore().List(), c.pods.GetStore().List()
		nodes := make([]corev1.Node, 0, len(nodeObjects))
		pods := make([]corev1.Pod, 0, len(podObjects))
		for _, obj := range nodeObjects {
			nodes = append(nodes, *obj.(*corev1.Node))
		}
		for _, obj := range podObjects {
			pods = append(pods, *obj.(*corev1.Pod))
		}
		c.snapshot = nodeAcceleratorAllocations(nodes, pods)
		c.dirty = false
	}
	// Callers cannot mutate the shared cached snapshot.
	return append([]NodeAcceleratorAllocation{}, c.snapshot...), nil
}
