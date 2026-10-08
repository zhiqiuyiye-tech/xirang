package api

import (
	"context"
	"net"
	"net/http"
	"strings"
	"sync"
	"time"

	"github.com/gin-gonic/gin"
	"xirang/control_panel/internal/db"
	"xirang/control_panel/internal/k8s"
	"xirang/control_panel/internal/workers"
)

type workerAcceleratorInfo struct {
	workers.AcceleratorInfo
	WorkerID         int64  `json:"worker_id"`
	Used             *int64 `json:"used"`
	SchedulableTotal *int64 `json:"schedulable_total"`
	AllocationStatus string `json:"allocation_status"`
}

// accelerators is separate from the worker list: slow or unavailable SSH probes
// cannot block ordinary node configuration. Each probe uses the configurable
// Worker SSH/device timeout, with at most four nodes probed concurrently per request.
func (h *workerHandlers) accelerators(c *gin.Context) {
	nodes, err := h.ws.List(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	out := make([]workerAcceleratorInfo, len(nodes))
	var wg sync.WaitGroup
	slots := make(chan struct{}, 4)
	for i, node := range nodes {
		wg.Add(1)
		go func(i int, node db.WorkerNode) {
			defer wg.Done()
			select {
			case slots <- struct{}{}:
				defer func() { <-slots }()
			case <-c.Request.Context().Done():
				out[i] = workerAcceleratorInfo{WorkerID: node.ID, AcceleratorInfo: workers.AcceleratorInfo{Status: "unknown", Devices: []workers.AcceleratorModel{}, Error: "设备采集已取消"}, AllocationStatus: "unknown"}
				return
			}
			out[i] = workerAcceleratorInfo{WorkerID: node.ID, AcceleratorInfo: h.ws.DiscoverAccelerators(c.Request.Context(), node), AllocationStatus: "unknown"}
		}(i, node)
	}
	var allocations []k8s.NodeAcceleratorAllocation
	if h.client != nil && len(nodes) > 0 {
		ctx, cancel := context.WithTimeout(c.Request.Context(), 5*time.Second)
		allocations, err = k8s.ListNodeAcceleratorAllocations(ctx, h.client)
		cancel()
	}
	wg.Wait()
	if err == nil {
		for i, node := range nodes {
			if allocation := matchWorkerAllocation(node, allocations); allocation != nil {
				used, total := allocation.Used, allocation.Total
				out[i].Used = &used
				out[i].SchedulableTotal = &total
				out[i].AllocationStatus = "available"
			}
		}
	}
	c.JSON(http.StatusOK, out)
}

func matchWorkerAllocation(worker db.WorkerNode, allocations []k8s.NodeAcceleratorAllocation) *k8s.NodeAcceleratorAllocation {
	var match *k8s.NodeAcceleratorAllocation
	for i := range allocations {
		allocation := &allocations[i]
		if allocation.Host != "" && allocation.Host == worker.Host {
			if match != nil {
				return nil
			} // Never attribute an ambiguous host to a node.
			match = allocation
		}
	}
	if match != nil {
		return match
	}
	// A configured hostname can match the Kubernetes name. A configured IP
	// conflicting with that node's InternalIP must not match by display name.
	for i := range allocations {
		allocation := &allocations[i]
		if allocation.Name != worker.Name && !strings.EqualFold(strings.TrimSuffix(worker.Host, "."), allocation.Name) {
			continue
		}
		if net.ParseIP(worker.Host) != nil && allocation.Host != "" && worker.Host != allocation.Host {
			continue
		}
		if match != nil {
			return nil
		}
		match = allocation
	}
	return match
}
