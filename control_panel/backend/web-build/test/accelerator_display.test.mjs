import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');
const window = { location: { search: '', pathname: '/', hash: '' }, addEventListener() {} };
const document = { cookie: '', title: 'Control Panel', addEventListener() {} };
const sandbox = { window, document };
runInNewContext(source.replace(/\}\)\(\);\s*$/, `
 window.renderWorkerAccelerators = typeof renderWorkerAccelerators === 'function' ? renderWorkerAccelerators : null;
 window.renderPodAccelerators = typeof renderPodAccelerators === 'function' ? renderPodAccelerators : null;
 window.loadWorkerAccelerators = typeof loadWorkerAccelerators === 'function' ? loadWorkerAccelerators : null;
})();`), sandbox);

test('worker displays card models, counts and allocated / physical total', () => {
 assert.equal(typeof window.renderWorkerAccelerators, 'function');
 const html = window.renderWorkerAccelerators({ status: 'available', devices: [{ model: 'Ascend 910B4', count: 8 }], total: 8, used: 3, allocation_status: 'available' });
 assert.match(html, /Ascend 910B4/);
 assert.match(html, /8 张/);
 assert.match(html, /3 \/ 8/);
 assert.match(html, /已使用/);
});
test('worker displays a successful zero-card probe distinctly from unknown hardware', () => {
 const html = window.renderWorkerAccelerators({ status: 'available', devices: [], total: 0, used: 0, allocation_status: 'available' });
 assert.match(html, /未检测到 GPU \/ NPU 卡/);
 assert.match(html, /0 \/ 0/);
 assert.ok(!html.includes('卡型号未知'));
});

test('unknown hardware and allocations are never displayed as zero', () => {
 assert.equal(typeof window.renderWorkerAccelerators, 'function');
 const html = window.renderWorkerAccelerators({ status: 'unknown', devices: [], total: null, used: null, error: '采集失败', allocation_status: 'unknown' });
 assert.match(html, /未知/);
 assert.ok(!html.includes('0 / 0'));
 const partial = window.renderWorkerAccelerators({ status: 'available', devices: [{ model: 'NVIDIA A100', count: 4 }], total: 4, used: null, allocation_status: 'unknown' });
 assert.match(partial, /未知 \/ 4/);
});
test('worker safely escapes model names and reports unavailable allocation', () => {
 assert.equal(typeof window.renderWorkerAccelerators, 'function');
 const html = window.renderWorkerAccelerators({ status: 'available', devices: [{ model: '<script>', count: 1 }], total: 1, used: null, allocation_status: 'unknown' });
 assert.ok(!html.includes('<script>'));
 assert.match(html, /&lt;script&gt;/);
 assert.match(html, /分配信息未知/);
});
test('notebook displays accelerator count and resource details', () => {
 assert.equal(typeof window.renderPodAccelerators, 'function');
 const html = window.renderPodAccelerators({ accelerator_count: 2, accelerator_resources: { 'huawei.com/Ascend910': 2 }, node: 'worker-1', status: 'Running' });
 assert.match(html, /2 张/);
 assert.match(html, /huawei.com\/Ascend910/);
 assert.match(window.renderPodAccelerators({ accelerator_count: 0, accelerator_resources: {} }), /0 张/);
 assert.match(window.renderPodAccelerators({}), /未知/);
});
test('unbound and terminal notebooks label configured cards without claiming allocation', () => {
 assert.equal(typeof window.renderPodAccelerators, 'function');
 for (const pod of [{ node: '', status: 'Pending' }, { node: 'w', status: 'Succeeded' }, { node: 'w', status: 'Failed' }]) {
  const html = window.renderPodAccelerators({ ...pod, accelerator_count: 2, accelerator_resources: {} });
  assert.match(html, /2 张/);
  assert.match(html, /未分配|已释放/);
 }
});
test('worker loader joins by worker id even when the response order changes', async () => {
 const cells = [2, 1].map(id => ({ innerHTML: '', getAttribute: () => String(id) }));
 const tbody = { isConnected: true, querySelectorAll: () => cells };
 sandbox.fetch = async url => {
  assert.equal(url, '/api/v1/workers/accelerators');
  return { ok: true, status: 200, json: async () => [
   { worker_id: 1, status: 'available', total: 8, used: 3, allocation_status: 'available', devices: [{ model: 'Ascend 910B4', count: 8 }] },
   { worker_id: 2, status: 'unknown', total: null, used: null, allocation_status: 'unknown', error: '采集失败' },
  ] };
 };
 await window.loadWorkerAccelerators(tbody);
 assert.match(cells[0].innerHTML, /采集失败/);
 assert.match(cells[1].innerHTML, /3 \/ 8/);
});
test('worker loader reports failed requests and skips detached tables', async () => {
 const cell = { innerHTML: '', getAttribute: () => '1' };
 const tbody = { isConnected: true, querySelectorAll: () => [cell] };
 sandbox.fetch = async () => { throw new Error('network unavailable'); };
 await window.loadWorkerAccelerators(tbody);
 assert.match(cell.innerHTML, /未知/);
 assert.match(cell.innerHTML, /刷新重试/);
 cell.innerHTML = 'unchanged';
 tbody.isConnected = false;
 await window.loadWorkerAccelerators(tbody);
 assert.equal(cell.innerHTML, 'unchanged');
});

test('worker and notebook tables and notebook modal use accelerator renderers', () => {
 assert.match(source, /id="workers-table"[\s\S]*?<th>GPU \/ NPU<\/th>/);
 assert.match(source, /loadWorkerAccelerators\(tbody\)/);
 assert.match(source, /id="pods-table"[\s\S]*?<th>用卡数量<\/th>/);
 assert.match(source, /renderPodAccelerators\(p\)/);
 assert.match(source, /renderPodAccelerators\(pod\)/);
});
