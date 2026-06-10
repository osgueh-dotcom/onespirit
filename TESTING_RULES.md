# TESTING_RULES.md

## Purpose

This file defines validation and testing expectations for the OneSpirit Workflow System.

The goal is to keep the system stable while it evolves sprint by sprint.

---

## Testing Philosophy

OneSpirit is a business workflow system. Testing should focus on:

1. Preventing broken pages
2. Preventing invalid workflow data
3. Preserving business terminology
4. Protecting CL / ROS / CK / PNL flows
5. Ensuring project status remains understandable
6. Ensuring users can complete core tasks

---

## Required Validation Before Completion

Before finishing any sprint, inspect `package.json` and run relevant available commands.

Common commands:

```bash
npm run lint
npm run typecheck
npm run test
npm run build
```

If using pnpm:

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

If using yarn:

```bash
yarn lint
yarn typecheck
yarn test
yarn build
```

Do not run commands that do not exist in the project.

---

## Development Server Check

After successful validation, run the app in dev mode if possible:

```bash
npm run dev
```

or equivalent.

Check that key pages load.

---

## Manual Testing Checklist

For UI or workflow changes, manually check:

```txt
[ ] Page loads without crashing
[ ] Navigation still works
[ ] Main data is visible
[ ] Empty state works
[ ] Loading state works if applicable
[ ] Error state works if applicable
[ ] Form validation works if applicable
[ ] Save/update/delete action works if applicable
[ ] Business terminology is correct
[ ] No obvious layout break
[ ] No console error from the changed feature
```

---

## Core Workflow Test Areas

When relevant, check these areas:

### Project

```txt
[ ] Project list loads
[ ] Project detail loads
[ ] Project status is visible
[ ] Project next action is clear
[ ] Project data can be created/updated if supported
```

### CL

```txt
[ ] CL status is visible
[ ] CL terminology is consistent
[ ] Missing CL is clearly shown
[ ] CL update flow works if supported
```

### ROS

```txt
[ ] ROS status is visible
[ ] ROS terminology is consistent
[ ] Missing ROS is clearly shown
[ ] ROS update flow works if supported
```

### CK

```txt
[ ] CK status/progress is visible
[ ] CK terminology is consistent
[ ] Checklist items are readable
[ ] Incomplete checklist items are visible
```

### PNL

```txt
[ ] PNL status is visible
[ ] PNL terminology is consistent
[ ] Financial values are formatted clearly
[ ] Invalid values are blocked if applicable
```

---

## Automated Testing Direction

When the codebase supports tests, prioritize tests for:

1. Workflow status calculations
2. Next action logic
3. Missing document detection
4. Form validation
5. PNL calculations
6. Permission logic
7. API/server actions
8. Critical UI rendering

---

## Suggested Unit Test Targets

If the project has test infrastructure, create tests for functions such as:

```txt
getProjectStatus()
getProjectReadiness()
getMissingProjectDocuments()
getNextProjectAction()
validatePNLInput()
calculatePNLSummary()
formatProjectTimeline()
```

Do not create fake test infrastructure unless the sprint explicitly asks for it. If no test framework exists, recommend one in the final report instead of forcing it.

---

## Build Quality Rules

Never finish a sprint with:

- Type errors
- Broken imports
- Missing exported components
- Invalid routes
- Broken build
- Unresolved merge conflict markers
- Disabled validation without explanation

---

## Error Reporting Rules

If a validation command fails, report:

```txt
Command:
Error:
Cause:
Fix:
Re-run result:
```

If not fixed, report:

```txt
Command:
Error:
Likely cause:
Why it remains unresolved:
Recommended next action:
```

---

## Regression Safety

Before completing a sprint, check that the change did not break:

- Existing pages
- Existing routes
- Existing shared components
- Existing database queries
- Existing authentication assumptions
- Existing project terminology
- Existing build process

---

## Test Data Rules

When test data or seed data is needed:

- Use realistic OneSpirit workflow terms.
- Do not use offensive or irrelevant names.
- Do not hardcode sensitive real client data unless explicitly provided and intended.
- Prefer clearly fake but realistic data.

Example fake project names:

```txt
Corporate Gathering 2026
Product Launch Event
Annual Meeting Production
Brand Activation Roadshow
```

---

## Final Validation Report Template

Use this in the final sprint report:

```txt
Validation:
- package manager detected:
- lint:
- typecheck:
- test:
- build:
- dev server:

Manual check:
- pages checked:
- workflow checked:
- known issue:
```

---

## Sprint 10 Final Validation Results

Tanggal Pengujian: 2026-06-10

Backend:
Command:
pytest app/tests -q
Result:
16 passed

Frontend:
Command:
npm run build
Result:
build success

Docker:
Command:
docker compose up --build
Result:
backend, frontend, database running
