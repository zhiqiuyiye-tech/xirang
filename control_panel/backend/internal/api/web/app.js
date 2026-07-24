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
            data = await resp.json();
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

    // ===== Hash Router =====
    var routes = {};

    function registerRoute(path, handler) {
        routes[path] = handler;
    }

    function handleRoute() {
        var hash = window.location.hash.slice(1) || '/workers';
        // Update nav active state
        var links = document.querySelectorAll('.nav-link');
        links.forEach(function (l) {
            l.classList.toggle('active', l.getAttribute('href') === '#' + hash);
        });

        // Find matching route (exact match or prefix match for /tasks/:id)
        var handler = routes[hash];
        if (!handler) {
            // Try prefix match for detail routes
            for (var r in routes) {
                if (hash.indexOf(r + '/') === 0) {
                    handler = routes[r];
                    break;
                }
            }
        }
        var content = document.getElementById('page-content');
        if (handler) {
            handler(content, hash);
        } else {
            content.innerHTML = '<h2 class="page-title">Page not found</h2><p>Unknown route: ' + hash + '</p>';
        }
    }

    // ===== Page Renderers (Task 1: placeholders, Task 2: full) =====

    function renderPlaceholder(content, title) {
        content.innerHTML = '<h2 class="page-title">' + title + '</h2><p class="muted">Loading...</p>';
    }

    // Register placeholder routes for Task 1; Task 2 replaces them.
    registerRoute('/workers', function (content) {
        renderPlaceholder(content, 'Workers');
    });
    registerRoute('/k8s', function (content) {
        renderPlaceholder(content, 'Kubernetes');
    });
    registerRoute('/storage', function (content) {
        renderPlaceholder(content, 'Storage');
    });
    registerRoute('/tasks', function (content) {
        renderPlaceholder(content, 'Tasks');
    });
    registerRoute('/audit', function (content) {
        renderPlaceholder(content, 'Audit Log');
    });

    // ===== Init =====
    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('login-form').addEventListener('submit', handleLogin);
        document.getElementById('logout-btn').addEventListener('click', handleLogout);
        window.addEventListener('hashchange', function () {
            if (getToken()) handleRoute();
        });

        if (getToken()) {
            showApp();
        } else {
            showLogin();
        }
    });

    // Export for Task 2 extensions
    window.CP = {
        apiFetch: apiFetch,
        apiJSON: apiJSON,
        getToken: getToken,
        setToken: setToken,
        clearToken: clearToken,
        registerRoute: registerRoute,
        showLogin: showLogin
    };
})();
