# Task Routing

Use the smallest row that covers the task.

| Task | Read first | Usually inspect | Validation |
|---|---|---|---|
| Backend/API | `backend/AGENTS.md` | module router, service, schemas, models, related tests | backend tests + pip check |
| Auth/roles | backend rules, `docs/role-aware-ui-audit.md` | auth module, deps, access helpers, router meta, tests | backend + frontend |
| Frontend/UI | `frontend/AGENTS.md` | target view, shared components, store/API calls, access helper | frontend baseline |
| Workflow/status/readiness | `PROJECT_CONTEXT.md` sections 3-8, workflow contract | projects, instruments, dashboard services and views | related backend + frontend |
| Database/schema | `ARCHITECTURE.md`, migration history | models, schemas, services, Alembic versions | migration review + backend tests |
| Security/deployment | relevant document under `docs/` | config, compose, Dockerfiles, workflows, smoke scripts | tests + config-specific checks |
| Documentation-only | target document and current implementation | README/status docs only when affected | link/status consistency |
| Repo audit/sprint planning | current audit, recent git log, tail of sprint/changelog | hotspots and current limitations | no invented scripts |

For historical details, search `SPRINT_LOG.md` or `CHANGELOG.md` for the exact
module or sprint. Do not read them in full unless chronology is the task.
