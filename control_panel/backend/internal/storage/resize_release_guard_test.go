package storage

import (
	"context"
	"strings"
	"testing"
)

func TestResizePathlessLVRequiresPodUsageProof(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	for _, action := range []string{"grow", "shrink"} {
		t.Run(action, func(t *testing.T) {
			var paths []string
			checker := func(_ context.Context, _, path string) (bool, []string, error) {
				paths = append(paths, path)
				return path == "", []string{"worker/raw-block-assignment"}, nil
			}
			result := runResizeSafetyTask(t, action, []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, checker)
			if result.status != "failed" || len(paths) != 1 || paths[0] != "" {
				t.Fatalf("pathless LV bypassed conservative Pod proof: status=%s paths=%v", result.status, paths)
			}
			for _, command := range result.runner.calls {
				if strings.Contains(command, "lvextend -r") || strings.Contains(command, "lvreduce -y") {
					t.Fatal("Pod-assigned LV reached resize mutation")
				}
			}
		})
	}
}

func TestResizePathlessLVRejectsMissingPodChecker(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	result := runResizeSafetyTask(t, "grow", []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, nil)
	if result.status != "failed" || !strings.Contains(result.taskError, "checker is unavailable") {
		t.Fatalf("unknown path/no checker accepted: %+v", result)
	}
}

func TestResizeRejectsUnsupportedOfflineFilesystems(t *testing.T) {
	identity := scriptResult{stdout: `{"ok":true,"result":{"uuid":"stable-uuid","major_minor":"253:0"}}`}
	for _, fsType := range []string{"xfs", "btrfs", "", "ext4\nxfs"} {
		for _, action := range []string{"grow", "shrink"} {
			t.Run(fsType+"/"+action, func(t *testing.T) {
				result := runResizeSafetyTask(t, action, []scriptResult{{stdout: unusedLVResizeState}}, []scriptResult{identity}, nil, noPodUsers, fsType)
				if result.status != "failed" || !strings.Contains(result.taskError, "filesystem") {
					t.Fatalf("offline filesystem %q reached mutation: %s %s", fsType, result.status, result.taskError)
				}
				for _, command := range result.runner.calls {
					if strings.Contains(command, "lvextend -r") || strings.Contains(command, "lvreduce -y") {
						t.Fatal("unsupported offline filesystem reached resize mutation")
					}
				}
			})
		}
	}
}
