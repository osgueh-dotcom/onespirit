# Workflow Contract

## Canonical Flow

`Inquiry -> Client Confirmation -> CL -> Project Setup -> Planning -> ROS -> CK -> Execution -> PNL -> Final Report / Archive`

## Terms

- `CL`: Contract Letter / Confirmation Letter.
- `ROS`: Rundown Of Show.
- `CK`: Check List.
- `PNL`: Profit and Loss.

Preserve these terms in code, UI, database fields, tests, and documentation when
they represent the business artifact.

## Role Intent

- `Super Admin` / `Admin`: administration and controlled override.
- `Management`: cross-project visibility and decision support.
- `PO`: commercial ownership, client follow-up, quotation, revenue, payment.
- `PM`: operational ownership, planning, ROS, CK, readiness, execution.
- `Finance`: PNL, invoice, payment, outstanding, reconciliation.
- `Staff`: assigned operational participation without implicit broad ownership.

## Behavior Rules

- Show current status, owner, risk, missing requirement, and next action.
- Block invalid transitions server-side.
- Keep important changes auditable.
- Do not infer access from hidden frontend controls.
- Do not mark a project ready when required workflow data is missing.
- Do not expose PNL data beyond authorized roles.
