import { createHash } from 'node:crypto';
import { readFile, writeFile } from 'node:fs/promises';
import { build } from 'esbuild';
import { fileURLToPath } from 'node:url';

const outfile = fileURLToPath(new URL('../internal/api/web/p256.bundle.js', import.meta.url));
const noticefile = fileURLToPath(new URL('./NOTICE.md', import.meta.url));

await build({
  entryPoints: [fileURLToPath(new URL('./src/key_crypto.js', import.meta.url))],
  outfile,
  bundle: true,
  format: 'iife',
  globalName: 'XirangCrypto',
  platform: 'browser',
  target: ['es2022'],
  minify: true,
  legalComments: 'eof',
  sourcemap: false,
});

const bundle = (await readFile(outfile, 'utf8')).replace(/[ \t]+(?=\r?$)/gm, '');
await writeFile(outfile, bundle, 'utf8');

const bundleHash = createHash('sha256').update(bundle).digest('hex');
const notice = await readFile(noticefile, 'utf8');
const hashPattern = /(Generated `p256\.bundle\.js` SHA-256: `)[a-f0-9]{64}(`)/;
if (!hashPattern.test(notice)) {
  throw new Error('NOTICE is missing the generated bundle hash');
}
await writeFile(noticefile, notice.replace(hashPattern, (_, prefix, suffix) => `${prefix}${bundleHash}${suffix}`), 'utf8');
