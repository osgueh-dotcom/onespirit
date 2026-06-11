# Deployment Runbook

This runbook covers current demo deployment and future production candidate preparation. It does not declare OneSpirit Workflow production-ready.

---

## 1. Local Demo Deployment

1. Confirm `.env` is configured with demo-safe credentials.
2. Start Docker Desktop.
3. Run:
   ```bash
   docker compose up -d --build
   ```
4. Open frontend at `http://localhost:5173`.
5. Open backend docs locally at `http://localhost:8000/docs` if needed.
6. Verify login, Dashboard, Projects, PM Control, PO Control, Finance, and Imports.

Current Compose is for local/demo use. It uses source bind mounts, Vite dev server, Uvicorn `--reload`, and a host-published database port.

---

## 2. GitHub Pages Frontend Deployment

1. Update GitHub Actions secret `VITE_API_BASE_URL` with the current backend tunnel URL.
2. Run the GitHub Pages workflow manually with `workflow_dispatch`.
3. Workflow should run:
   - checkout
   - setup node
   - `npm ci`
   - `npm run lint`
   - `npm run test`
   - `npm run quality:scan`
   - `npm run build`
   - upload `frontend/dist`
   - deploy Pages
4. Open `https://osgueh-dotcom.github.io/onespirit/`.

---

## 3. Backend Tunnel Demo Deployment

1. Start backend locally or via Docker Compose.
2. Expose only backend port `8000` through a temporary tunnel.
3. Never expose PostgreSQL port.
4. Add `https://osgueh-dotcom.github.io` to `BACKEND_CORS_ORIGINS`.
5. Update GitHub Actions `VITE_API_BASE_URL` and redeploy frontend.
6. Shut down the tunnel after demo.

---

## 4. Docker Compose Local Backend/DB

Use Docker Compose for local backend/database demo:

```bash
docker compose up -d --build
docker compose ps
```

Health checks:

```bash
curl http://localhost:8000/health
```

### VS Code Port Forward UI Test

When testing the Vite UI through VS Code's built-in port forwarding:

1. Start the backend in the same workspace environment on port `8000`.
2. Start the frontend with `npm run dev` or Docker Compose on port `5173`.
3. Forward/open the frontend port `5173` from VS Code.
4. Do not set `VITE_API_BASE_URL` for this local forwarded UI test unless the backend is also exposed through a stable public URL.

In local dev mode, frontend API calls use relative `/api/v1/...` requests so Vite can proxy them to the backend from inside the workspace. This avoids browser-side `localhost:8000` failures when the browser is outside the workspace machine.

Run the automated smoke test after both forwarded URLs are active:

```powershell
$env:SMOKE_FRONTEND_URL = "https://example-5173.asse.devtunnels.ms"
$env:SMOKE_BACKEND_URL = "https://example-8000.asse.devtunnels.ms"
$env:SMOKE_LOGIN_EMAIL = "demo@onespirit.asia"
$env:SMOKE_LOGIN_PASSWORD = "<demo-password-from-secure-channel>"
powershell -ExecutionPolicy Bypass -File scripts/dev-tunnel-smoke.ps1
Remove-Item Env:SMOKE_LOGIN_PASSWORD
```

The smoke test checks frontend HTML/assets, unauthenticated API proxy protection, login through the proxy, `/auth/me`, and direct backend `/health`. It never prints passwords or bearer tokens.

---

## 5. Pre-demo Checklist

- [ ] Backend tests pass.
- [ ] Frontend lint and tests pass.
- [ ] Frontend build passes.
- [ ] Demo data is clean.
- [ ] Tunnel URL is current.
- [ ] Dev tunnel smoke test passes if port forwarding is used.
- [ ] GitHub Pages frontend points to current backend URL.
- [ ] Database port is private.
- [ ] Demo credentials are prepared.
- [ ] Backup created before demo.

---

## 6. Post-demo Shutdown Checklist

- [ ] Stop backend tunnel.
- [ ] Stop Docker Compose if not needed.
- [ ] Rotate demo password if broadly shared.
- [ ] Record client feedback.
- [ ] Record issues found during demo.

---

## 7. Production Candidate Preparation Checklist

- [ ] Production domain chosen.
- [ ] HTTPS configured.
- [ ] Reverse proxy designed.
- [ ] Production Dockerfiles/Compose override remove dev servers and bind mounts.
- [ ] Database host port is not published.
- [ ] PostgreSQL persistent volume configured.
- [ ] Backup/restore drill completed.
- [ ] Secrets rotated and stored securely.
- [ ] Demo and placeholder user seeding disabled.
- [ ] `/docs` exposure reviewed.
- [ ] Monitoring and log collection planned.
- [ ] Rollback plan tested.

---

## 8. Rollback Plan

1. Record current release commit hash before deployment.
2. Create database and upload backup.
3. If deployment fails, redeploy previous commit.
4. Do not run destructive migration downgrade unless it has been rehearsed.
5. Restore database only if migration/data write caused corruption and the restore procedure has been verified.
6. Verify login, dashboard, project detail, finance, and documents.
7. Document incident and corrective action.
