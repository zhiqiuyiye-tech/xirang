package api

import (
	"bytes"
	"encoding/base64"
	"os/exec"
	"strings"
	"testing"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"sigs.k8s.io/yaml"
)

func TestHelmWorkerAcceleratorTimeoutIsConfigurable(t *testing.T) {
	helm, err := exec.LookPath("helm")
	if err != nil {
		t.Skip("helm is not installed")
	}
	for _, tc := range []struct{ name, value, want string }{{"default", "", "45s"}, {"custom", "60s", "60s"}} {
		t.Run(tc.name, func(t *testing.T) {
			args := []string{"template", "control-panel", "../../../charts/control-panel", "--show-only", "templates/deployment.yaml"}
			if tc.value != "" {
				args = append(args, "--set", "config.workerAcceleratorTimeout="+tc.value)
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
					if env.Name == "WORKER_ACCELERATOR_TIMEOUT" {
						if env.Value != tc.want {
							t.Fatalf("timeout %q want %q", env.Value, tc.want)
						}
						return
					}
				}
			}
			t.Fatal("deployment does not expose WORKER_ACCELERATOR_TIMEOUT")
		})
	}
}

func TestHelmWorkerHeartbeatTimeoutIsConfigurable(t *testing.T) {
	helm, err := exec.LookPath("helm")
	if err != nil {
		t.Skip("helm is not installed")
	}
	for _, tc := range []struct{ name, value, want string }{{"default", "", "30s"}, {"custom", "60s", "60s"}} {
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

func TestHelmPinnedAESKeyRoundTripsThroughSecretData(t *testing.T) {
	helm, err := exec.LookPath("helm")
	if err != nil {
		t.Skip("helm is not installed")
	}

	key := bytes.Repeat([]byte{0x42}, 32)
	envValue := base64.StdEncoding.EncodeToString(key)
	args := []string{
		"template", "control-panel", "../../../charts/control-panel",
		"--set-string", "secrets.aesKey=" + envValue,
	}
	output, err := exec.Command(helm, args...).CombinedOutput()
	if err != nil {
		t.Fatalf("render chart: %v %s", err, output)
	}

	var secret corev1.Secret
	for _, document := range strings.Split(string(output), "---") {
		var candidate corev1.Secret
		if err := yaml.Unmarshal([]byte(document), &candidate); err == nil && candidate.Kind == "Secret" && candidate.Name == "control-panel-secrets" {
			secret = candidate
			break
		}
	}
	if secret.Data == nil || len(secret.Data["AES_KEY"]) == 0 {
		t.Fatal("rendered Secret is missing AES_KEY")
	}

	appEnvValue := string(secret.Data["AES_KEY"])
	if appEnvValue != envValue {
		t.Fatalf("Secret AES_KEY decodes to an unexpected environment value (length %d), want %d bytes of base64 text", len(appEnvValue), len(envValue))
	}
	decoded, err := base64.StdEncoding.DecodeString(appEnvValue)
	if err != nil {
		t.Fatalf("application cannot decode pinned AES_KEY: %v", err)
	}
	if !bytes.Equal(decoded, key) {
		t.Fatalf("decoded key length=%d, want %d", len(decoded), len(key))
	}
}
