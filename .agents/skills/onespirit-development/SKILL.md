---
name: onespirit-development
description: Audit, design, implement, review, debug, validate, document, and deliver focused sprints for the OneSpirit Workflow System. Use for work in this repository involving FastAPI, Vue, PostgreSQL/SQLite, Alembic, authentication, roles, CRM, Projects, CL, ROS, CK, PNL, dashboards, imports, finance, deployment, tests, documentation, or repository health.
---

# OneSpirit Development

Develop OneSpirit as an event operations workflow product, not generic CRUD.
Load only task-relevant context and preserve business terminology.

## Start

1. Run the context snapshot with the narrowest useful scope:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .agents/skills/onespirit-development/scripts/context-snapshot.ps1 -Scope backend
   ```

   Valid scopes: `summary`, `backend`, `frontend`, `docs`, `runtime`,
   `full`. Use `runtime` when the task mentions installed dependencies, Docker,
   local app access, ports, or machine readiness.

2. Read root `AGENTS.md`. Read nested `backend/AGENTS.md` or
   `frontend/AGENTS.md` only for that area.
3. Read [repo-map.md](references/repo-map.md) only when the relevant ownership
   or path is unclear.
4. Use [task-routing.md](references/task-routing.md) to select files,
   documentation, and validation. Do not read all repository documentation.
5. Inspect the relevant routes, services, schemas, models, views, components,
   stores, tests, and recent history before editing.
6. State the current implementation, plan, risk, and validation commands.

## Product Decision Check

For a behavior change, determine:

- Which workflow stage and user role owns it?
- Which CL, ROS, CK, PNL, document, payment, or report is affected?
- What status, missing data, risk, owner, and next action must be visible?
- What must the backend block?
- What event must remain auditable?

Read [workflow-contract.md](references/workflow-contract.md) when changing
domain behavior, status transitions, permissions, readiness, or user-facing
terminology.

## Implement

- Prefer the existing module and component patterns.
- Keep changes narrow and reversible.
- Centralize rules that would otherwise be duplicated.
- Do not add dependencies unless the current stack cannot solve the problem
  cleanly.
- Add tests proportional to workflow and authorization risk.
- Guard destructive actions and validate all inputs.
- Update durable docs only when their subject changed.

## Token Budget Discipline

- Start with `summary` or the exact task scope; use `full` only for repo-wide
  audits or release baselines.
- Prefer `context-snapshot.ps1`, `rg`, and recent sprint tails over opening
  broad Markdown or source trees.
- Read workflow, deployment, or history documents only when task routing points
  to them or a finding needs verification.
- Reuse previous validation evidence only as a hint; re-run cheap checks when
  the machine, dependency, or runtime state matters.

## Validate And Deliver

Read [validation.md](references/validation.md), then run the smallest complete
validation set for the changed surface. Expand to the full baseline for shared
contracts, auth, schema, build configuration, or cross-stack changes.

Before completion:

1. Inspect the diff and `git status`.
2. Update `SPRINT_LOG.md`, `CHANGELOG.md`, and status docs when the sprint changes
   durable project state.
3. Start the relevant dev runtime for review when practical.
4. Stage only relevant files.
5. Commit as `Sprint <number>: <clear summary>`.
6. Push only after validation passes.
7. Report using the root `AGENTS.md` final format.

## Audit Guidance

Read [repository-audit-sprint-22.md](../../../docs/repository-audit-sprint-22.md)
for the current risk register and next-sprint priorities. Re-verify findings
against code before acting because the audit is a dated snapshot.
