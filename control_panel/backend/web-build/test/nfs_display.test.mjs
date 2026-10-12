import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const appSource = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');

function loadNFSRenderers() {
  const injection = `
    window.__nfsDisplayTest = {
      renderLVMountedPods: renderLVMountedPods,
      renderPodNFSMountDetails: renderPodNFSMountDetails,
      podNFSMountSummary: podNFSMountSummary,
      renderPortMappingPodIdentity: typeof renderPortMappingPodIdentity === 'function' ? renderPortMappingPodIdentity : null,
      taskRegistrationForResponse: taskRegistrationForResponse,
      subscribeSSE: subscribeSSE,
      setAuthenticatedForTest: function (value) { isAuthenticated = value; },
      taskPollTimerForTest: function () { return taskPollTimer; },
      taskStatusTimerForTest: function () { return taskStatusTimer; },
      closeSSEForTest: closeSSE,
      currentSSEForTest: function () { return currentSSE; },
      fetchTaskInfoForTest: fetchTaskInfo,
      setFetchTaskInfoForTest: function (fn) { fetchTaskInfo = fn; },
      setRenderTaskInfoForTest: function (fn) { renderTaskInfo = fn; },
      setApiJSONForTest: function (fn) { apiJSON = fn; }
    };
  `;
  const instrumentedSource = appSource.replace(/\}\)\(\);\s*$/, injection + '\n})();');
  assert.notEqual(instrumentedSource, appSource, 'test hook must be inserted into the application closure');

  const eventSources = [];
  const timers = [];
  const clearedTimers = [];
  class FakeEventSource {
    constructor(url, options) { this.url = url; this.options = options; this.listeners = {}; eventSources.push(this); }
    addEventListener(name, listener) { this.listeners[name] = listener; }
    close() { this.closed = true; }
  }
  const window = {
    location: { search: '', pathname: '/', hash: '' },
    addEventListener() {},
  };
  const document = {
    cookie: '',
    title: 'Xirang Control Panel',
    addEventListener() {},
    getElementById() { return null; },
  };
  runInNewContext(instrumentedSource, {
    window, document, EventSource: FakeEventSource,
    setInterval(fn, ms) { const timer = { id: timers.length + 1, fn, ms }; timers.push(timer); return timer.id; },
    clearInterval(id) { clearedTimers.push(id); },
  });
  Object.assign(window.__nfsDisplayTest, { eventSources, timers, clearedTimers });
  return window.__nfsDisplayTest;
}

const renderers = loadNFSRenderers();

test('task registration response exposes only whitelisted provision fields', () => {
  const details = renderers.taskRegistrationForResponse({ registration: {
    vg_name: 'vg_data', lv_name: 'lv_nb_1', size_gb: 200,
    fs_type: 'xfs', mount_point: '/data02/nb_1', password: 'must-not-pass-through',
  } });
  assert.deepEqual(JSON.parse(JSON.stringify(details)), {
    vg_name: 'vg_data', lv_name: 'lv_nb_1', size_gb: 200,
    fs_type: 'xfs', mount_point: '/data02/nb_1',
  });
  assert.equal(renderers.taskRegistrationForResponse({ task: {} }), null);
});

test('task detail polling uses fast fallback on errors and slow checks while SSE is open', () => {
  let statusChecks = 0;
  renderers.setFetchTaskInfoForTest(() => { statusChecks++; });
  renderers.setAuthenticatedForTest(true);
  renderers.subscribeSSE('42');
  const stream = renderers.eventSources.at(-1);
  assert.equal(renderers.taskPollTimerForTest(), null);
  assert.equal(renderers.taskStatusTimerForTest(), null);

  stream.onerror();
  assert.ok(renderers.taskPollTimerForTest());
  assert.equal(renderers.timers.at(-1).ms, 2000);
  const fallbackId = renderers.taskPollTimerForTest();

  stream.onopen();
  assert.equal(renderers.taskPollTimerForTest(), null);
  assert.ok(renderers.clearedTimers.includes(fallbackId));
  const statusTimerId = renderers.taskStatusTimerForTest();
  assert.ok(statusTimerId);
  assert.equal(renderers.timers.find((timer) => timer.id === statusTimerId).ms, 30000);
  renderers.timers.find((timer) => timer.id === statusTimerId).fn();
  assert.equal(statusChecks, 1);

  stream.onerror();
  assert.equal(renderers.taskStatusTimerForTest(), null);
  assert.ok(renderers.clearedTimers.includes(statusTimerId));
  assert.equal(renderers.timers.at(-1).ms, 2000);
  stream.onopen();
  assert.ok(renderers.taskStatusTimerForTest());
  renderers.closeSSEForTest();
});

test('periodic status reconciliation detects terminal tasks and clears timers', async () => {
  renderers.setFetchTaskInfoForTest(renderers.fetchTaskInfoForTest);
  renderers.setRenderTaskInfoForTest(() => {});
  let statusFetches = 0;
  renderers.setApiJSONForTest(async () => {
    statusFetches++;
    return { resp: { ok: true }, data: { task: { id: 7, status: 'succeeded' }, steps: [] } };
  });
  renderers.setAuthenticatedForTest(true);
  renderers.subscribeSSE('terminal');
  const stream = renderers.eventSources.at(-1);
  stream.onopen();
  const statusTimerId = renderers.taskStatusTimerForTest();

  await renderers.fetchTaskInfoForTest('terminal');
  await Promise.resolve();
  await Promise.resolve();
  await new Promise((resolve) => setTimeout(resolve, 0));

  assert.equal(statusFetches, 1);
  assert.equal(renderers.currentSSEForTest(), null);
  assert.equal(renderers.taskPollTimerForTest(), null);
  assert.equal(renderers.taskStatusTimerForTest(), null);
  assert.ok(renderers.clearedTimers.includes(statusTimerId));
});

