import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const appSource = await readFile(new URL('../../internal/api/web/app.js', import.meta.url), 'utf8');

function loadStorageUI() {
  const requests = [];
  const alerts = [];
  const confirms = [];
  let confirmResult = true;
  let reclaimClick = null;
  const window = { location: { search: '', pathname: '/', hash: '' }, addEventListener() {} };
  const taskInfo = { innerHTML: '' };
  const reclaimButton = {
    addEventListener(name, listener) { if (name === 'click') reclaimClick = listener; },
  };
  const document = {
    cookie: '',
    title: 'Xirang Control Panel',
    addEventListener() {},
    getElementById(id) {
      if (id === 'content') return {};
      if (id === 'task-info') return taskInfo;
      if (id === 'btn-reclaim-from-task') return reclaimButton;
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
    taskInfo,
    setConfirmResult(value) { confirmResult = value; },
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

function assertHandbookWarning(message) {
  assert.match(message, /《NFS创建流程》第 8 节/);
  assert.match(message, /目标逻辑卷中的全部数据/);
  assert.match(message, /不可逆/);
  assert.match(message, /停止业务使用/);
  assert.match(message, /数据可以永久丢弃/);
  assert.match(message, /后端不会检查 Kubernetes Pod\/PVC 引用/);
  assert.doesNotMatch(message, /普通主机/);
  const orderedSteps = [
    '/etc/exports',
    '宿主机上执行普通卸载（umount）',
    '持有者挂载命名空间执行普通卸载（nsenter）',
    'lvremove',
    '/etc/fstab',
  ];
  let previousStepPosition = -1;
  for (const step of orderedSteps) {
    const stepPosition = message.indexOf(step);
    assert.ok(stepPosition > previousStepPosition, `handbook step ${step} must appear in order`);
    previousStepPosition = stepPosition;
  }
}

test('LV delete confirms the handbook prerequisites and directly calls the existing API', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();

  await ui.app.doDeleteLV({}, 8, { vg: 'vg_data', name: 'lv_demo', size: 80, mp: '/data02/demo' });

  assert.equal(ui.confirms.length, 1);
  assertHandbookWarning(ui.confirms[0]);
  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/lv/delete');
  assert.deepEqual(ui.requests[0].body, { worker_id: 8, vg_name: 'vg_data', lv_name: 'lv_demo' });
  assert.equal(Object.hasOwn(ui.requests[0].body, 'maintenance_confirmed'), false);
  assert.doesNotMatch(appSource, /showStorageMaintenanceOption|activeStorageMaintenanceModal|storage-maintenance|SHARED_HOST_MAINTENANCE_ENABLED|maintenance_confirmed/i);
});

test('successful NFS provision tasks keep reclaim action with handbook confirmation and direct API call', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  ui.app.renderTaskInfo(successfulProvisionTask(), registration);

  assert.match(ui.taskInfo.innerHTML, /btn-reclaim-from-task/);
  assert.match(ui.taskInfo.innerHTML, /回收此 NFS 共享/);
  await ui.clickReclaim();

  assert.equal(ui.confirms.length, 1);
  assertHandbookWarning(ui.confirms[0]);
  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/reclaim');
  assert.deepEqual(ui.requests[0].body, { task_id: 42 });
  assert.equal(Object.hasOwn(ui.requests[0].body, 'maintenance_confirmed'), false);
});

test('canceling either destructive confirmation submits no storage request', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();

  ui.setConfirmResult(false);
  await ui.app.doDeleteLV({}, 8, { vg: 'vg_data', name: 'lv_cancelled', size: 80 });
  assert.equal(ui.requests.length, 0);

  ui.app.renderTaskInfo(successfulProvisionTask(), registration);
  await ui.clickReclaim();
  assert.equal(ui.requests.length, 0);
  assert.equal(ui.confirms.length, 2);
});

test('duplicate delete submissions while a request is pending make only one API call', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  const volume = { vg: 'vg_data', name: 'lv_double', size: 80 };

  await Promise.all([
    ui.app.doDeleteLV({}, 8, volume),
    ui.app.doDeleteLV({}, 8, volume),
  ]);

  assert.equal(ui.confirms.length, 1);
  assert.equal(ui.requests.length, 1);
});

test('duplicate NFS reclaim submissions while a request is pending make only one API call', async () => {
  const ui = loadStorageUI();
  ui.setSuccessfulAPI();
  ui.app.renderTaskInfo(successfulProvisionTask(), registration);

  await Promise.all([ui.clickReclaim(), ui.clickReclaim()]);

  assert.equal(ui.confirms.length, 1);
  assert.equal(ui.requests.length, 1);
  assert.equal(ui.requests[0].path, '/storage/reclaim');
});

test('API errors are surfaced once without automatic retry or fallback', async () => {
  const deleteUI = loadStorageUI();
  deleteUI.setFailingAPI('volume is busy');

  await deleteUI.app.doDeleteLV({}, 8, { vg: 'vg_data', name: 'lv_demo', size: 80 });

  assert.equal(deleteUI.requests.length, 1);
  assert.equal(deleteUI.requests[0].path, '/storage/lv/delete');
  assert.equal(deleteUI.alerts.length, 1);
  assert.match(deleteUI.alerts[0], /volume is busy/);

  const reclaimUI = loadStorageUI();
  reclaimUI.setFailingAPI('volume is busy');
  reclaimUI.app.renderTaskInfo(successfulProvisionTask(), registration);
  await reclaimUI.clickReclaim();

  assert.equal(reclaimUI.requests.length, 1);
  assert.equal(reclaimUI.requests[0].path, '/storage/reclaim');
  assert.equal(reclaimUI.alerts.length, 1);
  assert.match(reclaimUI.alerts[0], /volume is busy/);
});
