# Repository Audit - Sprint 21

Date: 2026-06-21

## Scope

This audit covers repository structure, agent instructions, workflow domain
alignment, validation coverage, security posture, maintainability, and
token-efficient Codex operation.

## Baseline

- Architecture: FastAPI modular backend and Vue 3 SPA frontend.
- Data: PostgreSQL for integrated runtime, SQLite for tests.
- Current automated baseline before Sprint 21: 38 backend tests and 4 frontend
  tests.
- Git: clean `main` aligned with `origin/main` at Sprint 20.
- Repository size: 234 tracked files, including 78 Python files, 73 frontend
  JavaScript/Vue files, and 62 Markdown files.

## Strengths

- CL, ROS, CK, and PNL are first-class workflow concepts.
- Backend modules consistently separate routers, services, schemas, and models.
- Production configuration rejects known default secrets and unsafe seed flags.
- Frontend access helpers and backend authorization tests already exist.
- Lint, tests, quality scan, dependency audit, and build scripts are established.
- Test databases use in-memory SQLite helpers and are ignored by Git.

## Findings

### P1 - Project ownership authorization is incomplete

Formal PO and PM roles exist, but assigned PO/PM ownership is not yet enforced
per project. A user with broad role permission may reach projects outside their
assignment. This is the highest-value workflow and security sprint.

### P1 Before Production - Runtime defaults remain demo-oriented

`AUTO_CREATE_TABLES`, demo seeding, placeholder seeding, default admin
credentials, and a default JWT secret remain enabled or defined for development.
Production validation blocks the known unsafe combination, but deployment must
set and verify every production variable before release.

### P2 - Frontend workflow views are concentrated

`ProjectDetail.vue`, `Projects.vue`, and `PmControlCenter.vue` exceed 1,000 lines.
This increases regression risk and makes focused testing harder. Extract only
cohesive workflow panels or composables during feature work; avoid a standalone
rewrite sprint.

### P2 - Frontend regression coverage is shallow

Four frontend tests are not proportional to the number of critical workflow
screens. Prioritize access rules, project transition controls, readiness
presentation, PNL masking, and form validation.

### P2 - Python dependency resolution is not reproducible

`backend/requirements.txt` uses broad minimum versions and has no lock or
constraints file. A future install may resolve materially different versions.
Add a deliberate constraints/lock workflow after production runtime decisions
are settled.

### P2 - Schema lifecycle has two authorities

Alembic exists, but application startup can also call `Base.metadata.create_all`.
This is convenient for demo setup and risky as a durable production schema
strategy. Production should disable auto-create and require migrations.

### P2 - Operational import utility is located under tests

`backend/app/tests/import_excel.py` can connect to PostgreSQL and write imported
records. Its location suggests test-only behavior even though it is an
operational data script. Move it to a guarded admin/import script with explicit
target confirmation before broader use.

### P3 - Documentation and agent instructions are duplicated

The previous root agent guide repeated development, sprint, testing, Git, and
reporting rules already present in three other root documents. This consumed
always-on context and increased drift risk.

Sprint 21 addresses this by:

- reducing root `AGENTS.md` to durable guardrails;
- adding focused backend/frontend agent files;
- adding the repo-scoped `$onespirit-development` skill;
- routing detailed context through on-demand references;
- adding a read-only context snapshot script.

## Token Efficiency Design

- Keep always-loaded instructions short.
- Use skill metadata for triggering and load the skill body only for repo work.
- Route tasks to exact docs instead of reading all Markdown files.
- Use the snapshot script for branch, scripts, modules, status, and hotspots.
- Search sprint history by keyword and read tails/sections, not full logs.
- Run targeted tests during iteration and full relevant baselines before commit.

## Recommended Next Sprint

Sprint 22 should enforce project ownership for assigned PO/PM users in backend
queries and mutations, mirror the restriction in frontend navigation and
actions, and add regression tests for allowed and denied project access.
