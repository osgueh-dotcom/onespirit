#!/usr/bin/env node
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const ROUTE_ITEMS = [
  { key: "dashboard", label: "Dashboard", hash: "#/" },
  { key: "projects", label: "Projects", hash: "#/projects" },
  { key: "pm_control", label: "PM Control", hash: "#/pm-control-center" },
  { key: "po_control", label: "PO Control", hash: "#/po-control-center" },
  { key: "source_vendor", label: "Pusat Source & Vendor", hash: "#/source-vendor-performance" },
  { key: "finance", label: "Finance", hash: "#/finance" },
  { key: "imports", label: "Import Data", hash: "#/imports" },
  { key: "crm", label: "CRM", hash: "#/crm" },
  { key: "documents", label: "Documents", hash: "#/documents" },
  { key: "settings", label: "Pengaturan", hash: "#/settings" }
];

const ALL_ROUTE_KEYS = ROUTE_ITEMS.map((item) => item.key);
const ROLE_MATRIX = [
  {
    role: "Admin",
    email: "smoke.admin@onespirit.asia",
    fullName: "Smoke Admin",
    allowed: ALL_ROUTE_KEYS
  },
  {
    role: "Management",
    email: "smoke.management@onespirit.asia",
    fullName: "Smoke Management",
    allowed: ALL_ROUTE_KEYS
  },
  {
    role: "PO",
    email: "smoke.po@onespirit.asia",
    fullName: "Smoke PO",
    allowed: ["dashboard", "projects", "po_control", "source_vendor", "finance", "crm", "documents", "settings"]
  },
  {
    role: "PM",
    email: "smoke.pm@onespirit.asia",
    fullName: "Smoke PM",
    allowed: ["dashboard", "projects", "pm_control", "crm", "documents", "settings"]
  },
  {
    role: "Finance",
    email: "smoke.finance@onespirit.asia",
    fullName: "Smoke Finance",
    allowed: ["dashboard", "projects", "finance", "documents", "settings"]
  },
  {
    role: "Staff",
    email: "smoke.staff@onespirit.asia",
    fullName: "Smoke Staff",
    allowed: ["dashboard", "projects", "pm_control", "po_control", "source_vendor", "crm", "documents", "settings"]
  }
];

function parseArgs(argv) {
  const parsed = { flags: new Set(), values: new Map() };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    if (["headful", "json", "skip-auth", "skip-role-matrix"].includes(key)) {
      parsed.flags.add(key);
      continue;
    }
    parsed.values.set(key, argv[i + 1]);
    i += 1;
  }
  return parsed;
}

function normalizeBaseUrl(url) {
  return String(url || "").trim().replace(/\/+$/, "");
}

function normalizeFrontendUrl(url) {
  const value = String(url || "").trim();
  return value.endsWith("/") ? value : `${value}/`;
}

function findEdgeExecutable(explicitPath) {
  const candidates = [
    explicitPath,
    process.env.EDGE_PATH,
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
  ].filter(Boolean);

  return candidates.find((candidate) => fs.existsSync(candidate)) || null;
}

function requireNativeWebSocket() {
  if (typeof WebSocket !== "function") {
    throw new Error("Native WebSocket is unavailable. Use the repo Node runtime or Node 22+.");
  }
}

async function waitJson(url, label) {
  for (let i = 0; i < 80; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return await response.json();
    } catch {
      // Edge CDP may take a moment to bind the port.
    }
    await sleep(250);
  }
  throw new Error(`${label} did not become ready.`);
}

async function createPage(port, url) {
  const response = await fetch(`http://127.0.0.1:${port}/json/new?${encodeURIComponent(url)}`, {
    method: "PUT"
  });
  if (!response.ok) {
    throw new Error(`CDP new page failed with HTTP ${response.status}.`);
  }
  return response.json();
}

function connectCdp(webSocketDebuggerUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(webSocketDebuggerUrl);
    const pending = new Map();
    const events = [];

    ws.onopen = () => {
      let id = 0;
      const send = (method, params = {}) => new Promise((res, rej) => {
        const message = { id: ++id, method, params };
        pending.set(message.id, { res, rej, method });
        ws.send(JSON.stringify(message));
      });

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.id && pending.has(message.id)) {
          const waiter = pending.get(message.id);
          pending.delete(message.id);
          if (message.error) {
            waiter.rej(new Error(`${waiter.method}: ${message.error.message}`));
          } else {
            waiter.res(message.result);
          }
          return;
        }
        if (message.method) events.push(message);
      };

      resolve({ ws, send, events });
    };

    ws.onerror = reject;
  });
}

async function waitForExpression(cdp, expression, timeoutMs = 8000) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const result = await cdp.send("Runtime.evaluate", {
      expression,
      returnByValue: true
    });
    if (result.result.value) return true;
    await sleep(250);
  }
  return false;
}

