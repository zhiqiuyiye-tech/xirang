import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');
const window = {
  location: { search: '', pathname: '/', hash: '' }, addEventListener() {},
  XirangCrypto: { generateRandomUUID: () => 'abcdef12-3456-4789-aaaa-123456789abc' },
};
const document = { cookie: '', title: '', addEventListener() {} };
runInNewContext(source.replace(/\}\)\(\);\s*$/, `
window.__test = {
  generateNFSName: typeof generateNFSName === 'function' ? generateNFSName : null,
  nfsStorageName: typeof nfsStorageName === 'function' ? nfsStorageName : null,
  renderAuditDetails: typeof renderAuditDetails === 'function' ? renderAuditDetails : null,
  renderWorkerHealth: typeof renderWorkerHealth === 'function' ? renderWorkerHealth : null,
  auditActionLabel: typeof auditActionLabel === 'function' ? auditActionLabel : null
};
})();`), { window, document });
const helpers = window.__test;

test('Worker state identifies SSH health and escapes diagnostic errors', () => {
  assert.equal(typeof helpers.renderWorkerHealth, 'function');
  const online = helpers.renderWorkerHealth({ status: 'online' });
  const unknown = helpers.renderWorkerHealth({ status: 'unknown', status_error: 'no credentials <configured>' });
  const offline = helpers.renderWorkerHealth({ status: 'offline', status_error: 'connection timeout' });
  assert.match(online, /在线/);
  assert.match(unknown, /待确认/);
  assert.match(unknown, /&lt;configured&gt;/);
  assert.match(offline, /离线/);
  assert.match(offline, /connection timeout/);
});

test('NFS auto-generated volume names contain eight random characters', () => {
  assert.equal(typeof helpers.generateNFSName, 'function');
  assert.equal(helpers.generateNFSName(), 'abcdef12');
  assert.match(helpers.generateNFSName(), /^[a-f0-9]{8}$/);
  assert.match(source, /var lv = generateNFSName\(\)/);
});

test('new short NFS names stay short in platform registration without renaming old volumes', () => {
  assert.equal(typeof helpers.nfsStorageName, 'function');
  assert.equal(helpers.nfsStorageName('abcdef12'), 'abcdef12');
  assert.equal(helpers.nfsStorageName('lv_nb_existing'), 'nfs-lv_nb_existing');
});

test('audit actions have readable labels with a fallback for historical actions', () => {
  assert.equal(typeof helpers.auditActionLabel, 'function');
  assert.equal(helpers.auditActionLabel('storage.provision_nfs'), '创建 NFS 共享');
  assert.equal(helpers.auditActionLabel('k8s.delete_service'), '删除端口映射');
  assert.equal(helpers.auditActionLabel('custom.old_action'), 'custom.old_action');
});

test('audit details display port, capacity, worker and task information safely', () => {
  assert.equal(typeof helpers.renderAuditDetails, 'function');
  const html = helpers.renderAuditDetails({
    worker_name: '<img src=x onerror=alert(1)>', host: '10.0.0.8',
    size_gb: 200, lv_name: 'abcdef12', task_id: 42,
    ports: [{ port: 8888, target_port: 8888, node_port: 31555, protocol: 'TCP' }],
    password: 'never-show-me', private_key: 'never-show-key',
  });
  for (const value of ['200', 'abcdef12', '10.0.0.8', '31555', '8888', '#/tasks/42']) {
    assert.ok(html.includes(value), value);
  }
  assert.ok(html.includes('&lt;img'));
  assert.ok(!html.includes('<img'));
  assert.ok(!html.includes('never-show'));
  assert.match(helpers.renderAuditDetails(null), /未记录/);
});
