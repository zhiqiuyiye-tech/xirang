import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

const chart = fileURLToPath(new URL('../../../charts/control-panel', import.meta.url));

function deploymentEnv(t, settings = []) {
  let rendered;
  try {
    rendered = execFileSync('helm', ['template', 'control-panel', chart, '--show-only', 'templates/deployment.yaml', ...settings], { encoding: 'utf8' });
  } catch (error) {
    if (error.code === 'ENOENT') {
      t.skip('Helm is unavailable; chart rendering is verified when Helm is installed');
      return null;
    }
    throw error;
  }
  return Object.fromEntries([...rendered.matchAll(/- name: ([A-Z_]+)\r?\n\s+value: "([^"\r\n]*)"/g)].map((match) => [match[1], match[2]]));
}

test('Helm renders approved history-retention defaults', (t) => {
  const env = deploymentEnv(t);
  if (!env) return;
  assert.equal(env.TASK_RETENTION_DAYS, '90');
  assert.equal(env.AUDIT_RETENTION_DAYS, '365');
  assert.equal(env.HISTORY_CLEANUP_INTERVAL, '1h');
  assert.equal(env.HISTORY_CLEANUP_BATCH_SIZE, '500');
});

test('Helm passes explicit history-retention overrides to the server', (t) => {
  const env = deploymentEnv(t, ['--set', 'config.taskRetentionDays=30', '--set', 'config.auditRetentionDays=180', '--set-string', 'config.historyCleanupInterval=10m', '--set', 'config.historyCleanupBatchSize=25']);
  if (!env) return;
  assert.equal(env.TASK_RETENTION_DAYS, '30');
  assert.equal(env.AUDIT_RETENTION_DAYS, '180');
  assert.equal(env.HISTORY_CLEANUP_INTERVAL, '10m');
  assert.equal(env.HISTORY_CLEANUP_BATCH_SIZE, '25');
});
