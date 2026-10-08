package k8s

import (
	"encoding/json"
	"reflect"
	"testing"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/resource"
)

func acceleratorTestResources(values map[string]string) corev1.ResourceList {
	out := corev1.ResourceList{}
	for name, value := range values {
		out[corev1.ResourceName(name)] = resource.MustParse(value)
	}
	return out
}

func acceleratorTestContainer(requests, limits map[string]string) corev1.Container {
	return corev1.Container{Resources: corev1.ResourceRequirements{
		Requests: acceleratorTestResources(requests),
		Limits:   acceleratorTestResources(limits),
	}}
}

func TestNotebookPodInfoAccelerators(t *testing.T) {
	always := corev1.ContainerRestartPolicyAlways
	sidecar := acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2"}, nil)
	sidecar.RestartPolicy = &always
	tests := []struct {
		name string
		spec corev1.PodSpec
		want map[string]int64
	}{
		{
			name: "requests override limits per resource and containers add",
			spec: corev1.PodSpec{Containers: []corev1.Container{
				acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2"}, map[string]string{"nvidia.com/gpu": "7", "amd.com/gpu": "1"}),
				acceleratorTestContainer(nil, map[string]string{"nvidia.com/gpu": "1", "hygon.com/dcu": "2"}),
			}},
			want: map[string]int64{"nvidia.com/gpu": 3, "amd.com/gpu": 1, "hygon.com/dcu": 2},
		},
		{
			name: "ordinary init uses per resource peak instead of sum",
			spec: corev1.PodSpec{
				Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2", "amd.com/gpu": "3"}, nil)},
				InitContainers: []corev1.Container{
					acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "5", "amd.com/gpu": "1"}, nil),
					acceleratorTestContainer(nil, map[string]string{"nvidia.com/gpu": "4", "amd.com/gpu": "2"}),
				},
			},
			want: map[string]int64{"nvidia.com/gpu": 5, "amd.com/gpu": 3},
		},
		{
			name: "restartable init adds to app and later init peak",
			spec: corev1.PodSpec{
				Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "3"}, nil)},
				InitContainers: []corev1.Container{
					sidecar,
					acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "6"}, nil),
					sidecar,
				},
			},
			want: map[string]int64{"nvidia.com/gpu": 8},
		},
		{
			name: "sidecar not added to earlier ordinary init",
			spec: corev1.PodSpec{
				Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "1"}, nil)},
				InitContainers: []corev1.Container{
					acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "6"}, nil), sidecar,
				},
			},
			want: map[string]int64{"nvidia.com/gpu": 6},
		},
		{
			name: "restartable init included during app execution",
			spec: corev1.PodSpec{
				Containers:     []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "5"}, nil)},
				InitContainers: []corev1.Container{sidecar, sidecar},
			},
			want: map[string]int64{"nvidia.com/gpu": 9},
		},
		{
			name: "ascend names case insensitive and scalar units excluded",
			spec: corev1.PodSpec{Containers: []corev1.Container{acceleratorTestContainer(map[string]string{
				"huawei.com/Ascend910": "2", "huawei.com/ascend310P": "1", "HUAWEI.COM/ASCEND910B": "3",
				"huawei.com/Ascend910-memory": "32000", "huawei.com/Ascend910-mem": "16000",
				"huawei.com/Ascend910-cores": "20", "huawei.com/Ascend910-core": "10",
				"huawei.com/Ascend910-share": "100", "huawei.com/Ascend910-percentage": "100",
				"nvidia.com/gpumem": "8000", "nvidia.com/gpucores": "100", "nvidia.com/gpu.shared": "10",
				"amd.com/gpu-memory": "8000", "hygon.com/dcu-percentage": "100",
				"example.com/gpu": "8", "cpu": "4", "memory": "1Gi",
			}, nil)}},
			want: map[string]int64{"huawei.com/Ascend910": 2, "huawei.com/ascend310P": 1, "HUAWEI.COM/ASCEND910B": 3},
		},
		{
			name: "explicit zero request does not fall back to limit",
			spec: corev1.PodSpec{Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "0"}, map[string]string{"nvidia.com/gpu": "4"})}},
			want: map[string]int64{},
		},
		{
			name: "whole device quantities accept decimal representations",
			spec: corev1.PodSpec{Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "2.0", "amd.com/gpu": "2000m"}, nil)}},
			want: map[string]int64{"nvidia.com/gpu": 2, "amd.com/gpu": 2},
		},
		{
			name: "fractional and negative device quantities excluded",
			spec: corev1.PodSpec{Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "500m", "amd.com/gpu": "-1"}, nil)}},
			want: map[string]int64{},
		},
		{
			name: "pod overhead added to effective requests",
			spec: corev1.PodSpec{
				Containers: []corev1.Container{acceleratorTestContainer(map[string]string{"nvidia.com/gpu": "1"}, nil)},
				Overhead:   acceleratorTestResources(map[string]string{"nvidia.com/gpu": "1"}),
			},
			want: map[string]int64{"nvidia.com/gpu": 2},
		},
		{name: "no accelerator", spec: corev1.PodSpec{}, want: map[string]int64{}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			data, err := json.Marshal(NotebookPodInfo(corev1.Pod{Spec: tt.spec}))
			if err != nil {
				t.Fatal(err)
			}
			var got struct {
				Count     *int64           `json:"accelerator_count"`
				Resources map[string]int64 `json:"accelerator_resources"`
			}
			if err := json.Unmarshal(data, &got); err != nil {
				t.Fatal(err)
			}
			if got.Count == nil {
				t.Fatalf("accelerator_count missing in PodInfo JSON: %s", data)
			}
			var wantCount int64
			for _, count := range tt.want {
				wantCount += count
			}
			if *got.Count != wantCount || !reflect.DeepEqual(got.Resources, tt.want) {
				t.Fatalf("got count=%d resources=%v, want count=%d resources=%v", *got.Count, got.Resources, wantCount, tt.want)
			}
		})
	}
}
