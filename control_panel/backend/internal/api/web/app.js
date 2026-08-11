/* Xirang Control Panel - Frontend SPA
 * Native HTML/CSS/JS - no build tools, no frameworks.
 * Hash-based routing, localStorage token, SSE via EventSource.
 */

(function () {
    'use strict';

    // ===== Token Management =====
    function getToken() { return localStorage.getItem('cp_token'); }
    function setToken(t) { localStorage.setItem('cp_token', t); }
    function clearToken() { localStorage.removeItem('cp_token'); }

    // ===== API Helper =====
    async function apiFetch(path, opts) {
        opts = opts || {};
        opts.headers = opts.headers || {};
        opts.headers['Authorization'] = 'Bearer ' + getToken();
        if (opts.body && !opts.headers['Content-Type']) {
            opts.headers['Content-Type'] = 'application/json';
        }
        var resp = await fetch('/api/v1' + path, opts);
        if (resp.status === 401) {
            clearToken();
            showLogin();
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
    function showLogin() {
        document.getElementById('login-view').style.display = 'flex';
        document.getElementById('app-view').style.display = 'none';
    }

    function showApp() {
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

        try {
            var resp = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password })
            });
            if (!resp.ok) {
                var d = await resp.json();
                errEl.textContent = d.error || '登录失败';
                return;
            }
            var data = await resp.json();
            setToken(data.token);
            showApp();
        } catch (err) {
            errEl.textContent = '网络错误: ' + err.message;
        }
    }

    // ===== Logout =====
    function handleLogout() {
        clearToken();
        showLogin();
    }

    // ===== Utility =====
    function esc(s) {
        if (s == null) return '';
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    function fmtTime(ts) {
        if (!ts) return '-';
        try {
            return new Date(ts).toLocaleString();
        } catch (e) { return String(ts); }
    }

    function statusBadge(status) {
        var cls = 'badge-pending';
        if (status === 'success' || status === 'succeeded' || status === 'ok') cls = 'badge-success';
        else if (status === 'running') cls = 'badge-running';
        else if (status === 'failed' || status === 'error') cls = 'badge-failed';
        return '<span class="badge ' + cls + '">' + esc(status) + '</span>';
    }

    function authModeBadge(mode) {
        var cls = 'badge-key';
        if (mode === 'password') cls = 'badge-password';
        else if (mode === 'both') cls = 'badge-both';
        return '<span class="badge ' + cls + '">' + esc(mode) + '</span>';
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
            content.innerHTML = '<h2 class="page-title">页面未找到</h2><p>未知路由: ' + esc(hash) + '</p>';
        }
    }

    // ====================================================================
    // WORKERS PAGE
    // ====================================================================

    registerRoute('/workers', async function (content) {
        content.innerHTML = '<h2 class="page-title">Worker 节点</h2>' +
            '<button class="btn btn-primary btn-sm" id="btn-new-worker">+ 新建 Worker</button>' +
            '<div id="workers-msg" class="info-msg"></div>' +
            '<table class="data-table mt-2" id="workers-table"><thead><tr>' +
            '<th>ID</th><th>名称</th><th>主机</th><th>端口</th><th>用户名</th><th>认证</th><th>状态</th><th>最近在线</th><th>操作</th>' +
            '</tr></thead><tbody id="workers-tbody"><tr><td colspan="9" class="muted">加载中...</td></tr></tbody></table>';

        document.getElementById('btn-new-worker').addEventListener('click', function () {
            showWorkerForm(content, null);
        });

        try {
            var r = await apiJSON('/workers');
            if (!r.resp.ok) { setMsg(document.getElementById('workers-msg'), '错误: ' + (r.data && r.data.error), 'error'); return; }
            var workers = r.data || [];
            var tbody = document.getElementById('workers-tbody');
            if (workers.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" class="muted">暂无 Worker。</td></tr>';
                return;
            }
            tbody.innerHTML = workers.map(function (w) {
                return '<tr>' +
                    '<td>' + esc(w.id) + '</td>' +
                    '<td>' + esc(w.name) + '</td>' +
                    '<td>' + esc(w.host) + '</td>' +
                    '<td>' + esc(w.port) + '</td>' +
                    '<td>' + esc(w.username) + '</td>' +
                    '<td>' + authModeBadge(w.auth_mode) + '</td>' +
                    '<td>' + statusBadge(w.status) + '</td>' +
                    '<td>' + esc(fmtTime(w.last_seen_at)) + '</td>' +
                    '<td>' +
                    '<button class="btn btn-sm btn-primary" data-action="edit" data-id="' + w.id + '">编辑</button> ' +
                    '<button class="btn btn-sm btn-success" data-action="test" data-id="' + w.id + '">测试</button> ' +
                    '<button class="btn btn-sm btn-primary" data-action="creds" data-id="' + w.id + '">凭证</button> ' +
                    '<button class="btn btn-sm btn-primary" data-action="install-deps" data-id="' + w.id + '">安装依赖</button> ' +
                    '<button class="btn btn-sm btn-danger" data-action="delete" data-id="' + w.id + '">删除</button>' +
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
            '<h3 class="modal-title">' + (isEdit ? '编辑 Worker' : '新建 Worker') + '</h3>' +
            '<form id="worker-form">' +
            (isEdit ? '' :
            '<div class="form-field"><label>从集群节点选择(可选)</label>' +
            '<select id="worker-node-select"><option value="">-- 手动填写或选择集群节点 --</option></select>' +
            '<p class="muted" style="font-size:12px;">选中后自动填入名称/主机。</p></div>') +
            '<div class="form-field"><label>名称</label><input type="text" name="name" value="' + esc(worker ? worker.name : '') + '" required></div>' +
            '<div class="form-field"><label>主机</label><input type="text" name="host" value="' + esc(worker ? worker.host : '') + '" required></div>' +
            '<div class="form-field"><label>端口</label><input type="number" name="port" value="' + esc(worker ? worker.port : 22) + '"></div>' +
            '<div class="form-field"><label>用户名</label><input type="text" name="username" value="' + esc(worker ? worker.username : 'root') + '"></div>' +
            '<div class="form-field"><label>SSH 密码' + (isEdit ? '(留空不修改)' : '(可选,与用户名一起用于密码登录)') + '</label><input type="password" name="password" placeholder="留空则后续在凭证中设置"></div>' +
            '<div class="row mt-2"><button type="submit" class="btn btn-primary">保存</button> ' +
            '<button type="button" class="btn btn-link" id="worker-cancel" style="color:#555;">取消</button></div>' +
            '<div id="worker-form-msg" class="error-msg"></div>' +
            '</form></div></div>';
        content.insertAdjacentHTML('beforeend', html);

        var modal = document.getElementById('worker-modal');
        document.getElementById('worker-cancel').addEventListener('click', function () { modal.remove(); });

        // New-worker mode: load cluster nodes into the dropdown; selecting one
        // prefills name + host so the admin only needs SSH credentials.
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
                // If a password was entered, store it as the panel-side SSH
                // password (encrypted at rest) via the credentials endpoint.
                var pw = form.password.value;
                if (pw) {
                    var wid = isEdit ? id : (r.data && r.data.id);
                    if (wid) {
                        var pr = await apiJSON('/workers/' + wid + '/credentials/password', { method: 'POST', body: JSON.stringify({ password: pw }) });
                        if (!pr.resp.ok) { setMsg(msgEl, 'Worker 已保存,但密码设置失败: ' + (pr.data && pr.data.error), 'error'); return; }
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
                alert('连接正常');
            } else {
                alert('连接失败: ' + (r.data && r.data.error || '未知'));
            }
            handleRoute();
        } catch (err) { alert('错误: ' + err.message); }
    }

    async function doDeleteWorker(content, id) {
        if (!confirm('确认删除 Worker ' + id + '?')) return;
        try {
            var r = await apiJSON('/workers/' + id, { method: 'DELETE' });
            if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
            handleRoute();
        } catch (err) { alert('错误: ' + err.message); }
    }

    // Credentials form: set private key, set panel password, change root password
    async function showCredentialsForm(content, id) {
        // Fetch worker to show auth_mode
        var worker = null;
        try {
            var r = await apiJSON('/workers/' + id);
            if (r.resp.ok) worker = r.data;
        } catch (e) { /* ignore */ }

        var html = '<div class="modal-overlay" id="creds-modal">' +
            '<div class="modal">' +
            '<h3 class="modal-title">Worker #' + esc(id) + ' Credentials' +
            (worker ? ' <span class="muted">(认证: ' + esc(worker.auth_mode) + ')</span>' : '') + '</h3>' +
            '<p class="muted mb-1">Credential values are encrypted at rest and never returned by the API.</p>' +

            '<div class="card"><div class="section-title">Set Private Key (Interface 1: panel-side)</div>' +
            '<form id="set-key-form">' +
            '<div class="form-field"><label>私钥 (PEM)</label><textarea name="private_key" rows="4" placeholder="-----BEGIN RSA PRIVATE KEY-----&#10;...&#10;-----END RSA PRIVATE KEY-----"></textarea></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">设置私钥</button>' +
            '<div id="set-key-msg" class="error-msg"></div></form></div>' +

            '<div class="card"><div class="section-title">Set Panel Password (Interface 1: panel-side)</div>' +
            '<form id="set-pw-form">' +
            '<div class="form-field"><label>密码</label><input type="password" name="password"></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">设置密码</button>' +
            '<div id="set-pw-msg" class="error-msg"></div></form></div>' +

            '<div class="card"><div class="section-title">Change Root Password (Interface 2: push to worker via SSH)</div>' +
            '<form id="root-pw-form">' +
            '<div class="form-field"><label>新 root 密码</label><input type="password" name="password"></div>' +
            '<button type="submit" class="btn btn-danger btn-sm">修改 root 密码</button>' +
            '<div id="root-pw-msg" class="error-msg"></div>' +
            '<p class="muted mt-1">This submits an async task (chpasswd via SSH). You will be redirected to the task page.</p></form></div>' +

            '<button type="button" class="btn btn-link mt-2" id="creds-cancel" style="color:#555;">关闭</button>' +
            '</div></div>';
        content.insertAdjacentHTML('beforeend', html);

        var modal = document.getElementById('creds-modal');
        document.getElementById('creds-cancel').addEventListener('click', function () { modal.remove(); });

        // Set private key
        document.getElementById('set-key-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { private_key: e.target.private_key.value };
            var msgEl = document.getElementById('set-key-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/credentials/private-key', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, '私钥已设置。', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        // Set panel password
        document.getElementById('set-pw-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { password: e.target.password.value };
            var msgEl = document.getElementById('set-pw-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/credentials/password', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, '面板密码已设置。', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        // Change root password (async -> task)
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

    // install-deps: confirm -> POST -> navigate to task page (same pattern as
    // changeRootPassword but no form needed - just worker_id in params).
    async function doInstallDeps(content, id) {
        if (!confirm('确认经 SSH 在 Worker #' + id + ' 上安装 lvm2/nfs-utils?')) return;
        try {
            var r = await apiJSON('/workers/' + id + '/install-deps', { method: 'POST' });
            if (!r.resp.ok) { alert('错误: ' + (r.data && r.data.error)); return; }
            var taskID = r.data && r.data.task_id;
            window.location.hash = '#/tasks/' + taskID;
        } catch (err) { alert('错误: ' + err.message); }
    }

    // ====================================================================
    // K8S PAGE (Pod-centric port mapping)
    var k8sServices = []; // notebook-namespace Services, refreshed with the pod list

    registerRoute('/k8s', async function (content) {
        content.innerHTML = '<h2 class="page-title">端口映射 (Pod -> Service)</h2>' +
            '<p class="muted">每个 notebook Pod 的已有端口映射(含非本面板创建的)按 Pod 分组显示。点击「端口映射」查看该 Pod 已有映射并新增。</p>' +
            '<div class="card">' +
            '<div class="section-title">Notebook Pod 列表</div>' +
            '<button class="btn btn-primary btn-sm" id="btn-load-pods">刷新 Pod 列表</button>' +
            '<div id="pods-msg" class="info-msg"></div>' +
            '<table class="data-table mt-2" id="pods-table"><thead><tr>' +
            '<th>Pod 名称</th><th>命名空间</th><th>节点</th><th>状态</th><th>IP</th><th>已有映射</th><th>操作</th>' +
            '</tr></thead><tbody id="pods-tbody"><tr><td colspan="7" class="muted">点击刷新加载。</td></tr></tbody></table>' +
            '</div>';

        document.getElementById('btn-load-pods').addEventListener('click', function () { loadPods(content); });
        loadPods(content);
    });

    // servicesForPod returns the cached Services that route to the given pod
    // (selector match, attributed by the backend via the pods field).
    function servicesForPod(podUid) {
        return k8sServices.filter(function (s) {
            return (s.pods || []).some(function (p) { return p.uid === podUid; });
        });
    }

    async function loadPods(content) {
        var tbody = document.getElementById('pods-tbody');
        var msgEl = document.getElementById('pods-msg');
        tbody.innerHTML = '<tr><td colspan="7" class="muted">加载中...</td></tr>';
        try {
            // Load pods and Services in parallel; Services are cached so the
            // per-pod "已有映射" count and the port-mapping modal can render them.
            var results = await Promise.all([apiJSON('/k8s/pods'), apiJSON('/k8s/services')]);
            var pr = results[0], sr = results[1];
            if (!pr.resp.ok) { setMsg(msgEl, '错误: ' + (pr.data && pr.data.error), 'error'); tbody.innerHTML = ''; return; }
            k8sServices = (sr.resp.ok && Array.isArray(sr.data)) ? sr.data : [];
            var pods = pr.data || [];
            if (pods.length === 0) { tbody.innerHTML = '<tr><td colspan="7" class="muted">未找到 notebook Pod(name 含 notebook)。</td></tr>'; return; }
            tbody.innerHTML = pods.map(function (p) {
                var cnt = servicesForPod(p.uid).length;
                return '<tr>' +
                    '<td>' + esc(p.name) + '</td>' +
                    '<td>' + esc(p.namespace) + '</td>' +
                    '<td>' + esc(p.node) + '</td>' +
                    '<td>' + statusBadge(p.status) + '</td>' +
                    '<td>' + esc((p.ips || []).join(', ')) + '</td>' +
                    '<td>' + (cnt > 0 ? '<span class="badge badge-success">' + cnt + '</span>' : '<span class="muted">-</span>') + '</td>' +
                    '<td><button class="btn btn-sm btn-success" data-pod=\'' + esc(JSON.stringify(p)) + '\'>端口映射</button></td>' +
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
        var html = '<div class="modal-overlay" id="port-modal"><div class="modal">' +
            '<h3 class="modal-title">端口映射 - ' + esc(pod.name) + '</h3>' +
            '<div class="card"><div class="section-title">该 Pod 已有的端口映射</div>' +
            '<p class="muted" style="font-size:12px;">含非本面板创建的已有映射。<span class="badge badge-success">本面板</span> 可删除,<span class="badge badge-muted">外部</span> 只读。</p>' +
            '<table class="data-table" id="pod-svc-table"><thead><tr><th>名称</th><th>类型</th><th>外部端口(NodePort)</th><th>内部端口(Port->Target)</th><th>来源</th><th>操作</th></tr></thead>' +
            '<tbody id="pod-existing-tbody"><tr><td colspan="6" class="muted">加载中...</td></tr></tbody></table></div>' +
            '<div class="card mt-2"><div class="section-title">新增端口映射</div>' +
            '<p class="muted">Service 与 NetworkPolicy 自动绑定到该 Pod(随 Pod 生命周期自动删除)。只需输入要映射的端口。</p>' +
            '<form id="port-form">' +
            '<div class="form-field"><label>命名空间</label><input type="text" name="namespace" value="' + esc(pod.namespace) + '" readonly></div>' +
            '<div class="form-field"><label>Pod 名称</label><input type="text" value="' + esc(pod.name) + '" readonly></div>' +
            '<div class="form-field"><label>Service 类型</label><select name="type"><option value="NodePort">NodePort</option><option value="ClusterIP">ClusterIP</option></select></div>' +
            '<div class="form-field"><label>要映射的端口 (逗号分隔,如 8080,22 或 8080:80)</label><input type="text" name="ports" placeholder="8080,22" required></div>' +
            '<p class="muted" style="font-size:12px;">格式: 端口 或 端口:目标端口。NetworkPolicy 会自动放行这些端口。</p>' +
            '<button type="submit" class="btn btn-primary">创建映射</button> <button type="button" class="btn btn-link" id="port-cancel" style="color:#555;">取消</button>' +
            '<div id="port-form-msg" class="error-msg"></div></form></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('port-modal');
        document.getElementById('port-cancel').addEventListener('click', function () { modal.remove(); });
        renderExistingMappings(modal, pod);
        document.getElementById('port-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var f = e.target;
            var ports = (f.ports.value || '').split(',').filter(Boolean).map(function (p) {
                var parts = p.split(':');
                var port = parseInt(parts[0], 10);
                return { port: port, target_port: parseInt(parts[1] || parts[0], 10), node_port: 0, protocol: 'TCP' };
            });
            var body = {
                namespace: pod.namespace, pod_name: pod.name, pod_uid: pod.uid,
                selector: pod.labels || {}, type: f.type.value, ports: ports
            };
            var msgEl = document.getElementById('port-form-msg');
            try {
                var r = await apiJSON('/k8s/services', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    // renderExistingMappings fills the modal's "该 Pod 已有的端口映射" table with
    // the cached Services that route to this pod (managed + external). Managed
    // rows get a delete button; external rows are read-only. Delete navigates
    // to the task page (async, consistent with create).
    function renderExistingMappings(scope, pod) {
        var el = scope.querySelector('#pod-existing-tbody');
        if (!el) return;
        var mine = servicesForPod(pod.uid);
        if (mine.length === 0) {
            el.innerHTML = '<tr><td colspan="6" class="muted">该 Pod 暂无已有端口映射。</td></tr>';
            return;
        }
        // Managed (ours) first, then external - ours are the actionable ones.
        mine.sort(function (a, b) { return (a.managed === b.managed) ? 0 : (a.managed ? -1 : 1); });
        el.innerHTML = mine.map(function (s) {
            var ports = s.ports || [];
            var extPorts = ports.length ? ports.map(function (p) { return (p.node_port || '-') + '/' + (p.protocol || 'TCP'); }).join(', ') : '-';
            var intPorts = ports.length ? ports.map(function (p) { return p.port + '->' + (p.target_port || p.port); }).join(', ') : '-';
            var srcBadge = s.managed ? '<span class="badge badge-success">本面板</span>' : '<span class="badge badge-muted">外部</span>';
            var action = s.managed
                ? '<button class="btn btn-sm btn-danger" data-name="' + esc(s.name) + '" data-ns="' + esc(s.namespace) + '">删除</button>'
                : '<span class="muted" style="font-size:12px;">只读</span>';
            return '<tr><td>' + esc(s.name) + '</td><td>' + esc(s.type) + '</td><td>' + esc(extPorts) + '</td><td>' + esc(intPorts) + '</td><td>' + srcBadge + '</td>' +
                '<td>' + action + '</td></tr>';
        }).join('');
        el.querySelectorAll('button[data-name]').forEach(function (btn) {
            btn.addEventListener('click', async function () {
                if (!confirm('确认删除 Service ' + this.getAttribute('data-name') + '?')) return;
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

    registerRoute('/storage', async function (content) {
        content.innerHTML = '<h2 class="page-title">NFS 存储编排</h2>' +
            '<div class="card">' +
            '<div class="section-title">Worker 节点</div>' +
            '<div class="form-field"><label>选择 Worker</label><select id="st-worker-select"><option value="">-- 选择 Worker --</option></select></div>' +
            '<div id="st-inv-msg" class="info-msg"></div>' +
            '</div>' +
            // Block A: VG pool management
            '<div class="card mt-2">' +
            '<div class="section-title">存储池 (VG) 管理</div>' +
            '<button class="btn btn-primary btn-sm" id="btn-init-vg" disabled>初始化 VG 池 (从未挂载盘)</button>' +
            '<span id="st-vg-summary" class="muted"></span>' +
            '<table class="data-table mt-2" id="st-vg-table"><thead><tr><th>VG 名称</th><th>总量</th><th>剩余</th></tr></thead>' +
            '<tbody id="st-vg-tbody"><tr><td colspan="3" class="muted">先选择 Worker。</td></tr></tbody></table>' +
            '</div>' +
            // Block B: LV management
            '<div class="card mt-2">' +
            '<div class="section-title">逻辑卷 (LV) 管理 <span class="muted" style="font-size:12px;">(含非本面板创建的 LV,可扩容/缩容/删除释放空间)</span></div>' +
            '<table class="data-table" id="st-lv-table"><thead><tr><th>名称</th><th>VG</th><th>大小(GB)</th><th>挂载点</th><th>文件系统</th><th>操作</th></tr></thead>' +
            '<tbody id="st-lv-tbody"><tr><td colspan="6" class="muted">先选择 Worker。</td></tr></tbody></table>' +
            '</div>' +
            // Block C: create NFS share
            '<div class="card mt-2">' +
            '<div class="section-title">创建 NFS 共享</div>' +
            '<div class="form-field"><label>Volume Group</label><select id="st-vg-select" disabled><option value="">-- 先选 Worker --</option></select> <span id="st-vg-free" class="muted"></span></div>' +
            '<div class="form-field"><label>大小 (GB)</label><input type="number" id="st-nfs-size" placeholder="如 200"></div>' +
            '<button class="btn btn-primary" id="btn-nfs-create" disabled>创建 NFS</button>' +
            '<div id="st-nfs-msg" class="error-msg"></div>' +
            '<p class="muted mt-1" style="font-size:12px;">逻辑卷名/挂载点/导出选项自动生成。异步任务,成功后跳转任务页。</p>' +
            '</div>' +
            // Block D: NFS shares list
            '<div class="card mt-2">' +
            '<div class="section-title">NFS 共享列表 (最近任务)</div>' +
            '<table class="data-table" id="st-storage-table"><thead><tr><th>ID</th><th>类型</th><th>Worker</th><th>状态</th><th>创建时间</th><th>完成时间</th><th>操作</th></tr></thead>' +
            '<tbody id="st-storage-tbody"><tr><td colspan="7" class="muted">加载中...</td></tr></tbody></table></div>';

        var wsel = document.getElementById('st-worker-select');
        var lastInventory = null; // cached for the init-VG modal

        // Load workers into the dropdown.
        try {
            var r = await apiJSON('/workers');
            if (r.resp.ok && Array.isArray(r.data)) {
                r.data.forEach(function (w) { var o = document.createElement('option'); o.value = w.id; o.textContent = w.name + ' (' + w.host + ')'; wsel.appendChild(o); });
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
            // reset
            btnInit.disabled = true; btnNfs.disabled = true; vsel.disabled = true;
            vsel.innerHTML = '<option value="">加载中...</option>';
            vfree.textContent = ''; summary.textContent = '';
            vgTbody.innerHTML = '<tr><td colspan="3" class="muted">加载中...</td></tr>';
            lvTbody.innerHTML = '<tr><td colspan="6" class="muted">加载中...</td></tr>';
            try {
                var r = await apiJSON('/storage/inventory?worker_id=' + encodeURIComponent(wid));
                if (!r.resp.ok) {
                    var err = (r.data && r.data.error) || '加载失败';
                    setMsg(invMsg, '加载存储清单失败: ' + err + ' (若未安装 lvm2/nfs,先点 Worker 页的"安装依赖")', 'error');
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">加载失败</td></tr>';
                    lvTbody.innerHTML = '<tr><td colspan="6" class="muted">加载失败</td></tr>';
                    vsel.innerHTML = '<option value="">-- 加载失败 --</option>';
                    return;
                }
                setMsg(invMsg, '', 'info');
                var inv = r.data || { vgs: [], lvs: [], unused_disks: [] };
                lastInventory = inv;

                // VG table
                var vgs = inv.vgs || [];
                if (vgs.length === 0) {
                    vgTbody.innerHTML = '<tr><td colspan="3" class="muted">无 VG。可从未挂载盘初始化一个 vg_data。</td></tr>';
                } else {
                    vgTbody.innerHTML = vgs.map(function (v) {
                        return '<tr><td>' + esc(v.name) + '</td><td>' + esc(v.vsize) + '</td><td>' + esc(v.vfree) + ' (' + (v.free_gb || 0).toFixed(1) + 'G)</td></tr>';
                    }).join('');
                }

                // Unused-disk summary + init button
                var disks = inv.unused_disks || [];
                if (disks.length > 0) {
                    btnInit.disabled = false;
                    summary.textContent = '发现 ' + disks.length + ' 块未挂载盘可创建 VG 池。';
                } else {
                    summary.textContent = '无未挂载盘可用于新建 VG 池。';
                }

                // LV table with resize/delete actions
                var lvs = inv.lvs || [];
                if (lvs.length === 0) {
                    lvTbody.innerHTML = '<tr><td colspan="6" class="muted">无逻辑卷。</td></tr>';
                } else {
                    lvTbody.innerHTML = lvs.map(function (lv) {
                        var data = JSON.stringify({ vg: lv.vg_name, name: lv.name, size: lv.size_gb, mp: lv.mount_point, fs: lv.fs_type });
                        return '<tr><td>' + esc(lv.name) + '</td><td>' + esc(lv.vg_name) + '</td><td>' + (lv.size_gb || 0).toFixed(1) + '</td><td>' + esc(lv.mount_point || '-') + '</td><td>' + esc(lv.fs_type || '-') + '</td>' +
                            '<td><button class="btn btn-sm btn-primary" data-act="grow" data-lv=\'' + esc(data) + '\'>扩容</button> ' +
                            '<button class="btn btn-sm btn-primary" data-act="shrink" data-lv=\'' + esc(data) + '\'>缩容</button> ' +
                            '<button class="btn btn-sm btn-danger" data-act="delete" data-lv=\'' + esc(data) + '\'>删除</button></td></tr>';
                    }).join('');
                    lvTbody.querySelectorAll('button[data-act]').forEach(function (btn) {
                        btn.addEventListener('click', function () {
                            var lv = JSON.parse(this.getAttribute('data-lv'));
                            var act = this.getAttribute('data-act');
                            if (act === 'delete') doDeleteLV(content, wid, lv);
                            else showResizeLVForm(content, wid, lv, act);
                        });
                    });
                }

                // NFS form VG dropdown
                if (vgs.length === 0) {
                    vsel.innerHTML = '<option value="">-- 该节点无 VG --</option>';
                } else {
                    vsel.innerHTML = '';
                    vgs.forEach(function (v) {
                        var o = document.createElement('option');
                        o.value = v.name;
                        o.textContent = v.name + ' (剩余 ' + (v.free_gb || 0).toFixed(1) + 'G / 共 ' + v.vsize + ')';
                        vsel.appendChild(o);
                    });
                    vsel.disabled = false; btnNfs.disabled = false;
                    vfree.textContent = '可用 ' + (vgs[0].free_gb || 0).toFixed(1) + ' GB';
                    vsel.onchange = function () {
                        var cur = vgs.find(function (x) { return x.name === vsel.value; });
                        vfree.textContent = cur ? '可用 ' + (cur.free_gb || 0).toFixed(1) + ' GB' : '';
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

        // Init VG pool: modal listing unused disks -> POST /storage/vg.
        document.getElementById('btn-init-vg').addEventListener('click', function () {
            if (!wsel.value || !lastInventory) return;
            showInitVGForm(content, parseInt(wsel.value, 10), lastInventory.unused_disks || [], function () {
                loadInventory(wsel.value);
            });
        });

        // Create NFS share.
        document.getElementById('btn-nfs-create').addEventListener('click', async function () {
            var wid = parseInt(wsel.value, 10);
            var vg = document.getElementById('st-vg-select').value;
            var size = parseInt(document.getElementById('st-nfs-size').value, 10);
            var msgEl = document.getElementById('st-nfs-msg');
            if (!wid || !vg || !size) { setMsg(msgEl, '请选择 Worker、VG 并输入大小', 'error'); return; }
            var lv = 'lv_nb_' + Date.now().toString(36);
            var mp = '/data02/nfs_' + lv;
            try {
                var r = await apiJSON('/storage/provision', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: vg, lv_name: lv, size_gb: size, fs_type: 'ext4', mount_point: mp }) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                window.location.hash = '#/tasks/' + (r.data && r.data.task_id);
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });

        // Load NFS tasks with a delete (reclaim) action.
        try {
            var r2 = await apiJSON('/storage');
            var tbody = document.getElementById('st-storage-tbody');
            if (!r2.resp.ok) { tbody.innerHTML = '<tr><td colspan="7" class="muted">加载失败</td></tr>'; return; }
            var tasks = r2.data || [];
            var shares = tasks.filter(function (t) { return t.type === 'storage_provision_nfs' && t.status === 'succeeded'; });
            if (shares.length === 0) { tbody.innerHTML = '<tr><td colspan="7" class="muted">暂无已创建的 NFS 共享。</td></tr>'; return; }
            tbody.innerHTML = shares.map(function (t) {
                return '<tr><td>' + esc(t.id) + '</td><td>' + esc(t.type) + '</td><td>' + esc(t.target_id) + '</td><td>' + statusBadge(t.status) + '</td><td>' + esc(fmtTime(t.created_at)) + '</td><td>' + esc(fmtTime(t.finished_at)) + '</td>' +
                    '<td><button class="btn btn-sm btn-danger" data-task=\'' + esc(JSON.stringify(t)) + '\'>删除</button></td></tr>';
            }).join('');
            tbody.querySelectorAll('button[data-task]').forEach(function (btn) {
                btn.addEventListener('click', async function () {
                    var t = JSON.parse(this.getAttribute('data-task'));
                    if (!confirm('确认回收该 NFS 共享 (任务 #' + t.id + ')?空间将归还 VG。')) return;
                    try {
                        var rr = await apiJSON('/storage/reclaim', { method: 'POST', body: JSON.stringify({ task_id: t.id }) });
                        if (!rr.resp.ok) { alert('错误: ' + (rr.data && rr.data.error)); return; }
                        window.location.hash = '#/tasks/' + (rr.data && rr.data.task_id);
                    } catch (err) { alert('错误: ' + err.message); }
                });
            });
        } catch (err) {}
    });

    // Init VG pool modal: lists unused disks (checkboxes, default all) + vg name.
    async function showInitVGForm(content, wid, disks, onDone) {
        if (!disks || disks.length === 0) { alert('该节点没有未挂载盘可用于创建 VG 池。'); return; }
        var diskRows = disks.map(function (d, i) {
            return '<label style="display:block;margin:4px 0;"><input type="checkbox" data-disk="' + esc(d.name) + '" checked> ' + esc(d.name) + ' <span class="muted">(' + (d.size_gb || 0).toFixed(1) + ' GB)</span></label>';
        }).join('');
        var html = '<div class="modal-overlay" id="vg-modal"><div class="modal">' +
            '<h3 class="modal-title">初始化 VG 池</h3>' +
            '<p class="muted">把以下未挂载盘 pvcreate 后合并成一个 VG(已有同名 VG 则 vgextend 加入)。<b>会擦除盘上现有数据。</b></p>' +
            '<div class="form-field"><label>VG 名称</label><input type="text" id="vg-name-input" value="vg_data"></div>' +
            '<div class="form-field"><label>未挂载盘</label>' + diskRows + '</div>' +
            '<button type="button" class="btn btn-primary" id="vg-create-btn">创建</button> ' +
            '<button type="button" class="btn btn-link" id="vg-cancel" style="color:#555;">取消</button>' +
            '<div id="vg-msg" class="error-msg"></div></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('vg-modal');
        document.getElementById('vg-cancel').addEventListener('click', function () { modal.remove(); });
        document.getElementById('vg-create-btn').addEventListener('click', async function () {
            var vgName = document.getElementById('vg-name-input').value.trim();
            var chosen = Array.from(modal.querySelectorAll('input[data-disk]:checked')).map(function (c) { return c.getAttribute('data-disk'); });
            var msgEl = document.getElementById('vg-msg');
            if (!vgName) { setMsg(msgEl, '请输入 VG 名称', 'error'); return; }
            if (chosen.length === 0) { setMsg(msgEl, '至少选择一块盘', 'error'); return; }
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

    // Resize LV modal: grow/shrink by delta GB.
    async function showResizeLVForm(content, wid, lv, action) {
        var isGrow = action === 'grow';
        var html = '<div class="modal-overlay" id="rsz-modal"><div class="modal">' +
            '<h3 class="modal-title">' + (isGrow ? '扩容' : '缩容') + ' LV - ' + esc(lv.name) + '</h3>' +
            '<p class="muted">当前大小 ' + (lv.size || 0).toFixed(1) + ' GB,文件系统 ' + esc(lv.fs || '未知') + '。</p>' +
            '<div class="form-field"><label>变化量 (GB)</label><input type="number" id="rsz-delta" placeholder="如 50" min="1"></div>' +
            (isGrow ? '' : '<p class="muted" style="font-size:12px;">缩容会先缩小文件系统再缩减 LV。<b>xfs 不支持缩容,ext4 缩容有数据风险,请先备份。</b></p>') +
            '<button type="button" class="btn btn-primary" id="rsz-go">' + (isGrow ? '扩容' : '缩容') + '</button> ' +
            '<button type="button" class="btn btn-link" id="rsz-cancel" style="color:#555;">取消</button>' +
            '<div id="rsz-msg" class="error-msg"></div></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('rsz-modal');
        document.getElementById('rsz-cancel').addEventListener('click', function () { modal.remove(); });
        document.getElementById('rsz-go').addEventListener('click', async function () {
            var delta = parseInt(document.getElementById('rsz-delta').value, 10);
            var msgEl = document.getElementById('rsz-msg');
            if (!delta || delta <= 0) { setMsg(msgEl, '请输入正整数 GB', 'error'); return; }
            try {
                var r = await apiJSON('/storage/lv/resize', { method: 'POST', body: JSON.stringify({ worker_id: wid, vg_name: lv.vg, lv_name: lv.name, action: action, delta_gb: delta }) });
                if (!r.resp.ok) { setMsg(msgEl, '错误: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                window.location.hash = '#/tasks/' + (r.data && r.data.task_id);
            } catch (err) { setMsg(msgEl, '错误: ' + err.message, 'error'); }
        });
    }

    // Delete LV: confirm (tears down exports/fstab/umount + lvremove, releases space).
    async function doDeleteLV(content, wid, lv) {
        var detail = 'LV ' + lv.vg + '/' + lv.name + ' (' + (lv.size || 0).toFixed(1) + ' GB' + (lv.mp ? ', 挂载于 ' + lv.mp : ', 未挂载') + ')';
        if (!confirm('确认删除 ' + detail + '?\n将先卸载并清理 /etc/exports、/etc/fstab,再 lvremove,空间归还 VG。\n该操作不可逆,请确认数据已备份。')) return;
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
        content.innerHTML = '<h2 class="page-title">任务列表</h2>' +
            '<table class="data-table" id="tasks-table"><thead><tr>' +
            '<th>ID</th><th>类型</th><th>目标</th><th>状态</th><th>错误</th><th>创建时间</th><th>完成时间</th>' +
            '</tr></thead><tbody id="tasks-tbody"><tr><td colspan="7" class="muted">加载中...</td></tr></tbody></table>';

        try {
            var r = await apiJSON('/tasks');
            if (!r.resp.ok) { return; }
            var tasks = r.data || [];
            var tbody = document.getElementById('tasks-tbody');
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="muted">暂无任务。</td></tr>';
                return;
            }
            tbody.innerHTML = tasks.map(function (t) {
                return '<tr style="cursor:pointer" data-href="#/tasks/' + t.id + '">' +
                    '<td>' + esc(t.id) + '</td>' +
                    '<td>' + esc(t.type) + '</td>' +
                    '<td>' + esc(t.target_kind) + '/' + esc(t.target_id) + '</td>' +
                    '<td>' + statusBadge(t.status) + '</td>' +
                    '<td>' + esc(t.error ? (t.error.length > 50 ? t.error.substring(0, 50) + '...' : t.error) : '-') + '</td>' +
                    '<td>' + esc(fmtTime(t.created_at)) + '</td>' +
                    '<td>' + esc(fmtTime(t.finished_at)) + '</td>' +
                    '</tr>';
            }).join('');
            tbody.querySelectorAll('tr[data-href]').forEach(function (tr) {
                tr.addEventListener('click', function () { window.location.hash = this.getAttribute('data-href'); });
            });
        } catch (err) { /* ignore */ }
    });

    // Task detail with SSE live updates
    var currentSSE = null;

    function closeSSE() {
        if (currentSSE) { currentSSE.close(); currentSSE = null; }
    }

    registerRoute('/tasks/', async function (content, hash) {
        var id = hash.split('/')[2];
        closeSSE();

        content.innerHTML = '<h2 class="page-title">任务 #' + esc(id) + '</h2>' +
            '<div class="card" id="task-info"><p class="muted">加载中...</p></div>' +
            '<div class="card"><div class="section-title">执行步骤 (SSE 实时)</div>' +
            '<div id="steps-container"></div></div>' +
            '<div id="task-error" class="error-msg"></div>';

        // Fetch task detail
        try {
            var r = await apiJSON('/tasks/' + id);
            if (!r.resp.ok) {
                document.getElementById('task-info').innerHTML = '<p class="error-msg">任务未找到。</p>';
                return;
            }
            var result = r.data;
            var task = result.task || result;
            var steps = result.steps || [];

            renderTaskInfo(task);
            renderSteps(steps);

            // Subscribe to SSE if task is not finished
            if (task.status === 'pending' || task.status === 'running') {
                subscribeSSE(id);
            }
        } catch (err) {
            document.getElementById('task-error').textContent = '错误: ' + err.message;
        }
    });

    function renderTaskInfo(task) {
        var el = document.getElementById('task-info');
        if (!el) return;
        el.innerHTML = '<div class="row">' +
            '<div class="col"><strong>ID:</strong> ' + esc(task.id) + '</div>' +
            '<div class="col"><strong>类型:</strong> ' + esc(task.type) + '</div>' +
            '<div class="col"><strong>目标:</strong> ' + esc(task.target_kind) + '/' + esc(task.target_id) + '</div>' +
            '</div><div class="row mt-1">' +
            '<div class="col"><strong>状态:</strong> ' + statusBadge(task.status) + '</div>' +
            '<div class="col"><strong>创建:</strong> ' + esc(fmtTime(task.created_at)) + '</div>' +
            '<div class="col"><strong>开始:</strong> ' + esc(fmtTime(task.started_at)) + '</div>' +
            '<div class="col"><strong>完成:</strong> ' + esc(fmtTime(task.finished_at)) + '</div>' +
            '</div>' +
            (task.error ? '<div class="error-msg mt-1">' + esc(task.error) + '</div>' : '');
    }

    function renderSteps(steps) {
        var el = document.getElementById('steps-container');
        if (!el) return;
        if (!steps || steps.length === 0) {
            el.innerHTML = '<p class="muted">暂无步骤。</p>';
            return;
        }
        el.innerHTML = steps.map(function (s) {
            return '<div class="step-item ' + esc(s.status) + '">' +
                '<div class="step-name">' + esc(s.seq) + '. ' + esc(s.name) + ' ' + statusBadge(s.status) + '</div>' +
                (s.stdout ? '<div class="step-stdout">' + esc(s.stdout) + '</div>' : '') +
                (s.stderr ? '<div class="step-stderr">' + esc(s.stderr) + '</div>' : '') +
                (s.error ? '<div class="step-stderr">Error: ' + esc(s.error) + '</div>' : '') +
                '</div>';
        }).join('');
    }

    function subscribeSSE(taskID) {
        var token = getToken();
        if (!token) return;
        var url = '/api/v1/tasks/' + taskID + '/stream?token=' + encodeURIComponent(token);
        var es = new EventSource(url);
        currentSSE = es;

        es.addEventListener('task', function (e) {
            try {
                var task = JSON.parse(e.data);
                renderTaskInfo(task);
                if (task.status !== 'pending' && task.status !== 'running') {
                    closeSSE();
                }
            } catch (err) { /* ignore parse errors */ }
        });

        es.addEventListener('step', function (e) {
            try {
                var step = JSON.parse(e.data);
                // Fetch the full steps list to re-render
                apiJSON('/tasks/' + taskID).then(function (r) {
                    if (r.resp.ok && r.data && r.data.steps) {
                        renderSteps(r.data.steps);
                    }
                }).catch(function () {});
            } catch (err) { /* ignore */ }
        });

        es.onerror = function () {
            // EventSource auto-reconnects; if the task is done, close.
            // We'll let it reconnect and the 'task' event will close it if finished.
        };
    }

    // ====================================================================
    // AUDIT PAGE
    // ====================================================================

    registerRoute('/audit', async function (content) {
        content.innerHTML = '<h2 class="page-title">审计日志</h2>' +
            '<table class="data-table" id="audit-table"><thead><tr>' +
            '<th>ID</th><th>操作者</th><th>动作</th><th>目标</th><th>结果</th><th>时间</th>' +
            '</tr></thead><tbody id="audit-tbody"><tr><td colspan="6" class="muted">加载中...</td></tr></tbody></table>';

        try {
            var r = await apiJSON('/audit-log');
            if (!r.resp.ok) { return; }
            var logs = r.data || [];
            var tbody = document.getElementById('audit-tbody');
            if (logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="muted">暂无审计记录。</td></tr>';
                return;
            }
            tbody.innerHTML = logs.map(function (a) {
                return '<tr>' +
                    '<td>' + esc(a.id) + '</td>' +
                    '<td>' + esc(a.actor) + '</td>' +
                    '<td>' + esc(a.action) + '</td>' +
                    '<td>' + esc(a.target) + '</td>' +
                    '<td>' + statusBadge(a.result) + '</td>' +
                    '<td>' + esc(fmtTime(a.at)) + '</td>' +
                    '</tr>';
            }).join('');
        } catch (err) { /* ignore */ }
    });

    // ===== Init =====
    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
        document.getElementById('logout-btn').addEventListener('click', handleLogout);
        window.addEventListener('hashchange', function () {
            closeSSE();
            if (getToken()) handleRoute();
        });

        if (getToken()) {
            showApp();
        } else {
            showLogin();
        }
    });

    // Clean up SSE when leaving the page
    window.addEventListener('beforeunload', closeSSE);
})();
