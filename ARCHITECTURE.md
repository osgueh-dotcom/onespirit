# ARCHITECTURE.md

## Architecture Goal

The OneSpirit Workflow System should be built as a maintainable business workflow application.

The architecture should support:

- Project workflow tracking
- Business document tracking
- Operational planning
- Checklist management
- Finance tracking through PNL
- Reporting
- Role-based expansion
- Future automation

---

## Architectural Principles

1. Keep business logic separate from UI rendering.
2. Keep data models explicit and consistent.
3. Use workflow terminology consistently.
4. Avoid duplicated logic across pages.
5. Centralize reusable status calculations.
6. Prefer small modules over large files.
7. Avoid premature abstraction.
8. Preserve existing conventions.
9. Make future sprints easier, not harder.
10. Treat CL, ROS, CK, and PNL as first-class workflow concepts.

---

## Recommended Layering

The exact folder names should follow the existing project structure, but the logical layers should be:

```txt
UI Layer
- Pages
- Layouts
- Components
- Forms
- Tables
- Cards
- Empty states
- Loading states
- Error states

Application Layer
- Use cases
- Workflow actions
- Validation
- Status transition logic
- Permission checks

Domain Layer
- Project model
- Client model
- CL model
- ROS model
- CK model
- PNL model
- Status definitions
- Business rules

Data Layer
- Database schema
- ORM queries
- Repository functions
- API handlers
- Server actions

Infrastructure Layer
- Auth
- Logging
- File storage
- Environment config
- External integrations
```

Do not force this structure if the current codebase uses another convention. Adapt gradually.

---

## Core Domain Concepts

### Project

A project is the central entity.

A project may connect to:

- Client
- CL
- ROS
- CK
- PNL
- Timeline
- Team
- Documents
- Activity log
- Final report

### CL

CL means Contract Letter / Confirmation Letter.

CL should help confirm the project agreement.

Potential statuses:

```txt
Not Started
Draft
Sent
Confirmed
Needs Revision
Cancelled
```

### ROS

ROS means Rundown Of Show.

ROS should define event flow, timing, agenda, and execution plan.

Potential statuses:

```txt
Not Started
Draft
In Review
Approved
Ready for Execution
Needs Revision
```

### CK

CK means Check List.

CK should track operational readiness.

Potential statuses:

```txt
Not Started
In Progress
Blocked
Completed
Verified
```

### PNL

PNL means Profit and Loss.

PNL should track financial planning and result.

Potential statuses:

```txt
Not Started
Draft
In Review
Approved
Finalized
```

---

## Recommended Project Status Model

A project may use a high-level status such as:

```txt
Inquiry
Confirmed
Planning
Ready
In Execution
Completed
Archived
Cancelled
```

A project readiness score may later be derived from:

- CL status
- ROS status
- CK completion
- PNL status
- Timeline risk
- Missing required information

Do not implement readiness scoring unless the sprint requests it or it is a small safe improvement.

---

## Data Modeling Guidelines

When adding or changing data models:

1. Use clear field names.
2. Avoid ambiguous generic fields.
3. Use enums for stable statuses when possible.
4. Keep timestamps for important records.
5. Track ownership or creator where relevant.
6. Avoid deleting records that should be archived.
7. Consider auditability for important workflow changes.
8. Keep migration changes small and reviewable.

---

## UI Architecture Guidelines

Reusable UI should be grouped around workflow needs.

Examples:

```txt
ProjectStatusBadge
ProjectReadinessCard
MissingDocumentsCard
CLStatusBadge
ROSStatusBadge
CKProgressCard
PNLStatusBadge
NextActionCard
WorkflowTimeline
```

Avoid one-off duplicated UI blocks across pages.

---

## Business Logic Guidelines

Business logic should not be scattered across components.

Examples of business logic to centralize:

- Project status mapping
- Next action calculation
- Missing document detection
- Readiness calculation
- CL/ROS/CK/PNL status rules
- PNL validation rules
- Workflow transition rules

Possible locations depend on the stack:

```txt
src/lib/workflow
src/lib/domain
src/domain
src/services
src/utils/workflow
```

Follow the existing project convention.

---

## Error Handling

Every user-facing workflow should handle:

- Loading state
- Empty state
- Not found state
- Validation error
- Server error
- Permission error when relevant

Do not expose raw technical errors to normal users.

---

## Future Architecture Direction

The system may eventually support:

- Role-based access control
- Activity log
- Document generation
- Notification/reminder system
- Project templates
- Recurring event workflows
- PNL analytics
- Dashboard analytics
- File upload and attachment tracking
- Client portal
- Vendor/crew management

These should be introduced incrementally, not all at once.

---

## Architecture Review Checklist

Before finishing a sprint, check:

```txt
[ ] Did this change preserve existing architecture?
[ ] Did this change reduce or increase duplication?
[ ] Is business terminology consistent?
[ ] Is workflow logic centralized where appropriate?
[ ] Are data structures clear?
[ ] Are UI states handled?
[ ] Can this be extended in the next sprint?
[ ] Did validation commands pass?
[ ] Is documentation updated if needed?
```