function routeUrl(frontendUrl, routeHash) {
  const url = new URL(frontendUrl);
  url.searchParams.set("smoke", String(Date.now()));
  url.hash = routeHash;
  return url.toString();
}

async function login(backendUrl, email, password) {
  const response = await fetch(`${backendUrl}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ username: email, password })
  });
  if (!response.ok) {
    throw new Error(`Login failed with HTTP ${response.status}.`);
  }
  const payload = await response.json();
  return payload.access_token;
}

function authHeaders(token) {
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json"
  };
}

async function apiJson(backendUrl, token, pathName, options = {}) {
  const response = await fetch(`${backendUrl}${pathName}`, {
    ...options,
    headers: {
      ...authHeaders(token),
      ...(options.headers || {})
    }
  });
  const text = await response.text();
  const payload = text ? JSON.parse(text) : null;
  if (!response.ok) {
    const detail = payload?.detail || payload?.message || text || `HTTP ${response.status}`;
    throw new Error(`${options.method || "GET"} ${pathName} failed: ${detail}`);
  }
  return payload;
}

function createMatrixPassword() {
  const suffix = Math.random().toString(36).slice(2, 10);
  return `EdgeMatrix${Date.now()}${suffix}!Aa1`;
}

function isAdminProfile(user) {
  return Boolean(user?.role?.permissions?.includes("admin"));
}

async function ensureMatrixUsers(backendUrl, adminToken, password) {
  const existingUsers = await apiJson(backendUrl, adminToken, "/api/v1/auth/users?limit=500");
  const byEmail = new Map(existingUsers.map((user) => [user.email, user]));
  const provisioned = [];

  for (const entry of ROLE_MATRIX) {
    let user = byEmail.get(entry.email);
    if (!user) {
      user = await apiJson(backendUrl, adminToken, "/api/v1/auth/users", {
        method: "POST",
        body: JSON.stringify({
          email: entry.email,
          full_name: entry.fullName,
          password,
          is_active: true,
          role: entry.role
        })
      });
    } else {
      await apiJson(backendUrl, adminToken, `/api/v1/auth/users/${user.id}/password`, {
        method: "PATCH",
        body: JSON.stringify({
          new_password: password,
          confirm_password: password
        })
      });

      if (!user.is_active) {
        user = await apiJson(backendUrl, adminToken, `/api/v1/auth/users/${user.id}/status`, {
          method: "PATCH",
          body: JSON.stringify({ is_active: true })
        });
      }
    }

    provisioned.push({ ...entry, user });
  }

  return provisioned;
}

async function setSessionToken(cdp, frontendUrl, token) {
  await cdp.send("Page.navigate", { url: frontendUrl });
  await sleep(600);
  await cdp.send("Runtime.evaluate", {
    expression: `localStorage.clear(); localStorage.setItem('token', ${JSON.stringify(token)})`
  });
}

async function visibleNavLabels(cdp) {
  const result = await cdp.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(() => [...document.querySelectorAll('aside nav a')]
      .filter((link) => {
        const style = window.getComputedStyle(link);
        return style.display !== 'none' && style.visibility !== 'hidden';
      })
      .map((link) => link.textContent.replace(/\\s+/g, ' ').trim())
      .filter(Boolean))()`
  });
  return result.result.value || [];
}

function routeItemByKey(key) {
  return ROUTE_ITEMS.find((item) => item.key === key);
}

function normalizedHash(hash) {
  return hash && hash !== "#" ? hash : "#/";
}

async function navigateAndReadHash(cdp, frontendUrl, hash) {
  await cdp.send("Page.navigate", { url: routeUrl(frontendUrl, hash) });
  await sleep(900);
  const result = await cdp.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `location.hash || '#/'`
  });
  return normalizedHash(result.result.value);
}

