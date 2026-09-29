import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

const bundle = await readFile(new URL('../../internal/api/web/p256.bundle.js', import.meta.url), 'utf8');
const notice = await readFile(new URL('../NOTICE.md', import.meta.url), 'utf8');

test('generated crypto bundle has no trailing whitespace', () => {
  const trailingWhitespace = bundle.match(/[ \t]+(?=\r?$)/gm) ?? [];
  assert.equal(trailingWhitespace.length, 0, 'bundle contains trailing whitespace');
});

test('NOTICE records the generated crypto bundle hash', () => {
  const hash = createHash('sha256').update(bundle).digest('hex');
  const noticeHash = notice.match(/Generated `p256\.bundle\.js` SHA-256: `([a-f0-9]{64})`/)?.[1];
  assert.ok(noticeHash, 'NOTICE is missing the generated bundle hash');
  assert.equal(noticeHash, hash, 'NOTICE bundle hash is stale');
});
