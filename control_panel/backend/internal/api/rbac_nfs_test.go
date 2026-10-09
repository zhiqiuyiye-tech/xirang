package api

import (
	"os"
	"strings"
	"testing"

	rbacv1 "k8s.io/api/rbac/v1"
	"sigs.k8s.io/yaml"
)

func TestNFSRBACRulesOnlyGrantPVCAndPVGetList(t *testing.T) {
	files := []string{
		"../../../charts/control-panel/templates/rbac.yaml",
		"../../../deploy/rbac.yaml",
	}
	for _, file := range files {
		t.Run(file, func(t *testing.T) {
			contents, err := os.ReadFile(file)
			if err != nil {
				t.Fatal(err)
			}
			roleDocument := ""
			for _, document := range strings.Split(string(contents), "---") {
				if strings.Contains(document, "kind: ClusterRole") && strings.Contains(document, "name: control-panel") {
					roleDocument = document
					break
				}
			}
			if roleDocument == "" {
				t.Fatal("control-panel ClusterRole document not found")
			}
			rulesStart := strings.Index(roleDocument, "rules:")
			if rulesStart < 0 {
				t.Fatal("ClusterRole rules block not found")
			}
			var parsed struct {
				Rules []rbacv1.PolicyRule `yaml:"rules"`
			}
			if err := yaml.Unmarshal([]byte(roleDocument[rulesStart:]), &parsed); err != nil {
				t.Fatalf("parse ClusterRole rules: %v", err)
			}
			daemonsetVerbs := map[string]bool{}
			for _, rule := range parsed.Rules {
				for _, resource := range rule.Resources {
					for _, verb := range rule.Verbs {
						if resource == "pods" && (verb == "delete" || verb == "deletecollection" || verb == "*" || verb == "create" || verb == "update" || verb == "patch") {
							t.Errorf("Pod write permission %q is forbidden", verb)
						}
						if resource == "daemonsets" && len(rule.APIGroups) == 1 && rule.APIGroups[0] == "apps" {
							daemonsetVerbs[verb] = true
						}
					}
				}
			}
			if len(daemonsetVerbs) != 1 || !daemonsetVerbs["get"] {
				t.Errorf("DaemonSet permissions=%v, want only get", daemonsetVerbs)
			}
			permissions := map[string]map[string]bool{
				"persistentvolumeclaims": {},
				"persistentvolumes":      {},
			}
			for _, rule := range parsed.Rules {
				if len(rule.APIGroups) != 1 || rule.APIGroups[0] != "" {
					continue
				}
				for _, resource := range rule.Resources {
					if allowed, ok := permissions[resource]; ok {
						for _, verb := range rule.Verbs {
							allowed[verb] = true
						}
					}
				}
			}
			for resource, verbs := range permissions {
				if len(verbs) != 2 || !verbs["get"] || !verbs["list"] {
					t.Errorf("%s permissions=%v, want only get/list", resource, verbs)
				}
			}
		})
	}
}
