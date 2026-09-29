(function () {
    'use strict';

    var authStatus = null;
    var bootstrapExpectedFingerprint = '';
    var rotationCurrentKeyReady = false;
    var rotationExpectedFingerprint = '';
    var rotationNewKeyReady = false;

    function csrfToken() {
        var match = document.cookie.match(/(?:^|;\s*)(?:cp_csrf|[^=;]*csrf[^=;]*)=([^;]+)/i);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function request(path, method, body) {
        var headers = {};
        var options = {
            method: method || 'GET',
            credentials: 'same-origin',
            cache: 'no-store',
            headers: headers
        };
        if (body != null) {
            headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(body);
        }
        if (options.method !== 'GET' && options.method !== 'HEAD') {
            var csrf = csrfToken();
            if (csrf) headers['X-CSRF-Token'] = csrf;
        }
        return fetch('/api/v1' + path, options);
    }

    async function responseJSON(response) {
        return response.json().catch(function () { return {}; });
    }

    async function refreshStatus() {
        var response = await request('/auth/status', 'GET');
        if (!response.ok) throw new Error('无法读取登录状态');
        authStatus = await responseJSON(response);
        return authStatus;
    }

    function setLoginError(message, success) {
        var element = document.getElementById('login-error');
        if (!element) return;
        element.className = success ? 'success-msg' : 'error-msg';
        element.textContent = message || '';
    }

    function loginControls() {
        return document.getElementById('login-controls');
    }

    function renderLogin(message) {
        var controls = loginControls();
        if (!controls) return;
        if (!authStatus) {
            controls.innerHTML = '<div class="info-msg">正在读取认证状态…</div>';
            refreshStatus().then(function () { renderLogin(message); }).catch(function (error) {
                controls.innerHTML = '<div class="error-msg">无法连接认证服务。</div>';
                setLoginError(error.message, false);
            });
            return;
        }

        if (authStatus.auth_state === 'PASSWORD_BOOTSTRAP') {
            controls.innerHTML = '<div class="key-login-panel">' +
                '<h2 class="login-mode-title">首次启用登录密钥</h2>' +
                '<p class="muted">使用初始化密码登记一把共享的 P-256 私钥。私钥文件只在此浏览器生成，不会上传到服务端。</p>' +
                '<div class="form-field"><label for="bootstrap-password">初始化管理员密码</label><input type="password" id="bootstrap-password" autocomplete="current-password" required></div>' +
                '<button type="button" id="bootstrap-generate" class="btn btn-secondary btn-block">生成并下载私钥文件</button>' +
                '<p id="bootstrap-file-status" class="muted" role="status">生成文件后，请重新选择刚下载的文件以确认可读取。</p>' +
                '<div class="form-field"><label for="bootstrap-private-key">重新选择下载的私钥文件</label><input type="file" id="bootstrap-private-key" accept=".pem,application/x-pem-file,text/plain" disabled></div>' +
                '<button type="submit" id="login-submit" class="btn btn-primary btn-block btn-lg" disabled>登记密钥并登录</button>' +
                '</div>';
            setLoginError(message || '', false);
            wireBootstrapForm();
            return;
        }

        if (authStatus.auth_state === 'KEY_ACTIVE') {
            controls.innerHTML = '<div class="key-login-panel">' +
                '<h2 class="login-mode-title">私钥文件登录</h2>' +
                '<p class="muted">选择管理员共享的 P-256 PKCS#8 PEM 文件。私钥只在浏览器内存中读取和签名。</p>' +
                '<div class="form-field"><label for="login-private-key">管理员私钥文件</label><input type="file" id="login-private-key" accept=".pem,application/x-pem-file,text/plain" required></div>' +
                '<div class="muted key-fingerprint">当前密钥指纹：<code id="login-key-fingerprint"></code></div>' +
                '<button type="submit" id="login-submit" class="btn btn-primary btn-block btn-lg">签名并登录</button>' +
                '</div>';
            var fingerprint = document.getElementById('login-key-fingerprint');
            if (fingerprint) fingerprint.textContent = authStatus.key_fingerprint || '不可用';
            setLoginError(message || '', false);
            return;
        }

        controls.innerHTML = '<div class="error-msg">服务端认证状态无效，登录已停止。</div>';
        setLoginError('请联系运维人员检查管理员认证状态。', false);
    }

    function downloadPrivateKey(privatePem, fileName) {
        var blob = new Blob([privatePem], { type: 'application/x-pem-file' });
        var url = URL.createObjectURL(blob);
        var anchor = document.createElement('a');
        anchor.href = url;
        anchor.download = fileName;
        anchor.style.display = 'none';
        document.body.appendChild(anchor);
        anchor.click();
        anchor.remove();
        window.setTimeout(function () { URL.revokeObjectURL(url); }, 0);
    }

    async function readPrivateKeyFile(input) {
        var file = input && input.files && input.files[0];
        if (!file) throw new Error('请选择私钥 PEM 文件。');
        if (file.size <= 0 || file.size > 16 * 1024) throw new Error('私钥文件大小必须在 1 到 16384 字节之间。');
        var contents = await file.text();
        if (new TextEncoder().encode(contents).length > 16 * 1024) throw new Error('私钥文件超过 16 KiB。');
        return contents;
    }

    function clearFileInput(input) {
        if (input) input.value = '';
    }

    function wireBootstrapForm() {
        var generateButton = document.getElementById('bootstrap-generate');
        var fileInput = document.getElementById('bootstrap-private-key');
        var submitButton = document.getElementById('login-submit');
        var status = document.getElementById('bootstrap-file-status');
        if (!generateButton || !fileInput || !submitButton) return;

        generateButton.addEventListener('click', async function () {
            var passwordInput = document.getElementById('bootstrap-password');
            if (!passwordInput || !passwordInput.value) {
                setLoginError('请输入初始化管理员密码。', false);
                return;
            }
            generateButton.disabled = true;
            setLoginError('', false);
            var privatePem = '';
            try {
                if (!window.XirangCrypto) throw new Error('本地 P-256 加密模块不可用。');
                privatePem = await window.XirangCrypto.generatePrivateKeyPem();
                var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
                bootstrapExpectedFingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
                downloadPrivateKey(privatePem, 'xirang-admin-p256-key.pem');
                fileInput.disabled = false;
                fileInput.value = '';
                submitButton.disabled = true;
                status.textContent = '文件已下载。请重新选择同一文件，确认它能被解析后再登记。';
            } catch (error) {
                bootstrapExpectedFingerprint = '';
                setLoginError(error.message || '无法生成密钥文件。', false);
            } finally {
                privatePem = '';
                generateButton.disabled = false;
            }
        });

        fileInput.addEventListener('change', async function () {
            submitButton.disabled = true;
            if (!bootstrapExpectedFingerprint) return;
            var privatePem = '';
            try {
                privatePem = await readPrivateKeyFile(fileInput);
                var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
                var fingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
                if (fingerprint !== bootstrapExpectedFingerprint) throw new Error('所选文件与刚刚生成的密钥不匹配。');
                submitButton.disabled = false;
                status.textContent = '私钥文件已重新导入并验证，可以登记。';
                setLoginError('', false);
            } catch (error) {
                status.textContent = '请重新选择刚刚下载的私钥文件。';
                setLoginError(error.message || '无法读取私钥文件。', false);
            } finally {
                privatePem = '';
            }
        });
    }

    async function handleBootstrap(privatePem, password) {
        var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
        var fingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
        if (!bootstrapExpectedFingerprint || fingerprint !== bootstrapExpectedFingerprint) {
            throw new Error('请重新选择刚刚下载的私钥文件。');
        }
        var challengeResponse = await request('/auth/challenges/bootstrap', 'POST', { public_key_pem: publicPem });
        var challenge = await responseJSON(challengeResponse);
        if (!challengeResponse.ok) throw new Error(challenge.error || '无法创建首次登记挑战。');
        var context = {
            id: challenge.challenge_id,
            nonce: challenge.nonce,
            purpose: challenge.purpose,
            auth_version: challenge.auth_version,
            new_key_fingerprint: challenge.new_key_fingerprint
        };
        var proofSignature = await window.XirangCrypto.signChallenge(privatePem, context, 'bootstrap');
        var response = await request('/auth/bootstrap', 'POST', {
            password: password,
            public_key_pem: publicPem,
            challenge_id: challenge.challenge_id,
            proof_signature: proofSignature
        });
        var result = await responseJSON(response);
        if (!response.ok) throw new Error(result.error || '首次密钥登记失败。');
        authStatus = { auth_state: 'KEY_ACTIVE', key_fingerprint: fingerprint };
    }

    async function handleKeyLogin(privatePem) {
        var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
        var fingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
        if (authStatus.key_fingerprint && fingerprint !== authStatus.key_fingerprint) {
            throw new Error('所选私钥与当前管理员密钥指纹不匹配。');
        }
        var challengeResponse = await request('/auth/challenges/login', 'POST');
        var challenge = await responseJSON(challengeResponse);
        if (!challengeResponse.ok) throw new Error(challenge.error || '无法创建登录挑战。');
        if (challenge.key_fingerprint !== fingerprint) throw new Error('私钥文件与服务端当前密钥不匹配。');
        var context = {
            id: challenge.challenge_id,
            nonce: challenge.nonce,
            purpose: challenge.purpose,
            auth_version: challenge.auth_version,
            key_fingerprint: challenge.key_fingerprint
        };
        var signature = await window.XirangCrypto.signChallenge(privatePem, context, 'login');
        var response = await request('/auth/login', 'POST', {
            challenge_id: challenge.challenge_id,
            signature: signature
        });
        var result = await responseJSON(response);
        if (!response.ok) throw new Error(result.error || '密钥签名登录失败。');
    }

    async function handleLoginSubmit(event) {
        event.preventDefault();
        var submitButton = document.getElementById('login-submit');
        var state = authStatus && authStatus.auth_state;
        var privatePem = '';
        var bootstrapPasswordInput = null;
        var activeKeyInput = null;
        if (submitButton) submitButton.disabled = true;
        setLoginError('', false);
        try {
            if (!window.XirangCrypto) throw new Error('本地 P-256 加密模块不可用。');
            if (state === 'PASSWORD_BOOTSTRAP') {
                bootstrapPasswordInput = document.getElementById('bootstrap-password');
                var fileInput = document.getElementById('bootstrap-private-key');
                activeKeyInput = fileInput;
                var password = bootstrapPasswordInput ? bootstrapPasswordInput.value : '';
                if (!password) throw new Error('请输入初始化管理员密码。');
                privatePem = await readPrivateKeyFile(fileInput);
                await handleBootstrap(privatePem, password);
                if (bootstrapPasswordInput) bootstrapPasswordInput.value = '';
                clearFileInput(fileInput);
                bootstrapExpectedFingerprint = '';
                window.XirangApp.showApp();
                return;
            }
            if (state === 'KEY_ACTIVE') {
                var loginFile = document.getElementById('login-private-key');
                activeKeyInput = loginFile;
                privatePem = await readPrivateKeyFile(loginFile);
                await handleKeyLogin(privatePem);
                clearFileInput(loginFile);
                window.XirangApp.clearLegacyTokens();
                window.XirangApp.showApp();
                return;
            }
            throw new Error('服务端认证状态不可用。');
        } catch (error) {
            setLoginError(error.message || '登录失败。', false);
        } finally {
            privatePem = '';
            if (bootstrapPasswordInput) bootstrapPasswordInput.value = '';
            clearFileInput(activeKeyInput);
            if (submitButton) submitButton.disabled = false;
        }
    }

    function renderRotation(container) {
        if (!container) return;
        if (!authStatus) {
            container.innerHTML = '<div class="card"><p class="muted">正在读取登录密钥状态…</p></div>';
            refreshStatus().then(function () { renderRotation(container); }).catch(function () {
                container.innerHTML = '<div class="card"><div class="error-msg">无法读取登录密钥状态。</div></div>';
            });
            return;
        }
        if (authStatus.auth_state !== 'KEY_ACTIVE') {
            container.innerHTML = '<div class="card"><div class="error-msg">当前没有可轮换的活动登录密钥。</div></div>';
            return;
        }

        container.innerHTML = '<div class="card key-rotation-card">' +
            '<h3 class="card-title">轮换共享管理员登录密钥</h3>' +
            '<p class="muted">轮换需要当前私钥签名，并用新私钥完成持有证明。新文件下载后必须重新选择；提交成功后旧私钥和其他 Session 立即失效。</p>' +
            '<div class="form-field"><label for="rotate-current-file">当前私钥文件</label><input type="file" id="rotate-current-file" accept=".pem,application/x-pem-file,text/plain"></div>' +
            '<div class="form-field"><label>新私钥文件</label><button type="button" id="rotate-generate" class="btn btn-secondary">生成并下载新密钥文件</button></div>' +
            '<div class="form-field"><label for="rotate-new-file">重新选择刚下载的新私钥文件</label><input type="file" id="rotate-new-file" accept=".pem,application/x-pem-file,text/plain" disabled></div>' +
            '<div id="rotate-message" class="info-msg" role="status"></div>' +
            '<button type="button" id="rotate-submit" class="btn btn-primary" disabled>用当前和新私钥签名并轮换</button>' +
            '</div>';

        rotationCurrentKeyReady = false;
        rotationExpectedFingerprint = '';
        rotationNewKeyReady = false;
        var currentInput = document.getElementById('rotate-current-file');
        var newInput = document.getElementById('rotate-new-file');
        var generateButton = document.getElementById('rotate-generate');
        var submitButton = document.getElementById('rotate-submit');
        var message = document.getElementById('rotate-message');

        function rotationMessage(text, type) {
            message.className = type === 'error' ? 'error-msg' : (type === 'success' ? 'success-msg' : 'info-msg');
            message.textContent = text || '';
        }
        function updateSubmitState() {
            submitButton.disabled = !(rotationCurrentKeyReady && rotationNewKeyReady);
        }

        currentInput.addEventListener('change', async function () {
            rotationCurrentKeyReady = false;
            updateSubmitState();
            var privatePem = '';
            try {
                privatePem = await readPrivateKeyFile(currentInput);
                var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
                var fingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
                if (fingerprint !== authStatus.key_fingerprint) throw new Error('所选文件不是当前活动的管理员私钥。');
                rotationCurrentKeyReady = true;
                rotationMessage('当前私钥已验证。', 'success');
            } catch (error) {
                rotationMessage(error.message || '无法验证当前私钥文件。', 'error');
            } finally {
                privatePem = '';
                updateSubmitState();
            }
        });

        generateButton.addEventListener('click', async function () {
            rotationNewKeyReady = false;
            updateSubmitState();
            if (!rotationCurrentKeyReady) {
                rotationMessage('请先选择并验证当前私钥文件。', 'error');
                return;
            }
            generateButton.disabled = true;
            var privatePem = '';
            try {
                if (!window.XirangCrypto) throw new Error('本地 P-256 加密模块不可用。');
                privatePem = await window.XirangCrypto.generatePrivateKeyPem();
                var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
                rotationExpectedFingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
                downloadPrivateKey(privatePem, 'xirang-admin-p256-key.pem');
                newInput.disabled = false;
                newInput.value = '';
                rotationMessage('新私钥已下载。请重新选择该文件以确认可读取。', 'info');
            } catch (error) {
                rotationExpectedFingerprint = '';
                rotationMessage(error.message || '无法生成新私钥文件。', 'error');
            } finally {
                privatePem = '';
                generateButton.disabled = false;
            }
        });

        newInput.addEventListener('change', async function () {
            rotationNewKeyReady = false;
            updateSubmitState();
            var privatePem = '';
            try {
                if (!rotationExpectedFingerprint) throw new Error('请先生成并下载新私钥文件。');
                privatePem = await readPrivateKeyFile(newInput);
                var publicPem = window.XirangCrypto.derivePublicKeyPem(privatePem);
                var fingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(publicPem);
                if (fingerprint !== rotationExpectedFingerprint) throw new Error('所选文件与刚刚生成的新私钥不匹配。');
                rotationNewKeyReady = true;
                rotationMessage('当前和新私钥文件均已验证，可以开始轮换。', 'success');
            } catch (error) {
                rotationMessage(error.message || '无法验证新私钥文件。', 'error');
            } finally {
                privatePem = '';
                updateSubmitState();
            }
        });

        submitButton.addEventListener('click', async function () {
            if (!(rotationCurrentKeyReady && rotationNewKeyReady)) return;
            submitButton.disabled = true;
            var currentPem = '';
            var newPem = '';
            try {
                currentPem = await readPrivateKeyFile(currentInput);
                newPem = await readPrivateKeyFile(newInput);
                var currentPublicPem = window.XirangCrypto.derivePublicKeyPem(currentPem);
                var currentFingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(currentPublicPem);
                var newPublicPem = window.XirangCrypto.derivePublicKeyPem(newPem);
                var newFingerprint = await window.XirangCrypto.fingerprintPublicKeyPem(newPublicPem);
                if (currentFingerprint !== authStatus.key_fingerprint || newFingerprint !== rotationExpectedFingerprint) {
                    throw new Error('私钥文件与已验证指纹不匹配，请重新选择文件。');
                }

                rotationMessage('正在获取轮换挑战…', 'info');
                var challengeResponse = await request('/auth/challenges/rotate', 'POST', { new_public_key_pem: newPublicPem });
                var challenge = await responseJSON(challengeResponse);
                if (challengeResponse.status === 401 && window.XirangApp) window.XirangApp.showLogin('会话已失效，请重新登录。');
                if (!challengeResponse.ok) throw new Error(challenge.error || '无法创建轮换挑战。');
                var context = {
                    id: challenge.challenge_id,
                    nonce: challenge.nonce,
                    purpose: challenge.purpose,
                    auth_version: challenge.auth_version,
                    key_fingerprint: challenge.key_fingerprint,
                    new_key_fingerprint: challenge.new_key_fingerprint
                };
                var currentSignature = await window.XirangCrypto.signChallenge(currentPem, context, 'key_rotate');
                var proofSignature = await window.XirangCrypto.signChallenge(newPem, context, 'new_key');
                var response = await request('/auth/key', 'PUT', {
                    challenge_id: challenge.challenge_id,
                    new_public_key_pem: newPublicPem,
                    current_signature: currentSignature,
                    proof_signature: proofSignature
                });
                var result = await responseJSON(response);
                if (response.status === 401 && window.XirangApp) window.XirangApp.showLogin('会话已失效，请重新登录。');
                if (!response.ok) throw new Error(result.error || '登录密钥轮换失败。');
                authStatus = { auth_state: 'KEY_ACTIVE', key_fingerprint: newFingerprint };
                rotationExpectedFingerprint = '';
                rotationCurrentKeyReady = false;
                rotationNewKeyReady = false;
                currentInput.value = '';
                newInput.value = '';
                newInput.disabled = true;
                updateSubmitState();
                rotationMessage('密钥已轮换。请通过受控渠道向所有操作者分发新文件。', 'success');
                var fingerprintElement = document.getElementById('sec-fingerprint');
                if (fingerprintElement) fingerprintElement.textContent = newFingerprint;
                var sessionResponse = await request('/auth/me', 'GET');
                var sessionInfo = await responseJSON(sessionResponse);
                var versionElement = document.getElementById('sec-version');
                if (sessionResponse.ok && versionElement) versionElement.textContent = 'v' + (sessionInfo.auth_version || '-');
            } catch (error) {
                rotationMessage(error.message || '密钥轮换失败。', 'error');
            } finally {
                currentPem = '';
                newPem = '';
                currentInput.value = '';
                newInput.value = '';
                rotationCurrentKeyReady = false;
                rotationNewKeyReady = false;
                updateSubmitState();
            }
        });
    }

    async function logoutCurrent() {
        try {
            var response = await request('/auth/logout', 'POST');
            if (!response.ok) {
                var result = await responseJSON(response);
                throw new Error(result.error || '服务器未能清除当前会话。');
            }
        } catch (error) {
            window.alert('退出当前浏览器失败：' + (error.message || '请检查连接后重试。'));
            return;
        }
        if (window.XirangApp) {
            window.XirangApp.clearLegacyTokens();
            window.XirangApp.showLogin('已退出当前浏览器。');
        }
    }

    async function logoutAll() {
        if (!window.confirm('这会撤销所有操作者当前的登录会话。是否继续？')) return;
        try {
            var response = await request('/auth/logout-all', 'POST');
            if (!response.ok) {
                var result = await responseJSON(response);
                throw new Error(result.error || '服务器未能撤销所有会话。');
            }
        } catch (error) {
            window.alert('退出所有会话失败：' + (error.message || '请检查连接后重试。'));
            return;
        }
        if (window.XirangApp) {
            window.XirangApp.clearLegacyTokens();
            window.XirangApp.showLogin('所有共享账号会话已撤销。');
        }
    }

    function init() {
        var form = document.getElementById('login-form');
        if (form) form.addEventListener('submit', handleLoginSubmit);
        refreshStatus().then(function () { renderLogin(''); }).catch(function (error) {
            renderLogin(error.message || '无法连接认证服务。');
        });
    }

    window.XirangKeyLogin = {
        init: init,
        refreshStatus: refreshStatus,
        renderLogin: renderLogin,
        renderRotation: renderRotation,
        logoutCurrent: logoutCurrent,
        logoutAll: logoutAll,
        handleLoginSubmit: handleLoginSubmit
    };
})();
