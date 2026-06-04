# Sprint 1 — One Spirit Domain Refactor

This document outlines the technical decisions, architecture adjustments, database modifications, and APIs introduced in Sprint 1 of the One Spirit Workflow Modernization.

---

## 1. Domain & Architectural Decisions

To match the real One Spirit workflow, the business domains and roles were restructured:

1. **Internal Users vs. External Sales**:
   - **Internal Users** represent actual employees who log in to the system.
   - **External Sales Agents** are external contacts representing partner agencies, venues, or independent sales reps. They do not log in and are handled under the **Event Source** model.
   
2. **Project-Level Role Assignment (PO and PM)**:
   - **Program Owner (PO)** and **Program Manager (PM)** are no longer permanent user roles.
   - They are project-level assignments. Any internal user (regardless of their security access level) can act as the PO or PM for a given project/event.
   
3. **Pure Access Control Roles**:
   - Internal system roles are strictly reserved for access controls:
     - `Super Admin`: Full system configuration.
     - `Management`: Administrative actions, approvals, project cancellation.
     - `Finance`: Billing, invoicing, payment audits.
     - `Staff`: General operations, task checklist management, schedule updates.

4. **Event Source Entity**:
   - Tracks how a project/event opportunity was brought to One Spirit (e.g., Hotel, Direct, Repeater, Partner, Instagram, Web, etc.), vendor associations, and the external sales representative's contact info.

---

## 2. Database Schema Changes (Alembic)

Database schema modifications were applied incrementally using Alembic migrations (revision `16cff05b1eef`).

### New Table: `event_sources`
- `id` (UUID, Primary Key)
- `source_type` (String, e.g., Hotel, Partner, Direct, etc.)
- `vendor_name` (String, Nullable)
- `sales_name` (String, Nullable)
- `contact` (String, Nullable)
- `notes` (Text, Nullable)
- `is_active` (Boolean, default True)
- `created_at` / `updated_at` / `deleted_at`

### Modified Table: `projects`
- Added the following foreign keys:
  - `event_source_id` -> references `event_sources.id` (Nullable)
  - `program_owner_id` -> references `users.id` (Nullable)
  - `program_manager_id` -> references `users.id` (Nullable)
- Added new workflow/details fields:
  - `project_code` (String, Unique index)
  - `inquiry_date` (Date, Nullable)
  - `event_category` (String, Nullable)
  - `program_type` (String, Nullable)
  - `program_name` (String, Nullable)
  - `quantity` (Integer, Nullable)
  - `venue` (String, Nullable)
  - `duration` (String, Nullable)
  - `event_date_start` (Date, Nullable)
  - `event_date_end` (Date, Nullable)
  - `quotation_date` (Date, Nullable)
  - `quotation_number` (String, Nullable)
  - `quotation_status` (String, default "Draft")
  - `program_status` (String, default "Inquiry")
  - `payment_status` (String, default "Not Invoiced")
  - `project_status` (String, default "Open")
  - `cancel_reason` (Text, Nullable)
  - `mom_notes` (Text, Nullable)
  - `general_notes` (Text, Nullable)
- **Backward Compatibility**: Existing columns (like `status`, `start_date`, `end_date`) are marked as deprecated but remain operational. Write actions auto-replicate values to these columns to prevent legacy features from breaking.

---

## 3. Backend API Modernization

### Event Sources Endpoints (`/api/v1/event-sources`)
- `GET /` - List active event sources (with pagination).
- `GET /{source_id}` - Retrieve details of an event source.
- `POST /` - Register a new event source.
- `PUT /{source_id}` - Update details of an event source.
- `DELETE /{source_id}` - Soft-delete/archive an event source.

### Projects List Query Filtering (`GET /api/v1/projects`)
Introduced parameters to allow flexible server-side filtering:
- `po_id` (UUID): Filter by assigned Program Owner.
- `pm_id` (UUID): Filter by assigned Program Manager.
- `source_id` (UUID): Filter by Event Source.
- `quotation_status` (String): Filter by quote stage.
- `program_status` (String): Filter by operational workflow stage.
- `payment_status` (String): Filter by invoice status.
- `project_status` (String): Filter by overall project pipeline state.

### Transition Workflow Gates (`POST /api/v1/projects/{project_id}/transition`)
Operational gates are now enforced during state transitions:
1. **Cancellation**: Only users with `Super Admin` or `Management` roles can advance status to `Cancel`.
2. **Operations Completion**: Transitioning to `Completed` program status requires that all associated tasks in the Project checklist have a status of `"done"`.

---

## 4. Excel Import Logic & Mappings

The Excel parsing engine (`imports/service.py`) maps the standard workflow spreadsheets to the refactored domain:

* **Header Aliases**: Built robust, case-insensitive mapping lists matching standard Excel titles (e.g. `INQ Date` -> `inquiry_date`, `Pax` -> `quantity`, `ROS` -> `ros` checklist).
* **Automatic Event Source Provisioning**: If the row specifies a `Partner` or `Sales` name that does not exist in the database, the importer auto-provisions a new `EventSource` entity.
* **Initials Resolution**: Matches PM and PO initials (e.g., `JD` -> `John Doe`) to internal users. If initials cannot be matched, it falls back to keeping the raw text and logging unresolved names in the project's `general_notes` for manual review.

---

## 5. Frontend Enhancements

1. **Filters Toolbar**: Added a collapsible/responsive multi-criteria select toolbar on the `/projects` page to filter the dashboard layout by PO, PM, Source, and the 4 status types.
2. **List View Columns**: Upgraded All Projects List table to output `Code`, `Source / Sales`, `PO`, `PM`, `Quotation Status`, `Payment Status`, and `Project Status`.
3. **Creation Form**: Expanded the project registration modal to capture all new refactored fields in an elegant, scrollable two-column CSS grid.
4. **Kanban Pipelines**: Shifted columns from legacy status names to real-world status terms (`Inquiry`, `Confirmed`, `Preparation`, `Ready`, `Running`, `Completed`, `Reporting`, `Closed`, `Cancel`).

---

## 6. Known Limitations & Next Steps

* **Analytics Dashboard**: The dashboard widgets and charts still analyze using the legacy `status` values and do not yet reflect the multi-dimensional status taxonomies (Program, Payment, Project).
* **Recommendations for Sprint 2**:
  - Refactor `/dashboard` charts and endpoints to compile statistics using `payment_status` (for revenue pipelines) and `program_status` / `project_status` (for project delivery metrics).
  - Integrate a detailed edit screen for project profiles to change new fields post-creation.
