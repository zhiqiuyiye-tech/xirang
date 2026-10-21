package storage

import (
	"context"
	"strings"
	"testing"
)

func TestResizeShrinkRequiresPodUsageProof(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	var paths []string
	checker := func(_ context.Context, _, path string) (bool, []string, error) {
		paths = append(paths, path)
		return path == "", []string{"worker/raw-block-assignment"}, nil
	}
	result := runResizeSafetyTask(t, "shrink", []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, checker)
	if result.status != "failed" || len(paths) != 1 || paths[0] != "" {
		t.Fatalf("pathless LV bypassed conservative Pod proof: status=%s paths=%v", result.status, paths)
	}
	for _, command := range result.runner.calls {
		if strings.Contains(command, "lvreduce -y") {
			t.Fatal("Pod-assigned LV reached resize mutation")
		}
	}
}

func TestResizeShrinkRejectsMissingPodChecker(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	result := runResizeSafetyTask(t, "shrink", []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, nil)
	if result.status != "failed" || !strings.Contains(result.taskError, "checker is unavailable") {
		t.Fatalf("unknown path/no checker accepted: %+v", result)
	}
}

func TestResizeGrowDoesNotRequireExclusiveUse(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	// The handbook grows a mounted NFS share online, so a grow must not consult
	// the Pod guard or treat the mounted volume as unsafe.
	result := runResizeSafetyTask(t, "grow",
		[]scriptResult{{stdout: `{"mount_targets":["/data02/share"],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":3}`}},
		[]scriptResult{identity}, nil, noPodUsers)
	if result.status != "succeeded" {
		t.Fatalf("mounted grow status=%q, want succeeded: %s", result.status, result.taskError)
	}
	if !strings.Contains(strings.Join(result.runner.calls, "\n"), "lvextend -r -L +10G /dev/vg_data/lv_data") {
		t.Fatalf("mounted grow did not run the guarded resize: %v", result.runner.calls)
	}
}

func TestResizeRejectsUnsupportedFilesystems(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	for _, fsType := range []string{"btrfs", "", "ext4\nxfs", "vfat", "swap"} {
		for _, action := range []string{"grow", "shrink"} {
			t.Run(fsType+"/"+action, func(t *testing.T) {
				result := runResizeSafetyTask(t, action, []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, noPodUsers, fsType)
				if result.status != "failed" || !strings.Contains(result.taskError, "filesystem") {
					t.Fatalf("unsupported filesystem %q reached mutation: %s %s", fsType, result.status, result.taskError)
				}
				for _, command := range result.runner.calls {
					if strings.Contains(command, "lvextend -r") || strings.Contains(command, "lvreduce -y") {
						t.Fatal("unsupported filesystem reached resize mutation")
					}
				}
			})
		}
	}
}

func TestResizeGrowSupportsXFSAndShrinkRejectsIt(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	mountedXFS := `{"mount_targets":["/data02/share"],"fstab_targets":["/data02/share"],"swap_active":false,"device_open_count":1}`

	grown := runResizeSafetyTask(t, "grow", []scriptResult{{stdout: mountedXFS}}, []scriptResult{identity}, nil, noPodUsers, "xfs")
	if grown.status != "succeeded" {
		t.Fatalf("mounted XFS grow status=%q, want succeeded: %s", grown.status, grown.taskError)
	}
	commands := strings.Join(grown.runner.calls, "\n")
	if !strings.Contains(commands, "lvextend -r -L +10G /dev/vg_data/lv_data") || !strings.Contains(commands, "xfs_growfs '/data02/share'") {
		t.Fatalf("mounted XFS grow did not run the handbook completion step: %v", grown.runner.calls)
	}

	shrunk := runResizeSafetyTask(t, "shrink", []scriptResult{{stdout: mountedXFS}}, []scriptResult{identity}, nil, noPodUsers, "xfs")
	if shrunk.status != "failed" || !strings.Contains(shrunk.taskError, "XFS filesystem cannot be shrunk") {
		t.Fatalf("XFS shrink status=%q error=%q, want a clear refusal", shrunk.status, shrunk.taskError)
	}
	for _, command := range shrunk.runner.calls {
		if strings.Contains(command, "lvreduce -y") {
			t.Fatal("XFS shrink reached resize mutation")
		}
	}
}
