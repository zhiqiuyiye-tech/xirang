package api

import (
	"os/exec"
	"testing"

	appsv1 "k8s.io/api/apps/v1"
	"sigs.k8s.io/yaml"
)

func TestHelmWorkerHeartbeatTimeoutIsConfigurable(t *testing.T) {
	helm, err := exec.LookPath("helm")
	if err != nil {
		t.Skip("helm is not installed")
	}
	for _, tc := range []struct{ name, value, want string }{{"default", "", "15s"}, {"custom", "30s", "30s"}} {
		t.Run(tc.name, func(t *testing.T) {
			args := []string{"template", "control-panel", "../../../charts/control-panel", "--show-only", "templates/deployment.yaml"}
			if tc.value != "" {
				args = append(args, "--set", "config.workerHeartbeatTimeout="+tc.value)
			}
			output, err := exec.Command(helm, args...).CombinedOutput()
			if err != nil {
				t.Fatalf("render deployment: %v %s", err, output)
			}
			var deployment appsv1.Deployment
			if err := yaml.Unmarshal(output, &deployment); err != nil {
				t.Fatal(err)
			}
			for _, container := range deployment.Spec.Template.Spec.Containers {
				for _, env := range container.Env {
					if env.Name == "WORKER_HEARTBEAT_TIMEOUT" {
						if env.Value != tc.want {
							t.Fatalf("timeout %q want %q", env.Value, tc.want)
						}
						return
					}
				}
			}
			t.Fatal("deployment does not expose WORKER_HEARTBEAT_TIMEOUT")
		})
	}
}
