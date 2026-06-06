# Sprint 7: Project Instruments Workflow Refinement

## Objective
The goal of Sprint 7 is to refine Project Instruments / Operational Checklist workflows, transforming CL, ROS, CK, PNL, PF, and MATRIX documents into actionable indicators for project readiness, dashboard statistics, data quality checks, and client validation.

---

## Technical Details

### 1. Instrument Readiness Calculations
For each project, the system now calculates:
- **`required_instruments_count`**: Total active instruments where status is NOT `Not Required`.
- **`completed_required_instruments_count`**: Total required instruments where status is `Done`.
- **`instrument_completion_rate`**: `completed_required_instruments_count` divided by `required_instruments_count` (returns `0.0` if `required_instruments_count` is 0).
- **`missing_required_instruments_count`**: Total required instruments where status is NOT `Done`.
- **`revision_required_count`**: Total required instruments where status is `Need Revision`.
- **`overdue_instruments_count`**: Total instruments where `due_date` has passed (i.e. `due_date < today`) and status is NOT `Done` and NOT `Not Required`.

### 2. Project Readiness Score Formula
A project readiness score (`project_readiness_score` ranging from `0.0` to `1.0` / `0%` to `100%`) is calculated in the backend to provide a transparent indicators of operational health:
$$\text{Readiness Score} = (\text{Instrument Completion Rate} \times 0.6) + (\text{Documentation Score} \times 0.2) + (\text{Status Consistency Score} \times 0.2)$$

Where:
- **`Documentation Score`**: `1.0` if the project has at least one active document uploaded, else `0.0`.
- **`Status Consistency Score`**: `max(0.0, 1.0 - 0.2 * len(warnings))` based on the number of active project validation warnings.

### 3. Extended Project Validation Warnings
The system checks for:
- **CL missing or not Done** when quotation status is Signed & Deal.
- **PNL missing, not Done, or missing document URL** when quotation status is Signed & Deal.
- **ROS not Done** when program status is Ready, Running, Completed, Reporting, or Closed.
- **CK not Done** when program status is Ready, Running, Completed, Reporting, or Closed.
- **Instrument has status Need Revision**.
- **Instrument is overdue** (`due_date` in the past and status is not Done or Not Required).
- **PNL sensitivity warning** alerting managers that PNL access needs restriction.

*Note: These warnings do not block workflow state transitions; they act as operational guide rails.*

### 4. PNL Sensitivity Foundation
- Users who are NOT `Super Admin`, `Management`, or `Finance` (e.g. `Staff`) will have PNL `document_url` masked as `None` in all backend API responses.
- The frontend `ProjectInstrumentsPanel.vue` shows the PNL instrument exists but displays a secure lock badge with the note: *"Restricted (Admin/Finance/Mgmt Only)"* and disables URL inputs.

### 5. Automated Completed Date & Activity Logs
- Shifting status to `Done` automatically sets `completed_date` to `date.today()`.
- Shifting status away from `Done` **preserves** the `completed_date` (no automatic clearing).
- Activity logging logs changes to:
  - Instrument status (with custom actions `instrument_marked_not_required` and `instrument_marked_need_revision`).
  - Instrument due dates (`instrument_due_date_changed`).
  - Instrument completed dates (`instrument_completed_date_changed`).
  - Instrument document URLs (`instrument_document_url_updated`).

### 6. Excel Import Refinement
The import logic parses instrument status column inputs case-insensitively:
- `"Done"`, `"Yes"`, `"Ada"`, `"OK"`, `"Complete"`, `"Completed"`, `"1"`, `"x"`, `"true"`, `"check"` $\rightarrow$ **Done** (sets completed date to today).
- URL-like value (starts with `http`) $\rightarrow$ **Done** with `document_url` set to the value.
- `"-"`, empty, null $\rightarrow$ **Not Started**.
- `"N/A"`, `"Not Required"` $\rightarrow$ **Not Required**.
- `"Revision"`, `"Revise"`, `"Need Revision"` $\rightarrow$ **Need Revision**.
- Other text $\rightarrow$ **In Progress** with the notes column populated and an import warning generated.

---

## API & Schema Changes
- `ProjectDetailResponse` schema: added required metrics and scores.
- `DashboardAnalyticsResponse`: added `instrument_summary` (contains aggregated dashboard data: `missing_cl`, `missing_ros`, `missing_ck`, `missing_pnl`, `instruments_need_revision`, `instruments_overdue`, `average_instrument_completion_rate`).

---

## Frontend Changes
- **`ProjectDetail.vue`**: Added a Project Readiness Indicator sidebar card with completion rates, overdue and revision counts, progress bar, and score-based colored badges.
- **`ProjectInstrumentsPanel.vue`**: Added a dashboard summary block at the top, red overdue alerts, a quick inline status select dropdown in the table, and client-side PNL masking.

---

## How to Test

### Automated Tests
- Run `pytest backend/app/tests/test_instruments.py` to test instrument workflow, auto completed dates, overdue detection, Need Revision warnings, and PNL masking.
- Run `pytest backend/app/tests/test_analytics.py` to test executive dashboard instrument summary analytics.

### Manual Verification
1. Run `docker compose up --build`.
2. Navigate to project details. Look for the **Project Readiness Indicator** sidebar card.
3. Edit an instrument. Mark it as **Done**, check that Completed Date is set. Move it back to **In Progress**, check that Completed Date is preserved.
4. Set an instrument's due date in the past, verify the red **Overdue** indicator animates on screen.
5. Log in as a staff user and verify that the PNL document link is masked.

---

---

## Sprint 7.1: Instruments Readiness Stabilization Patch
Sprint 7.1 stabilizes the readiness calculations, warning score penalties, and empty-state safeguards:
- **Scoring Adjustment on PNL Security Notes**: The system-wide PNL sensitivity note (*"PNL access warning: PNL document is sensitive..."*) is treated as a security reminder rather than an operational checklist failure. It is now excluded from the readiness score calculation (it no longer reduces the operational readiness score) but remains visible in the UI validation warnings.
- **Empty-State and Filter Division by Zero Safeguards**: All dashboard aggregation metrics (including `average_instrument_completion_rate`) and frontend Vue panel metrics handle empty lists, missing fields, `NaN`, and `null` gracefully without crash or layout deformation.
- **Verification Coverage**: Backend tests now assert that empty instruments, non-existent years in dashboards, and PNL warnings are processed cleanly.

---

## Next Sprint Recommendation
Implement Sprint 8: Role-based document access controls for all modules to graduate the PNL sensitivity foundation into a complete system-wide file access authorization layer.

