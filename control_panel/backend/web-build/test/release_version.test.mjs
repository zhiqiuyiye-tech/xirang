import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const chart = await readFile(new URL('../../../charts/control-panel/Chart.yaml', import.meta.url), 'utf8');
const page = await readFile(new URL('../../internal/api/web/index.html', import.meta.url), 'utf8');
const chartReadme = await readFile(new URL('../../../charts/control-panel/README.md', import.meta.url), 'utf8');

test('release version stays consistent across UI and Helm metadata', () => {
  const version = chart.match(/^version:\s*(\d+\.\d+\.\d+)\s*$/m)?.[1];
  const appVersion = chart.match(/^appVersion:\s*"(\d+\.\d+\.\d+)"\s*$/m)?.[1];
  const uiVersion = page.match(/class="brand-version">v(\d+\.\d+\.\d+)</)?.[1];
  assert.ok(version, 'chart release version must be semantic version text');
  assert.equal(appVersion, version);
  assert.equal(uiVersion, version);
});

test('chart packaging documentation uses the current release version', () => {
  const version = chart.match(/^version:\s*(\d+\.\d+\.\d+)\s*$/m)?.[1];
  assert.ok(version);
  assert.ok(chartReadme.includes(`control-panel-${version}.tgz`));
  assert.ok(chartReadme.includes(`control-panel:${version}`));
});
