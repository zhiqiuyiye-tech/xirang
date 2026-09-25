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
            '<th>Pod 名称</th><th>使用人 / 备注</th><th>命名空间</th><th>宿主节点</th><th>Pod 状态</th><th>容器 IP</th><th>已有映射数</th><th style="text-align:right;">操作</th>' +
            '</tr></thead><tbody id="pods-tbody"><tr><td colspan="8" class="muted">正在加载 Pod 与 Service 映射...</td></tr></tbody></table>' +
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
        tbody.innerHTML = '<tr><td colspan="8" class="muted">正在从 Kubernetes 集群同步资源...</td></tr>';
        try {
            var results = await Promise.all([apiJSON('/k8s/pods'), apiJSON('/k8s/services')]);
            var pr = results[0], sr = results[1];
            if (!pr.resp.ok) { setMsg(msgEl, '错误: ' + (pr.data && pr.data.error), 'error'); tbody.innerHTML = ''; return; }
            k8sServices = (sr.resp.ok && Array.isArray(sr.data)) ? sr.data : [];
            var pods = pr.data || [];
            if (pods.length === 0) { tbody.innerHTML = '<tr><td colspan="8" class="muted">当前集群未检测到符合名称规则的 notebook Pod 实例。</td></tr>'; return; }
            tbody.innerHTML = pods.map(function (p) {
                var cnt = servicesForPod(p.uid).length;
                var ownerDisplay = p.owner_name
                    ? ('<strong>' + esc(p.owner_name) + '</strong>' + (p.note ? '<div class="muted" style="font-size:11.5px;">' + esc(p.note) + '</div>' : ''))
                    : '<span class="muted" style="font-size:12px;">(未设置)</span>';
                return '<tr>' +
                    '<td><strong>' + esc(p.name) + '</strong></td>' +
                    '<td>' + ownerDisplay + '</td>' +
                    '<td><span class="badge badge-muted font-mono">' + esc(p.namespace) + '</span></td>' +
                    '<td><span class="font-mono">' + esc(p.node) + '</span></td>' +
                    '<td>' + statusBadge(p.status) + '</td>' +
                    '<td><span class="font-mono">' + esc((p.ips || []).join(', ')) + '</span></td>' +
                    '<td>' + (cnt > 0 ? '<span class="badge badge-success">' + cnt + ' 条映射</span>' : '<span class="muted">-</span>') + '</td>' +
                    '<td style="text-align:right;"><button class="btn btn-sm btn-primary" data-pod=\'' + esc(JSON.stringify(p)) + '\'>配置端口映射与备注</button></td>' +
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
        var editingSvc = null;

        var html = '<div class="modal-overlay" id="port-modal"><div class="modal" style="max-width: 760px;">' +
            '<h3 class="modal-title">' +
            '<span>Notebook 端口映射与归属配置</span>' +
            '<span class="badge badge-primary font-mono">' + esc(pod.name) + '</span>' +
            '</h3>' +
            // Section 1: Metadata / Remark
            '<div class="card mb-2">' +
            '<div class="section-title" style="margin-bottom:6px;">使用人与备注信息</div>' +
            '<p class="muted mb-2" style="font-size:12px;">标注 Notebook 的责任人与用途，帮助集群运维人员清晰识别容器使用者。</p>' +
            '<div class="row">' +
            '<div class="col"><div class="form-field mb-1"><label>使用人 / 负责人</label><input type="text" id="nb-meta-owner" placeholder="如：张三、算法组李工" value="' + esc(pod.owner_name || '') + '"></div></div>' +
            '<div class="col"><div class="form-field mb-1"><label>业务备注说明</label><input type="text" id="nb-meta-note" placeholder="如：大模型微调实验、PyTorch训练" value="' + esc(pod.note || '') + '"></div></div>' +
            '</div>' +
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px;">' +
            '<span class="muted" style="font-size:11.5px;">' +
            (pod.key_kind === 'business_labels'
                ? '<span class="badge badge-success" style="font-size:10.5px;">稳定业务标签</span> Pod 重建后将自动保持备注'
                : '<span class="badge badge-muted" style="font-size:10.5px;">Pod UID 绑定</span> 缺少 workspace/project 标签，Pod 重建后不继承') +
            (pod.updated_by ? (' · 最近修改: ' + esc(pod.updated_by) + ' (' + fmtTime(pod.metadata_updated_at) + ')') : '') +
            '</span>' +
            '<button type="button" class="btn btn-xs btn-outline" id="btn-save-meta">保存使用人与备注</button>' +
            '</div>' +
            '<div id="nb-meta-msg" class="info-msg" style="margin-top:4px;"></div>' +
            '</div>' +
            // Section 2: Existing Mappings
            '<div class="card"><div class="section-title">该 Pod 关联的 Service 映射</div>' +
            '<p class="muted mb-2" style="font-size:12px;">包含全部匹配该 Pod 的 Service。<span class="badge badge-success">本面板创建</span> 可随时原地编辑或清理，<span class="badge badge-muted">外部创建</span> 为集群固有只读。</p>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="pod-svc-table"><thead><tr><th>Service 名称</th><th>端口映射规则 (NodePort &rarr; 容器目标端口)</th><th>归属</th><th style="text-align:right;">操作</th></tr></thead>' +
            '<tbody id="pod-existing-tbody"><tr><td colspan="4" class="muted">加载中...</td></tr></tbody></table></div></div>' +
            // Section 3: Add/Edit Port Rules
            '<div class="card mt-2">' +
            '<div style="display:flex;justify-content:space-between;align-items:center;">' +
            '<div class="section-title" id="port-form-title" style="margin-bottom:0;">新建 NodePort 映射规则</div>' +
            '<button type="button" class="btn btn-xs btn-outline" id="btn-cancel-edit" style="display:none;">取消编辑并返回新建</button>' +
            '</div>' +
            '<p class="muted mb-2" style="font-size:12px;">直接配置容器内部端口与可选外部 NodePort（30000-32767，若不填则由 Kubernetes 自动随机分配）。系统将联动配置 NetworkPolicy 放行外部流量。</p>' +
            '<form id="port-form">' +
            '<div id="port-rows-container"></div>' +
            '<div style="margin-bottom:12px;">' +
            '<button type="button" class="btn btn-xs btn-outline" id="btn-add-port-row">+ 添加一行端口映射</button>' +
            '</div>' +
            '<div class="row mt-2" style="justify-content: flex-end;">' +
            '<button type="button" class="btn btn-outline" id="port-cancel">关闭</button>' +
            '<button type="submit" class="btn btn-primary" id="btn-submit-port">立即创建映射</button>' +
            '</div>' +
            '<div id="port-form-msg" class="error-msg"></div></form></div></div></div>';

        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('port-modal');
        document.getElementById('port-cancel').addEventListener('click', function () { modal.remove(); });

        // Save metadata handler
        document.getElementById('btn-save-meta').addEventListener('click', async function () {
            var owner = document.getElementById('nb-meta-owner').value.trim();
            var note = document.getElementById('nb-meta-note').value.trim();
            var msgEl = document.getElementById('nb-meta-msg');
            this.disabled = true;
            try {
                var r = await apiJSON('/k8s/notebooks/' + encodeURIComponent(pod.namespace) + '/' + encodeURIComponent(pod.name) + '/metadata', {
                    method: 'PUT',
                    body: JSON.stringify({ owner_name: owner, note: note })
                });
                if (!r.resp.ok) {
                    setMsg(msgEl, '保存失败: ' + (r.data && r.data.error), 'error');
                } else {
                    setMsg(msgEl, '使用人与备注已成功保存！', 'info');
                    pod.owner_name = owner;
                    pod.note = note;
                    loadPods(content);
                }
            } catch (err) {
                setMsg(msgEl, '保存失败: ' + err.message, 'error');
            } finally {
                this.disabled = false;
            }
        });

        var rowsContainer = document.getElementById('port-rows-container');

        function createPortRow(podPort, nodePort) {
            var row = document.createElement('div');
            row.className = 'port-row-item';
            row.style.cssText = 'display:flex;gap:10px;align-items:center;margin-bottom:8px;';
            row.innerHTML = '<div style="flex:1;"><input type="number" class="row-pod-port" placeholder="Pod 内部端口 (必填，如 8888)" min="1" max="65535" value="' + (podPort || '') + '" required style="margin-bottom:0;"></div>' +
                '<div style="flex:1.3;"><input type="number" class="row-node-port" placeholder="外部 NodePort (可选，留空自动分配)" min="30000" max="32767" value="' + (nodePort || '') + '" style="margin-bottom:0;"></div>' +
                '<button type="button" class="btn btn-xs btn-danger btn-del-row" style="padding:6px 10px;">&times; 删除行</button>';
            row.querySelector('.btn-del-row').addEventListener('click', function () {
                row.remove();
            });
            rowsContainer.appendChild(row);
        }

        // Add initial row
        createPortRow('', '');

        document.getElementById('btn-add-port-row').addEventListener('click', function () {
            createPortRow('', '');
        });

        var btnCancelEdit = document.getElementById('btn-cancel-edit');
        var formTitle = document.getElementById('port-form-title');
        var submitBtn = document.getElementById('btn-submit-port');

        function resetFormToCreate() {
            editingSvc = null;
            formTitle.textContent = '新建 NodePort 映射规则';
            submitBtn.textContent = '立即创建映射';
            btnCancelEdit.style.display = 'none';
            rowsContainer.innerHTML = '';
            createPortRow('', '');
            setMsg(document.getElementById('port-form-msg'), '', 'error');
        }

        btnCancelEdit.addEventListener('click', resetFormToCreate);

        function setupEditMode(svc) {
            editingSvc = svc;
            formTitle.innerHTML = '正在编辑 Service: <code>' + esc(svc.name) + '</code>';
            submitBtn.textContent = '保存并更新规则';
            btnCancelEdit.style.display = 'inline-block';
            rowsContainer.innerHTML = '';
            var ports = svc.ports || [];
            if (ports.length === 0) {
                createPortRow('', '');
            } else {
                ports.forEach(function (p) {
                    createPortRow(p.target_port || p.port, p.node_port || '');
                });
            }
            document.getElementById('port-form').scrollIntoView({ behavior: 'smooth' });
        }

        renderExistingMappings(modal, pod, setupEditMode);

        document.getElementById('port-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var msgEl = document.getElementById('port-form-msg');
            setMsg(msgEl, '', 'error');
            var rowEls = rowsContainer.querySelectorAll('.port-row-item');

            if (rowEls.length === 0) {
                if (editingSvc) {
                    if (!confirm('已移除全部端口映射。保存将彻底删除 Service ' + editingSvc.name + ' 及对应 NetworkPolicy，是否确认？')) {
                        return;
                    }
                } else {
                    setMsg(msgEl, '请至少添加一行端口映射规则', 'error');
                    return;
                }
            }

            var mappings = [];
            var parseErr = null;
            var seenPodPorts = {};
            var seenNodePorts = {};

            rowEls.forEach(function (row) {
                if (parseErr) return;
                var podPortVal = parseInt(row.querySelector('.row-pod-port').value, 10);
                var nodePortInput = row.querySelector('.row-node-port').value.trim();
                var nodePortVal = nodePortInput ? parseInt(nodePortInput, 10) : 0;

                if (isNaN(podPortVal) || podPortVal < 1 || podPortVal > 65535) {
                    parseErr = 'Pod 内部端口必须在 1 到 65535 之间';
                    return;
                }
                if (nodePortInput && (isNaN(nodePortVal) || nodePortVal < 30000 || nodePortVal > 32767)) {
                    parseErr = '外部 NodePort (' + nodePortInput + ') 必须在 30000 到 32767 范围内，或留空让系统自动分配';
                    return;
                }
                if (seenPodPorts[podPortVal]) {
                    parseErr = '同一次配置中不能重复相同的 Pod 内部端口 (' + podPortVal + ')';
                    return;
                }
                seenPodPorts[podPortVal] = true;
                if (nodePortVal > 0) {
                    if (seenNodePorts[nodePortVal]) {
                        parseErr = '同一次配置中不能指定重复的外部 NodePort (' + nodePortVal + ')';
                        return;
                    }
                    seenNodePorts[nodePortVal] = true;
                }
                mappings.push({ pod_port: podPortVal, node_port: nodePortVal });
            });

            if (parseErr) {
                setMsg(msgEl, '错误: ' + parseErr, 'error');
                return;
            }

            try {
                var r;
                if (editingSvc) {
                    r = await apiJSON('/k8s/services/' + encodeURIComponent(editingSvc.name) + '?namespace=' + encodeURIComponent(editingSvc.namespace), {
                        method: 'PUT',
                        body: JSON.stringify({
                            resource_version: editingSvc.resource_version || '',
                            mappings: mappings
                        })
                    });
                } else {
                    var body = {
                        namespace: pod.namespace, pod_name: pod.name, pod_uid: pod.uid,
                        selector: pod.labels || {}, type: 'NodePort', mappings: mappings
                    };
                    r = await apiJSON('/k8s/services', { method: 'POST', body: JSON.stringify(body) });
                }
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    function renderExistingMappings(scope, pod, onEditSvc) {
        var el = scope.querySelector('#pod-existing-tbody');
        if (!el) return;
        var mine = servicesForPod(pod.uid);
        if (mine.length === 0) {
            el.innerHTML = '<tr><td colspan="4" class="muted">当前 Pod 尚无关联端口映射。可在下方新建映射规则。</td></tr>';
            return;
        }
        mine.sort(function (a, b) { return (a.managed === b.managed) ? 0 : (a.managed ? -1 : 1); });
        el.innerHTML = mine.map(function (s) {
            var ports = s.ports || [];
            var rulesHtml = ports.length === 0 ? '<span class="muted">(未定义端口)</span>' : ports.map(function (p) {
                var ext = p.node_port ? ('<strong style="color:var(--primary);">' + p.node_port + '</strong>') : '<span class="muted">自动分配</span>';
                var target = p.target_port || p.port;
                return '<span class="badge" style="margin:2px 4px 2px 0;background:rgba(255,255,255,0.05);">' + ext + ' &rarr; <span class="font-mono">' + target + '/TCP</span></span>';
            }).join('');
            var srcBadge = s.managed ? '<span class="badge badge-success">本面板管理</span>' : '<span class="badge badge-muted">外部固有</span>';
            var action = s.managed
                ? '<div class="actions-cell" style="justify-content:flex-end;">' +
                  '<button class="btn btn-xs btn-outline" data-act="edit-svc" data-svc=\'' + esc(JSON.stringify(s)) + '\'>编辑规则</button>' +
                  '<button class="btn btn-xs btn-danger" data-act="del-svc" data-name="' + esc(s.name) + '" data-ns="' + esc(s.namespace) + '">删除</button>' +
                  '</div>'
                : '<span class="muted" style="font-size:12px;">只读</span>';
            return '<tr><td><span class="font-mono" style="font-weight:600;">' + esc(s.name) + '</span></td><td>' + rulesHtml + '</td><td>' + srcBadge + '</td>' +
                '<td style="text-align:right;">' + action + '</td></tr>';
        }).join('');

        el.querySelectorAll('button[data-act="edit-svc"]').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var s = JSON.parse(this.getAttribute('data-svc'));
                if (onEditSvc) onEditSvc(s);
            });
        });

        el.querySelectorAll('button[data-act="del-svc"]').forEach(function (btn) {
            btn.addEventListener('click', async function () {
                if (!confirm('确认删除 Service ' + this.getAttribute('data-name') + '？\n删除将释放对应的 NodePort 端口并清理配套 NetworkPolicy 规则。')) return;
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
            // Block 0: Active NFS Hosts & Virtual Disks Overview
            '<div class="card mb-3" id="st-nfs-overview-card">' +
            '<div class="card-header" style="justify-content:space-between;align-items:center;">' +
            '<div>' +
            '<div class="section-title" style="margin-bottom:0;">当前已开启 NFS 的主机概览</div>' +
            '<span class="muted" style="font-size:12px;">展示已开启 NFS 的主机硬件磁盘分布、剩余可用容量、划分的虚拟盘及其挂载目录与空间占用</span>' +
            '</div>' +
            '<button class="btn btn-outline btn-xs" id="btn-refresh-nfs-hosts">🔄 刷新全部缓存</button>' +
            '</div>' +
            '<div id="st-nfs-hosts-container" style="padding-top:10px;">' +
            '<div class="muted">正在查询存储快照...</div>' +
            '</div>' +
            '</div>' +
            // Worker Selector
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
            '<div class="section-title" style="margin-bottom:0;">存储池 (VG) 与物理硬盘</div>' +
            '<div style="display:flex;align-items:center;gap:12px;">' +
            '<span id="st-vg-summary" class="muted" style="font-size:12.5px;"></span>' +
            '<button class="btn btn-outline btn-xs" id="btn-refresh-worker-inv" style="display:none;">🔄 刷新此节点</button>' +
            '<button class="btn btn-primary btn-sm" id="btn-init-vg" disabled>初始化 VG 池 (从未挂载裸盘)</button>' +
            '</div></div>' +
            '<div id="st-disks-container" style="margin-bottom:12px;"></div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="st-vg-table"><thead><tr><th>VG 卷组名称</th><th>总容量</th><th>剩余可用容量</th></tr></thead>' +
            '<tbody id="st-vg-tbody"><tr><td colspan="3" class="muted">请在上方选择 Worker 节点以获取 VG 存储池状态。</td></tr></tbody></table>' +
            '</div></div>' +
            // Block B: LV management
            '<div class="card mt-2">' +
            '<div class="card-header">' +
            '<div class="section-title" style="margin-bottom:0;">逻辑卷 (虚拟盘) 管理</div>' +
            '<span class="muted" style="font-size:12px;">包含全部底层识别的 LV 虚拟盘，实时监控所属物理盘、挂载目录、空间已用/剩余与 NFS 导出状态</span>' +
            '</div>' +
            '<div class="table-responsive">' +
            '<table class="data-table" id="st-lv-table"><thead><tr><th>虚拟盘名称</th><th>所属 VG</th><th>底层物理盘</th><th>总容量</th><th>挂载目录</th><th>已用空间</th><th>剩余可用</th><th>使用率</th><th>NFS 导出</th><th style="text-align:right;">操作</th></tr></thead>' +
            '<tbody id="st-lv-tbody"><tr><td colspan="10" class="muted">请先在上方选择 Worker 节点。</td></tr></tbody></table>' +
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

        async function loadNFSHosts() {
            var container = document.getElementById('st-nfs-hosts-container');
            if (!container) return;
            container.innerHTML = '<div class="muted">正在查询存储快照...</div>';
            try {
                var r = await apiJSON('/storage/nfs-hosts');
                if (!r.resp.ok) {
                    container.innerHTML = '<div class="error-msg">获取已开启 NFS 主机失败: ' + esc((r.data && r.data.error) || '请求异常') + '</div>';
                    return;
                }
                var hosts = r.data || [];
                if (hosts.length === 0) {
                    container.innerHTML = '<div class="muted" style="padding:8px 0;">当前暂无运行中或配置有 NFS 共享的主机。可在下方选择 Worker 节点创建并导出 NFS 共享。</div>';
                    return;
                }

                container.innerHTML = hosts.map(function (h) {
                    var disks = h.physical_disks || [];
                    var vdisks = h.virtual_disks || [];
                    var exports = h.nfs_exports || [];

                    var disksHtml = disks.length === 0 ? '<span class="muted">暂未检测到物理硬盘信息</span>' : disks.map(function (d) {
                        var roleTag = '';
                        var capLabel = '';
                        if (d.is_reserved || d.role === 'reserved') {
                            roleTag = '<span class="badge badge-danger" style="font-size:11px;" title="挂载在 /data01，为 K8s 保留盘，禁止用于 NFS">K8s保留盘 (/data01)</span>';
                            capLabel = '<span style="color:var(--danger);font-size:11.5px;">(保留禁止作为NFS盘)</span>';
                        } else if (d.is_system || d.role === 'system') {
                            roleTag = '<span class="badge badge-muted" style="font-size:11px;">系统盘</span>';
                            capLabel = '剩余: <span class="muted font-mono">' + (d.free_gb ? d.free_gb.toFixed(1) + ' GB' : '-') + '</span>';
                        } else if (d.role === 'lvm') {
                            roleTag = '<span class="badge badge-primary" style="font-size:11px;">LVM ' + esc(d.vg_name || '') + '</span>';
                            capLabel = 'VG可用: <strong style="color:var(--success);" class="font-mono">' + (d.free_gb || 0).toFixed(1) + ' GB</strong>';
                        } else if (d.role === 'unused') {
                            roleTag = '<span class="badge badge-success" style="font-size:11px;">未分配裸盘</span>';
                            capLabel = '可初始化: <strong style="color:var(--success);" class="font-mono">' + (d.free_gb || 0).toFixed(1) + ' GB</strong>';
                        } else {
                            roleTag = '<span class="badge badge-muted" style="font-size:11px;">普通数据盘</span>';
                            capLabel = '剩余: <strong style="color:var(--text);" class="font-mono">' + (d.free_gb ? d.free_gb.toFixed(1) + ' GB' : '-') + '</strong>';
                        }

                        return '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:8px 12px;min-width:190px;">' +
                            '<div style="display:flex;justify-content:space-between;align-items:center;gap:6px;">' +
                            '<strong>' + esc(d.name) + '</strong>' + roleTag +
                            '</div>' +
                            '<div style="font-size:12px;color:var(--text-muted);margin-top:4px;">' +
                            '总计: <span class="font-mono">' + (d.size_gb || 0).toFixed(1) + ' GB</span><br>' + capLabel +
                            '</div>' +
                            '</div>';
                    }).join('');

                    function renderLVRows(lvList) {
                        return lvList.map(function (lv) {
                            var pctNum = parseInt(lv.use_pct || '0', 10) || 0;
                            var pctColor = pctNum > 85 ? 'var(--danger)' : (pctNum > 60 ? 'var(--warning, #f59e0b)' : 'var(--success)');
                            var nfsBadge = lv.is_nfs_export
                                ? '<span class="badge badge-success" title="' + esc(lv.nfs_export_opt || '') + '">✓ NFS 已导出</span>'
                                : '<span class="badge badge-muted">未导出</span>';
                            var data = JSON.stringify({ vg: lv.vg_name, name: lv.name, size: lv.size_gb, mp: lv.mount_point, fs: lv.fs_type });
                            var platBtn = lv.mount_point
                                ? '<button class="btn btn-xs btn-outline" data-act="platform" data-wid="' + h.worker_id + '" data-host="' + esc(h.host) + '" data-lv=\'' + esc(data) + '\'>平台参数</button>'
                                : '-';
                            var freeStr = lv.mount_point ? '<strong style="color:var(--success);">' + (lv.free_gb || 0).toFixed(1) + ' GB</strong>' : '<span class="muted">(未挂载)</span>';
                            var disksBadge = (lv.physical_disks && lv.physical_disks.length)
                                ? lv.physical_disks.map(function (x) { return '<span class="badge badge-mono font-mono" style="font-size:10.5px;">' + esc(x) + '</span>'; }).join(' ')
                                : '<span class="muted">-</span>';
                            return '<tr>' +
                                '<td><strong>' + esc(lv.name) + '</strong></td>' +
                                '<td><span class="badge badge-muted font-mono" style="font-size:11px;">' + esc(lv.vg_name || '-') + '</span></td>' +
                                '<td>' + disksBadge + '</td>' +
                                '<td><span class="font-mono">' + esc(lv.mount_point || '(未挂载)') + '</span></td>' +
                                '<td><span class="font-mono">' + (lv.size_gb || 0).toFixed(1) + ' GB</span></td>' +
                                '<td><span class="font-mono">' + (lv.mount_point ? (lv.used_gb || 0).toFixed(1) + ' GB' : '-') + '</span></td>' +
                                '<td><span class="font-mono">' + freeStr + '</span></td>' +
                                '<td>' + (lv.mount_point ? ('<div style="display:flex;align-items:center;gap:6px;"><div style="flex:1;height:6px;background:rgba(255,255,255,0.08);border-radius:3px;overflow:hidden;min-width:40px;"><div style="width:' + Math.min(pctNum, 100) + '%;height:100%;background:' + pctColor + ';"></div></div><span style="font-size:11px;min-width:28px;">' + esc(lv.use_pct || '0%') + '</span></div>') : '-') + '</td>' +
                                '<td>' + nfsBadge + '</td>' +
                                '<td>' + platBtn + '</td>' +
                                '</tr>';
                        }).join('');
                    }

                    function renderLVTableContainer(rowsHtml) {
                        return '<div class="table-responsive" style="margin-top:6px;">' +
                            '<table class="data-table" style="font-size:12px;">' +
                            '<thead><tr><th>虚拟盘名称</th><th>所属卷组</th><th>底层物理盘</th><th>挂载目录</th><th>总容量</th><th>已用空间</th><th>剩余空间</th><th>使用率</th><th>NFS 状态</th><th>操作</th></tr></thead>' +
                            '<tbody>' + rowsHtml + '</tbody></table></div>';
                    }

                    var groupedByDisk = {};
                    var crossDiskLVs = [];
                    var unassignedLVs = [];

                    vdisks.forEach(function (lv) {
                        var pds = lv.physical_disks || [];
                        if (pds.length === 1) {
                            var dn = pds[0];
                            if (!groupedByDisk[dn]) groupedByDisk[dn] = [];
                            groupedByDisk[dn].push(lv);
                        } else if (pds.length > 1) {
                            crossDiskLVs.push(lv);
                        } else {
                            unassignedLVs.push(lv);
                        }
                    });

                    var vdisksHtml = '';
                    if (vdisks.length === 0) {
                        vdisksHtml = '<div class="muted" style="padding:6px 0;font-size:12px;">该主机暂无划分的虚拟盘。可在下方选择该 Worker 节点进行创建。</div>';
                    } else {
                        var groupsHtml = [];
                        disks.forEach(function (d) {
                            var myLVs = groupedByDisk[d.name] || [];
                            if (d.role === 'lvm' || myLVs.length > 0) {
                                var countBadge = myLVs.length > 0
                                    ? '<span class="badge badge-success font-mono" style="font-size:11px;">' + myLVs.length + ' 个虚拟盘</span>'
                                    : '<span class="badge badge-muted" style="font-size:11px;">0 个虚拟盘</span>';
                                var diskHeader = '<div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:6px 12px;margin-top:8px;">' +
                                    '<div style="display:flex;align-items:center;gap:8px;"><strong>物理数据盘: ' + esc(d.name) + '</strong> <span class="muted font-mono" style="font-size:11.5px;">(总计 ' + (d.size_gb||0).toFixed(1) + ' GB · VG可用 ' + (d.free_gb||0).toFixed(1) + ' GB)</span> ' + countBadge + '</div>' +
                                    '<span class="muted" style="font-size:11.5px;">' + (d.vg_name ? '卷组: ' + esc(d.vg_name) : '') + '</span>' +
                                    '</div>';
                                var tbl = myLVs.length === 0
                                    ? '<div class="muted" style="padding:6px 12px;font-size:12px;">该物理数据盘当前尚未切分出虚拟盘。</div>'
                                    : renderLVTableContainer(renderLVRows(myLVs));
                                groupsHtml.push('<div style="margin-bottom:8px;">' + diskHeader + tbl + '</div>');
                            }
                        });

                        if (crossDiskLVs.length > 0) {
                            var crossHeader = '<div style="display:flex;justify-content:space-between;align-items:center;background:rgba(234,179,8,0.05);border:1px solid rgba(234,179,8,0.2);border-radius:6px;padding:6px 12px;margin-top:10px;">' +
                                '<div style="display:flex;align-items:center;gap:8px;"><strong>🔀 跨盘存储池虚拟盘 (跨越多块物理盘)</strong> <span class="badge badge-warning font-mono" style="font-size:11px;">' + crossDiskLVs.length + ' 个跨盘虚拟盘</span></div>' +
                                '<span class="muted" style="font-size:11.5px;">此类虚拟盘由多个底层物理盘共同支撑</span>' +
                                '</div>';
                            groupsHtml.push('<div style="margin-bottom:8px;">' + crossHeader + renderLVTableContainer(renderLVRows(crossDiskLVs)) + '</div>');
                        }

                        if (unassignedLVs.length > 0) {
                            var unHeader = '<div style="display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:6px;padding:6px 12px;margin-top:10px;">' +
                                '<div><strong>其他虚拟盘 (未定位具体物理盘)</strong></div>' +
                                '</div>';
                            groupsHtml.push('<div style="margin-bottom:8px;">' + unHeader + renderLVTableContainer(renderLVRows(unassignedLVs)) + '</div>');
                        }

                        vdisksHtml = groupsHtml.join('');
                    }

                    var syncBadge = h.refreshing
                        ? '<span class="badge badge-warning">🔄 正在后台刷新...</span>'
                        : (h.stale
                            ? '<span class="badge badge-muted" title="快照采集时间: ' + esc(fmtTime(h.collected_at)) + '">⏳ 缓存较旧</span>'
                            : '<span class="badge badge-success" title="同步时间: ' + esc(fmtTime(h.collected_at)) + '">✓ 快照已同步</span>');

                    var errHtml = h.error_message
                        ? '<div class="error-msg" style="margin-top:6px;font-size:12px;">最近采集提示: ' + esc(h.error_message) + ' (展示历史快照)</div>'
                        : '';

                    return '<div style="border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:14px;margin-bottom:12px;background:rgba(255,255,255,0.015);">' +
                        '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:10px;margin-bottom:10px;">' +
                        '<div style="display:flex;align-items:center;gap:10px;">' +
                        '<strong style="font-size:14px;">' + esc(h.worker_name) + '</strong>' +
                        '<span class="badge badge-muted font-mono">' + esc(h.host) + ':' + h.port + '</span>' +
                        (h.nfs_active ? '<span class="badge badge-success"><span class="badge-dot"></span>NFS 服务运行中</span>' : '<span class="badge badge-muted">NFS 未激活</span>') +
                        syncBadge +
                        '<button class="btn btn-xs btn-outline" data-act="refresh-worker" data-wid="' + h.worker_id + '">🔄 刷新此节点</button>' +
                        '</div>' +
                        '<div style="font-size:12px;color:var(--text-muted);">' +
                        '物理硬盘: <strong class="font-mono">' + (h.total_disks || disks.length) + '</strong> 块 · 虚拟盘: <strong class="font-mono">' + vdisks.length + '</strong> 个 · 导出路径: <strong class="font-mono">' + exports.length + '</strong> 个' +
                        '</div>' +
                        '</div>' +
                        errHtml +
                        '<div style="margin-bottom:10px;">' +
                        '<div style="font-size:12px;font-weight:600;color:var(--text-muted);margin-bottom:6px;">物理硬盘情况 (分别有 ' + (h.total_disks || disks.length) + ' 块硬盘，及其剩余容量)：</div>' +
                        '<div style="display:flex;flex-wrap:wrap;gap:8px;">' + disksHtml + '</div>' +
                        '</div>' +
                        '<div>' +
                        '<div style="font-size:12px;font-weight:600;color:var(--text-muted);margin-bottom:4px;">划分的虚拟盘与挂载状态 (按所属物理数据盘分开显示)：</div>' +
                        vdisksHtml +
                        '</div>' +
                        '</div>';
                }).join('');

                container.querySelectorAll('button[data-act="refresh-worker"]').forEach(function (btn) {
                    btn.addEventListener('click', async function () {
                        var wid = parseInt(this.getAttribute('data-wid'), 10);
                        this.disabled = true;
                        this.textContent = '刷新中...';
                        await apiJSON('/storage/refresh', { method: 'POST', body: JSON.stringify({ worker_id: wid }) });
                        await loadNFSHosts();
                    });
                });

                container.querySelectorAll('button[data-act="platform"]').forEach(function (btn) {
                    btn.addEventListener('click', function () {
                        var lv = JSON.parse(this.getAttribute('data-lv'));
                        var wid = this.getAttribute('data-wid');
                        var host = this.getAttribute('data-host') || '127.0.0.1';
                        showPlatformRegistrationModal(content, {
                            name: 'nfs-' + lv.name,
                            service_address: host,
                            path: lv.mp || '/data02/notebook_nfs',
                            size_gb: lv.size,
                            workspace_uuid: ''
                        });
                    });
                });
            } catch (e) {
                container.innerHTML = '<div class="error-msg">加载异常: ' + esc(e.message) + '</div>';
            }
        }

        document.getElementById('btn-refresh-nfs-hosts').addEventListener('click', async function () {
            var btn = this;
            btn.disabled = true;
            btn.textContent = '正在发起后台刷新...';
            try {
                await apiJSON('/storage/refresh', { method: 'POST', body: '{}' });
                await loadNFSHosts();
            } finally {
                btn.disabled = false;
                btn.textContent = '🔄 刷新全部缓存';
            }
        });
        loadNFSHosts();
        loadNFSHosts();

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
            var disksContainer = document.getElementById('st-disks-container');
            var btnRefreshWorker = document.getElementById('btn-refresh-worker-inv');

            if (btnRefreshWorker) {
                btnRefreshWorker.style.display = 'inline-block';
                btnRefreshWorker.onclick = async function () {
                    this.disabled = true;
                    this.textContent = '刷新中...';
                    try {
                        await apiJSON('/storage/refresh', { method: 'POST', body: JSON.stringify({ worker_id: parseInt(wid, 10) }) });
                        await loadInventory(wid);
                        await loadNFSHosts();
                    } finally {
                        this.disabled = false;
                        this.textContent = '🔄 刷新此节点';
                    }
                };
            }

            btnInit.disabled = true; btnNfs.disabled = true; vsel.disabled = true;
            vsel.innerHTML = '<option value="">正在分析节点存储...</option>';
            vfree.textContent = ''; summary.textContent = '';
            if (disksContainer) disksContainer.innerHTML = '';
            vgTbody.innerHTML = '<tr><td colspan="3" class="muted">正在获取存储池 (VG) 数据...</td></tr>';
            lvTbody.innerHTML = '<tr><td colspan="10" class="muted">正在获取逻辑卷 (虚拟盘) 数据...</td></tr>';
            try {
                var r = await apiJSON('/storage/inventory?worker_id=' + encodeURIComponent(wid));
                if (!r.resp.ok) {
                    var err = (r.data && r.data.error) || '加载失败';
                    setMsg(invMsg, '加载存储清单失败: ' + err + ' (若未安装 lvm2/nfs,请先在 Worker 页面点击「安装依赖」)', 'error');
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">存储池清单获取失败</td></tr>';
                    lvTbody.innerHTML = '<tr><td colspan="10" class="muted">逻辑卷清单获取失败</td></tr>';
                    vsel.innerHTML = '<option value="">-- 加载失败 --</option>';
                    return;
                }
                var inv = (r.data && r.data.data) ? r.data.data : (r.data || { vgs: [], lvs: [], unused_disks: [] });
                lastInventory = inv;

                if (r.data && r.data.refreshing) {
                    setMsg(invMsg, '后台正在同步探测该节点存储，当前展示最近快照...', 'info');
                } else if (r.data && r.data.last_error) {
                    setMsg(invMsg, '最近采集提醒: ' + r.data.last_error + ' (当前展示历史有效快照)', 'info');
                } else if (r.data && r.data.stale) {
                    setMsg(invMsg, '当前展示历史快照 (' + (r.data.collected_at ? fmtTime(r.data.collected_at) : '未同步') + ')，可点击刷新。', 'info');
                } else {
                    setMsg(invMsg, '', 'info');
                }

                var vgs = inv.vgs || [];
                if (vgs.length === 0) {
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">当前节点未初始化任何 VG 卷组。可从未挂载裸盘新建存储池。</td></tr>';
                } else {
                    vgTbody.innerHTML = vgs.map(function (v) {
                        return '<tr><td><strong>' + esc(v.name) + '</strong></td><td><span class="font-mono">' + esc(v.vsize) + '</span></td><td><span class="badge badge-success font-mono">' + esc(v.vfree) + ' (' + (v.free_gb || 0).toFixed(1) + ' GB 可用)</span></td></tr>';
                    }).join('');
                }

                var pdisks = inv.physical_disks || [];
                if (disksContainer) {
                    if (pdisks.length === 0) {
                        disksContainer.innerHTML = '';
                    } else {
                        disksContainer.innerHTML = '<div style="font-size:12px;font-weight:600;color:var(--text-muted);margin-bottom:6px;">节点物理硬盘列表 (共 ' + pdisks.length + ' 块物理硬盘)：</div>' +
                            '<div style="display:flex;flex-wrap:wrap;gap:8px;">' +
                            pdisks.map(function (d) {
                                var roleTag = '';
                                var capLabel = '';
                                if (d.is_reserved || d.role === 'reserved') {
                                    roleTag = '<span class="badge badge-danger" style="font-size:11px;" title="挂载在 /data01，为 K8s 保留盘，禁止作为 NFS 存储">K8s保留盘 (/data01)</span>';
                                    capLabel = '<span style="color:var(--danger);font-size:11px;">(保留禁止作为NFS盘)</span>';
                                } else if (d.is_system || d.role === 'system') {
                                    roleTag = '<span class="badge badge-muted" style="font-size:11px;">系统盘</span>';
                                    capLabel = '剩余: <span class="muted font-mono">' + (d.free_gb ? d.free_gb.toFixed(1) + ' GB' : '-') + '</span>';
                                } else if (d.role === 'lvm') {
                                    roleTag = '<span class="badge badge-primary" style="font-size:11px;">LVM ' + esc(d.vg_name || '') + '</span>';
                                    capLabel = 'VG可用: <strong style="color:var(--success);" class="font-mono">' + (d.free_gb || 0).toFixed(1) + ' GB</strong>';
                                } else if (d.role === 'unused') {
                                    roleTag = '<span class="badge badge-success" style="font-size:11px;">未分配裸盘</span>';
                                    capLabel = '可初始化: <strong style="color:var(--success);" class="font-mono">' + (d.free_gb || 0).toFixed(1) + ' GB</strong>';
                                } else {
                                    roleTag = '<span class="badge badge-muted" style="font-size:11px;">普通数据盘</span>';
                                    capLabel = '剩余: <strong style="color:var(--text);" class="font-mono">' + (d.free_gb ? d.free_gb.toFixed(1) + ' GB' : '-') + '</strong>';
                                }
                                return '<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:6px 10px;min-width:170px;">' +
                                    '<div style="display:flex;justify-content:space-between;align-items:center;gap:6px;"><strong>' + esc(d.name) + '</strong>' + roleTag + '</div>' +
                                    '<div style="font-size:11.5px;color:var(--text-muted);margin-top:3px;">总计: ' + (d.size_gb || 0).toFixed(1) + ' GB<br>' + capLabel + '</div>' +
                                    '</div>';
                            }).join('') + '</div>';
                    }
                }

                var disks = inv.unused_disks || [];
                if (disks.length > 0) {
                    btnInit.disabled = false;
                    summary.textContent = '发现 ' + disks.length + ' 处未挂载可用裸盘/分区可供初始化。';
                } else {
                    summary.textContent = '未检测到可用未挂载裸盘或分区（系统盘及 /data01 保留盘已自动排除）。';
                }

                var lvs = inv.lvs || [];
                if (lvs.length === 0) {
                    lvTbody.innerHTML = '<tr><td colspan="10" class="muted">该节点当前无划分的虚拟盘。</td></tr>';
                } else {
                    lvTbody.innerHTML = lvs.map(function (lv) {
                        var data = JSON.stringify({ vg: lv.vg_name, name: lv.name, size: lv.size_gb, mp: lv.mount_point, fs: lv.fs_type });
                        var platBtn = lv.mount_point
                            ? '<button class="btn btn-xs btn-outline" data-act="platform" data-lv=\'' + esc(data) + '\'>平台参数</button>'
                            : '';
                        var pctNum = parseInt(lv.use_pct || '0', 10) || 0;
                        var pctColor = pctNum > 85 ? 'var(--danger)' : (pctNum > 60 ? 'var(--warning, #f59e0b)' : 'var(--success)');
                        var nfsBadge = lv.is_nfs_export
                            ? '<span class="badge badge-success" title="' + esc(lv.nfs_export_opt || '') + '">✓ 已导出</span>'
                            : '<span class="badge badge-muted">未导出</span>';
                        var usedCol = lv.mount_point ? (lv.used_gb || 0).toFixed(1) + ' GB' : '-';
                        var freeCol = lv.mount_point ? '<strong style="color:var(--success);">' + (lv.free_gb || 0).toFixed(1) + ' GB</strong>' : '<span class="muted">(未挂载)</span>';
                        var pctCol = lv.mount_point ? ('<div style="display:flex;align-items:center;gap:6px;"><div style="flex:1;height:6px;background:rgba(255,255,255,0.08);border-radius:3px;overflow:hidden;min-width:40px;"><div style="width:' + Math.min(pctNum, 100) + '%;height:100%;background:' + pctColor + ';"></div></div><span style="font-size:11px;min-width:28px;">' + esc(lv.use_pct || '0%') + '</span></div>') : '-';
                        var disksCol = (lv.physical_disks && lv.physical_disks.length)
                            ? lv.physical_disks.map(function (x) { return '<span class="badge badge-mono font-mono" style="font-size:10.5px;">' + esc(x) + '</span>'; }).join(' ')
                            : '<span class="muted">' + esc(lv.vg_name || '-') + '</span>';

                        return '<tr>' +
                            '<td><strong>' + esc(lv.name) + '</strong></td>' +
                            '<td><span class="font-mono">' + esc(lv.vg_name) + '</span></td>' +
                            '<td>' + disksCol + '</td>' +
                            '<td><span class="font-mono">' + (lv.size_gb || 0).toFixed(1) + ' GB</span></td>' +
                            '<td><span class="font-mono">' + esc(lv.mount_point || '-') + '</span></td>' +
                            '<td><span class="font-mono">' + usedCol + '</span></td>' +
                            '<td><span class="font-mono">' + freeCol + '</span></td>' +
                            '<td>' + pctCol + '</td>' +
                            '<td>' + nfsBadge + '</td>' +
                            '<td style="text-align:right;">' +
                            '<div class="actions-cell" style="justify-content: flex-end;">' +
                            platBtn +
                            '<button class="btn btn-xs btn-outline" data-act="grow" data-lv=\'' + esc(data) + '\'>扩容</button>' +
                            '<button class="btn btn-xs btn-outline" data-act="shrink" data-lv=\'' + esc(data) + '\'>缩容</button>' +
                            '<button class="btn btn-xs btn-danger" data-act="delete" data-lv=\'' + esc(data) + '\'>删除释放</button>' +
                            '</div>' +
                            '</td></tr>';
                    }).join('');
                            '<td><span class="font-mono">' + usedCol + '</span></td>' +
                            '<td><span class="font-mono">' + freeCol + '</span></td>' +
                            '<td>' + pctCol + '</td>' +
                            '<td>' + nfsBadge + '</td>' +
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
                loadNFSHosts();
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

    // ====================================================================
    // SECURITY & PASSWORD PAGE
    // ====================================================================

    registerRoute('/security', async function (content) {
        content.innerHTML = '<div class="page-header">' +
            '<div>' +
            '<h2 class="page-title">系统安全与凭证管理</h2>' +
            '<p class="page-subtitle">修改管理员访问密码、查看会话安全状态与加固策略</p>' +
            '</div>' +
            '</div>' +
            '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:20px;margin-top:16px;">' +
            '<div class="card">' +
            '<h3 class="card-title" style="margin-bottom:14px;">修改管理员密码</h3>' +
            '<form id="page-pwd-form">' +
            '<div class="form-field"><label>当前密码</label><input type="password" name="old_password" required placeholder="请输入当前管理员密码"></div>' +
            '<div class="form-field"><label>新密码 (12-72 字符)</label><input type="password" name="new_password" required minlength="12" maxlength="72" placeholder="请输入至少 12 位新密码"></div>' +
            '<div class="form-field"><label>确认新密码</label><input type="password" name="confirm_password" required minlength="12" maxlength="72" placeholder="再次输入新密码"></div>' +
            '<div id="page-pwd-msg" class="error-msg" style="margin-bottom:12px;"></div>' +
            '<button type="submit" class="btn btn-primary" style="width:100%;">保存并更新密码</button>' +
            '</form>' +
            '</div>' +
            '<div class="card">' +
            '<h3 class="card-title" style="margin-bottom:14px;">系统安全防护状态</h3>' +
            '<div style="display:flex;flex-direction:column;gap:12px;font-size:0.9rem;">' +
            '<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;"><span class="muted">当前登录账号</span><strong id="sec-user">admin</strong></div>' +
            '<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;"><span class="muted">凭证存储机制</span><span class="badge badge-success">bcrypt + 动态盐</span></div>' +
            '<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;"><span class="muted">会话隔离机制</span><span class="badge badge-success">HttpOnly + SameSite Cookie</span></div>' +
            '<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;"><span class="muted">跨站请求伪造</span><span class="badge badge-success">CSRF 双提交 Cookie + 同源校验</span></div>' +
            '<div style="display:flex;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.06);padding-bottom:8px;"><span class="muted">暴力破解防御</span><span class="badge badge-success">连续 5 次失败封禁 15 分钟</span></div>' +
            '<div style="display:flex;justify-content:space-between;"><span class="muted">会话认证版本</span><span id="sec-version" class="badge-mono font-mono">-</span></div>' +
            '</div>' +
            '</div>' +
            '</div>';

        try {
            var meResp = await apiJSON('/auth/me');
            if (meResp.resp.ok && meResp.data) {
                var uEl = document.getElementById('sec-user');
                var vEl = document.getElementById('sec-version');
                if (uEl) uEl.textContent = meResp.data.username || 'admin';
                if (vEl) vEl.textContent = 'v' + (meResp.data.auth_version || 1);
            }
        } catch (e) {}

        var form = document.getElementById('page-pwd-form');
        if (form) {
            form.addEventListener('submit', async function (e) {
                e.preventDefault();
                var msgEl = document.getElementById('page-pwd-msg');
                msgEl.style.color = 'var(--danger)';
                msgEl.textContent = '';
                var oldP = form.old_password.value;
                var newP = form.new_password.value;
                var confirmP = form.confirm_password.value;

                if (newP !== confirmP) {
                    msgEl.textContent = '两次输入的新密码不一致';
                    return;
                }
                if (newP.length < 12 || newP.length > 72) {
                    msgEl.textContent = '新密码长度必须在 12 到 72 位之间';
                    return;
                }

                try {
                    var res = await apiJSON('/auth/password', {
                        method: 'PUT',
                        body: JSON.stringify({ old_password: oldP, new_password: newP })
                    });
                    if (!res.resp.ok) {
                        msgEl.textContent = (res.data && res.data.error) || '修改失败，请检查原密码';
                        return;
                    }
                    form.reset();
                    msgEl.style.color = '#10b981';
                    msgEl.textContent = '密码修改成功！旧会话已全部失效，当前会话已刷新。';
                    try {
                        var r2 = await apiJSON('/auth/me');
                        if (r2.resp.ok && r2.data) {
                            var vEl2 = document.getElementById('sec-version');
                            if (vEl2) vEl2.textContent = 'v' + (r2.data.auth_version || 1);
                        }
                    } catch (err) {}
                } catch (err) {
                    msgEl.textContent = '操作异常: ' + err.message;
                }
            });
        }
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
