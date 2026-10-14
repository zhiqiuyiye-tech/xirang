import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';

const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');

test('handbook deletion is not wired to maintenance enablement or workload allowlists', () => {
  const server = read('../../cmd/server/main.go');
  assert.doesNotMatch(server, /WithSharedHostMaintenance\(/);
  assert.doesNotMatch(server, /WithHostUnmountAuthorizer\(/);
  assert.match(server, /WithNamespaceCleanup\(nil,/);
  const handler = read('../../internal/storage/handlers.go');
  const deletion = handler.slice(handler.indexOf('func (h *deleteLVHandler) Run'));
  assert.doesNotMatch(deletion, /checkPodUsage\(|PlanHostUnmount\(|shared host maintenance is disabled/);
});

test('private resize recovery remains separate from handbook deletion recovery', () => {
  const handler = read('../../internal/storage/handlers.go');
  assert.match(handler, /recovery\.forDeletion = true/);
  assert.match(handler, /recovery: resizeRecovery/);
});
