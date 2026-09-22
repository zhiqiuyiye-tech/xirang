/* Xirang Control Panel - Frontend SPA
 * Native HTML/CSS/JS - no build tools, no frameworks.
 * Hash-based routing, HttpOnly Cookie session, CSRF double-submit, SSE via EventSource.
 */

(function () {
    'use strict';

    var isAuthenticated = false;

    // ===== CSRF & Cookie Management =====
    function getCSRFToken() {
        var match = document.cookie.match(/(?:^|;\s*)cp_csrf=([^;]+)/);
        return match ? decodeURIComponent(match[1]) : '';
    }

    function clearLegacyTokens() {
        try { localStorage.removeItem('cp_token'); } catch (e) {}
    }

    // ===== API Helper =====
    async function apiFetch(path, opts) {
        opts = opts || {};
        opts.headers = opts.headers || {};
        opts.credentials = 'same-origin';

        var method = (opts.method || 'GET').toUpperCase();
        if (method !== 'GET' && method !== 'HEAD') {
            var csrf = getCSRFToken();
            if (csrf) {
                opts.headers['X-CSRF-Token'] = csrf;
            }
        }
        if (opts.body && !opts.headers['Content-Type']) {
            opts.headers['Content-Type'] = 'application/json';
        }
        var resp = await fetch('/api/v1' + path, opts);
        if (resp.status === 401) {
            isAuthenticated = false;
            clearLegacyTokens();
            showLogin('会话已失效或未登录，请重新登录');
            throw new Error('未授权');
        }
        return resp;
    }

    async function apiJSON(path, opts) {
        var resp = await apiFetch(path, opts);
        var data = null;
        if (resp.status !== 204) {
            data = await resp.json().catch(function () { return null; });
        }
        return { resp: resp, data: data };
    }

    // ===== View Management =====
    function showLogin(msg) {
        isAuthenticated = false;
        document.getElementById('login-view').style.display = 'flex';
        document.getElementById('app-view').style.display = 'none';
        var errEl = document.getElementById('login-error');
        if (errEl) {
            errEl.textContent = msg || '';
        }
    }

    function showApp() {
        isAuthenticated = true;
        document.getElementById('login-view').style.display = 'none';
        document.getElementById('app-view').style.display = 'block';
        handleRoute();
    }

    // ===== Login =====
    async function handleLogin(e) {
        e.preventDefault();
        var username = document.getElementById('login-username').value;
        var password = document.getElementById('login-password').value;
        var errEl = document.getElementById('login-error');
        errEl.textContent = '';
        var submitBtn = e.target.querySelector('button[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;

        try {
            var resp = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({ username: username, password: password })
            });
            if (!resp.ok) {
                var d = await resp.json().catch(function () { return {}; });
                errEl.textContent = d.error || '登录失败，请检查账号密码';
                return;
            }
            clearLegacyTokens();
            showApp();
        } catch (err) {
            errEl.textContent = '网络连接异常: ' + err.message;
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    }

    // ===== Logout =====
    async function handleLogout() {
        try {
            await apiFetch('/auth/logout', { method: 'POST' });
        } catch (e) { /* ignore */ }
        clearLegacyTokens();
        showLogin();
    }

    // ===== Change Password Modal =====
    function showChangePasswordModal() {
        var existing = document.getElementById('pwd-modal');
        if (existing) existing.remove();

        var html = '<div class="modal-overlay" id="pwd-modal">' +
            '<div class="modal" style="max-width: 460px;">' +
            '<h3 class="modal-title">修改管理员密码</h3>' +
            '<form id="pwd-form">' +
            '<div class="form-field"><label>当前密码</label><input type="password" name="old_password" required placeholder="请输入当前管理员密码"></div>' +
            '<div class="form-field"><label>新密码 (12-72 字符)</label><input type="password" name="new_password" required minlength="12" maxlength="72" placeholder="请输入至少 12 位新密码"></div>' +
            '<div class="form-field"><label>确认新密码</label><input type="password" name="confirm_password" required minlength="12" maxlength="72" placeholder="再次输入新密码"></div>' +
            '<div id="pwd-error" class="error-msg"></div>' +
            '<div class="modal-actions">' +
            '<button type="button" class="btn btn-secondary" id="pwd-cancel">取消</button>' +
            '<button type="submit" class="btn btn-primary">保存修改</button>' +
            '</div>' +
            '</form>' +
            '</div></div>';

        document.body.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('pwd-modal');
        document.getElementById('pwd-cancel').addEventListener('click', function () { modal.remove(); });

        document.getElementById('pwd-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var errEl = document.getElementById('pwd-error');
            errEl.textContent = '';
            var oldP = e.target.old_password.value;
            var newP = e.target.new_password.value;
            var confirmP = e.target.confirm_password.value;

            if (newP !== confirmP) {
                errEl.textContent = '两次输入的新密码不一致';
                return;
            }
            if (newP.length < 12 || newP.length > 72) {
                errEl.textContent = '新密码长度必须在 12 到 72 位之间';
                return;
            }

            try {
                var res = await apiJSON('/auth/password', {
                    method: 'PUT',
                    body: JSON.stringify({ old_password: oldP, new_password: newP })
                });
                if (!res.resp.ok) {
                    errEl.textContent = (res.data && res.data.error) || '修改失败，请重试';
                    return;
                }
                modal.remove();
                alert('管理员密码修改成功，新会话已更新！');
            } catch (err) {
                errEl.textContent = '操作异常: ' + err.message;
            }
        });
    }

    // ===== Utility =====
    function esc(s) {
        if (s == null) return '';
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function fmtTime(ts) {
        if (!ts) return '-';
        try {
            return new Date(ts).toLocaleString('zh-CN', { hour12: false });
        } catch (e) { return String(ts); }
    }

    function statusBadge(status) {
        var cls = 'badge-pending';
        var text = esc(status);
        if (status === 'success' || status === 'succeeded' || status === 'ok') {
            cls = 'badge-success';
            text = '运行正常';
        } else if (status === 'running') {
            cls = 'badge-running';
            text = '执行中';
        } else if (status === 'failed' || status === 'error') {
            cls = 'badge-failed';
            text = '异常/失败';
        } else if (status === 'pending') {
            text = '排队中';
        }
        return '<span class="badge ' + cls + '"><span class="badge-dot"></span>' + text + '</span>';
    }

    function authModeBadge(mode) {
        var cls = 'badge-key';
        var label = esc(mode);
        if (mode === 'password') {
            cls = 'badge-password';
            label = '密码认证';
        } else if (mode === 'key') {
            cls = 'badge-key';
            label = '私钥认证';
        } else if (mode === 'both') {
            cls = 'badge-both';
            label = '双重认证';
        }
        return '<span class="badge ' + cls + '">' + label + '</span>';
    }

    // Generic message helper for a content div
    function setMsg(el, msg, type) {
        el.className = type === 'error' ? 'error-msg' : (type === 'success' ? 'success-msg' : 'info-msg');
        el.textContent = msg;
    }

    // ===== Hash Router =====
    var routes = {};

    function registerRoute(path, handler) {
        routes[path] = handler;
    }

    function handleRoute() {
        var hash = window.location.hash.slice(1) || '/workers';
        var links = document.querySelectorAll('.nav-link');
        links.forEach(function (l) {
            l.classList.toggle('active', l.getAttribute('href') === '#' + hash.split('/')[0] + '/' + (hash.split('/')[1] || ''));
        });

        // Exact match first
        var handler = routes[hash];
        if (!handler) {
            // Prefix match for detail routes (e.g. /tasks/5 matches /tasks/)
            var parts = hash.split('/');
            if (parts.length >= 3) {
                var prefix = '/' + parts[1] + '/';
                if (routes[prefix]) {
                    handler = routes[prefix];
                }
            }
        }
        var content = document.getElementById('page-content');
        if (handler) {
            handler(content, hash);
        } else {
            content.innerHTML = '<div class="card"><h2 class="page-title">页面未找到</h2><p class="muted mt-1">未知路由路径: ' + esc(hash) + '</p></div>';
        }
    }

    // ====================================================================
    // WORKERS PAGE
    // ====================================================================

    registerRoute('/workers', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">Worker 节点管理</h2>' +
            '<p class="page-subtitle">配置与维护集群计算 Worker、SSH 连接认证、远程依赖与连通性</p>' +
            '</div>' +
            '<button class="btn btn-primary" id="btn-new-worker">' +
            '<svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd"/></svg>' +
            '新建 Worker' +
            '</button>' +
            '</div>' +
            '<div id="workers-msg" class="info-msg"></div>' +
            '<div class="table-responsive mt-2">' +
            '<table class="data-table" id="workers-table"><thead><tr>' +
            '<th>ID</th><th>节点名称</th><th>主机地址</th><th>端口</th><th>用户名</th><th>认证方式</th><th>状态</th><th>最近上报</th><th style="text-align:right;">操作</th>' +
            '</tr></thead><tbody id="workers-tbody"><tr><td colspan="9" class="muted">正在加载节点列表...</td></tr></tbody></table>' +
            '</div>';

        document.getElementById('btn-new-worker').addEventListener('click', function () {
            showWorkerForm(content, null);
        });

        try {
            var r = await apiJSON('/workers');
            if (!r.resp.ok) { setMsg(document.getElementById('workers-msg'), '错误: ' + (r.data && r.data.error), 'error'); return; }
            var workers = r.data || [];
            var tbody = document.getElementById('workers-tbody');
            if (workers.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" class="muted">暂无 Worker 节点，点击右上角「新建 Worker」开始接入。</td></tr>';
                return;
            }
            tbody.innerHTML = workers.map(function (w) {
                return '<tr>' +
                    '<td><span class="badge-mono font-mono">' + esc(w.id) + '</span></td>' +
                    '<td><strong>' + esc(w.name) + '</strong></td>' +
                    '<td><span class="font-mono">' + esc(w.host) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(w.port) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(w.username) + '</span></td>' +
                    '<td>' + authModeBadge(w.auth_mode) + '</td>' +
                    '<td>' + statusBadge(w.status) + '</td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(w.last_seen_at)) + '</span></td>' +
                    '<td style="text-align:right;">' +
                    '<div class="actions-cell" style="justify-content: flex-end;">' +
                    '<button class="btn btn-xs btn-outline" data-action="edit" data-id="' + w.id + '">编辑</button>' +
                    '<button class="btn btn-xs btn-success" data-action="test" data-id="' + w.id + '">测试连接</button>' +
                    '<button class="btn btn-xs btn-primary" data-action="creds" data-id="' + w.id + '">凭证配置</button>' +
                    '<button class="btn btn-xs btn-outline" data-action="install-deps" data-id="' + w.id + '">安装依赖</button>' +
                    '<button class="btn btn-xs btn-danger" data-action="delete" data-id="' + w.id + '">删除</button>' +
                    '</div>' +
                    '</td></tr>';
            }).join('');

            // Wire action buttons
            tbody.querySelectorAll('button[data-action]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var action = this.getAttribute('data-action');
                    var id = this.getAttribute('data-id');
                    if (action === 'edit') showWorkerForm(content, id);
                    else if (action === 'test') doTestWorker(content, id);
                    else if (action === 'creds') showCredentialsForm(content, id);
                    else if (action === 'install-deps') doInstallDeps(content, id);
                    else if (action === 'delete') doDeleteWorker(content, id);
                });
            });
        } catch (err) {
            setMsg(document.getElementById('workers-msg'), '错误: ' + err.message, 'error');
        }
    });

    async function showWorkerForm(content, id) {
        var isEdit = !!id;
        var worker = null;
        if (isEdit) {
            var r = await apiJSON('/workers/' + id);
            if (!r.resp.ok) { alert('加载 Worker 失败: ' + (r.data && r.data.error)); return; }
            worker = r.data;
        }

        var html = '<div class="modal-overlay" id="worker-modal">' +
            '<div class="modal">' +
            '<h3 class="modal-title">' +
            '<span>' + (isEdit ? '编辑 Worker 节点 #' + esc(id) : '接入新 Worker 节点') + '</span>' +
            '<span class="badge badge-muted">' + (isEdit ? '修改配置' : '集群注册') + '</span>' +
            '</h3>' +
            '<form id="worker-form">' +
            (isEdit ? '' :
            '<div class="form-field"><label>从集群节点选择 (可选快捷填充)</label>' +
            '<select id="worker-node-select"><option value="">-- 手动填写或选择集群节点 --</option></select>' +
            '<p class="muted" style="font-size:12px;margin-top:4px;">选中后自动填入节点名称与内网主机地址。</p></div>') +
            '<div class="row">' +
            '<div class="col"><div class="form-field"><label>节点名称</label><input type="text" name="name" placeholder="如 worker-node-01" value="' + esc(worker ? worker.name : '') + '" required></div></div>' +
            '<div class="col"><div class="form-field"><label>SSH 主机 IP / 域名</label><input type="text" name="host" placeholder="192.168.x.x" value="' + esc(worker ? worker.host : '') + '" required></div></div>' +
            '</div>' +
            '<div class="row">' +
            '<div class="col"><div class="form-field"><label>SSH 端口</label><input type="number" name="port" value="' + esc(worker ? worker.port : 22) + '"></div></div>' +
            '<div class="col"><div class="form-field"><label>登录用户名</label><input type="text" name="username" value="' + esc(worker ? worker.username : 'root') + '"></div></div>' +
            '</div>' +
            '<div class="form-field"><label>SSH 密码' + (isEdit ? ' (留空则保持原密码不变)' : ' (可选，与用户名一起用于远程连接)') + '</label><input type="password" name="password" placeholder="留空可在凭证管理中单独设置"></div>' +
            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="worker-cancel">取消</button>' +
            '<button type="submit" class="btn btn-primary">确认保存</button>' +
            '</div>' +
            '<div id="worker-form-msg" class="error-msg"></div>' +
            '</form></div></div>';
        content.insertAdjacentHTML('beforeend', html);

        var modal = document.getElementById('worker-modal');
        document.getElementById('worker-cancel').addEventListener('click', function () { modal.remove(); });

        if (!isEdit) {
            var sel = document.getElementById('worker-node-select');
            apiJSON('/k8s/nodes').then(function (r) {
                if (!r.resp.ok || !Array.isArray(r.data)) return;
                r.data.forEach(function (n) {
                    var opt = document.createElement('option');
                    opt.value = JSON.stringify(n);
                    opt.textContent = n.name + (n.host ? ' (' + n.host + ')' : '') + ' [' + n.role + ']';
                    sel.appendChild(opt);
                });
            }).catch(function () {});
            sel.addEventListener('change', function () {
                if (!sel.value) return;
                try {
                    var n = JSON.parse(sel.value);
                    var f = document.getElementById('worker-form');
                    if (n.name) f.name.value = n.name;
                    if (n.host) f.host.value = n.host;
                } catch (e) {}
            });
        }
        document.getElementById('worker-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var form = e.target;
            var body = {
                name: form.name.value,
                host: form.host.value,
                port: parseInt(form.port.value, 10) || 22,
                username: form.username.value || 'root'
            };
            var msgEl = document.getElementById('worker-form-msg');
            try {
                var r;
                if (isEdit) {
                    r = await apiJSON('/workers/' + id, { method: 'PUT', body: JSON.stringify(body) });
                } else {
                    r = await apiJSON('/workers', { method: 'POST', body: JSON.stringify(body) });
                }
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                var pw = form.password.value;
                if (pw) {
                    var wid = isEdit ? id : (r.data && r.data.id);
                    if (wid) {
                        var pr = await apiJSON('/workers/' + wid + '/credentials/password', { method: 'POST', body: JSON.stringify({ password: pw }) });
                        if (!pr.resp.ok) { setMsg(msgEl, 'Worker 已保存，但密码设置失败: ' + (pr.data && pr.data.error), 'error'); return; }
                    }
                }
                modal.remove();
                handleRoute();
            } catch (err) {
                setMsg(msgEl, '错误: ' + err.message, 'error');
            }
        });
    }

    async function doTestWorker(content, id) {
        try {
            var r = await apiJSON('/workers/' + id + '/test', { method: 'POST' });
            if (r.data && r.data.ok) {
                alert('Worker #' + id + ' SSH 连通测试成功！');
            } else {
                alert('Worker #' + id + ' 连通失败: ' + (r.data && r.data.error || '未知网络错误'));
            }
            handleRoute();
        } catch (err) { alert('错误: ' + err.message); }
    }

    async function doDeleteWorker(content, id) {
        if (!confirm('确认删除 Worker 节点 #' + id + '？\n删除后相关配置将丢失，已有容器需手动核对。')) return;
        try {
            var r = await apiJSON('/workers/' + id, { method: 'DELETE' });
            if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
            handleRoute();
        } catch (err) { alert('错误: ' + err.message); }
    }

    // Credentials form: set private key, set panel password, change root password
    async function showCredentialsForm(content, id) {
        var worker = null;
        try {
            var r = await apiJSON('/workers/' + id);
            if (r.resp.ok) worker = r.data;
        } catch (e) {}

        var html = '<div class="modal-overlay" id="creds-modal">' +
            '<div class="modal" style="max-width: 600px;">' +
            '<h3 class="modal-title">' +
            '<span>Worker #' + esc(id) + ' 安全凭证管理</span>' +
            (worker ? '<span>' + authModeBadge(worker.auth_mode) + '</span>' : '') +
            '</h3>' +
            '<p class="muted mb-2" style="font-size: 12.5px;">全部敏感凭证在落盘前均通过 AES-256 GCM 强加密存储，前端与日志不回显明文。</p>' +

            '<div class="card">' +
            '<div class="section-title">设置 SSH 私钥 (面板控制端)</div>' +
            '<p class="muted mb-1" style="font-size:12px;">用于控制面板免密远程 SSH 纳管该 Worker 节点。</p>' +
            '<form id="set-key-form">' +
            '<div class="form-field"><label>PEM 私钥内容</label><textarea class="font-mono" name="private_key" rows="4" placeholder="-----BEGIN RSA PRIVATE KEY-----&#10;...&#10;-----END RSA PRIVATE KEY-----"></textarea></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">保存私钥</button>' +
            '<div id="set-key-msg" class="error-msg"></div></form></div>' +

            '<div class="card">' +
            '<div class="section-title">设置 SSH 密码 (面板控制端)</div>' +
            '<p class="muted mb-1" style="font-size:12px;">存储在控制面板内部，由面板调度发起 SSH 时使用。</p>' +
            '<form id="set-pw-form">' +
            '<div class="form-field"><label>SSH 访问密码</label><input type="password" name="password" placeholder="请输入远程主机登录密码"></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">保存密码</button>' +
            '<div id="set-pw-msg" class="error-msg"></div></form></div>' +

            '<div class="card">' +
            '<div class="section-title">修改主机 root 密码 (经 SSH 推送修改)</div>' +
            '<p class="muted mb-1" style="font-size:12px;">提交异步任务，通过当前可用 SSH 隧道执行 chpasswd 修改远程 Linux root 密码。</p>' +
            '<form id="root-pw-form">' +
            '<div class="form-field"><label>新 root 密码</label><input type="password" name="password" placeholder="请输入要设置的新 root 密码"></div>' +
            '<button type="submit" class="btn btn-danger btn-sm">确认推送修改 root 密码</button>' +
            '<div id="root-pw-msg" class="error-msg"></div>' +
            '</form></div>' +

            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="creds-cancel">关闭</button>' +
            '</div>' +
            '</div></div>';
        content.insertAdjacentHTML('beforeend', html);

        var modal = document.getElementById('creds-modal');
        document.getElementById('creds-cancel').addEventListener('click', function () { modal.remove(); });

        document.getElementById('set-key-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { private_key: e.target.private_key.value };
            var msgEl = document.getElementById('set-key-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/credentials/private-key', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, '私钥配置已成功保存！', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        document.getElementById('set-pw-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { password: e.target.password.value };
            var msgEl = document.getElementById('set-pw-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/credentials/password', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, '控制端密码已成功保存！', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        document.getElementById('root-pw-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { password: e.target.password.value };
            var msgEl = document.getElementById('root-pw-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/root-password', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                var taskID = r.data && r.data.task_id;
                modal.remove();
                window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    async function doInstallDeps(content, id) {
        if (!confirm('确认经 SSH 在 Worker #' + id + ' 上远程安装 lvm2 与 nfs-utils 依赖包？\n系统将自动创建异步作业并追踪安装进度。')) return;
        try {
            var r = await apiJSON('/workers/' + id + '/install-deps', { method: 'POST' });
            if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
            var taskID = r.data && r.data.task_id;
            window.location.hash = '#/tasks/' + taskID;
        } catch (err) { alert('错误: ' + err.message); }
    }

    // ====================================================================
    // K8S PAGE (Pod-centric port mapping)
    var k8sServices = [];

    registerRoute('/k8s', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">K8s 端口映射编排</h2>' +
            '<p class="page-subtitle">按 Notebook Pod 统一发现并配置 NodePort / ClusterIP 端口映射与配套 NetworkPolicy 隔离策略</p>' +
            '</div>' +
            '<button class="btn btn-outline" id="btn-load-pods">' +
            '<svg width="15" height="15" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/></svg>' +
            '刷新 Pod 状态' +
            '</button>' +
            '</div>' +
            '<div id="pods-msg" class="info-msg"></div>' +
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">Notebook Pod 列表</div>' +
            '<span class="muted" style="font-size:12px;">自动过滤名称包含 notebook 的业务容器</span>' +
            '</div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="pods-table"><thead><tr>' +
            '<th>Pod 名称</th><th>命名空间</th><th>宿主节点</th><th>Pod 状态</th><th>容器 IP</th><th>已有映射数</th><th style="text-align:right;">操作</th>' +
            '</tr></thead><tbody id="pods-tbody"><tr><td colspan="7" class="muted">正在加载 Pod 与 Service 映射...</td></tr></tbody></table>' +
            '</div></div>';

        document.getElementById('btn-load-pods').addEventListener('click', function () { loadPods(content); });
        loadPods(content);
    });

    function servicesForPod(podUid) {
        return k8sServices.filter(function (s) {
            return (s.pods || []).some(function (p) { return p.uid === podUid; });
        });
    }

    async function loadPods(content) {
        var tbody = document.getElementById('pods-tbody');
        var msgEl = document.getElementById('pods-msg');
        tbody.innerHTML = '<tr><td colspan="7" class="muted">正在从 Kubernetes 集群同步资源...</td></tr>';
        try {
            var results = await Promise.all([apiJSON('/k8s/pods'), apiJSON('/k8s/services')]);
            var pr = results[0], sr = results[1];
            if (!pr.resp.ok) { setMsg(msgEl, '错误: ' + (pr.data && pr.data.error), 'error'); tbody.innerHTML = ''; return; }
            k8sServices = (sr.resp.ok && Array.isArray(sr.data)) ? sr.data : [];
            var pods = pr.data || [];
            if (pods.length === 0) { tbody.innerHTML = '<tr><td colspan="7" class="muted">当前集群未检测到符合名称规则的 notebook Pod 实例。</td></tr>'; return; }
            tbody.innerHTML = pods.map(function (p) {
                var cnt = servicesForPod(p.uid).length;
                return '<tr>' +
                    '<td><strong>' + esc(p.name) + '</strong></td>' +
                    '<td><span class="badge badge-muted font-mono">' + esc(p.namespace) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(p.node) + '</span></td>' +
                    '<td>' + statusBadge(p.status) + '</td>' +
                    '<td><span class="font-mono">' + esc((p.ips || []).join(', ')) + '</span></td>' +
                    '<td>' + (cnt > 0 ? '<span class="badge badge-success">' + cnt + ' 条映射</span>' : '<span class="muted">-</span>') + '</td>' +
                    '<td style="text-align:right;"><button class="btn btn-sm btn-primary" data-pod=\'' + esc(JSON.stringify(p)) + '\'>配置端口映射</button></td>' +
                    '</tr>';
            }).join('');
            tbody.querySelectorAll('button[data-pod]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var pod = JSON.parse(this.getAttribute('data-pod'));
                    showPortMappingForm(content, pod);
                });
            });
        } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
    }

    async function showPortMappingForm(content, pod) {
        var html = '<div class="modal-overlay" id="port-modal"><div class="modal" style="max-width: 680px;">' +
            '<h3 class="modal-title">' +
            '<span>端口映射管理</span>' +
            '<span class="badge badge-primary font-mono">' + esc(pod.name) + '</span>' +
            '</h3>' +
            '<div class="card"><div class="section-title">该 Pod 关联的 Service 映射</div>' +
            '<p class="muted mb-2" style="font-size:12px;">包含全部匹配该 Pod 的 Service。<span class="badge badge-success">本面板创建</span> 可执行清理，<span class="badge badge-muted">外部创建</span> 为集群固有只读。</p>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="pod-svc-table"><thead><tr><th>Service 名称</th><th>类型</th><th>NodePort</th><th>Pod 目标端口</th><th>归属</th><th style="text-align:right;">操作</th></tr></thead>' +
            '<tbody id="pod-existing-tbody"><tr><td colspan="6" class="muted">加载中...</td></tr></tbody></table></div></div>' +
            '<div class="card mt-2"><div class="section-title">新增端口映射规则</div>' +
            '<p class="muted mb-2" style="font-size:12px;">系统将自动生成对应 K8s Service 并联动下发 NetworkPolicy 允许外部流量通过。</p>' +
            '<form id="port-form">' +
            '<div class="row">' +
            '<div class="col"><div class="form-field"><label>目标命名空间</label><input type="text" name="namespace" value="' + esc(pod.namespace) + '" readonly></div></div>' +
            '<div class="col"><div class="form-field"><label>Service 暴露模式</label><select name="type"><option value="NodePort">NodePort (主机端口映射)</option><option value="ClusterIP">ClusterIP (集群内网互通)</option></select></div></div>' +
            '</div>' +
            '<div class="form-field">' +
            '<label>映射端口 (逗号分隔，如 31555、8080:80 或 显式指定NodePort 8080:80:31555)</label>' +
            '<input type="text" name="ports" placeholder="如 31555 或 8080:80 或 8080:80:31555" required>' +
            '<p class="muted mt-1" style="font-size:12px;">格式说明：端口（如 31555，内外同端口且由K8s分配NodePort）、服务端口:容器端口（如 8080:80）、服务端口:容器端口:NodePort（如 8080:80:31555，指定NodePort 30000-32767）。</p>' +
            '</div>' +
            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="port-cancel">取消</button>' +
            '<button type="submit" class="btn btn-primary">立即创建映射</button>' +
            '</div>' +
            '<div id="port-form-msg" class="error-msg"></div></form></div></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('port-modal');
        document.getElementById('port-cancel').addEventListener('click', function () { modal.remove(); });
        renderExistingMappings(modal, pod);
        document.getElementById('port-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var f = e.target;
            var msgEl = document.getElementById('port-form-msg');
            var rawList = (f.ports.value || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
            if (rawList.length === 0) {
                setMsg(msgEl, '请输入映射端口', 'error');
                return;
            }
            var parseErr = null;
            var ports = rawList.map(function (p) {
                var parts = p.split(':').map(function (x) { return x.trim(); });
                var port = parseInt(parts[0], 10);
                var targetPort = port;
                var nodePort = 0;
                if (parts.length === 2) {
                    targetPort = parseInt(parts[1], 10);
                } else if (parts.length >= 3) {
                    targetPort = parseInt(parts[1], 10);
                    nodePort = parseInt(parts[2], 10);
                }
                if (isNaN(port) || port <= 0 || isNaN(targetPort) || targetPort <= 0 || isNaN(nodePort) || nodePort < 0) {
                    parseErr = '端口输入有误，端口号必须为正整数';
                }
                if (nodePort > 0 && (nodePort < 30000 || nodePort > 32767)) {
                    parseErr = '外部 NodePort (' + nodePort + ') 超出 Kubernetes 默认端口范围 (30000-32767)';
                }
                return { port: port, target_port: targetPort, node_port: nodePort, protocol: 'TCP' };
            });
            if (parseErr) {
                setMsg(msgEl, '错误: ' + parseErr, 'error');
                return;
            }
            var body = {
                namespace: pod.namespace, pod_name: pod.name, pod_uid: pod.uid,
                selector: pod.labels || {}, type: f.type.value, ports: ports
            };
            try {
                var r = await apiJSON('/k8s/services', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    function renderExistingMappings(scope, pod) {
        var el = scope.querySelector('#pod-existing-tbody');
        if (!el) return;
        var mine = servicesForPod(pod.uid);
        if (mine.length === 0) {
            el.innerHTML = '<tr><td colspan="6" class="muted">当前 Pod 尚无关联端口映射。</td></tr>';
            return;
        }
        mine.sort(function (a, b) { return (a.managed === b.managed) ? 0 : (a.managed ? -1 : 1); });
        el.innerHTML = mine.map(function (s) {
            var ports = s.ports || [];
            var extPorts = ports.length ? ports.map(function (p) { return (p.node_port || '-') + '/' + (p.protocol || 'TCP'); }).join(', ') : '-';
            var intPorts = ports.length ? ports.map(function (p) { return p.port + '->' + (p.target_port || p.port); }).join(', ') : '-';
            var srcBadge = s.managed ? '<span class="badge badge-success">本面板</span>' : '<span class="badge badge-muted">外部</span>';
            var action = s.managed
                ? '<button class="btn btn-xs btn-danger" data-name="' + esc(s.name) + '" data-ns="' + esc(s.namespace) + '">删除</button>'
                : '<span class="muted" style="font-size:12px;">只读</span>';
            return '<tr><td><span class="font-mono">' + esc(s.name) + '</span></td><td>' + esc(s.type) + '</td><td><span class="font-mono">' + esc(extPorts) + '</span></td><td><span class="font-mono">' + esc(intPorts) + '</span></td><td>' + srcBadge + '</td>' +
                '<td style="text-align:right;">' + action + '</td></tr>';
        }).join('');
        el.querySelectorAll('button[data-name]').forEach(function (btn) {
            btn.addEventListener('click', async function () {
                if (!confirm('确认删除 Service ' + this.getAttribute('data-name') + '？\n删除将释放对应的 NodePort 端口并清理 NetworkPolicy 规则。')) return;
                var name = this.getAttribute('data-name');
                var ns2 = this.getAttribute('data-ns');
                try {
                    var r = await apiJSON('/k8s/services/' + encodeURIComponent(name) + '?namespace=' + encodeURIComponent(ns2), { method: 'DELETE' });
                    if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
                    var taskID = r.data && r.data.task_id;
                    if (taskID) window.location.hash = '#/tasks/' + taskID;
                } catch (err) { alert('错误: ' + err.message); }
            });
        });
    }

    // ====================================================================
    // STORAGE PAGE
    // ====================================================================

    registerRoute('/storage', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">NFS 存储与 LVM 编排</h2>' +
            '<p class="page-subtitle">节点磁盘资源发现、卷组 (VG) 与逻辑卷 (LV) 容量伸缩、NFS 共享目录生命周期管理</p>' +
            '</div>' +
            '</div>' +
            '<div class="card">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">目标 Worker 存储节点</div>' +
            '<span class="muted" style="font-size:12px;">请先选择需要查看或编排存储的计算 Worker</span>' +
            '</div>' +
            '<div class="form-field"><label>选择 Worker 节点</label><select id="st-worker-select"><option value="">-- 请选择 Worker 节点 --</option></select></div>' +
            '<div id="st-inv-msg" class="info-msg"></div>' +
            '</div>' +
            // Block A: VG pool management
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">存储池 (VG) 管理</div>' +
            '<div style="display:flex;align-items:center;gap:12px;">' +
            '<span id="st-vg-summary" class="muted" style="font-size:12.5px;"></span>' +
            '<button class="btn btn-primary btn-sm" id="btn-init-vg" disabled>初始化 VG 池 (从未挂载裸盘)</button>' +
            '</div></div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="st-vg-table"><thead><tr><th>VG 卷组名称</th><th>总容量</th><th>剩余可用容量</th></tr></thead>' +
            '<tbody id="st-vg-tbody"><tr><td colspan="3" class="muted">请在上方选择 Worker 节点以获取 VG 存储池状态。</td></tr></tbody></table>' +
            '</div></div>' +
            // Block B: LV management
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">逻辑卷 (LV) 管理</div>' +
            '<span class="muted" style="font-size:12px;">包含全部底层识别的 LV 卷，支持动态扩容、缩容及卸载释放空间</span>' +
            '</div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="st-lv-table"><thead><tr><th>LV 卷名称</th><th>所属 VG</th><th>容量 (GB)</th><th>挂载点</th><th>文件系统</th><th style="text-align:right;">操作</th></tr></thead>' +
            '<tbody id="st-lv-tbody"><tr><td colspan="6" class="muted">请先在上方选择 Worker 节点。</td></tr></tbody></table>' +
            '</div></div>' +
            // Block C: create NFS share
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">新建 NFS 共享卷</div>' +
            '<span class="muted" style="font-size:12px;">自动格式化、持久化挂载至 fstab 并配置 /etc/exports 导出共享</span>' +
            '</div>' +
            '<div class="row">' +
            '<div class="col"><div class="form-field"><label>存储池 (Volume Group)</label><select id="st-vg-select" disabled><option value="">-- 先选择 Worker --</option></select><span id="st-vg-free" class="muted" style="font-size:12px;margin-top:4px;display:inline-block;"></span></div></div>' +
            '<div class="col"><div class="form-field"><label>分配大小 (GB)</label><input type="number" id="st-nfs-size" placeholder="例如 200" min="1"></div></div>' +
            '</div>' +
            '<button class="btn btn-primary" id="btn-nfs-create" disabled>创建并导出 NFS 共享</button>' +
            '<div id="st-nfs-msg" class="error-msg"></div>' +
            '</div>' +
            // Block D: NFS shares list
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">NFS 共享列表 (最近编排记录)</div>' +
            '<span class="muted" style="font-size:12px;">由控制面板调度的持久化 NFS 共享目录状态</span>' +
            '</div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="st-storage-table"><thead><tr><th>任务 ID</th><th>编排类型</th><th>目标 Worker</th><th>状态</th><th>发起时间</th><th>完成时间</th><th style="text-align:right;">操作</th></tr></thead>' +
            '<tbody id="st-storage-tbody"><tr><td colspan="7" class="muted">正在加载历史存储共享任务...</td></tr></tbody></table>' +
            '</div></div>';

        var wsel = document.getElementById('st-worker-select');
        var lastInventory = null;
        var workersMap = {};

        try {
            var r = await apiJSON('/workers');
            if (r.resp.ok && Array.isArray(r.data)) {
                r.data.forEach(function (w) {
                    workersMap[w.id] = w;
                    var o = document.createElement('option');
                    o.value = w.id;
                    o.textContent = w.name + ' (' + w.host + ')';
                    wsel.appendChild(o);
                });
            }
        } catch (e) {}

        async function loadInventory(wid) {
            var invMsg = document.getElementById('st-inv-msg');
            var vgTbody = document.getElementById('st-vg-tbody');
            var lvTbody = document.getElementById('st-lv-tbody');
            var vsel = document.getElementById('st-vg-select');
            var vfree = document.getElementById('st-vg-free');
            var btnInit = document.getElementById('btn-init-vg');
            var btnNfs = document.getElementById('btn-nfs-create');
            var summary = document.getElementById('st-vg-summary');

            btnInit.disabled = true; btnNfs.disabled = true; vsel.disabled = true;
            vsel.innerHTML = '<option value="">正在分析节点存储...</option>';
            vfree.textContent = ''; summary.textContent = '';
            vgTbody.innerHTML = '<tr><td colspan="3" class="muted">正在获取存储池 (VG) 数据...</td></tr>';
            lvTbody.innerHTML = '<tr><td colspan="6" class="muted">正在获取逻辑卷 (LV) 数据...</td></tr>';
            try {
                var r = await apiJSON('/storage/inventory?worker_id=' + encodeURIComponent(wid));
                if (!r.resp.ok) {
                    var err = (r.data && r.data.error) || '加载失败';
                    setMsg(invMsg, '加载存储清单失败: ' + err + ' (若未安装 lvm2/nfs,请先在 Worker 页面点击「安装依赖」)', 'error');
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">存储池清单获取失败</td></tr>';
                    lvTbody.innerHTML = '<tr><td colspan="6" class="muted">逻辑卷清单获取失败</td></tr>';
                    vsel.innerHTML = '<option value="">-- 加载失败 --</option>';
                    return;
                }
                setMsg(invMsg, '', 'info');
                var inv = r.data || { vgs: [], lvs: [], unused_disks: [] };
                lastInventory = inv;

                var vgs = inv.vgs || [];
                if (vgs.length === 0) {
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">当前节点未初始化任何 VG 卷组。可从未挂载裸盘新建存储池。</td></tr>';
                } else {
                    vgTbody.innerHTML = vgs.map(function (v) {
                        return '<tr><td><strong>' + esc(v.name) + '</strong></td><td><span class="font-mono">' + esc(v.vsize) + '</span></td><td><span class="badge badge-success font-mono">' + esc(v.vfree) + ' (' + (v.free_gb || 0).toFixed(1) + ' GB 可用)</span></td></tr>';
                    }).join('');
                }

                var disks = inv.unused_disks || [];
                if (disks.length > 0) {
                    btnInit.disabled = false;
                    summary.textContent = '发现 ' + disks.length + ' 块未挂载裸盘可供初始化。';
                } else {
                    summary.textContent = '未检测到可用未挂载裸盘。';
                }

                var lvs = inv.lvs || [];
                if (lvs.length === 0) {
                    lvTbody.innerHTML = '<tr><td colspan="6" class="muted">该节点当前无逻辑卷。</td></tr>';
                } else {
                    lvTbody.innerHTML = lvs.map(function (lv) {
                        var data = JSON.stringify({ vg: lv.vg_name, name: lv.name, size: lv.size_gb, mp: lv.mount_point, fs: lv.fs_type });
                        var platBtn = lv.mount_point
                            ? '<button class="btn btn-xs btn-outline" data-act="platform" data-lv=\'' + esc(data) + '\'>平台参数</button>'
                            : '';
                        return '<tr>' +
                            '<td><strong>' + esc(lv.name) + '</strong></td>' +
                            '<td><span class="font-mono">' + esc(lv.vg_name) + '</span></td>' +
                            '<td><span class="font-mono">' + (lv.size_gb || 0).toFixed(1) + ' GB</span></td>' +
                            '<td><span class="font-mono">' + esc(lv.mount_point || '-') + '</span></td>' +
                            '<td><span class="badge badge-muted">' + esc(lv.fs_type || '-') + '</span></td>' +
                            '<td style="text-align:right;">' +
                            '<div class="actions-cell" style="justify-content: flex-end;">' +
                            platBtn +
                            '<button class="btn btn-xs btn-outline" data-act="grow" data-lv=\'' + esc(data) + '\'>扩容</button>' +
                            '<button class="btn btn-xs btn-outline" data-act="shrink" data-lv=\'' + esc(data) + '\'>缩容</button>' +
                            '<button class="btn btn-xs btn-danger" data-act="delete" data-lv=\'' + esc(data) + '\'>删除释放</button>' +
                            '</div>' +
                            '</td></tr>';
                    }).join('');
                    lvTbody.querySelectorAll('button[data-act]').forEach(function (btn) {
                        btn.addEventListener('click', function () {
                            var lv = JSON.parse(this.getAttribute('data-lv'));
                            var act = this.getAttribute('data-act');
                            if (act === 'platform') {
                                var curWorker = workersMap[wid] || {};
                                showPlatformRegistrationModal(content, {
                                    name: 'nfs-' + lv.name,
                                    service_address: curWorker.host || '127.0.0.1',
                                    path: lv.mp || '/data02/notebook_nfs',
                                    size_gb: lv.size,
                                    workspace_uuid: ''
                                });
                            } else if (act === 'delete') {
                                doDeleteLV(content, wid, lv);
                            } else {
                                showResizeLVForm(content, wid, lv, act);
                            }
                        });
                    });
                }

                if (vgs.length === 0) {
                    vsel.innerHTML = '<option value="">-- 该节点暂无可用 VG --</option>';
                } else {
                    vsel.innerHTML = '';
                    vgs.forEach(function (v) {
                        var o = document.createElement('option');
                        o.value = v.name;
                        o.textContent = v.name + ' (剩余 ' + (v.free_gb || 0).toFixed(1) + 'G / 共 ' + v.vsize + ')';
                        vsel.appendChild(o);
                    });
                    vsel.disabled = false; btnNfs.disabled = false;
                    vfree.textContent = '可用容量: ' + (vgs[0].free_gb || 0).toFixed(1) + ' GB';
                    vsel.onchange = function () {
                        var cur = vgs.find(function (x) { return x.name === vsel.value; });
                        vfree.textContent = cur ? '可用容量: ' + (cur.free_gb || 0).toFixed(1) + ' GB' : '';
                    };
                }
            } catch (err) {
                setMsg(invMsg, '加载存储清单出错: ' + err.message, 'error');
            }
        }

        wsel.addEventListener('change', function () {
            var wid = wsel.value;
            if (!wid) { return; }
            loadInventory(wid);
        });

        document.getElementById('btn-init-vg').addEventListener('click', function () {
            if (!wsel.value || !lastInventory) return;
            showInitVGForm(content, parseInt(wsel.value, 10), lastInventory.unused_disks || [], function () {
                loadInventory(wsel.value);
            });
        });

        document.getElementById('btn-nfs-create').addEventListener('click', async function () {
            var wid = parseInt(wsel.value, 10);
            var vg = document.getElementById('st-vg-select').value;
            var size = parseInt(document.getElementById('st-nfs-size').value, 10);
            var msgEl = document.getElementById('st-nfs-msg');
            if (!wid || !vg || !size) { setMsg(msgEl, '请选择目标 Worker、存储卷组并输入容量 (GB)', 'error'); return; }
            var lv = 'lv_nb_' + Date.now().toString(36);
            var mp = '/data02/nfs_' + lv;
            try {
                var r = await apiJSON('/storage/provision', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: vg, lv_name: lv, size_gb: size, fs_type: 'ext4', mount_point: mp }) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                window.location.hash = '#/tasks/' + (r.data && r.data.task_id);
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        try {
            var r2 = await apiJSON('/storage');
            var tbody = document.getElementById('st-storage-tbody');
            if (!r2.resp.ok) { tbody.innerHTML = '<tr><td colspan="7" class="muted">加载失败</td></tr>'; return; }
            var tasks = r2.data || [];
            var shares = tasks.filter(function (t) { return t.type === 'storage_provision_nfs' && t.status === 'succeeded'; });
            if (shares.length === 0) { tbody.innerHTML = '<tr><td colspan="7" class="muted">暂无已完成创建的 NFS 共享任务记录。</td></tr>'; return; }
            tbody.innerHTML = shares.map(function (t) {
                return '<tr>' +
                    '<td><span class="badge-mono font-mono">' + esc(t.id) + '</span></td>' +
                    '<td><span class="badge badge-muted font-mono">' + esc(t.type) + '</span></td>' +
                    '<td><span class="font-mono">Worker #' + esc(t.target_id) + '</span></td>' +
                    '<td>' + statusBadge(t.status) + '</td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(t.created_at)) + '</span></td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(t.finished_at)) + '</span></td>' +
                    '<td style="text-align:right;">' +
                    '<div class="actions-cell" style="justify-content: flex-end;">' +
                    '<button class="btn btn-xs btn-outline" data-reg-task=\'' + esc(JSON.stringify(t)) + '\'>平台参数</button>' +
                    '<button class="btn btn-xs btn-danger" data-task=\'' + esc(JSON.stringify(t)) + '\'>回收释放</button>' +
                    '</div>' +
                    '</td></tr>';
            }).join('');
            tbody.querySelectorAll('button[data-reg-task]').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var t = JSON.parse(this.getAttribute('data-reg-task'));
                    var curWorker = workersMap[t.target_id] || {};
                    showPlatformRegistrationModal(content, {
                        name: 'nfs-task-' + t.id,
                        service_address: curWorker.host || '127.0.0.1',
                        path: '/data02/notebook_nfs',
                        workspace_uuid: ''
                    });
                });
            });
            tbody.querySelectorAll('button[data-task]').forEach(function (btn) {
                btn.addEventListener('click', async function () {
                    var t = JSON.parse(this.getAttribute('data-task'));
                    if (!confirm('确认回收该 NFS 共享 (任务 #' + t.id + ')？\n空间将安全归还底层 VG 卷组。')) return;
                    try {
                        var rr = await apiJSON('/storage/reclaim', { method: 'POST', body: JSON.stringify({ task_id: t.id }) });
                        if (!rr.resp.ok) { alert('错误: ' + (rr.data && rr.data.error)); return; }
                        window.location.hash = '#/tasks/' + (rr.data && rr.data.task_id);
                    } catch (err) { alert('错误: ' + err.message); }
                });
            });
        } catch (err) {}
    });

    function genUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    function showPlatformRegistrationModal(content, info) {
        var uuid = info.uuid || genUUID();
        var name = info.name || ('nfs-' + (info.size_gb ? info.size_gb + 'g' : 'vol'));
        var path = info.path || '/data02/notebook_nfs';
        var addr = info.service_address || '10.0.0.1';
        var ws = info.workspace_uuid || '';

        function renderSQL(u, n, p, a, w) {
            return "INSERT INTO esx_tai.file_storage (uuid, name, path, service_address, workspace_uuid, type)\n" +
                "VALUES ('" + u + "', '" + n + "', '" + p + "', '" + a + "', '" + (w || '<workspace_uuid>') + "', 'EnterprtseAllocate');";
        }

        var html = '<div class="modal-overlay" id="plat-modal"><div class="modal" style="max-width: 680px;">' +
            '<h3 class="modal-title">' +
            '<span>平台存储手动录入参考</span>' +
            '<span class="badge badge-primary font-mono">' + esc(name) + '</span>' +
            '</h3>' +
            '<p class="muted mb-2" style="font-size:12.5px;">该 NFS 共享已由底层系统格式化并持久化导出。由于平台要求在控制台或数据库手动录入，可直接参考以下配置字段或一键复制 SQL 录入：</p>' +
            '<div class="card" style="background:#f8fafc;border:1px solid #e2e8f0;padding:12px;margin-bottom:12px;">' +
            '<div class="row" style="row-gap:8px;">' +
            '<div class="col"><span class="muted" style="font-size:12px;">存储 UUID:</span><br><code class="font-mono" id="pl-uuid-val">' + esc(uuid) + '</code></div>' +
            '<div class="col"><span class="muted" style="font-size:12px;">存储名称 (name):</span><br><strong id="pl-name-val">' + esc(name) + '</strong></div>' +
            '</div>' +
            '<div class="row mt-1" style="row-gap:8px;">' +
            '<div class="col"><span class="muted" style="font-size:12px;">NFS 服务地址 (service_address):</span><br><span class="badge badge-muted font-mono" id="pl-addr-val">' + esc(addr) + '</span></div>' +
            '<div class="col"><span class="muted" style="font-size:12px;">共享挂载路径 (path):</span><br><span class="font-mono" id="pl-path-val">' + esc(path) + '</span></div>' +
            '</div>' +
            '<div class="row mt-1" style="row-gap:8px;">' +
            '<div class="col"><span class="muted" style="font-size:12px;">存储类型 (type):</span><br><span class="badge badge-success font-mono">EnterprtseAllocate</span></div>' +
            '<div class="col"><div class="form-field" style="margin-bottom:0;"><label style="font-size:12px;">所属工作区 UUID (workspace_uuid)</label><input type="text" id="pl-ws-input" value="' + esc(ws) + '" placeholder="如 ws-d8t5nq1uma3bg0ocu5cg" style="padding:4px 8px;font-size:12px;"></div></div>' +
            '</div>' +
            '</div>' +
            '<div class="form-field"><label>平台注册 SQL 参考语句 (esx_tai.file_storage)</label>' +
            '<textarea id="pl-sql-box" class="font-mono" readonly style="width:100%;height:85px;font-size:12px;padding:8px;background:#0f172a;color:#f8fafc;border-radius:6px;resize:none;">' + esc(renderSQL(uuid, name, path, addr, ws)) + '</textarea>' +
            '</div>' +
            '<div class="row mt-2" style="justify-content: space-between; align-items: center;">' +
            '<div><span id="pl-copy-msg" class="text-success" style="font-size:13px;font-weight:600;"></span></div>' +
            '<div style="display:flex;gap:8px;">' +
            '<button type="button" class="btn btn-outline" id="pl-cancel">关闭</button>' +
            '<button type="button" class="btn btn-primary" id="pl-copy-sql">一键复制 SQL</button>' +
            '</div>' +
            '</div></div></div>';

        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('plat-modal');
        document.getElementById('pl-cancel').addEventListener('click', function () { modal.remove(); });
        var wsInput = document.getElementById('pl-ws-input');
        var sqlBox = document.getElementById('pl-sql-box');
        var copyBtn = document.getElementById('pl-copy-sql');
        var copyMsg = document.getElementById('pl-copy-msg');

        wsInput.addEventListener('input', function () {
            sqlBox.value = renderSQL(uuid, name, path, addr, wsInput.value.trim());
        });

        copyBtn.addEventListener('click', function () {
            var text = sqlBox.value;
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(function () {
                    copyMsg.textContent = '✓ SQL 已成功复制到剪贴板！';
                    setTimeout(function () { copyMsg.textContent = ''; }, 3000);
                }).catch(function () {
                    sqlBox.select();
                    document.execCommand('copy');
                    copyMsg.textContent = '✓ SQL 已成功复制到剪贴板！';
                    setTimeout(function () { copyMsg.textContent = ''; }, 3000);
                });
            } else {
                sqlBox.select();
                document.execCommand('copy');
                copyMsg.textContent = '✓ SQL 已成功复制到剪贴板！';
                setTimeout(function () { copyMsg.textContent = ''; }, 3000);
            }
        });
    }

    async function showInitVGForm(content, wid, disks, onDone) {
        if (!disks || disks.length === 0) { alert('该节点没有可用未挂载裸盘用于创建 VG 存储池。'); return; }
        function vgFor(disk, prefix) { return prefix + '_' + disk.split('/').pop(); }
        function renderDiskRows(prefix) {
            return disks.map(function (d) {
                return '<label style="display:flex;align-items:center;gap:8px;padding:8px 12px;background:#f8fafc;border:1px solid #e2e8f0;border-radius:6px;margin:6px 0;cursor:pointer;">' +
                    '<input type="checkbox" data-disk="' + esc(d.name) + '" checked style="width:auto;"> ' +
                    '<span class="font-mono" style="font-weight:600;">' + esc(d.name) + '</span> ' +
                    '<span class="badge badge-muted">' + (d.size_gb || 0).toFixed(1) + ' GB</span> ' +
                    '<span class="muted" style="font-size:12px;">&rarr; 卷组名 <strong>' + esc(vgFor(d.name, prefix)) + '</strong></span>' +
                    '</label>';
            }).join('');
        }
        var html = '<div class="modal-overlay" id="vg-modal"><div class="modal" style="max-width: 600px;">' +
            '<h3 class="modal-title">' +
            '<span>初始化 VG 存储池</span>' +
            '<span class="badge badge-primary">独立卷组模式</span>' +
            '</h3>' +
            '<p class="muted mb-2" style="font-size:12.5px;">系统将为选中的每块盘独立建立单盘 VG（命名为 <code>前缀_盘符</code>），避免跨不同扇区格式磁盘合并带来的兼容性问题。<b>操作将格式化目标磁盘，请确认无有用数据。</b></p>' +
            '<div class="form-field"><label>VG 命名统一前缀</label><input type="text" id="vg-name-input" value="vg_data"></div>' +
            '<div class="form-field"><label>待初始化未挂载裸盘列表</label><div id="vg-disk-list">' + renderDiskRows('vg_data') + '</div></div>' +
            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="vg-cancel">取消</button>' +
            '<button type="button" class="btn btn-primary" id="vg-create-btn">确认格式化并初始化</button>' +
            '</div>' +
            '<div id="vg-msg" class="error-msg"></div></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('vg-modal');
        var nameInput = document.getElementById('vg-name-input');
        nameInput.addEventListener('input', function () {
            document.getElementById('vg-disk-list').innerHTML = renderDiskRows(nameInput.value.trim() || 'vg_data');
        });
        document.getElementById('vg-cancel').addEventListener('click', function () { modal.remove(); });
        document.getElementById('vg-create-btn').addEventListener('click', async function () {
            var vgName = nameInput.value.trim();
            var chosen = Array.from(modal.querySelectorAll('input[data-disk]:checked')).map(function (c) { return c.getAttribute('data-disk'); });
            var msgEl = document.getElementById('vg-msg');
            if (!vgName) { setMsg(msgEl, '请输入 VG 名称前缀', 'error'); return; }
            if (chosen.length === 0) { setMsg(msgEl, '请至少勾选一块磁盘', 'error'); return; }
            try {
                var r = await apiJSON('/storage/vg', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: vgName, disks: chosen }) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
                else if (onDone) onDone();
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    async function showResizeLVForm(content, wid, lv, action) {
        var isGrow = action === 'grow';
        var html = '<div class="modal-overlay" id="rsz-modal"><div class="modal">' +
            '<h3 class="modal-title">' +
            '<span>' + (isGrow ? '动态扩容' : '缩减容量') + ' 逻辑卷</span>' +
            '<span class="badge badge-primary font-mono">' + esc(lv.name) + '</span>' +
            '</h3>' +
            '<p class="muted mb-2">当前大小 <strong>' + (lv.size || 0).toFixed(1) + ' GB</strong>，底层文件系统 <code>' + esc(lv.fs || 'ext4') + '</code>。</p>' +
            '<div class="form-field"><label>容量调整步长 (GB)</label><input type="number" id="rsz-delta" placeholder="请输入正整数如 50" min="1"></div>' +
            (isGrow ? '' : '<p class="muted mb-2" style="font-size:12px;color:#dc2626;">提示：缩减容量会先压缩文件系统再收缩 LV。<b>XFS 文件系统不支持缩容，ext4 缩容存在数据风险，请务必提前备份。</b></p>') +
            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="rsz-cancel">取消</button>' +
            '<button type="button" class="btn ' + (isGrow ? 'btn-primary' : 'btn-danger') + '" id="rsz-go">' + (isGrow ? '确认扩容' : '确认缩容') + '</button>' +
            '</div>' +
            '<div id="rsz-msg" class="error-msg"></div></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('rsz-modal');
        document.getElementById('rsz-cancel').addEventListener('click', function () { modal.remove(); });
        document.getElementById('rsz-go').addEventListener('click', async function () {
            var delta = parseInt(document.getElementById('rsz-delta').value, 10);
            var msgEl = document.getElementById('rsz-msg');
            if (!delta || delta <= 0) { setMsg(msgEl, '请输入有效的正整数 GB 容量', 'error'); return; }
            try {
                var r = await apiJSON('/storage/lv/resize', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: lv.vg, lv_name: lv.name, action: action, delta_gb: delta }) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                window.location.hash = '#/tasks/' + (r.data && r.data.task_id);
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    async function doDeleteLV(content, wid, lv) {
        var detail = 'LV ' + lv.vg + '/' + lv.name + ' (' + (lv.size || 0).toFixed(1) + ' GB' + (lv.mp ? ', 挂载于 ' + lv.mp : ', 未挂载') + ')';
        if (!confirm('确认删除 ' + detail + '？\n系统将自动先卸载并清理 /etc/exports、/etc/fstab, 再执行 lvremove 释放空间。\n该操作不可撤销！')) return;
        try {
            var r = await apiJSON('/storage/lv/delete', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: lv.vg, lv_name: lv.name }) });
            if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
            window.location.hash = '#/tasks/' + (r.data && r.data.task_id);
        } catch (err) { alert('错误: ' + err.message); }
    }

    // ====================================================================
    // TASKS PAGE (list + detail + SSE)
    // ====================================================================

    registerRoute('/tasks', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">系统任务作业</h2>' +
            '<p class="page-subtitle">查看所有由控制平面发起的异步编排作业状态与执行审计流水</p>' +
            '</div>' +
            '</div>' +
            '<div class="table-responsive mt-2">' +
            '<table class="data-table" id="tasks-table"><thead><tr>' +
            '<th>任务 ID</th><th>作业类型</th><th>目标资源</th><th>状态</th><th>错误摘要</th><th>创建时间</th><th>完成时间</th>' +
            '</tr></thead><tbody id="tasks-tbody"><tr><td colspan="7" class="muted">正在加载任务列表...</td></tr></tbody></table>' +
            '</div>';

        try {
            var r = await apiJSON('/tasks');
            if (!r.resp.ok) { return; }
            var tasks = r.data || [];
            var tbody = document.getElementById('tasks-tbody');
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="muted">当前系统暂无执行任务。</td></tr>';
                return;
            }
            tbody.innerHTML = tasks.map(function (t) {
                return '<tr style="cursor:pointer" data-href="#/tasks/' + t.id + '">' +
                    '<td><span class="badge-mono font-mono">' + esc(t.id) + '</span></td>' +
                    '<td><span class="badge badge-muted font-mono">' + esc(t.type) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(t.target_kind) + '/' + esc(t.target_id) + '</span></td>' +
                    '<td>' + statusBadge(t.status) + '</td>' +
                    '<td>' + esc(t.error ? (t.error.length > 50 ? t.error.substring(0, 50) + '...' : t.error) : '-') + '</td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(t.created_at)) + '</span></td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(t.finished_at)) + '</span></td>' +
                    '</tr>';
            }).join('');
            tbody.querySelectorAll('tr[data-href]').forEach(function (tr) {
                tr.addEventListener('click', function () { window.location.hash = this.getAttribute('data-href'); });
            });
        } catch (err) {}
    });

    var currentSSE = null;
    var stepsData = {};

    function closeSSE() {
        if (currentSSE) { currentSSE.close(); currentSSE = null; }
    }

    registerRoute('/tasks/', async function (content, hash) {
        var id = hash.split('/')[2];
        closeSSE();
        stepsData = {};

        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">' +
            '<span>任务 #' + esc(id) + ' 执行详情</span>' +
            '</h2>' +
            '<p class="page-subtitle">Server-Sent Events (SSE) 实时长连接流式日志监听</p>' +
            '</div>' +
            '<a href="#/tasks" class="btn btn-outline btn-sm">&larr; 返回任务列表</a>' +
            '</div>' +
            '<div class="card" id="task-info"><p class="muted">正在获取作业元数据...</p></div>' +
            '<div class="card">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">执行步骤与控制台输出</div>' +
            '<span class="badge badge-running"><span class="badge-dot"></span>SSE 实时通信中</span>' +
            '</div>' +
            '<div id="steps-container"></div></div>' +
            '<div id="task-error" class="error-msg"></div>';

        try {
            var r = await apiJSON('/tasks/' + id);
            if (!r.resp.ok) {
                document.getElementById('task-info').innerHTML = '<p class="error-msg">未找到指定任务信息。</p>';
                return;
            }
            var result = r.data;
            var task = result.task || result;
            var steps = result.steps || [];

            renderTaskInfo(task);
            steps.forEach(function (s) { stepsData[s.seq] = s; });
            renderStepsFromCache();

            if (task.status === 'pending' || task.status === 'running') {
                subscribeSSE(id);
            }
        } catch (err) {
            document.getElementById('task-error').textContent = '获取任务详情失败: ' + err.message;
        }
    });

    function renderTaskInfo(task) {
        var el = document.getElementById('task-info');
        if (!el) return;
        el.innerHTML = '<div class="row" style="row-gap: 16px;">' +
            '<div class="col" style="min-width:200px;">' +
            '<span class="muted" style="font-size:12px;display:block;margin-bottom:2px;">任务作业 ID</span>' +
            '<span class="font-mono" style="font-weight:700;font-size:15px;">#' + esc(task.id) + '</span>' +
            '</div>' +
            '<div class="col" style="min-width:200px;">' +
            '<span class="muted" style="font-size:12px;display:block;margin-bottom:2px;">作业类型</span>' +
            '<span class="badge badge-muted font-mono">' + esc(task.type) + '</span>' +
            '</div>' +
            '<div class="col" style="min-width:200px;">' +
            '<span class="muted" style="font-size:12px;display:block;margin-bottom:2px;">目标资源</span>' +
            '<span class="font-mono">' + esc(task.target_kind) + '/' + esc(task.target_id) + '</span>' +
            '</div>' +
            '<div class="col" style="min-width:200px;">' +
            '<span class="muted" style="font-size:12px;display:block;margin-bottom:2px;">执行状态</span>' +
            '<div>' + statusBadge(task.status) + '</div>' +
            '</div>' +
            '</div>' +
            '<div class="row mt-2" style="border-top:1px solid #f1f5f9;padding-top:14px;row-gap:12px;">' +
            '<div class="col"><span class="muted" style="font-size:12px;">创建时间：</span><span class="font-mono" style="font-size:12.5px;">' + esc(fmtTime(task.created_at)) + '</span></div>' +
            '<div class="col"><span class="muted" style="font-size:12px;">启动时间：</span><span class="font-mono" style="font-size:12.5px;">' + esc(fmtTime(task.started_at)) + '</span></div>' +
            '<div class="col"><span class="muted" style="font-size:12px;">结束时间：</span><span class="font-mono" style="font-size:12.5px;">' + esc(fmtTime(task.finished_at)) + '</span></div>' +
            '</div>' +
            (task.error ? '<div class="error-msg mt-2">' + esc(task.error) + '</div>' : '') +
            (task.type === 'storage_provision_nfs' && task.status === 'succeeded'
                ? '<div class="mt-2" style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:6px;padding:10px 14px;display:flex;align-items:center;justify-content:space-between;">' +
                  '<div><strong class="text-success">✓ NFS 存储卷供给完成</strong><span class="muted" style="margin-left:8px;font-size:12px;">已完成底层格式化与网络导出，可直接用于平台注册</span></div>' +
                  '<button class="btn btn-sm btn-primary" id="btn-plat-from-task">查看/复制平台注册参数</button>' +
                  '</div>'
                : '');

        var platBtn = document.getElementById('btn-plat-from-task');
        if (platBtn) {
            platBtn.addEventListener('click', async function () {
                var addr = '127.0.0.1';
                try {
                    var wr = await apiJSON('/workers/' + task.target_id);
                    if (wr.resp.ok && wr.data && wr.data.host) addr = wr.data.host;
                } catch (e) {}
                showPlatformRegistrationModal(document.getElementById('content'), {
                    name: 'nfs-task-' + task.id,
                    service_address: addr,
                    path: '/data02/notebook_nfs',
                    workspace_uuid: ''
                });
            });
        }
    }

    function renderStepsFromCache() {
        var el = document.getElementById('steps-container');
        if (!el) return;
        var seqs = Object.keys(stepsData).map(Number).sort(function (a, b) { return a - b; });
        if (seqs.length === 0) {
            el.innerHTML = '<p class="muted">当前任务尚未生成步骤指令流水。</p>';
            return;
        }
        el.innerHTML = seqs.map(function (seq) {
            var s = stepsData[seq];
            return '<div class="step-item ' + esc(s.status) + '">' +
                '<div class="step-name">' +
                '<span><strong>步骤 ' + esc(s.seq) + '</strong> &mdash; ' + esc(s.name) + '</span>' +
                '<span>' + statusBadge(s.status) + '</span>' +
                '</div>' +
                (s.stdout ? '<div class="step-stdout">' + esc(s.stdout) + '</div>' : '') +
                (s.stderr ? '<div class="step-stderr">' + esc(s.stderr) + '</div>' : '') +
                (s.error ? '<div class="step-stderr">Error: ' + esc(s.error) + '</div>' : '') +
                '</div>';
        }).join('');
    }

    function upsertStep(s) {
        if (!s || !s.seq) return;
        var prev = stepsData[s.seq] || {};
        stepsData[s.seq] = {
            seq: s.seq,
            name: s.name || prev.name || '',
            status: s.status || prev.status || '',
            stdout: (s.stdout != null && s.stdout !== '') ? s.stdout : (prev.stdout || ''),
            stderr: (s.stderr != null && s.stderr !== '') ? s.stderr : (prev.stderr || ''),
            error: (s.error != null && s.error !== '') ? s.error : (prev.error || '')
        };
    }

    function fetchFinalSteps(taskID) {
        apiJSON('/tasks/' + taskID).then(function (r) {
            if (r.resp.ok && r.data && r.data.steps) {
                r.data.steps.forEach(function (s) { upsertStep(s); });
                renderStepsFromCache();
            }
        }).catch(function () {});
    }

    function subscribeSSE(taskID) {
        if (!isAuthenticated) return;
        var url = '/api/v1/tasks/' + taskID + '/stream';
        var es = new EventSource(url, { withCredentials: true });
        currentSSE = es;

        es.addEventListener('task', function (e) {
            try {
                var task = JSON.parse(e.data);
                renderTaskInfo(task);
                if (task.status !== 'pending' && task.status !== 'running') {
                    fetchFinalSteps(taskID);
                    closeSSE();
                }
            } catch (err) {}
        });

        es.addEventListener('step', function (e) {
            try {
                var step = JSON.parse(e.data);
                upsertStep(step);
                renderStepsFromCache();
            } catch (err) {}
        });

        es.onerror = function () {};
    }

    // ====================================================================
    // AUDIT PAGE
    // ====================================================================

    registerRoute('/audit', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">系统操作审计日志</h2>' +
            '<p class="page-subtitle">完整记录控制台关键配置变更、凭证更新与存储编排动作</p>' +
            '</div>' +
            '</div>' +
            '<div class="table-responsive mt-2">' +
            '<table class="data-table" id="audit-table"><thead><tr>' +
            '<th>流水 ID</th><th>操作者</th><th>触发动作</th><th>目标对象</th><th>执行结果</th><th>发生时间</th>' +
            '</tr></thead><tbody id="audit-tbody"><tr><td colspan="6" class="muted">正在加载审计日志...</td></tr></tbody></table>' +
            '</div>';

        try {
            var r = await apiJSON('/audit-log');
            if (!r.resp.ok) { return; }
            var logs = r.data || [];
            var tbody = document.getElementById('audit-tbody');
            if (logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="muted">暂无历史操作审计记录。</td></tr>';
                return;
            }
            tbody.innerHTML = logs.map(function (a) {
                return '<tr>' +
                    '<td><span class="badge-mono font-mono">' + esc(a.id) + '</span></td>' +
                    '<td><strong>' + esc(a.actor) + '</strong></td>' +
                    '<td><span class="badge badge-muted font-mono">' + esc(a.action) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(a.target) + '</span></td>' +
                    '<td>' + statusBadge(a.result) + '</td>' +
                    '<td><span class="muted" style="font-size:12px;">' + esc(fmtTime(a.at)) + '</span></td>' +
                    '</tr>';
            }).join('');
        } catch (err) {}
    });

    // ===== Init =====
    async function checkAuth() {
        try {
            var resp = await fetch('/api/v1/auth/me', { credentials: 'same-origin' });
            if (resp.ok) {
                var adminInfo = await resp.json().catch(function () { return null; });
                if (adminInfo && adminInfo.username) {
                    var nameEl = document.querySelector('.user-name');
                    if (nameEl) nameEl.textContent = adminInfo.username;
                }
                showApp();
                return;
            }
        } catch (e) {}
        showLogin();
    }

    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
        document.getElementById('logout-btn').addEventListener('click', handleLogout);

        var chgBtn = document.getElementById('change-pwd-btn');
        if (chgBtn) {
            chgBtn.addEventListener('click', showChangePasswordModal);
        }

        window.addEventListener('hashchange', function () {
            closeSSE();
            if (isAuthenticated) handleRoute();
        });

        checkAuth();
    });

    window.addEventListener('beforeunload', closeSSE);
})();
