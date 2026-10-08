import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');
const start = source.indexOf('        // Render Existing Mappings in Modal');
const end = source.indexOf('\n        renderExistingMappings();', start);
const section = source.slice(start, end);

function harness(services, apiJSON) {
  const messages = [];
  let buttons = [];
  const container = {
    set innerHTML(value) {
      this.html = value;
      buttons = [...value.matchAll(/<button\b([^>]*data-act="del-svc"[^>]*)>/g)].map(match => {
        const attrs = Object.fromEntries([...match[1].matchAll(/([\w-]+)="([^"]*)"/g)].map(m => [m[1], m[2]]));
        return {
          disabled: false, isConnected: true, innerHTML: '删除', style: {},
          classList: { add() {}, remove() {} },
          getAttribute(key) { return attrs[key]; },
          setAttribute(key, value) { attrs[key] = value; },
          removeAttribute(key) { delete attrs[key]; },
          addEventListener(_, listener) { this.click = () => listener.call(this); },
        };
      });
    },
    querySelectorAll(selector) { return selector.includes('del-svc') ? buttons : []; },
  };
  const modal = { isConnected: true, querySelector: selector => selector === '#pod-existing-container' ? container : { textContent: '' } };
  const context = {
    modal, pod: { uid: 'pod-1' }, editingSvc: null, k8sServices: services,
    servicesForPod: () => context.k8sServices,
    updatePodMappingsCountInTable() {}, setupEditMode() {}, resetFormToCreate() {},
    document: { getElementById: () => ({}) },
    setMsg: (_, text, level) => messages.push({ text, level }),
    esc: text => String(text).replaceAll("'", '&#39;'),
    apiJSON, console, encodeURIComponent, Date,
    setTimeout(fn, ms) { if (ms !== 3500) queueMicrotask(fn); },
  };
  runInNewContext(section + '\nthis.render = renderExistingMappings;', context);
  context.render();
  return { container, messages, buttons: () => buttons, context };
}

const external = { name: 'platform-ports', namespace: 'ns1', type: 'NodePort', managed: false, deletable: true, ports: [{ port: 8888, node_port: 31088 }] };
const managed = { ...external, managed: true };

test('external Notebook NodePort can be deleted but not edited', () => {
  const h = harness([external], async () => {});
  assert.equal(h.buttons().length, 1);
  assert.ok(!h.container.html.includes('data-act="edit-svc"'));
});

test('external ClusterIP and protected mappings remain read-only', () => {
  const h = harness([{ ...external, type: 'ClusterIP', deletable: false }, { ...managed, name: 'protected', namespace: 'kube-system', deletable: false }], async () => {});
  assert.equal(h.buttons().length, 0);
});

test('deletion waits for terminal task success before refreshing', async () => {
  const requests = [];
  let taskChecks = 0;
  const h = harness([managed], async (url, options) => {
    requests.push({ url, method: options?.method });
    if (options?.method === 'DELETE') return { resp: { ok: true }, data: { task_id: 9 } };
    if (url === '/tasks/9') return { resp: { ok: true }, data: { task: { status: ++taskChecks === 1 ? 'running' : 'succeeded' } } };
    assert.ok(taskChecks >= 2, 'refresh occurred before deletion completed');
    return { resp: { ok: true }, data: [] };
  });
  const button = h.buttons()[0];
  await button.click();
  await button.click();
  assert.deepEqual(requests.map(r => r.url), ['/k8s/services/platform-ports?namespace=ns1', '/tasks/9', '/tasks/9', '/k8s/services']);
  assert.equal(h.buttons().length, 0);
  assert.match(h.messages.at(-1).text, /已删除/);
});

test('failed task shows backend error and permits retry', async () => {
  const h = harness([managed], async (url, options) => options?.method === 'DELETE'
    ? { resp: { ok: true }, data: { task_id: 9 } }
    : { resp: { ok: true }, data: { task: { status: 'failed', error: 'policy deletion forbidden' } } });
  const button = h.buttons()[0];
  await button.click(); await button.click();
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /policy deletion forbidden/);
  assert.equal(button.disabled, false);
});

test('missing task id cannot be presented as deletion success', async () => {
  const h = harness([managed], async () => ({ resp: { ok: true }, data: {} }));
  const button = h.buttons()[0];
  await button.click(); await button.click();
  assert.equal(h.messages.at(-1).level, 'error');
  assert.equal(button.disabled, false);
});

test('cancelled task is a failure rather than successful submission', async () => {
  const h = harness([managed], async (url, options) => options?.method === 'DELETE'
    ? { resp: { ok: true }, data: { task_id: 9 } }
    : { resp: { ok: true }, data: { task: { status: 'cancelled', error: 'operation cancelled' } } });
  const button = h.buttons()[0]; await button.click(); await button.click();
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /operation cancelled/);
});

test('task polling failure preserves the failure message', async () => {
  const h = harness([managed], async (url, options) => options?.method === 'DELETE'
    ? { resp: { ok: true }, data: { task_id: 9 } }
    : { resp: { ok: false }, data: { error: 'task lookup unavailable' } });
  const button = h.buttons()[0]; await button.click(); await button.click();
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /task lookup unavailable/);
});

test('pending task polling is bounded without reporting deletion success', async () => {
  let checks = 0;
  const h = harness([managed], async (url, options) => {
    if (options?.method === 'DELETE') return { resp: { ok: true }, data: { task_id: 9 } };
    assert.equal(url, '/tasks/9'); checks++;
    return { resp: { ok: true }, data: { task: { status: 'pending' } } };
  });
  const button = h.buttons()[0]; await button.click(); await button.click();
  assert.equal(checks, 120);
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /超时/);
  assert.equal(button.disabled, false);
});

test('closing the modal stops polling without claiming success', async () => {
  let checks = 0;
  const h = harness([managed], async (url, options) => {
    if (options?.method === 'DELETE') return { resp: { ok: true }, data: { task_id: 9 } };
    checks++; h.context.modal.isConnected = false;
    return { resp: { ok: true }, data: { task: { status: 'running' } } };
  });
  const button = h.buttons()[0]; await button.click(); await button.click();
  assert.equal(checks, 1);
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /窗口已关闭/);
});

test('successful task with failed refresh reports stale list explicitly', async () => {
  const h = harness([managed], async (url, options) => {
    if (options?.method === 'DELETE') return { resp: { ok: true }, data: { task_id: 9 } };
    if (url === '/tasks/9') return { resp: { ok: true }, data: { task: { status: 'succeeded' } } };
    return { resp: { ok: false }, data: { error: 'list unavailable' } };
  });
  const button = h.buttons()[0]; await button.click(); await button.click();
  assert.equal(h.messages.at(-1).level, 'error');
  assert.match(h.messages.at(-1).text, /list unavailable/);
});
