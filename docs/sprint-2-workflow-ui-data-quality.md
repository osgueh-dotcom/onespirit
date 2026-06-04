# One Spirit Modernization - Sprint 2: Workflow UI & Data Quality

This document outlines the changes, new data structures, custom business validations, Excel import mapping upgrades, and frontend enhancements introduced in Sprint 2.

## What Changed

1. **Database Schema Enhancements (Migrations)**:
   - Added unique `initial_code` column and index on `users` table to map Excel PO and PM initials into internal users.
   - Added `normalized_name` column and index on `customers` table to prevent duplicate customer candidates.
   - Refactored `project_status_logs` (timeline logs) to support `status_type`, `old_status`, `new_status`, and `changed_by_user_id` columns, alongside legacy columns for backward compatibility.
   - Created the `project_activity_logs` table to log general mutations (e.g., changes to PM, PO, budget, document assets, project creation, closures, and Excel syncs).
   - Added `document_type` and `url` to the `documents` table to map and group attachments systematically.

2. **Backend Domain Logic Upgrades**:
   - Mapped Excel PO/PM initials using the new `initial_code` lookups.
   - Normalized client names by removing spaces, lowercasing, collapsing spaces, and stripping punctuation (using a custom helper) to detect matching duplicate client candidates during import.
   - Normalized event sources to clean controlled source types: `Hotel`, `Direct`, `Repeater`, `Partner`, `Instagram`, `Web`, `Other`. Falling back to `Other` generates an import warning.
   - Created custom validation warning checks (such as end dates before start dates, outstanding payments upon closing, missing cancel reasons, exceeding budgets, and completing events without operational assets).
   - Upgraded document mappings to standard uppercase types: `SIGNED_FILE`, `PHOTO`, `VIDEO`, `TEASER`, `INSTAGRAM`, `YOUTUBE`, `OTHER`.

3. **Advanced Excel Import preview and quality reporting**:
   - Validating/Previewing and committing Excel sheets returns row counts, success statistics, unmapped initials, unknown sources, duplicate customers, and warnings per row.

4. **Frontend Operations Center Overhaul**:
   - Modified `ProjectDetail.vue` to show client details, assignment initials, progress progress bars, status timeline history, activity logs, and quality warning alerts.
   - Added status selectors directly on the detail page to allow program owners to execute workflow gate transitions.
   - Enhanced `Projects.vue` pipeline boards and tables to show inline visual quality alerts (e.g. missing PO/PM, overdue payments, and missing cancellation reasons).

---

## New Models & Database Schema

### `ProjectActivityLog`
Stores non-status modifications on projects for audit ledger compliance.
- `id` (UUID, Primary Key)
- `project_id` (ForeignKey referencing `projects.id`)
- `user_id` (ForeignKey referencing `users.id`, nullable)
- `action` (String, e.g. `project_created`, `pm_changed`, `po_changed`, `budget_updated`, `document_added`, etc.)
- `field_name` (String, nullable)
- `old_value` (Text, nullable)
- `new_value` (Text, nullable)
- `notes` (Text, nullable)
- `created_at` (DateTime)

### Refactored Fields
- `users.initial_code` (String, Unique Index)
- `customers.normalized_name` (String, Index)
- `documents.document_type` (String)
- `documents.url` (String)
- `project_status_logs.status_type` (String)
- `project_status_logs.old_status` (String)
- `project_status_logs.new_status` (String)
- `project_status_logs.changed_by_user_id` (UUID)

---

## Validation Rules & Warning Criteria

The system automatically checks for the following 8 data quality discrepancies and flags them as warning banners on the frontend detail pages and spreadsheet import reviews:
1. **Date Sequence**: `event_date_end` occurs before `event_date_start`.
2. **Missing Budget**: The project budget is null, missing, or negative.
3. **Cancel Reason missing**: Quotation status is marked as 'Cancel' but no cancel reason is recorded.
4. **Deal discrepancy**: Quotation status is marked as 'Signed & Deal' (or approved) but budget is zero or missing.
5. **Close status discrepancy**: Project status is marked as 'Closed' but payment status is not 'Paid'.
6. **Documentation checklist discrepancy**: Program status is marked as 'Completed' or 'Closed' but no documents/assets are linked.
7. **Zero paid collection**: Payment status is marked as 'Paid' but total collected amount from invoices is zero or missing.
8. **Budget Overrun**: Paid collected amount exceeds the deal budget.

---

## Excel Import Engine Quality Notes

Standard columns mapping for documents:
- `Signed File` &rarr; `SIGNED_FILE`
- `Link Photo` &rarr; `PHOTO`
- `Link Video` &rarr; `VIDEO`
- `Link Teaser` &rarr; `TEASER`
- `IG` &rarr; `INSTAGRAM`
- `YT` &rarr; `YOUTUBE`

If initials cannot be matched to users, the importer preserves raw PO/PM strings in the project notes and adds an unmapped initials warning.

---

## Known Limitations

- **Deduplication Safeguards**: Duplicate customer candidates are highlighted as quality warnings during Excel preview and detail views, but are not automatically merged. Merging should be executed manually or in a future dashboard screen to prevent unintended data loss.
- **Legacy Columns sync**: Legacy fields like `from_status` and `to_status` on `ProjectStatusLog` are synced in parallel to prevent third-party database dependency breaks.

---

## How to Test

### Backend Automated Test suite
Verify imports, data validation logic, and user resolution:
```bash
docker compose exec backend pytest
```

### Frontend Compilation
Verify that all Vue views compile successfully without warnings:
```bash
docker compose exec frontend npm run build
```

### Manual Verification Flows
1. Spin up docker containers: `docker compose up --build`.
2. Access `http://localhost:5173/projects`.
3. Check the inline visual indicators next to project titles and Kanban cards.
4. Open a project detail page and verify tabs render client detail cards, assignments with initials, and timelines.
5. Link a new reference document and verify that quality warnings refresh.
6. Verify status transitions generate audit trails in the timeline tab.
