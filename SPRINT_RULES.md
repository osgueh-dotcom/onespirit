# SPRINT_RULES.md

## Purpose

This file defines how development sprints should be executed for the OneSpirit Workflow System.

Every sprint should create measurable progress without destabilizing the project.

---

## Sprint Philosophy

OneSpirit should be improved through small, safe, validated increments.

Each sprint must:

1. Have a clear objective.
2. Respect the existing codebase.
3. Improve real workflow value.
4. Avoid unnecessary rewrites.
5. Run validation before completion.
6. Commit and push successful work.
7. Leave the project reviewable in dev mode.

---

## Standard Sprint Flow

Use this process for every sprint:

```txt
1. Inspect
2. Understand
3. Plan
4. Implement
5. Validate
6. Fix
7. Document
8. Run dev
9. Commit
10. Push
11. Report
```

---

## 1. Inspect

Before editing:

- Read `AGENTS.md`
- Read `PROJECT_CONTEXT.md`
- Read `ARCHITECTURE.md`
- Read `package.json`
- Inspect relevant routes/pages/components/services/schema
- Inspect current git status

Do not modify files before understanding the relevant area.

---

## 2. Understand

Summarize:

- What exists now
- What the current workflow does
- What files are relevant
- What risk exists
- What should not be changed

---

## 3. Plan

Before implementation, produce a concise plan:

```txt
Implementation plan:
1. ...
2. ...
3. ...

Risk:
- ...

Validation:
- ...
```

The plan should be small enough to finish in the current sprint.

---

## 4. Implement

Implementation rules:

- Make focused changes.
- Avoid broad rewrites.
- Preserve existing routes unless the sprint requires route changes.
- Use existing UI conventions.
- Use OneSpirit business terminology.
- Add validation where data is entered or changed.
- Add empty/loading/error states where relevant.
- Keep code maintainable.

---

## 5. Validate

After implementation:

1. Inspect available scripts.
2. Run relevant commands.
3. Fix failures.

Possible commands:

```bash
npm run lint
npm run typecheck
npm run test
npm run build
npm run dev
```

Use the project’s actual package manager and scripts.

---

## 6. Fix

If validation fails:

1. Read the error.
2. Identify the root cause.
3. Fix properly.
4. Re-run the failed command.
5. Report what was fixed.

Do not bypass validation with unsafe hacks.

---

## 7. Document

Update documentation if:

- New workflow behavior is added
- New command is required
- New entity/status is introduced
- Architecture changes
- Testing process changes

Keep documentation practical and short.

---

## 8. Run Dev

After successful build/checks, run the development server when possible.

Use the available command, for example:

```bash
npm run dev
```

or:

```bash
pnpm dev
```

Leave the app ready for user review if the environment allows it.

---

## 9. Commit

After successful validation:

```bash
git status
git add <relevant-files-only>
git commit -m "Sprint <number>: <summary>"
```

Do not commit unrelated files.

---

## 10. Push

If a remote repository is configured:

```bash
git push
```

If push fails because of authentication or remote configuration, report the reason.

---

## 11. Report

Final report must include:

```txt
Summary:
- ...

Changed files:
- ...

Validation:
- ...

Git:
- branch:
- commit:
- push status:

Dev server:
- command:
- status:

Known limitations:
- ...

Recommended next sprint:
- ...
```

---

## Sprint Scope Rules

A sprint should usually focus on one of these:

- One feature
- One workflow improvement
- One foundation improvement
- One UI/UX improvement
- One data model improvement
- One validation improvement
- One bug-fix group

Avoid mixing too many unrelated changes.

---

## OneSpirit-Specific Sprint Priorities

Prioritize:

1. Project workflow foundation
2. CL tracking
3. ROS tracking
4. CK tracking
5. PNL tracking
6. Project dashboard
7. Project readiness
8. Missing data visibility
9. Timeline and deadline clarity
10. Reporting foundation

---

## Creative Expansion Pass

At the end of implementation, review the work from these angles:

```txt
1. What user friction remains?
2. What manual step can be reduced?
3. What missing data should be more visible?
4. What next action can be clearer?
5. What error can the system prevent?
6. What would make this feel more professional?
```

Only implement the smallest safe improvement that fits the sprint.

Do not add unstable or speculative features.

---

## Sprint Anti-Patterns

Avoid:

- “Improve everything”
- “Make it more advanced” without a specific target
- Large redesigns without need
- Database rewrites without migration plan
- Adding dependencies without justification
- Creating generic CRUD screens disconnected from workflow
- Ignoring CL, ROS, CK, and PNL terminology
- Committing broken code
- Skipping validation

---

## Sprint Definition of Done

A sprint is done only when:

```txt
[ ] Objective is implemented
[ ] Existing functionality is preserved
[ ] Relevant validation commands pass or failures are explained
[ ] Documentation is updated if needed
[ ] Git commit is created
[ ] Push is attempted if remote exists
[ ] Dev server is run if possible
[ ] Final report is provided
```
