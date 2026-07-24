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
            throw new Error('Unauthorized');
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
                errEl.textContent = d.error || 'Login failed';
                return;
            }
            var data = await resp.json();
            setToken(data.token);
            showApp();
        } catch (err) {
            errEl.textContent = 'Network error: ' + err.message;
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
            content.innerHTML = '<h2 class="page-title">Page not found</h2><p>Unknown route: ' + esc(hash) + '</p>';
        }
    }

    // ====================================================================
    // WORKERS PAGE
    // ====================================================================

    registerRoute('/workers', async function (content) {
        content.innerHTML = '<h2 class="page-title">Workers</h2>' +
            '<button class="btn btn-primary btn-sm" id="btn-new-worker">+ New Worker</button>' +
            '<div id="workers-msg" class="info-msg"></div>' +
            '<table class="data-table mt-2" id="workers-table"><thead><tr>' +
            '<th>ID</th><th>Name</th><th>Host</th><th>Port</th><th>Username</th><th>Auth</th><th>Status</th><th>Last Seen</th><th>Actions</th>' +
            '</tr></thead><tbody id="workers-tbody"><tr><td colspan="9" class="muted">Loading...</td></tr></tbody></table>';

        document.getElementById('btn-new-worker').addEventListener('click', function () {
            showWorkerForm(content, null);
        });

        try {
            var r = await apiJSON('/workers');
            if (!r.resp.ok) { setMsg(document.getElementById('workers-msg'), 'Error: ' + (r.data && r.data.error), 'error'); return; }
            var workers = r.data || [];
            var tbody = document.getElementById('workers-tbody');
            if (workers.length === 0) {
                tbody.innerHTML = '<tr><td colspan="9" class="muted">No workers yet.</td></tr>';
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
                    '<button class="btn btn-sm btn-primary" data-action="edit" data-id="' + w.id + '">Edit</button> ' +
                    '<button class="btn btn-sm btn-success" data-action="test" data-id="' + w.id + '">Test</button> ' +
                    '<button class="btn btn-sm btn-primary" data-action="creds" data-id="' + w.id + '">Creds</button> ' +
                    '<button class="btn btn-sm btn-danger" data-action="delete" data-id="' + w.id + '">Delete</button>' +
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
                    else if (action === 'delete') doDeleteWorker(content, id);
                });
            });
        } catch (err) {
            setMsg(document.getElementById('workers-msg'), 'Error: ' + err.message, 'error');
        }
    });

    async function showWorkerForm(content, id) {
        var isEdit = !!id;
        var worker = null;
        if (isEdit) {
            var r = await apiJSON('/workers/' + id);
            if (!r.resp.ok) { alert('Failed to load worker: ' + (r.data && r.data.error)); return; }
            worker = r.data;
        }

        var html = '<div class="modal-overlay" id="worker-modal">' +
            '<div class="modal">' +
            '<h3 class="modal-title">' + (isEdit ? 'Edit Worker' : 'New Worker') + '</h3>' +
            '<form id="worker-form">' +
            '<div class="form-field"><label>Name</label><input type="text" name="name" value="' + esc(worker ? worker.name : '') + '" required></div>' +
            '<div class="form-field"><label>Host</label><input type="text" name="host" value="' + esc(worker ? worker.host : '') + '" required></div>' +
            '<div class="form-field"><label>Port</label><input type="number" name="port" value="' + esc(worker ? worker.port : 22) + '"></div>' +
            '<div class="form-field"><label>Username</label><input type="text" name="username" value="' + esc(worker ? worker.username : 'root') + '"></div>' +
            '<div class="row mt-2"><button type="submit" class="btn btn-primary">Save</button> ' +
            '<button type="button" class="btn btn-link" id="worker-cancel" style="color:#555;">Cancel</button></div>' +
            '<div id="worker-form-msg" class="error-msg"></div>' +
            '</form></div></div>';
        content.insertAdjacentHTML('beforeend', html);

        var modal = document.getElementById('worker-modal');
        document.getElementById('worker-cancel').addEventListener('click', function () { modal.remove(); });
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
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                handleRoute();
            } catch (err) {
                setMsg(msgEl, 'Error: ' + err.message, 'error');
            }
        });
    }

    async function doTestWorker(content, id) {
        try {
            var r = await apiJSON('/workers/' + id + '/test', { method: 'POST' });
            if (r.data && r.data.ok) {
                alert('Connection OK');
            } else {
                alert('Connection failed: ' + (r.data && r.data.error || 'unknown'));
            }
            handleRoute();
        } catch (err) { alert('Error: ' + err.message); }
    }

    async function doDeleteWorker(content, id) {
        if (!confirm('Delete worker ' + id + '?')) return;
        try {
            var r = await apiJSON('/workers/' + id, { method: 'DELETE' });
            if (!r.resp.ok) { alert('Error: ' + (r.data && r.data.error)); return; }
            handleRoute();
        } catch (err) { alert('Error: ' + err.message); }
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
            (worker ? ' <span class="muted">(auth: ' + esc(worker.auth_mode) + ')</span>' : '') + '</h3>' +
            '<p class="muted mb-1">Credential values are encrypted at rest and never returned by the API.</p>' +

            '<div class="card"><div class="section-title">Set Private Key (Interface 1: panel-side)</div>' +
            '<form id="set-key-form">' +
            '<div class="form-field"><label>Private Key (PEM)</label><textarea name="private_key" rows="4" placeholder="-----BEGIN RSA PRIVATE KEY-----&#10;...&#10;-----END RSA PRIVATE KEY-----"></textarea></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">Set Key</button>' +
            '<div id="set-key-msg" class="error-msg"></div></form></div>' +

            '<div class="card"><div class="section-title">Set Panel Password (Interface 1: panel-side)</div>' +
            '<form id="set-pw-form">' +
            '<div class="form-field"><label>Password</label><input type="password" name="password"></div>' +
            '<button type="submit" class="btn btn-primary btn-sm">Set Password</button>' +
            '<div id="set-pw-msg" class="error-msg"></div></form></div>' +

            '<div class="card"><div class="section-title">Change Root Password (Interface 2: push to worker via SSH)</div>' +
            '<form id="root-pw-form">' +
            '<div class="form-field"><label>New Root Password</label><input type="password" name="password"></div>' +
            '<button type="submit" class="btn btn-danger btn-sm">Change Root Password</button>' +
            '<div id="root-pw-msg" class="error-msg"></div>' +
            '<p class="muted mt-1">This submits an async task (chpasswd via SSH). You will be redirected to the task page.</p></form></div>' +

            '<button type="button" class="btn btn-link mt-2" id="creds-cancel" style="color:#555;">Close</button>' +
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
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, 'Private key set.', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });

        // Set panel password
        document.getElementById('set-pw-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { password: e.target.password.value };
            var msgEl = document.getElementById('set-pw-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/credentials/password', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                setMsg(msgEl, 'Panel password set.', 'success');
                e.target.reset();
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });

        // Change root password (async -> task)
        document.getElementById('root-pw-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var body = { password: e.target.password.value };
            var msgEl = document.getElementById('root-pw-msg');
            try {
                var r = await apiJSON('/workers/' + id + '/root-password', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                var taskID = r.data && r.data.task_id;
                modal.remove();
                window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });
    }

    // ====================================================================
    // K8S PAGE
    // ====================================================================

    registerRoute('/k8s', async function (content) {
        content.innerHTML = '<h2 class="page-title">Kubernetes</h2>' +
            '<div class="row">' +
            '<div class="col"><div class="card">' +
            '<div class="section-title">Services</div>' +
            '<div class="form-field"><label>Namespace</label><input type="text" id="k8s-svc-ns" placeholder="default" value="default"></div>' +
            '<button class="btn btn-primary btn-sm" id="btn-list-svc">List</button> ' +
            '<button class="btn btn-success btn-sm" id="btn-new-svc">+ Create Service</button>' +
            '<div id="svc-msg" class="info-msg"></div>' +
            '<table class="data-table mt-2" id="svc-table"><thead><tr><th>Name</th><th>Namespace</th><th>Type</th><th>ClusterIP</th><th>Ports</th><th>Actions</th></tr></thead>' +
            '<tbody id="svc-tbody"><tr><td colspan="6" class="muted">Click List to load.</td></tr></tbody></table>' +
            '</div></div>' +

            '<div class="col"><div class="card">' +
            '<div class="section-title">Network Policies</div>' +
            '<div class="form-field"><label>Namespace</label><input type="text" id="k8s-np-ns" placeholder="default" value="default"></div>' +
            '<button class="btn btn-primary btn-sm" id="btn-list-np">List</button> ' +
            '<button class="btn btn-success btn-sm" id="btn-new-np">+ Create Policy</button>' +
            '<div id="np-msg" class="info-msg"></div>' +
            '<table class="data-table mt-2" id="np-table"><thead><tr><th>Name</th><th>Namespace</th><th>Pod Selector</th><th>Actions</th></tr></thead>' +
            '<tbody id="np-tbody"><tr><td colspan="4" class="muted">Click List to load.</td></tr></tbody></table>' +
            '</div></div>' +
            '</div>';

        document.getElementById('btn-list-svc').addEventListener('click', function () { listK8sServices(content); });
        document.getElementById('btn-new-svc').addEventListener('click', function () { showCreateServiceForm(content); });
        document.getElementById('btn-list-np').addEventListener('click', function () { listK8sNetworkPolicies(content); });
        document.getElementById('btn-new-np').addEventListener('click', function () { showCreateNetworkPolicyForm(content); });
    });

    async function listK8sServices(content) {
        var ns = document.getElementById('k8s-svc-ns').value || 'default';
        var tbody = document.getElementById('svc-tbody');
        var msgEl = document.getElementById('svc-msg');
        tbody.innerHTML = '<tr><td colspan="6" class="muted">Loading...</td></tr>';
        try {
            var r = await apiJSON('/k8s/services?namespace=' + encodeURIComponent(ns));
            if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); tbody.innerHTML = ''; return; }
            var svcs = r.data || [];
            if (svcs.items) svcs = svcs.items; // handle k8s List format if returned
            if (!Array.isArray(svcs) || svcs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="muted">No services found.</td></tr>';
                return;
            }
            tbody.innerHTML = svcs.map(function (s) {
                var name = s.metadata ? s.metadata.name : s.name || '?';
                var namespace = s.metadata ? s.metadata.namespace : s.namespace || ns;
                var type = s.spec ? s.spec.type : s.type || '-';
                var clusterIP = s.spec ? s.spec.clusterIP : s.clusterIP || '-';
                var ports = '-';
                if (s.spec && s.spec.ports) {
                    ports = s.spec.ports.map(function (p) { return p.port + '/' + (p.protocol || 'TCP'); }).join(', ');
                } else if (s.ports) {
                    ports = s.ports;
                }
                return '<tr><td>' + esc(name) + '</td><td>' + esc(namespace) + '</td><td>' + esc(type) + '</td><td>' + esc(clusterIP) + '</td><td>' + esc(ports) + '</td>' +
                    '<td><button class="btn btn-sm btn-danger" data-name="' + esc(name) + '" data-ns="' + esc(namespace) + '">Delete</button></td></tr>';
            }).join('');
            tbody.querySelectorAll('button[data-name]').forEach(function (btn) {
                btn.addEventListener('click', async function () {
                    if (!confirm('Delete service ' + this.getAttribute('data-name') + '?')) return;
                    var name = this.getAttribute('data-name');
                    var ns2 = this.getAttribute('data-ns');
                    try {
                        var r = await apiJSON('/k8s/services/' + encodeURIComponent(name) + '?namespace=' + encodeURIComponent(ns2), { method: 'DELETE' });
                        if (!r.resp.ok) { alert('Error: ' + (r.data && r.data.error)); return; }
                        var taskID = r.data && r.data.task_id;
                        if (taskID) window.location.hash = '#/tasks/' + taskID;
                        else listK8sServices(content);
                    } catch (err) { alert('Error: ' + err.message); }
                });
            });
        } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
    }

    async function showCreateServiceForm(content) {
        var html = '<div class="modal-overlay" id="svc-modal"><div class="modal">' +
            '<h3 class="modal-title">Create Service</h3>' +
            '<form id="svc-create-form">' +
            '<div class="form-field"><label>Namespace</label><input type="text" name="namespace" value="default"></div>' +
            '<div class="form-field"><label>Pod Name</label><input type="text" name="pod_name" required></div>' +
            '<div class="form-field"><label>Pod UID</label><input type="text" name="pod_uid" required></div>' +
            '<div class="form-field"><label>Selector (key=value, comma-separated)</label><input type="text" name="selector" placeholder="app=web"></div>' +
            '<div class="form-field"><label>Type</label><select name="type"><option value="ClusterIP">ClusterIP</option><option value="NodePort">NodePort</option></select></div>' +
            '<div class="form-field"><label>Ports (port:target_port:protocol, comma-separated)</label><input type="text" name="ports" placeholder="80:8080:TCP"></div>' +
            '<button type="submit" class="btn btn-primary">Create</button> <button type="button" class="btn btn-link" id="svc-cancel" style="color:#555;">Cancel</button>' +
            '<div id="svc-form-msg" class="error-msg"></div></form></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('svc-modal');
        document.getElementById('svc-cancel').addEventListener('click', function () { modal.remove(); });

        document.getElementById('svc-create-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var form = e.target;
            var selector = {};
            (form.selector.value || '').split(',').filter(Boolean).forEach(function (kv) {
                var parts = kv.split('=');
                if (parts.length === 2) selector[parts[0].trim()] = parts[1].trim();
            });
            var ports = [];
            (form.ports.value || '').split(',').filter(Boolean).forEach(function (p) {
                var parts = p.split(':');
                ports.push({ port: parseInt(parts[0], 10), target_port: parseInt(parts[1] || parts[0], 10), protocol: parts[2] || 'TCP' });
            });
            var body = {
                namespace: form.namespace.value || 'default',
                pod_name: form.pod_name.value,
                pod_uid: form.pod_uid.value,
                selector: selector,
                type: form.type.value,
                ports: ports
            };
            var msgEl = document.getElementById('svc-form-msg');
            try {
                var r = await apiJSON('/k8s/services', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });
    }

    async function listK8sNetworkPolicies(content) {
        var ns = document.getElementById('k8s-np-ns').value || 'default';
        var tbody = document.getElementById('np-tbody');
        var msgEl = document.getElementById('np-msg');
        tbody.innerHTML = '<tr><td colspan="4" class="muted">Loading...</td></tr>';
        try {
            var r = await apiJSON('/k8s/network-policies?namespace=' + encodeURIComponent(ns));
            if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); tbody.innerHTML = ''; return; }
            var nps = r.data || [];
            if (nps.items) nps = nps.items;
            if (!Array.isArray(nps) || nps.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" class="muted">No network policies found.</td></tr>';
                return;
            }
            tbody.innerHTML = nps.map(function (np) {
                var name = np.metadata ? np.metadata.name : np.name || '?';
                var namespace = np.metadata ? np.metadata.namespace : np.namespace || ns;
                var sel = '-';
                if (np.spec && np.spec.podSelector && np.spec.podSelector.matchLabels) {
                    sel = Object.entries(np.spec.podSelector.matchLabels).map(function (kv) { return kv[0] + '=' + kv[1]; }).join(',');
                }
                return '<tr><td>' + esc(name) + '</td><td>' + esc(namespace) + '</td><td>' + esc(sel) + '</td>' +
                    '<td><button class="btn btn-sm btn-danger" data-name="' + esc(name) + '" data-ns="' + esc(namespace) + '">Delete</button></td></tr>';
            }).join('');
            tbody.querySelectorAll('button[data-name]').forEach(function (btn) {
                btn.addEventListener('click', async function () {
                    if (!confirm('Delete network policy ' + this.getAttribute('data-name') + '?')) return;
                    var name = this.getAttribute('data-name');
                    var ns2 = this.getAttribute('data-ns');
                    try {
                        var r = await apiJSON('/k8s/network-policies/' + encodeURIComponent(name) + '?namespace=' + encodeURIComponent(ns2), { method: 'DELETE' });
                        if (!r.resp.ok) { alert('Error: ' + (r.data && r.data.error)); return; }
                        var taskID = r.data && r.data.task_id;
                        if (taskID) window.location.hash = '#/tasks/' + taskID;
                        else listK8sNetworkPolicies(content);
                    } catch (err) { alert('Error: ' + err.message); }
                });
            });
        } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
    }

    async function showCreateNetworkPolicyForm(content) {
        var html = '<div class="modal-overlay" id="np-modal"><div class="modal">' +
            '<h3 class="modal-title">Create Network Policy</h3>' +
            '<form id="np-create-form">' +
            '<div class="form-field"><label>Namespace</label><input type="text" name="namespace" value="default"></div>' +
            '<div class="form-field"><label>Pod Name</label><input type="text" name="pod_name" required></div>' +
            '<div class="form-field"><label>Pod UID</label><input type="text" name="pod_uid" required></div>' +
            '<div class="form-field"><label>Pod Selector (key=value, comma-separated)</label><input type="text" name="pod_selector" placeholder="app=web"></div>' +
            '<div class="form-field"><label>Ingress Ports (protocol:port, comma-separated)</label><input type="text" name="ingress_ports" placeholder="TCP:80,TCP:443"></div>' +
            '<button type="submit" class="btn btn-primary">Create</button> <button type="button" class="btn btn-link" id="np-cancel" style="color:#555;">Cancel</button>' +
            '<div id="np-form-msg" class="error-msg"></div></form></div></div>';
        content.insertAdjacentHTML('beforeend', html);
        var modal = document.getElementById('np-modal');
        document.getElementById('np-cancel').addEventListener('click', function () { modal.remove(); });

        document.getElementById('np-create-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var form = e.target;
            var sel = {};
            (form.pod_selector.value || '').split(',').filter(Boolean).forEach(function (kv) {
                var parts = kv.split('=');
                if (parts.length === 2) sel[parts[0].trim()] = parts[1].trim();
            });
            var ports = [];
            (form.ingress_ports.value || '').split(',').filter(Boolean).forEach(function (p) {
                var parts = p.split(':');
                ports.push({ protocol: parts[0] || 'TCP', port: parseInt(parts[1], 10) });
            });
            var body = {
                namespace: form.namespace.value || 'default',
                pod_name: form.pod_name.value,
                pod_uid: form.pod_uid.value,
                pod_selector: sel,
                ingress_ports: ports
            };
            var msgEl = document.getElementById('np-form-msg');
            try {
                var r = await apiJSON('/k8s/network-policies', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                modal.remove();
                var taskID = r.data && r.data.task_id;
                if (taskID) window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });
    }

    // ====================================================================
    // STORAGE PAGE
    // ====================================================================

    registerRoute('/storage', async function (content) {
        content.innerHTML = '<h2 class="page-title">Storage</h2>' +
            '<div class="row">' +
            '<div class="col"><div class="card">' +
            '<div class="section-title">Provision NFS Storage</div>' +
            '<form id="provision-form">' +
            '<div class="form-field"><label>Worker ID</label><input type="number" name="worker_id" required></div>' +
            '<div class="form-field"><label>Volume Group Name</label><input type="text" name="vg_name" placeholder="vg0" required></div>' +
            '<div class="form-field"><label>LV Name</label><input type="text" name="lv_name" required></div>' +
            '<div class="form-field"><label>Size (GB)</label><input type="number" name="size_gb" required></div>' +
            '<div class="form-field"><label>Filesystem Type</label><input type="text" name="fs_type" value="ext4"></div>' +
            '<div class="form-field"><label>Mount Point</label><input type="text" name="mount_point" placeholder="/mnt/nfs/export1" required></div>' +
            '<div class="form-field"><label>Export Opts (optional)</label><input type="text" name="export_opts" placeholder="*(rw,sync,no_root_squash)"></div>' +
            '<button type="submit" class="btn btn-primary">Provision</button>' +
            '<div id="provision-msg" class="error-msg"></div>' +
            '<p class="muted mt-1">Async: submits a task and redirects to task page on success.</p>' +
            '</form></div>' +

            '<div class="col"><div class="card">' +
            '<div class="section-title">Reclaim Storage</div>' +
            '<form id="reclaim-form">' +
            '<div class="form-field"><label>Worker ID</label><input type="number" name="worker_id" required></div>' +
            '<div class="form-field"><label>Volume Group Name</label><input type="text" name="vg_name" required></div>' +
            '<div class="form-field"><label>LV Name</label><input type="text" name="lv_name" required></div>' +
            '<div class="form-field"><label>Mount Point</label><input type="text" name="mount_point" required></div>' +
            '<button type="submit" class="btn btn-danger">Reclaim</button>' +
            '<div id="reclaim-msg" class="error-msg"></div>' +
            '<p class="muted mt-1">Async: submits a task and redirects to task page on success.</p>' +
            '</form></div>' +
            '</div>' +
            '<div class="card mt-2"><div class="section-title">Recent Storage Tasks</div>' +
            '<table class="data-table" id="storage-table"><thead><tr><th>ID</th><th>Type</th><th>Worker</th><th>Status</th><th>Created</th><th>Finished</th></tr></thead>' +
            '<tbody id="storage-tbody"><tr><td colspan="6" class="muted">Loading...</td></tr></tbody></table></div>';

        document.getElementById('provision-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var f = e.target;
            var body = {
                worker_id: parseInt(f.worker_id.value, 10),
                vg_name: f.vg_name.value,
                lv_name: f.lv_name.value,
                size_gb: parseInt(f.size_gb.value, 10),
                fs_type: f.fs_type.value || 'ext4',
                mount_point: f.mount_point.value
            };
            if (f.export_opts.value) body.export_opts = f.export_opts.value;
            var msgEl = document.getElementById('provision-msg');
            try {
                var r = await apiJSON('/storage/provision', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                var taskID = r.data && r.data.task_id;
                window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });

        document.getElementById('reclaim-form').addEventListener('submit', async function (e) {
            e.preventDefault();
            var f = e.target;
            var body = {
                worker_id: parseInt(f.worker_id.value, 10),
                vg_name: f.vg_name.value,
                lv_name: f.lv_name.value,
                mount_point: f.mount_point.value
            };
            var msgEl = document.getElementById('reclaim-msg');
            try {
                var r = await apiJSON('/storage/reclaim', { method: 'POST', body: JSON.stringify(body) });
                if (!r.resp.ok) { setMsg(msgEl, 'Error: ' + (r.data && r.data.error), 'error'); return; }
                var taskID = r.data && r.data.task_id;
                window.location.hash = '#/tasks/' + taskID;
            } catch (err) { setMsg(msgEl, 'Error: ' + err.message, 'error'); }
        });

        // Load storage tasks
        try {
            var r = await apiJSON('/storage');
            var tbody = document.getElementById('storage-tbody');
            if (!r.resp.ok) { tbody.innerHTML = '<tr><td colspan="6" class="muted">Error loading.</td></tr>'; return; }
            var tasks = r.data || [];
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="muted">No storage tasks.</td></tr>';
                return;
            }
            tbody.innerHTML = tasks.map(function (t) {
                return '<tr style="cursor:pointer" data-href="#/tasks/' + t.id + '"><td>' + esc(t.id) + '</td><td>' + esc(t.type) + '</td><td>' + esc(t.target_id) + '</td><td>' + statusBadge(t.status) + '</td><td>' + esc(fmtTime(t.created_at)) + '</td><td>' + esc(fmtTime(t.finished_at)) + '</td></tr>';
            }).join('');
            tbody.querySelectorAll('tr[data-href]').forEach(function (tr) {
                tr.addEventListener('click', function () { window.location.hash = this.getAttribute('data-href'); });
            });
        } catch (err) { /* ignore */ }
    });

    // ====================================================================
    // TASKS PAGE (list + detail + SSE)
    // ====================================================================

    registerRoute('/tasks', async function (content) {
        content.innerHTML = '<h2 class="page-title">Tasks</h2>' +
            '<table class="data-table" id="tasks-table"><thead><tr>' +
            '<th>ID</th><th>Type</th><th>Target</th><th>Status</th><th>Error</th><th>Created</th><th>Finished</th>' +
            '</tr></thead><tbody id="tasks-tbody"><tr><td colspan="7" class="muted">Loading...</td></tr></tbody></table>';

        try {
            var r = await apiJSON('/tasks');
            if (!r.resp.ok) { return; }
            var tasks = r.data || [];
            var tbody = document.getElementById('tasks-tbody');
            if (tasks.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" class="muted">No tasks.</td></tr>';
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

        content.innerHTML = '<h2 class="page-title">Task #' + esc(id) + '</h2>' +
            '<div class="card" id="task-info"><p class="muted">Loading...</p></div>' +
            '<div class="card"><div class="section-title">Steps (live SSE)</div>' +
            '<div id="steps-container"></div></div>' +
            '<div id="task-error" class="error-msg"></div>';

        // Fetch task detail
        try {
            var r = await apiJSON('/tasks/' + id);
            if (!r.resp.ok) {
                document.getElementById('task-info').innerHTML = '<p class="error-msg">Task not found.</p>';
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
            document.getElementById('task-error').textContent = 'Error: ' + err.message;
        }
    });

    function renderTaskInfo(task) {
        var el = document.getElementById('task-info');
        if (!el) return;
        el.innerHTML = '<div class="row">' +
            '<div class="col"><strong>ID:</strong> ' + esc(task.id) + '</div>' +
            '<div class="col"><strong>Type:</strong> ' + esc(task.type) + '</div>' +
            '<div class="col"><strong>Target:</strong> ' + esc(task.target_kind) + '/' + esc(task.target_id) + '</div>' +
            '</div><div class="row mt-1">' +
            '<div class="col"><strong>Status:</strong> ' + statusBadge(task.status) + '</div>' +
            '<div class="col"><strong>Created:</strong> ' + esc(fmtTime(task.created_at)) + '</div>' +
            '<div class="col"><strong>Started:</strong> ' + esc(fmtTime(task.started_at)) + '</div>' +
            '<div class="col"><strong>Finished:</strong> ' + esc(fmtTime(task.finished_at)) + '</div>' +
            '</div>' +
            (task.error ? '<div class="error-msg mt-1">' + esc(task.error) + '</div>' : '');
    }

    function renderSteps(steps) {
        var el = document.getElementById('steps-container');
        if (!el) return;
        if (!steps || steps.length === 0) {
            el.innerHTML = '<p class="muted">No steps yet.</p>';
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
        content.innerHTML = '<h2 class="page-title">Audit Log</h2>' +
            '<table class="data-table" id="audit-table"><thead><tr>' +
            '<th>ID</th><th>Actor</th><th>Action</th><th>Target</th><th>Result</th><th>Time</th>' +
            '</tr></thead><tbody id="audit-tbody"><tr><td colspan="6" class="muted">Loading...</td></tr></tbody></table>';

        try {
            var r = await apiJSON('/audit-log');
            if (!r.resp.ok) { return; }
            var logs = r.data || [];
            var tbody = document.getElementById('audit-tbody');
            if (logs.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="muted">No audit entries.</td></tr>';
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
