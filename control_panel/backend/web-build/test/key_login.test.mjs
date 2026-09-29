import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const source = await readFile(new URL('../../internal/api/web/key_login.js', import.meta.url), 'utf8');

function makeElement(id) {
  const listeners = new Map();
  return {
    id,
    value: '',
    files: [],
    disabled: false,
    className: '',
    textContent: '',
    innerHTML: '',
    style: {},
    addEventListener(type, listener) {
      const registered = listeners.get(type) || [];
      registered.push(listener);
      listeners.set(type, registered);
    },
    async dispatch(type, event = {}) {
      for (const listener of listeners.get(type) || []) await listener(event);
    },
    click() {},
    remove() {},
  };
}

async function loadBootstrapLogin() {
  const ids = [
    'login-form', 'login-controls', 'login-error', 'bootstrap-password',
    'bootstrap-generate', 'bootstrap-private-key', 'login-submit', 'bootstrap-file-status',
  ];
  const elements = new Map(ids.map((id) => [id, makeElement(id)]));
  const body = { appendChild() {} };
  let generatedKeys = 0;
  let downloadedKeys = 0;
  const window = {
    XirangCrypto: {
      async generatePrivateKeyPem() {
        generatedKeys++;
        return 'private-key-pem';
      },
      derivePublicKeyPem() {
        return 'public-key-pem';
      },
      async fingerprintPublicKeyPem() {
        return 'fingerprint';
      },
    },
    setTimeout(callback) {
      callback();
    },
  };
  const document = {
    cookie: '',
    body,
    getElementById(id) {
      return elements.get(id) || null;
    },
    createElement() {
      return {
        href: '',
        download: '',
        style: {},
        click() {
          downloadedKeys++;
        },
        remove() {},
      };
    },
  };
  const context = {
    window,
    document,
    URL: {
      createObjectURL() {
        return 'blob:test';
      },
      revokeObjectURL() {},
    },
    Blob,
    fetch: async () => ({
      ok: true,
      async json() {
        return { auth_state: 'PASSWORD_BOOTSTRAP' };
      },
    }),
  };

  runInNewContext(source, context);
  window.XirangKeyLogin.init();
  await new Promise((resolve) => setImmediate(resolve));

  return {
    elements,
    get generatedKeys() {
      return generatedKeys;
    },
    get downloadedKeys() {
      return downloadedKeys;
    },
  };
}

test('does not generate or download a bootstrap key when the password is empty', async () => {
  const login = await loadBootstrapLogin();

  await login.elements.get('bootstrap-generate').dispatch('click');

  assert.equal(login.generatedKeys, 0);
  assert.equal(login.downloadedKeys, 0);
  assert.match(login.elements.get('login-error').textContent, /初始化管理员密码/);
});
