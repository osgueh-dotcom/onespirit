# PROJECT_CONTEXT.md

## Project Name

OneSpirit Workflow System

---

## Business Context

OneSpirit Workflow System is being developed for PT One Spirit Asia.

The system supports event/project operations, project documentation, operational planning, execution tracking, and financial visibility.

This is the user's first external client system project and should be treated as a serious production-oriented business system.

---

## Core Business Purpose

The system should help One Spirit Asia manage work from inquiry to completion.

The system should reduce scattered manual coordination by centralizing:

- Client/project information
- Project status
- CL status
- ROS preparation
- CK progress
- PNL tracking
- Execution readiness
- Reporting and archive

---

## Important Terms

- PNL = Profit and Loss
- CL = Contract Letter / Confirmation Letter
- ROS = Rundown Of Show
- CK = Check List

These are not optional labels. They are core workflow instruments in the OneSpirit system.

---

## Main Workflow

The target business workflow is:

```txt
Inquiry
→ Client Confirmation
→ CL
→ Project Setup
→ Planning
→ ROS
→ CK
→ Execution
→ PNL
→ Report / Archive
```

Each project should move through clear operational stages.

---

## Core Entities

The system may include or evolve toward these entities:

1. Client
2. Project
3. Inquiry
4. CL
5. ROS
6. CK
7. PNL
8. Team Member
9. Task / Checklist Item
10. Vendor / Partner
11. Timeline / Milestone
12. Document
13. Report
14. User / Role
15. Activity Log

The exact implementation must follow the current codebase and database structure.

---

## Core User Roles

Potential user roles:

- Admin
- Owner / Director
- Project Manager
- Operations Team
- Finance Team
- Sales / Client Relation
- Staff / Crew

The system should be designed so role-based access can be added or improved later.

---

## Product Principles

1. Workflow-first
2. Business terminology must be consistent
3. Every project should have visible status
4. Every important document should be connected to a project
5. Every operational step should be traceable
6. Users should know what to do next
7. Missing data should be visible
8. Finance and operation should connect through PNL
9. The system should reduce manual follow-up
10. The product should be maintainable sprint by sprint

---

## Current Development Method

Development is handled through iterative sprints.

Each sprint should:

- Improve the foundation or workflow
- Preserve existing functionality
- Avoid unnecessary rewrites
- Add validation where relevant
- Improve usability where relevant
- Run checks before completion
- Commit and push after successful validation
- Run dev mode for review

---

## Preferred Feature Direction

Priority features should support:

- Project dashboard
- Project status flow
- CL management
- ROS management
- CK management
- PNL management
- Project readiness indicators
- Missing document indicators
- Timeline and deadline visibility
- Operational next actions
- Simple reporting

---

## Design Direction

The system should feel like:

- Clean
- Professional
- Operational
- Clear
- Reliable
- Business-oriented

Avoid making it feel like:

- A generic admin template
- A decorative landing page
- A disconnected CRUD app
- A demo-only prototype

---

## Decision Rule

When choosing between two possible implementations:

Prefer the one that is:

1. Safer
2. Easier to maintain
3. More aligned with OneSpirit workflow
4. Easier for staff to understand
5. Easier to validate
6. Easier to extend in later sprints

---

## Current Priority

The current priority is to mature the OneSpirit workflow foundation before adding overly advanced features.

Focus on:

- Data structure clarity
- Workflow clarity
- UI consistency
- Project status logic
- CL / ROS / CK / PNL terminology
- Validation
- Maintainability
- Test/build stability
