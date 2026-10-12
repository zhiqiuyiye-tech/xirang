import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const appSource = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');

function loadPlatformModal() {
  const injection = `
    window.__platformModalTest = { show: showPlatformRegistrationModal };
  `;
  const instrumentedSource = appSource.replace(/\}\)\(\);\s*$/, injection + '\n})();');
  assert.notEqual(instrumentedSource, appSource, 'test hook must be inserted into the application closure');

  const listeners = {};
  let modalRemoved = false;
  const elements = new Map([
    ['plat-modal', { remove() { modalRemoved = true; } }],
    ['pl-cancel', { addEventListener(name, listener) { listeners.cancel = listener; } }],
    ['pl-ws-input', { addEventListener(name, listener) { listeners.workspace = listener; }, value: 'workspace-uuid' }],
    ['pl-sql-box', { value: '', select() {} }],
    ['pl-copy-sql', { addEventListener(name, listener) { listeners.copy = listener; } }],
    ['pl-copy-msg', { textContent: '' }],
  ]);
  const clipboardWrites = [];
  const window = { location: { search: '', pathname: '/', hash: '' }, addEventListener() {} };
  const document = {
    cookie: '',
    title: 'Xirang Control Panel',
    addEventListener() {},
    getElementById(id) { return elements.get(id) || null; },
  };
  runInNewContext(instrumentedSource, {
    window,
    document,
    navigator: { clipboard: { writeText(text) { clipboardWrites.push(text); return Promise.resolve(); } } },
  });

  return {
    show: window.__platformModalTest.show,
    listeners,
    clipboardWrites,
    wasModalRemoved: () => modalRemoved,
  };
}

test('platform registration modal keeps NFS fields without generating or copying SQL', () => {
  const modal = loadPlatformModal();
  let renderedHTML = '';
  modal.show({ insertAdjacentHTML(position, html) { renderedHTML = html; } }, {
    uuid: 'storage-uuid',
    name: 'nfs-volume',
    path: '/data02/nfs-volume',
    service_address: '10.0.0.8',
    workspace_uuid: 'workspace-uuid',
  });

  for (const field of ['pl-uuid-val', 'pl-name-val', 'pl-addr-val', 'pl-path-val', 'pl-ws-input']) {
    assert.ok(renderedHTML.includes(field), `modal should retain ${field}`);
  }
  assert.match(renderedHTML, /关闭/);
  assert.doesNotMatch(renderedHTML, /SQL|INSERT INTO|pl-sql-box|pl-copy-sql|pl-copy-msg|复制/);
  assert.equal(modal.listeners.workspace, undefined, 'workspace edits must not generate SQL');
  assert.equal(typeof modal.listeners.cancel, 'function');

  modal.listeners.cancel();
  assert.equal(modal.wasModalRemoved(), true);
  assert.deepEqual(modal.clipboardWrites, []);
});
