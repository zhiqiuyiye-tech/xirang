import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';

import {
  derivePublicKeyPem,
  fingerprintPublicKeyPem,
  generatePrivateKeyPem,
  generateRandomUUID,
  signChallenge,
  verifyChallenge,
} from '../src/key_crypto.js';

const vector = JSON.parse(await readFile(new URL('../../internal/auth/testdata/p256-login-vector.json', import.meta.url), 'utf8'));

const challenge = {
  id: 'AQIDBAUGBwgJCgsMDQ4PEA',
  nonce: 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
  purpose: 'LOGIN',
  auth_version: 1,
  key_fingerprint: '5cd252fb0ce8932436faf8ccd1040981b89ee4ad6b9fe9e2a2b7e71aacb27cd3',
};

function toPemBase64(bytes) {
  return Buffer.from(bytes).toString('base64').match(/.{1,64}/g).join('\n');
}

test('imports PKCS#8 P-256 key and verifies Go signature vector', async () => {
  const publicKeyPem = derivePublicKeyPem(vector.private_key_pem);
  assert.equal(await fingerprintPublicKeyPem(publicKeyPem), challenge.key_fingerprint);
  assert.equal(verifyChallenge(publicKeyPem, vector.message, vector.signature), true);
});

test('signs the exact login challenge as raw canonical base64url r||s', async () => {
  const signature = await signChallenge(vector.private_key_pem, challenge, 'login');
  assert.match(signature, /^[A-Za-z0-9_-]{86}$/);
  assert.equal(signature, vector.js_signature);
  assert.equal(verifyChallenge(vector.public_key_pem, vector.message, signature), true);
});

test('generates an importable PKCS#8 P-256 private key file', async () => {
  const privatePem = await generatePrivateKeyPem();
  assert.match(privatePem, /^-----BEGIN PRIVATE KEY-----\n/);
  const publicKeyPem = derivePublicKeyPem(privatePem);
  assert.match(publicKeyPem, /^-----BEGIN PUBLIC KEY-----\n/);
  assert.match(await fingerprintPublicKeyPem(publicKeyPem), /^[0-9a-f]{64}$/);
});

test('rejects malformed and non-P-256 private key PEM and invalid signatures', async () => {
  assert.throws(() => derivePublicKeyPem('not a PEM'), /private key/i);
  const p384Pair = await globalThis.crypto.subtle.generateKey(
    { name: 'ECDSA', namedCurve: 'P-384' }, true, ['sign', 'verify'],
  );
  const p384Der = new Uint8Array(await globalThis.crypto.subtle.exportKey('pkcs8', p384Pair.privateKey));
  const p384Pem = `-----BEGIN PRIVATE KEY-----\n${toPemBase64(p384Der)}\n-----END PRIVATE KEY-----\n`;
  assert.throws(() => derivePublicKeyPem(p384Pem), /P-256/i);
  assert.equal(verifyChallenge(vector.public_key_pem, vector.message, 'A'.repeat(85)), false);
});

test('generates the PKCS#8 interoperability fixture Go can parse', async () => {
  const originalCrypto = globalThis.crypto;
  Object.defineProperty(globalThis, 'crypto', {
    value: { getRandomValues(bytes) { bytes.fill(1); return bytes; } },
    configurable: true,
  });
  try {
    const privatePem = await generatePrivateKeyPem();
    assert.equal(privatePem, vector.browser_generated_private_key_pem);
    const publicPem = derivePublicKeyPem(privatePem);
    assert.equal(publicPem, vector.browser_generated_public_key_pem);
    assert.equal(await fingerprintPublicKeyPem(publicPem), vector.browser_generated_fingerprint);
  } finally {
    Object.defineProperty(globalThis, 'crypto', { value: originalCrypto, configurable: true });
  }
});

test('generates UUIDv4 with secure random bytes', async () => {
  const originalCrypto = globalThis.crypto;
  Object.defineProperty(globalThis, 'crypto', {
    value: { getRandomValues(bytes) { bytes.fill(0); return bytes; } },
    configurable: true,
  });
  try {
    const uuid = generateRandomUUID();
    assert.match(uuid, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
  } finally {
    Object.defineProperty(globalThis, 'crypto', { value: originalCrypto, configurable: true });
  }
});

test('fails closed when secure browser randomness is unavailable', async () => {
  const originalCrypto = globalThis.crypto;
  Object.defineProperty(globalThis, 'crypto', { value: undefined, configurable: true });
  try {
    await assert.rejects(generatePrivateKeyPem(), /crypto\.getRandomValues/);
  } finally {
    Object.defineProperty(globalThis, 'crypto', { value: originalCrypto, configurable: true });
  }
});
