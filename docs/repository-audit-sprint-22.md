# Repository Audit - Sprint 22

Date: 2026-06-24

## Scope

This audit re-checks repository structure, agent/skill routing, validation
coverage, runtime dependency readiness on the current Windows machine, and
token-efficient Codex operation.

## Baseline

- Architecture: FastAPI modular backend and Vue 3 SPA frontend.
- Data: PostgreSQL for Docker/integrated runtime, SQLite for tests.
- Current automated baseline before Sprint 22: 38 backend tests and 4 frontend
  tests.
- Git: clean `main` aligned with `origin/main` at Sprint 21.1 before this audit.
- Agent stack: root `AGENTS.md`, backend/frontend scoped `AGENTS.md`, and the
  repo-scoped `$onespirit-development` skill.

## Current Machine Runtime Snapshot

Observed on 2026-06-24:

- Docker: `Docker version 29.5.3`.
- Docker Compose: `v5.1.4`.
- Node: `v26.3.0`.
- npm: `11.16.0`.
- Python: `3.12.10`.
- `backend/.venv` is installed and `pip check` is clean.
- `frontend/node_modules` is installed and `npm ls --depth=0` resolves the
  project dependency tree.
- Docker Compose stack is running; `db` and `backend` are healthy, and
  `frontend` is running.
- Container backend `pip check` is clean.

Refresh this dated snapshot with:

```powershell
powershell -ExecutionPolicy Bypass -File .agents/skills/onespirit-development/scripts/context-snapshot.ps1 -Scope runtime
```

## Strengths

- Business workflow terminology (`CL`, `ROS`, `CK`, `PNL`) remains explicit in
  instructions and product documentation.
- Backend authorization is still documented as the security authority.
- Existing validation scripts are discoverable from package scripts and skill
  references.
- Local runtime dependencies are present on this machine for Docker and local
  backend/frontend development.
- The agent instruction stack is now layered enough to avoid loading broad docs
  by default.

## Findings

### P1 - Project ownership authorization is still the highest-value product risk

Formal PO and PM roles exist, but per-project assigned ownership is not yet the
backend enforcement boundary for all reads and mutations. This remains the next
workflow/security sprint.

### P1 Before Production - Runtime defaults remain demo-oriented

Development defaults still include demo seeding, auto-create tables, placeholder
users, default admin credentials, and a default JWT secret. The production config
guard blocks known unsafe defaults, but deployment still requires an explicit
production environment checklist and verified secret rotation.

### P2 - Dependency resolution remains only partially reproducible

Frontend has `package-lock.json`; backend still uses broad minimum versions in
`requirements.txt` without a constraints or lock file. Keep current runtime
checks, then add a backend constraints workflow when production runtime decisions
are settled.

### P2 - Frontend regression depth is still shallow

Four frontend tests do not cover enough critical workflow states. Prioritize
access rules, transition controls, readiness display, PNL masking, and form
validation.

### P2 - Large workflow views remain hotspots

`ProjectDetail.vue`, `Projects.vue`, `PmControlCenter.vue`,
`SourceVendorPerformance.vue`, `PoControlCenter.vue`, and `Finance.vue` should
be edited in small cohesive slices. Avoid broad view rewrites.

### P2 - Schema lifecycle still has two authorities

Alembic migrations exist, but development startup can still call
`Base.metadata.create_all`. Production should require migrations and disable
auto-create.

### P2 - Operational import utility remains under tests

`backend/app/tests/import_excel.py` can write imported records and should move to
a guarded admin/import script before broader operational use.

## Sprint 22 Agent Upgrade

Sprint 22 upgrades the Codex workflow by:

- adding a `runtime` scope to the context snapshot;
- routing agent/skill/runtime readiness tasks directly to that scope;
- documenting machine dependency verification commands in the validation matrix;
- updating skill token-budget rules so agents use `summary`, targeted scopes,
  and `rg` before opening broad documentation;
- moving audit guidance to this current Sprint 22 audit.

## Recommended Next Sprint

Sprint 23 should enforce project ownership for assigned PO/PM users in backend
queries and mutations, mirror the restriction in frontend navigation/actions,
and add regression tests for allowed and denied project access.
