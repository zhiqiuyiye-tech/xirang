package k8s

import (
	"context"
	"testing"
)

func TestAuthorizedSharedLeafOnPrivateHostPathMayBeReleased(t *testing.T) {
	client, holders := cleanupFixture()
	holders[0].Mounts[0].Optional = []string{"shared:578"}
	if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err != nil {
		t.Fatalf("shared leaf with private hostPath parent must reach remote parent revalidation: %v", err)
	}
	for _, flags := range [][]string{{"master:1"}, {"shared:0"}, {"shared:578", "shared:579"}, {"future:1"}} {
		holders[0].Mounts[0].Optional = flags
		if err := AuthorizeNamespaceCleanup(context.Background(), client, "10.0.0.10", "/data/lv", holders, []string{"monitoring/promtail/promtail"}); err == nil {
			t.Fatalf("unsupported leaf metadata accepted: %v", flags)
		}
	}
}
