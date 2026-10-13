import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');

test('VG initialization requires explicit disk selection and warns about existing filesystem data', async () => {
  const window = { location: { search: '', pathname: '/', hash: '' }, addEventListener() {} };
  const elements = new Map([
    ['vg-modal', { remove() {} }],
    ['vg-name-input', { value: 'vg_data', addEventListener() {} }],
    ['vg-cancel', { addEventListener() {} }],
    ['vg-create-btn', { addEventListener() {} }],
  ]);
  const document = { cookie: '', title: '', addEventListener() {}, getElementById: id => elements.get(id) };
  const instrumented = source.replace(/\}\)\(\);\s*$/, 'window.showInitVGForm = showInitVGForm; })();');
  runInNewContext(instrumented, { window, document });
  let html;
  await window.showInitVGForm({ insertAdjacentHTML(position, markup) { html = markup; } }, 1, [
    { name: '/dev/sdb', size_gb: 100 },
    { name: '/dev/sdc1', size_gb: 50 },
  ]);
  assert.match(html, /现有文件系统及其中全部数据/);
  const checkboxes = [...html.matchAll(/<input type="checkbox"[^>]*>/g)].map(([input]) => input);
  assert.equal(checkboxes.length, 2);
  for (const checkbox of checkboxes) assert.doesNotMatch(checkbox, /\bchecked\b/);
  assert.match(html, /确认格式化并初始化/);
});
