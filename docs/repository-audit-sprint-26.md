# Repository Audit - Sprint 26

Date: 2026-06-25

## Scope

This audit re-checks the repository structure, codebase health (backend & frontend), database integrity, dependency tree stability, testing coverage, and security postures for the OneSpirit Workflow System as of Sprint 25 (head `ea66a4d`) on the current development machine.

## Baseline

- **Architecture**: FastAPI modular backend, Vue 3 SPA frontend.
- **Data**: PostgreSQL for container/production environment, SQLite for local unit testing.
- **Testing Baseline**: 41 backend tests (all passing), 4 frontend unit tests (all passing).
- **Quality Control**: Clean ESLint check (0 errors, 0 warnings), clean quality scan, and fully operational local Edge CDP role-aware smoke tests.
- **Git**: Clean `main` aligned with `origin/main` at head `ea66a4d` (Sprint 25).

## Current Machine Runtime Snapshot

Observed on 2026-06-25:

- **Docker**: `Docker version 29.5.3`
- **Docker Compose**: `v5.1.4`
- **Node**: `v26.3.0`
- **npm**: `11.16.0`
- **Python**: `3.12.10`
- **Microsoft Edge**: Installed (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`)
- **Backend environment**: `.venv` is installed, `pip check` reports no broken requirements.
- **Frontend environment**: `node_modules` is installed, production build (`npm run build`) compiles successfully.
- **Local Database**: SQLite test databases (`test_analytics.db`, `test_imports.db`, `test_instruments.db`, `test_readiness_gates.db`) are correctly ignored by git.

## Strengths

1. **Role-Aware Smoke Matrix (Sprint 25)**: Local Edge CDP browser automation covers role-based menu/routing constraints for Admin, Management, PO, PM, Finance, and Staff with zero browser console errors.
2. **Simplified Intake Workflow (Sprint 23)**: Projects can now be created with an existing customer or by entering a new customer name (which auto-creates a minimal CRM Prospect profile), resolving the duplicate intake friction.
3. **Database Security (Sprint 21.1)**: PostgreSQL port `5433` is successfully bound to `127.0.0.1` on the host, preventing direct external database connections and exposing only application-level routes to the local network.
4. **Strong Security Guards**: Pydantic/settings validators block execution in `production` environment if unsafe defaults (default JWT secret, debug mode active, default DB password, or demo/placeholder user seeding) are active.
5. **No Warnings Baseline**: Stale warnings are fully eliminated from both backend test suites and frontend ESLint runs.

## Findings

### P1 - Project Ownership Authorization Gate
While backend roles (Super Admin, Admin, Management, PO, PM, Finance, Staff) are fully formalized and UI access is masked accordingly, the backend query scopes do not yet restrict project reads and mutations strictly based on assigned PO/PM project ownership. A PM can query details for projects they do not manage if they guess the ID, which violates backend-first authority guidelines.

### P1 Before Production - Seeding & Default Secrets
The backend codebase uses settings-level enforcement to reject defaults when `ENV=production`. However, the deployment flow still lacks automated secret rotation recipes and an automated check script for production container startup.

### P2 - Dependency Locking
The frontend has a robust dependency lock (`package-lock.json`), but the backend relies on minimum boundaries in `requirements.txt` (`fastapi>=0.111.0`, etc.) without a constraints or lock file. Lockfile or constraints verification should be established before production deployment.

### P2 - Frontend Test Depth
The frontend testing suite consists of only 4 unit tests covering basic access utility (`access.test.js`). The views (especially large workflow dashboards like `ProjectDetail.vue` and `PmControlCenter.vue`) have no unit test coverage. While the CDP smoke test covers UI integrations, unit testing of component logic is shallow.

### P2 - Hardcoded Paths in Diagnostic Scripts
The diagnostic Excel import script `backend/app/tests/import_excel.py` has a hardcoded path (`d:\One Spirit\Project Workflow OS 2025.xlsx`) which fails on systems that use different drive letters or folder paths. This script should be updated to resolve paths relatively within the repository.

## Recommended Next Sprint (Sprint 26)

1. **Assigned Project Ownership Gates**: Enforce database query filters and mutation checks in `backend/app/modules/projects` so that non-admin/non-management PO and PM users can only read and write projects where they are assigned as `program_owner_id` or `program_manager_id`.
2. **Frontend UI Mirroring**: Ensure the frontend router and views handle restricted access states gracefully when accessing unassigned project detail paths.
3. **Write Access Integration Tests**: Create backend integration tests verifying that `projects:read` and `projects:write` permissions are validated against project ownership for PO and PM roles.
