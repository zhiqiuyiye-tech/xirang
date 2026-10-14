import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');

test('shared host maintenance is disabled by default in both deployment formats', () => {
  const values = read('../../../charts/control-panel/values.yaml');
  const helm = read('../../../charts/control-panel/templates/deployment.yaml');
  const manifest = read('../../../deploy/deployment.yaml');
  assert.match(values, /sharedHostMaintenanceEnabled:\s*false/);
  assert.match(helm, /name: SHARED_HOST_MAINTENANCE_ENABLED\s+value:.*sharedHostMaintenanceEnabled.*default false.*quote/);
  assert.match(manifest, /name: SHARED_HOST_MAINTENANCE_ENABLED\s+value: "false"/);
});

test('server wires maintenance opt-in independently of the workload allowlist', () => {
  const server = read('../../cmd/server/main.go');
  assert.match(server, /WithSharedHostMaintenance\(cfg\.SharedHostMaintenance\)/);
  assert.match(server, /WithHostUnmountAuthorizer\(hostUnmountAuthorizer\)/);
  const handler = read('../../internal/storage/handlers.go');
  assert.match(handler, /MaintenanceConfirmed\s+bool\s+`json:"maintenance_confirmed"`/);
});