async function inspectRoleMatrix(cdp, frontendUrl, backendUrl, matrixUsers, password) {
  const results = [];

  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: 1366,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  for (const entry of matrixUsers) {
    const token = await login(backendUrl, entry.email, password);
    await setSessionToken(cdp, frontendUrl, token);
    await cdp.send("Page.navigate", { url: routeUrl(frontendUrl, "#/") });
    await waitForExpression(
      cdp,
      `document.body.innerText.includes(${JSON.stringify(entry.role)})`
    );

    const labels = await visibleNavLabels(cdp);
    const allowedLabels = entry.allowed.map((key) => routeItemByKey(key).label);
    const hiddenLabels = ROUTE_ITEMS
      .filter((item) => !entry.allowed.includes(item.key))
      .map((item) => item.label);
    const missingLabels = allowedLabels.filter((label) => !labels.includes(label));
    const leakedLabels = hiddenLabels.filter((label) => labels.includes(label));

    results.push({
      role: entry.role,
      area: "menu",
      ok: missingLabels.length === 0 && leakedLabels.length === 0,
      detail: missingLabels.length === 0 && leakedLabels.length === 0
        ? `visible=${allowedLabels.length}; hidden=${hiddenLabels.length}`
        : `missing=${missingLabels.join(", ") || "-"}; leaked=${leakedLabels.join(", ") || "-"}`
    });

    for (const routeItem of ROUTE_ITEMS) {
      const shouldAllow = entry.allowed.includes(routeItem.key);
      const currentHash = await navigateAndReadHash(cdp, frontendUrl, routeItem.hash);
      const ok = shouldAllow ? currentHash === routeItem.hash : currentHash === "#/";
      results.push({
        role: entry.role,
        area: `route:${routeItem.key}`,
        ok,
        detail: shouldAllow
          ? `${routeItem.hash} -> ${currentHash}`
          : `${routeItem.hash} redirected to ${currentHash}`
      });
    }
  }

  return results;
}

async function inspectProjectsModal(cdp, frontendUrl, token, width, height) {
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width,
    height,
    deviceScaleFactor: 1,
    mobile: width < 600
  });

  await cdp.send("Page.navigate", { url: frontendUrl });
  await sleep(1000);
  await cdp.send("Runtime.evaluate", {
    expression: `localStorage.setItem('token', ${JSON.stringify(token)})`
  });

  await cdp.send("Page.navigate", { url: routeUrl(frontendUrl, "#/projects") });
  const projectsReady = await waitForExpression(
    cdp,
    "document.body.innerText.includes('Add New Project')"
  );
  if (!projectsReady) {
    return {
      ok: false,
      detail: "Projects route did not expose Add New Project."
    };
  }

  await cdp.send("Runtime.evaluate", {
    expression: `(() => {
      const add = [...document.querySelectorAll('button')]
        .find((button) => button.textContent.includes('Add New Project'));
      if (add) add.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
    })()`
  });

  const modalReady = await waitForExpression(
    cdp,
    "document.body.innerText.includes('Create Project Entry')"
  );
  if (!modalReady) {
    return {
      ok: false,
      detail: "Create Project modal did not open."
    };
  }

  const result = await cdp.send("Runtime.evaluate", {
    returnByValue: true,
    expression: `(() => {
      const labels = [...document.querySelectorAll('label')].map((label) => label.textContent.trim());
      const optionText = [...document.querySelectorAll('select option')].map((option) => option.textContent.trim());
      return {
        hasProjectTitle: labels.some((label) => label.includes('Project/Event Title')),
        hasNewClientName: labels.some((label) => label.includes('New Client Name')),
        hasNewClientCategory: labels.some((label) => label.includes('New Client Category')),
        hasNewClientOption: optionText.includes('New client')
      };
    })()`
  });

  const value = result.result.value;
  const ok = Boolean(
    value.hasProjectTitle &&
    value.hasNewClientName &&
    value.hasNewClientCategory &&
    value.hasNewClientOption
  );

  return {
    ok,
    detail: ok
      ? "Projects modal includes quick customer intake controls."
      : `Missing expected controls: ${JSON.stringify(value)}`
  };
}

function consoleErrorsFrom(events) {
  return events.filter((event) => {
    if (event.method === "Runtime.consoleAPICalled") {
      return event.params.type === "error";
    }
    if (event.method === "Log.entryAdded") {
      return event.params.entry?.level === "error";
    }
    return false;
  });
}

