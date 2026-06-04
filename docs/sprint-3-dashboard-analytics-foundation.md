# Sprint 3 — Dashboard Analytics Foundation Documentation

This document provides a comprehensive overview of the analytics foundation built during Sprint 3, covering calculations, filter mechanics, database schemas, and manual/automated verification.

---

## Analytics Endpoint Overview

The newly introduced endpoint is:
`GET /api/v1/dashboard/analytics`

It returns a structured, nested JSON payload detailing:
1. **Executive KPIs**: General conversion performance, revenue aggregates, and average deal sizes.
2. **Quotation Status Breakdown**: Counts for Draft, Sent, Follow Up, Revision, Signed & Deal, Cancel.
3. **Program Status Breakdown**: Counts for Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, Closed, Cancel.
4. **Payment Status Breakdown**: Counts for Not Invoiced, Invoice Sent, Partial Paid, Paid, Outstanding, Overdue.
5. **Project Status Breakdown**: Counts for Open, Active, Reporting, Closed, Canceled.
6. **PO Performance**: In-depth metrics (deals, cancels, closed projects, confirmed revenue) per Program Owner user.
7. **PM Workload**: Task and status balance (active, preparation, running, reporting, closed) per Program Manager user.
8. **Event Source share**: Confirmed/potential revenue, deal count, and cancels per Event Source type (Hotel, Direct, Repeater, Partner, etc.).
9. **Customer Category analytics**: Statistics grouped by client sector (Corporate, Government, Agency, etc.).
10. **Data Integrity Audits**: Automatic flags highlighting missing data, invalid budgets, or closed-but-unpaid entries.

---

## KPI Formulas & Analytics Logic

### Revenue Logic

*   **Potential Revenue**: Sum of budget fields for all projects matching the filter query.
*   **Confirmed Revenue**: Sum of budgets where the project's `quotation_status` is `"Signed & Deal"` OR `program_status` is one of `["Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed"]`.
*   **Revenue Conversion Rate**: `(Confirmed Revenue / Potential Revenue) * 100` (defaults to `0.0` if potential revenue is zero).
*   **Average Project Value**: `Confirmed Revenue / Deal Count` (defaults to `0.0` if deal count is zero).

### Ratios & Counts

*   **Deal Count**: Number of projects where `quotation_status == "Signed & Deal"`.
*   **Cancel Count**: Number of projects where `quotation_status == "Cancel"` OR `project_status == "Canceled"`.
*   **Deal Rate (%)**: `(Deal Count / Total Projects) * 100`.
*   **Cancel Rate (%)**: `(Cancel Count / Total Projects) * 100`.

---

## Filter Behavior

The endpoint accepts the following optional query parameters:
*   `year`: Filters project dates matching the specified integer year.
*   `month`: Filters project dates matching the specified integer month (1 to 12).
*   `date_from` / `date_to`: Filters projects within the given date boundaries.
*   `po_id` / `pm_id`: Restricts results to a specific Program Owner or Program Manager user ID.
*   `source_type`: Filters by event source types (e.g. Hotel, Repeater).
*   `quotation_status`, `program_status`, `payment_status`, `project_status`: Selects projects by exact status strings.
*   `customer_category`: Grouped by customer category.
*   `event_category` / `program_type`: Performs text filters on tags.

### Date Filtering Fallback

Since the DB model contains both deprecated columns (`start_date`, `end_date`) and modern columns (`event_date_start`, `event_date_end`), the service layer uses SQL coalesce to resolve dates seamlessly:
`func.coalesce(Project.event_date_start, Project.start_date)`

---

## Data Quality Logic

The audit metrics calculate:
*   `missing_po`: Projects where `program_owner_id` is null.
*   `missing_pm`: Projects where `program_manager_id` is null.
*   `missing_customer`: Projects where `customer_id` is null.
*   `missing_budget`: Projects where budget is null or `<= 0`.
*   `cancel_without_reason`: Projects marked as Cancel in `quotation_status` but having no text in `cancel_reason`.
*   `closed_not_paid`: Projects where `project_status == "Closed"` and `payment_status != "Paid"`.
*   `documentation_missing`: Projects with no linked documents.
*   `unknown_source`: Projects where `event_source_id` is null, or `source_type` is `"Other"` or `"Unknown"`.

---

## Known Limitations

1.  **In-Memory Processing**: Aggregate matrices are generated in-memory on python queryset results. While highly performant for portfolios up to a few thousand items, extremely large datasets (e.g. 50k+ projects) may benefit from SQL-level indexing and grouping in future sprints.
2.  **Date Coalescing**: If both `event_date_start` and `start_date` are null, the project is excluded from year and month date range queries but will still be evaluated for general queries and data quality audits.

---

## Next Sprint Recommendations

1.  **Clean up Legacy Endpoints**: Remove obsolete routes like `/dashboard/overview` or `/dashboard/revenue` once the premium Analytics Hub is fully adopted.
2.  **Scheduled Data Backups**: Since data audits identify mapping gaps, enable background warning notifications to POs/PMs via email/SMS weekly to encourage active record corrections.
