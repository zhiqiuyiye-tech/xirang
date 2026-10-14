import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const appSource = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');

function loadStorageUI() {
  const requests = [];
  const alerts = [];
  const confirms = [];
  const modals = [];
  let currentModal = null;
  let confirmResult = true;
  let reclaimClick = null;
  const window = { location: { search: '', pathname: '/', hash: '' }, addEventListener() {} };
  const maintenanceContent = {
    insertAdjacentHTML(position, html) {
      currentModal = {
        html,
        checkbox: { checked: false },
        removed: false,
        click: null,
        cancel: null,
        querySelector(selector) {
          if (selector === '#storage-maintenance-confirmed') return this.checkbox;
          if (selector === '#storage-maintenance-submit') return { addEventListener: (name, listener) => { if (name === 'click') this.click = listener; } };
          if (selector === '#storage-maintenance-cancel') return { addEventListener: (name, listener) => { if (name === 'click') this.cancel = listener; } };
          return null;
        },
        remove() { this.removed = true; if (currentModal === this) currentModal = null; },

      };
      modals.push(currentModal);
    },
    querySelector(selector) {
      return selector === '#storage-maintenance-modal' ? currentModal : null;
    },
  };
  const taskInfo = { innerHTML: '' };
  const reclaimButton = {
    addEventListener(name, listener) { if (name === 'click') reclaimClick = listener; },
  };
  const document = {
    cookie: '',
    title: 'Xirang Control Panel',
    addEventListener() {},
    getElementById(id) {
      if (id === 'content') return maintenanceContent;
      if (id === 'task-info') return taskInfo;
      if (id === 'btn-reclaim-from-task') return reclaimButton;
      if (id === 'storage-maintenance-modal') return currentModal;
      if (id === 'storage-maintenance-confirmed') return currentModal && currentModal.checkbox;
      if (id === 'storage-maintenance-submit') {
        if (!currentModal) return null;
        return { addEventListener(name, listener) { if (name === 'click') currentModal.click = listener; } };
      }
      if (id === 'storage-maintenance-cancel') {
        if (!currentModal) return null;
        return { addEventListener(name, listener) { if (name === 'click') currentModal.cancel = listener; } };
      }
      return null;
    },
  };
  const instrumentedSource = appSource.replace(/\}\)\(\);\s*$/, `
    window.__storageMaintenanceTest = {
      doDeleteLV: doDeleteLV,
      renderTaskInfo: renderTaskInfo,
      setApiJSON: function (fn) { apiJSON = fn; }
    };
  })();`);
  assert.notEqual(instrumentedSource, appSource, 'test hook must be inserted into the application closure');
  runInNewContext(instrumentedSource, {
    window,
    document,
    confirm(message) { confirms.push(message); return confirmResult; },
    alert(message) { alerts.push(message); },
  });

  return {
    app: window.__storageMaintenanceTest,
    requests,
    alerts,
    confirms,
    modals,
    taskInfo,
    content: maintenanceContent,
    setConfirmResult(value) { confirmResult = value; },
    latestModal() { return modals.at(-1); },
    setSuccessfulAPI() {
      window.__storageMaintenanceTest.setApiJSON(async (path, options) => {
        requests.push({ path, options, body: JSON.parse(options.body) });
        return { resp: { ok: true }, data: { task_id: 73 } };
      });
    },
    setFailingAPI(error) {
      window.__storageMaintenanceTest.setApiJSON(async (path, options) => {
        requests.push({ path, options, body: JSON.parse(options.body) });
        return { resp: { ok: false }, data: { error } };
      });
    },
    clickReclaim() { return reclaimClick && reclaimClick(); },
  };
}

function successfulProvisionTask() {
  return {
    id: 42,
    type: 'storage_provision_nfs',
    status: 'succeeded',
    target_kind: 'storage',
    target_id: 8,
    created_at: '2026-10-14T00:00:00Z',
  };
}

const registration = {
  vg_name: 'vg_data',
  lv_name: 'lv_nfs_demo',
  size_gb: 100,
  fs_type: 'ext4',
  mount_point: '/data02/nfs_demo',
};

test('LV delete keeps its irreversible confirmation and defaults maintenance mode off', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_demo', size: 80, mp: '/data02/demo' });

  assert.equal(ui.confirms.length, 1);
  assert.match(ui.confirms[0], /该操作不可撤销/);
  const modal = ui.latestModal();
  assert.ok(modal, 'delete should open the maintenance choice modal after the original confirmation');
  assert.equal(modal.checkbox.checked, false);
  assert.doesNotMatch(modal.html, /<input[^>]*\schecked(?:\s|=|>)/i, 'maintenance confirmation must not be checked in the markup');
  assert.match(modal.html, /SHARED_HOST_MAINTENANCE_ENABLED/);
  assert.match(modal.html, /受控维护/);
  assert.match(modal.html, /没有并发的相关挂载、卸载或 LVM 操作/);
  assert.match(modal.html, /人工核实/);
  assert.match(modal.html, /授权.*完整.*受影响.*维护范围/);
  assert.match(modal.html, /命名空间引用.*(?:无法|不能)发现/);
  assert.match(modal.html, /Linux 5\.10/);
  assert.match(modal.html, /不能证明完整的内核/);
  assert.match(modal.html, /未知.*持有者|持有者.*未知/);
  assert.match(modal.html, /业务用途/);
  assert.match(modal.html, /allowlist|allowlisted|白名单/i);

  await modal.click();
  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/lv/delete');
  assert.deepEqual(ui.requests[0].body, { worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_demo' });
});

test('LV delete sends maintenance_confirmed only when its request checkbox is checked', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  await ui.app.doDeleteLV(ui.content, 3, { vg: 'vg_shared', name: 'lv_shared', size: 20, mp: '/data02/shared' });
  const modal = ui.latestModal();
  modal.checkbox.checked = true;
  await modal.click();

  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/lv/delete');
  assert.equal(ui.requests[0].body.maintenance_confirmed, true);
});

