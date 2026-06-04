# Sprint 2.5 — Stabilization & QA Report

This document summarizes the QA, testing, and stabilization results of the One Spirit Workflow System carried out during Sprint 2.5.

## What Was Tested
1. **Alembic Database Migration Flow**: Verified execution of migrations from scratch. Ensured naming conventions map consistently.
2. **Table Startup Creation Guards**: Checked that `Base.metadata.create_all` respects `AUTO_CREATE_TABLES` environments.
3. **PATCH /projects/{project_id}/status**: Tested the generic endpoint for transitions across all four workflows (quotation, program, payment, and project status) with comment notes prompts.
4. **Excel Import Engine**: Validated synchronization and error detection on `Project Workflow OS 2025.xlsx`.
5. **Role Assignment Checks**: Audited PM/PO operations to check project-level `program_manager_id` assignments instead of user-level roles.
6. **Frontend Split Sub-components**: Ensured modular panels split from `ProjectDetail.vue` compile into target production scripts without errors.

## What Was Fixed
- **Unnamed Constraint Errors**: Applied explicit SQLAlchemy naming conventions (`naming_convention` in `database.py`) to enforce safe database schema migrations.
- **Double Space and Line Break Mappings**: Handled `\n` and double spaces in header columns dynamically inside the cleaning parser.
- **Project Detail UI Coupling**: Extracted timeline logs, audit activity timeline ledger, validation warning cards, documents linking uploads panel, and summary headers to component modularity.
- **Dynamic PM Status Shifts**: Corrected authorization checks to evaluate matching `current_user.id == project.program_manager_id` for program updates.

## Migration Notes
- Database models now use declarative metadata conventions preventing database-specific index naming errors.
- Default settings for development auto-create tables via `AUTO_CREATE_TABLES=true` while production deployments handle migrations via Alembic command CLI.

## Build/Test Results
- **Pytest Suite**: All 8 backend tests passed successfully with zero failures.
- **Frontend Assets Build**: Clean production build run via Vite with zero warnings or errors.

## Excel Import Verification Results
Verification dry-run processed all 264 workbook rows of `Project Workflow OS 2025.xlsx`:
- **Total Rows**: 264 (263 valid rows, 1 skipped empty row).
- **Quotation Status Distribution**:
  - `Cancel`: 141 (Target: ~142)
  - `Signed & Deal`: 122 (Target: ~122)
- **Payment Status Distribution**:
  - `Paid`: 103 (Target: ~103)
  - `Invoice Sent`: 1
  - `Not Invoiced`: 159
- **PO/PM Mappings**: 961 warnings identified. PO initials like `JIP` and PM initials like `OME` are reported as unmapped initials because no corresponding database users exist for these on seed initialization.

## Known Issues
- Seed user initial mappings: Warnings regarding unmapped PO/PM initials (`JIP`, `OME`, etc.) will continue until those users are officially provisioned in the CRM base.

## Readiness for Sprint 3
The workflow core, migration configurations, status patch logs, and Excel importing engine are in a highly stable, production-ready state. The database naming conventions and settings guards ensure safe deployments. This system is fully prepared to proceed with the Sprint 3 Dashboard Analytics module.
