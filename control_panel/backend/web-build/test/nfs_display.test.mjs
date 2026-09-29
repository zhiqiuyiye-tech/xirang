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
      renderPortMappingPodIdentity: typeof renderPortMappingPodIdentity === 'function' ? renderPortMappingPodIdentity : null
    };
  `;
  const instrumentedSource = appSource.replace(/\}\)\(\);\s*$/, injection + '\n})();');
  assert.notEqual(instrumentedSource, appSource, 'test hook must be inserted into the application closure');

  const window = {
    location: { search: '', pathname: '/', hash: '' },
    addEventListener() {},
  };
  const document = {
    cookie: '',
    title: 'Xirang Control Panel',
    addEventListener() {},
  };
  runInNewContext(instrumentedSource, { window, document });
  return window.__nfsDisplayTest;
}

const renderers = loadNFSRenderers();

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
