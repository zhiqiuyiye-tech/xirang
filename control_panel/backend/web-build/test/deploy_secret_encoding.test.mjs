import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const installer = await readFile(new URL('../../../deploy/install.sh', import.meta.url), 'utf8');

test('installer writes AES_KEY as Secret data encoding and reuses existing data verbatim', () => {
  assert.match(installer, /AES_KEY_DATA="\$\(read_secret_key AES_KEY\)"/);
  assert.match(installer, /AES_KEY_DATA="\$\(printf '%s' "\$\{AES_KEY_ENV\}" \| base64 \| tr -d '\\n'\)"/);
  assert.match(installer, /AES_KEY: \$\{AES_KEY_DATA\}/);
});