test('stale EventSource callbacks cannot change the current task poller', () => {
  renderers.setAuthenticatedForTest(true);
  renderers.subscribeSSE('stale');
  const staleStream = renderers.eventSources.at(-1);
  staleStream.onerror();

  renderers.subscribeSSE('current');
  const currentStream = renderers.eventSources.at(-1);
  currentStream.onopen();
  const currentStatusTimerId = renderers.taskStatusTimerForTest();
  const timerCount = renderers.timers.length;

  staleStream.onopen();
  staleStream.onerror();
  assert.equal(renderers.taskPollTimerForTest(), null);
  assert.equal(renderers.taskStatusTimerForTest(), currentStatusTimerId);
  assert.equal(renderers.timers.length, timerCount);
  renderers.closeSSEForTest();
});

test('route cleanup clears polling and ignores callbacks from closed streams', () => {
  renderers.setAuthenticatedForTest(true);
  renderers.subscribeSSE('route-cleanup');
  const closedStream = renderers.eventSources.at(-1);
  closedStream.onerror();
  const fallbackTimerId = renderers.taskPollTimerForTest();

  renderers.closeSSEForTest();
  closedStream.onopen();
  closedStream.onerror();

  assert.equal(renderers.taskPollTimerForTest(), null);
  assert.equal(renderers.taskStatusTimerForTest(), null);
  assert.ok(renderers.clearedTimers.includes(fallbackTimerId));
});

function countOccurrences(value, needle) {
  return value.split(needle).length - 1;
}

test('NFS storage shows one short Notebook identity and owner per Pod', () => {
  const shortName = 'notebook-9a953dbb7917';
  const fullPodName = 'notebook-9a953dbb-7917-4104-887b-b044aa425282-7764c7bdbc-pt47b';
  const html = renderers.renderLVMountedPods([
    { namespace: shortName, pod_name: fullPodName, pod_uid: 'pod-uid-1', owner_name: '宇锐科技', note: '不应展示的备注', pvc_name: 'claim-a' },
    { namespace: shortName, pod_name: fullPodName, pod_uid: 'pod-uid-1', owner_name: '宇锐科技', note: '不应展示的备注', pvc_name: 'claim-b' },
  ], 'available');

  assert.equal(countOccurrences(html, shortName), 1);
  assert.equal(countOccurrences(html, '宇锐科技'), 1);
  assert.equal(html.includes(fullPodName), false);
  assert.equal(html.includes('不应展示的备注'), false);
});

test('port mapping identifies a Pod by namespace without showing its Pod name', () => {
  assert.equal(typeof renderers.renderPortMappingPodIdentity, 'function');
  const namespace = 'notebook-namespace';
  const fullPodName = 'notebook-long-generated-pod-name';
  const html = renderers.renderPortMappingPodIdentity({ namespace, name: fullPodName });

  assert.equal(html.includes(namespace), true);
  assert.equal(html.includes(fullPodName), false);
});

test('port mapping combines mounts for the same NFS disk and export while preserving details', () => {
  const html = renderers.renderPodNFSMountDetails({
    nfs_mounts_status: 'available',
    nfs_mounts: [
      {
        status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_notebook', export_path: '/nfs/notebook',
        pvc_name: 'claim-a', pv_name: 'pv-a',
        container_mounts: [{ container_name: 'notebook', mount_path: '/workspace/a', read_only: false }],
      },
      {
        status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_notebook', export_path: '/nfs/notebook',
        pvc_name: 'claim-b', pv_name: 'pv-b',
        container_mounts: [
          { container_name: 'notebook', mount_path: '/workspace/a', read_only: false },
          { container_name: 'init', mount_path: '/workspace/cache', read_only: true },
        ],
      },
      {
        status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_other', export_path: '/nfs/other',
        pvc_name: 'claim-c', pv_name: 'pv-c', container_mounts: [],
      },
    ],
  });

  assert.equal(countOccurrences(html, 'class="nfs-mount-card"'), 2);
  for (const name of ['claim-a', 'pv-a', 'claim-b', 'pv-b', 'claim-c', 'pv-c']) {
    assert.equal(countOccurrences(html, name), 1, `${name} should be shown once`);
  }
  assert.equal(countOccurrences(html, '/workspace/a'), 1);
  assert.equal(countOccurrences(html, '/workspace/cache'), 1);

  const summary = renderers.podNFSMountSummary({
    nfs_mounts_status: 'available',
    nfs_mounts: [
      { status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_notebook', export_path: '/nfs/notebook' },
      { status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_notebook', export_path: '/nfs/notebook' },
      { status: 'matched', worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_other', export_path: '/nfs/other' },
    ],
  });
  assert.match(summary, /2 个 NFS 卷/);
});