test('NFS reclaim is available from a successful provision task and defaults maintenance mode off', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  ui.app.renderTaskInfo(successfulProvisionTask(), registration);

  assert.match(ui.taskInfo.innerHTML, /btn-reclaim-from-task/);
  assert.match(ui.taskInfo.innerHTML, /回收此 NFS 共享/);
  await ui.clickReclaim();
  assert.equal(ui.confirms.length, 1);
  assert.match(ui.confirms[0], /不可撤销/);

  const modal = ui.latestModal();
  assert.ok(modal, 'reclaim should offer a per-request maintenance choice');
  assert.equal(modal.checkbox.checked, false);
  await modal.click();

  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/reclaim');
  assert.deepEqual(ui.requests[0].body, { task_id: 42 });
});

test('NFS reclaim sends maintenance_confirmed only from the checked request checkbox', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  ui.app.renderTaskInfo(successfulProvisionTask(), registration);
  await ui.clickReclaim();
  const modal = ui.latestModal();
  modal.checkbox.checked = true;
  await modal.click();

  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/reclaim');
  assert.deepEqual(ui.requests[0].body, { task_id: 42, maintenance_confirmed: true });
});

test('maintenance checkbox state is fresh for each destructive request', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_first', size: 80 });
  const firstModal = ui.latestModal();
  firstModal.checkbox.checked = true;
  await firstModal.click();

  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_second', size: 80 });
  const secondModal = ui.latestModal();
  assert.notEqual(secondModal, firstModal);
  assert.equal(secondModal.checkbox.checked, false);
  await secondModal.click();

  assert.equal(ui.requests.length, 2);
  assert.equal(ui.requests[0].body.maintenance_confirmed, true);
  assert.equal(Object.hasOwn(ui.requests[1].body, 'maintenance_confirmed'), false);
});

test('opening another destructive request retires the previous dialog and its callback', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_first', size: 80 });
  const firstModal = ui.latestModal();
  firstModal.checkbox.checked = true;

  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_second', size: 80 });
  const secondModal = ui.latestModal();
  assert.equal(firstModal.removed, true);
  assert.equal(secondModal.checkbox.checked, false);
  await firstModal.click();
  await secondModal.click();

  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].body.lv_name, 'lv_second');
  assert.equal(Object.hasOwn(ui.requests[0].body, 'maintenance_confirmed'), false);
});

test('maintenance submit is one-shot and stale clicks after cancel are inert', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_double', size: 80 });
  const submitModal = ui.latestModal();
  await Promise.all([submitModal.click(), submitModal.click()]);

  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_cancelled', size: 80 });
  const cancelledModal = ui.latestModal();
  const staleClick = cancelledModal.click;
  cancelledModal.cancel();
  await staleClick();

  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].body.lv_name, 'lv_double');
});
test('canceling either destructive confirmation submits no storage request', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();

  ui.setConfirmResult(false);
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_cancelled', size: 80 });
  assert.equal(ui.modals.length, 0);

  ui.setConfirmResult(true);
  await ui.app.doDeleteLV(ui.content, 8, { vg: 'vg_data', name: 'lv_modal_cancelled', size: 80 });
  const modal = ui.latestModal();
  modal.cancel();

  assert.equal(modal.removed, true);
  assert.equal(ui.requests.length, 0);
});

test('unsupported maintenance request is surfaced without retry or fallback for delete and reclaim', async () => {
  const deleteUI = loadStorageUI();
  deleteUI.setFailingAPI('required kernel namespace ioctl is unsupported');
  await deleteUI.app.doDeleteLV(deleteUI.content, 8, { vg: 'vg_data', name: 'lv_demo', size: 80 });
  const deleteModal = deleteUI.latestModal();
  deleteModal.checkbox.checked = true;
  await deleteModal.click();

  assert.equal(deleteUI.requests.length, 1);
  assert.equal(deleteUI.requests[0].path, '/storage/lv/delete');
  assert.equal(deleteUI.alerts.length, 1);
  assert.match(deleteUI.alerts[0], /required kernel namespace ioctl is unsupported/);

  const reclaimUI = loadStorageUI();
  reclaimUI.setFailingAPI('required kernel namespace ioctl is unsupported');
  reclaimUI.app.renderTaskInfo(successfulProvisionTask(), registration);
  await reclaimUI.clickReclaim();
  const reclaimModal = reclaimUI.latestModal();
  reclaimModal.checkbox.checked = true;
  await reclaimModal.click();

  assert.equal(reclaimUI.requests.length, 1);
  assert.equal(reclaimUI.requests[0].path, '/storage/reclaim');
  assert.equal(reclaimUI.alerts.length, 1);
  assert.match(reclaimUI.alerts[0], /required kernel namespace ioctl is unsupported/);
});
