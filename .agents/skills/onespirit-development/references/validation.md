# Validation Matrix

Run commands from the stated directory. Do not invent unavailable scripts.

## Backend

```powershell
cd backend
python -m pytest app/tests -q
python -m pip check
```

Use targeted pytest paths during iteration, then the full suite for shared
services, auth, schema, configuration, or cross-module changes.

## Frontend

```powershell
cd frontend
npm run lint
npm run test
npm run quality:scan
npm audit
npm run build
```

There is no frontend `typecheck` script. The codebase is JavaScript, not a
TypeScript project.

## Runtime

- Local frontend: `npm run dev` from `frontend/`.
- Local backend: `uvicorn app.main:app --reload` from `backend/`.
- Integrated demo: `docker compose up -d --build` from the repository root.
- Dev tunnel smoke test: `scripts/dev-tunnel-smoke.ps1` only when tunnel
  environment variables and secure credentials are available.

For machine/runtime readiness checks:

```powershell
powershell -ExecutionPolicy Bypass -File .agents/skills/onespirit-development/scripts/context-snapshot.ps1 -Scope runtime
cd backend
.venv\Scripts\python.exe -m pip check
cd ..\frontend
npm ls --depth=0
npm audit
cd ..
docker compose ps
docker compose exec -T backend python -m pip check
```

If `backend/.venv` or `frontend/node_modules` is missing, install with the
documented commands before running local development. Prefer Docker Compose for
the integrated runtime baseline.

For UI work, inspect the changed route at desktop and mobile widths and check the
browser console. For API work, check the affected response and authorization
path, not only `/health`.
