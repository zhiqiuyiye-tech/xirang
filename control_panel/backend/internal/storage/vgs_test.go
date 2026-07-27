package storage

import (
	"context"
	"io"
	"testing"

	"xirang/control_panel/internal/db"
)

type fakeRunner struct {
	out string
	err error
}

func (f *fakeRunner) Run(_ context.Context, _ db.WorkerNode, _ string) (string, string, int, error) {
	if f.err != nil {
		return "", "", 1, f.err
	}
	return f.out, "", 0, nil
}
func (f *fakeRunner) RunWithStdin(_ context.Context, _ db.WorkerNode, _ string, _ io.Reader) (string, string, int, error) {
	return f.out, "", 0, nil
}

func TestListVGs(t *testing.T) {
	r := &fakeRunner{out: "vg_data,3.50g,2.30g\nvg_extra,1.00g,0.50g\n"}
	vgs, err := ListVGs(context.Background(), r, db.WorkerNode{})
	if err != nil {
		t.Fatal(err)
	}
	if len(vgs) != 2 {
		t.Fatalf("expected 2 VGs, got %d: %+v", len(vgs), vgs)
	}
	if vgs[0].Name != "vg_data" || vgs[0].VSize != "3.50g" || vgs[0].VFree != "2.30g" || vgs[0].FreeGB != 2.30 {
		t.Fatalf("vg_data wrong: %+v", vgs[0])
	}
	if vgs[1].Name != "vg_extra" || vgs[1].FreeGB != 0.50 {
		t.Fatalf("vg_extra wrong: %+v", vgs[1])
	}
}

func TestListVGsEmpty(t *testing.T) {
	r := &fakeRunner{out: ""}
	vgs, err := ListVGs(context.Background(), r, db.WorkerNode{})
	if err != nil {
		t.Fatal(err)
	}
	if len(vgs) != 0 {
		t.Fatalf("expected 0 VGs, got %d", len(vgs))
	}
}
