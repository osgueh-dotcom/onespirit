# AGENTS.md

## Mission

Develop OneSpirit Workflow System as a production-oriented business workflow
product for PT One Spirit Asia. Prefer small, auditable improvements over broad
rewrites.

## Always-Active Invariants

- Keep the business terms `CL`, `ROS`, `CK`, and `PNL`. Do not replace them with
  generic labels when the workflow means those artifacts.
- Preserve the workflow:
  `Inquiry -> Client Confirmation -> CL -> Project Setup -> Planning -> ROS -> CK -> Execution -> PNL -> Final Report / Archive`.
- Treat backend authorization as the security authority. Frontend visibility is
  usability, not access control.
- Never commit credentials, `.env`, client data, uploads, database files, or
  production-like backups.
- Do not make destructive schema/data changes without explicit approval and a
  migration or recovery plan.
- Do not hide lint, test, build, type, validation, or runtime failures.
- Preserve existing architecture and behavior unless the task requires change.

## Working Protocol

1. Use the repo skill `$onespirit-development` for audits, implementation,
   reviews, debugging, workflow changes, and sprint delivery.
2. Inspect `git status`, the relevant implementation, and actual package scripts
   before editing.
3. Read only the documentation routed by the skill. Do not load every project
   document by default.
4. Summarize the current implementation and state a short plan before edits.
5. Implement the smallest complete change, including validation and user-facing
   loading, empty, error, and permission states where relevant.
6. Update documentation only when behavior, architecture, setup, schema, or
   durable workflow rules change.
7. Run relevant validation. Fix root causes instead of weakening checks.
8. Run the dev app for review when the change affects runtime behavior and the
   environment permits it.

## Git Delivery

- After validation, run `git status` and stage only task files.
- Use `Sprint <number>: <clear summary>`, deriving the next number from history.
- Push the current branch when a remote is configured and validation passes.
- Never commit unrelated user changes or broken work.

## Review Guidelines

- Prioritize authorization gaps, unsafe data changes, workflow regressions,
  incorrect CL/ROS/CK/PNL rules, missing validation, and missing tests.
- Check both backend enforcement and frontend workflow clarity.
- Treat production default credentials or exposed sensitive data as blocking.

## Final Report

Use this exact structure:

```txt
Summary:
- ...

Changed files:
- ...

Validation:
- command: result

Git:
- branch:
- commit:
- push:

Known limitations:
- ...

Recommended next sprint:
- ...
```