function addCheck(checks, name, ok, detail) {
  checks.push({ name, ok, detail });
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const frontendUrl = normalizeFrontendUrl(
    args.values.get("frontend-url") ||
      process.env.EDGE_SMOKE_FRONTEND_URL ||
      process.env.SMOKE_FRONTEND_URL ||
      "http://localhost:5173/onespirit/"
  );
  const backendUrl = normalizeBaseUrl(
    args.values.get("backend-url") ||
      process.env.EDGE_SMOKE_BACKEND_URL ||
      process.env.SMOKE_BACKEND_URL ||
      "http://localhost:8000"
  );
  const loginEmail =
    args.values.get("email") ||
    process.env.EDGE_SMOKE_LOGIN_EMAIL ||
    process.env.SMOKE_LOGIN_EMAIL ||
    "demo@onespirit.asia";
  const loginPassword =
    process.env.EDGE_SMOKE_LOGIN_PASSWORD ||
    process.env.SMOKE_LOGIN_PASSWORD ||
    "";
  const edgePath = findEdgeExecutable(args.values.get("edge-path"));
  const headful = args.flags.has("headful");
  const skipAuth = args.flags.has("skip-auth");
  const skipRoleMatrix = args.flags.has("skip-role-matrix");
  const checks = [];

  requireNativeWebSocket();
  addCheck(checks, "node_websocket", true, "Native WebSocket is available.");

  if (!edgePath) {
    throw new Error("Microsoft Edge executable was not found. Set EDGE_PATH or --edge-path.");
  }
  addCheck(checks, "edge_executable", true, edgePath);

  const backendHealth = await fetch(`${backendUrl}/health`);
  addCheck(checks, "backend_health", backendHealth.ok, `HTTP ${backendHealth.status}`);

  const frontendResponse = await fetch(frontendUrl);
  addCheck(checks, "frontend_load", frontendResponse.ok, `HTTP ${frontendResponse.status}`);

  if (skipAuth) {
    return { checks, skippedAuthenticatedBrowserChecks: true };
  }

  if (!loginPassword) {
    throw new Error("Set EDGE_SMOKE_LOGIN_PASSWORD or SMOKE_LOGIN_PASSWORD for authenticated browser checks.");
  }

  const token = await login(backendUrl, loginEmail, loginPassword);
  addCheck(checks, "login", Boolean(token), `Authenticated as ${loginEmail}.`);
  const profile = await apiJson(backendUrl, token, "/api/v1/auth/me");
  addCheck(checks, "profile", Boolean(profile?.role?.name), `Role ${profile?.role?.name || "unknown"}.`);

  const roleMatrixPassword = createMatrixPassword();
  let matrixUsers = [];
  if (!skipRoleMatrix) {
    if (!isAdminProfile(profile)) {
      throw new Error("Role matrix checks require an admin-capable login. Set EDGE_SMOKE_LOGIN_EMAIL to an Admin/Super Admin user or use --skip-role-matrix.");
    }
    matrixUsers = await ensureMatrixUsers(backendUrl, token, roleMatrixPassword);
    addCheck(checks, "role_matrix_setup", matrixUsers.length === ROLE_MATRIX.length, `${matrixUsers.length} smoke users ready.`);
  }

  const port = 9200 + Math.floor(Math.random() * 600);
  const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), "onespirit-edge-"));
  const browser = spawn(edgePath, [
    headful ? "" : "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    "about:blank"
  ].filter(Boolean), { stdio: "ignore" });

  let cdp;
  try {
    await waitJson(`http://127.0.0.1:${port}/json/version`, "Edge CDP");
    const page = await createPage(port, frontendUrl);
    cdp = await connectCdp(page.webSocketDebuggerUrl);
    await cdp.send("Runtime.enable");
    await cdp.send("Log.enable");
    await cdp.send("Page.enable");

    const desktop = await inspectProjectsModal(cdp, frontendUrl, token, 1366, 900);
    addCheck(checks, "projects_modal_desktop", desktop.ok, desktop.detail);

    const mobile = await inspectProjectsModal(cdp, frontendUrl, token, 390, 844);
    addCheck(checks, "projects_modal_mobile", mobile.ok, mobile.detail);

    if (!skipRoleMatrix) {
      const roleMatrixResults = await inspectRoleMatrix(cdp, frontendUrl, backendUrl, matrixUsers, roleMatrixPassword);
      for (const item of roleMatrixResults) {
        addCheck(checks, `role_${item.role.toLowerCase()}_${item.area}`, item.ok, item.detail);
      }
    }

    const consoleErrors = consoleErrorsFrom(cdp.events);
    addCheck(checks, "browser_console_errors", consoleErrors.length === 0, `${consoleErrors.length} error(s).`);
  } finally {
    try {
      cdp?.ws?.close();
    } catch {
      // No-op.
    }
    browser.kill();
    await sleep(500);
    try {
      fs.rmSync(userDataDir, { recursive: true, force: true });
    } catch {
      // Edge can briefly hold profile files on Windows; this should not fail the smoke result.
    }
  }

  return { checks, skippedRoleMatrix: skipRoleMatrix };
}

try {
  const result = await main();
  const failed = result.checks.filter((check) => !check.ok);
  if (process.argv.includes("--json")) {
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } else {
    process.stdout.write("OneSpirit local Edge smoke test\n");
    for (const check of result.checks) {
      process.stdout.write(`${check.ok ? "PASS" : "FAIL"} ${check.name}: ${check.detail}\n`);
    }
    if (result.skippedAuthenticatedBrowserChecks) {
      process.stdout.write("SKIP authenticated browser checks: --skip-auth was used.\n");
    }
    if (result.skippedRoleMatrix) {
      process.stdout.write("SKIP role matrix checks: --skip-role-matrix was used.\n");
    }
  }
  process.exitCode = failed.length > 0 ? 1 : 0;
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
}
