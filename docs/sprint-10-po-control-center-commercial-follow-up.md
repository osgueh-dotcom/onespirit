# Sprint 10 — PO Control Center & Commercial Follow-up

## Objective
The goal of Sprint 10 is to build a **PO Control Center** (Commercial Dashboard) that allows Program Owners (POs) to monitor project ownership, commercial proposal (quotation) progression, deal/cancel status, confirmed and potential revenue values, outstanding payment risks, external sales/vendor lead contributions, and follow-up priorities.

---

## Core Concept
The PO Control Center answers:
*"Program/event mana yang menjadi tanggung jawab PO, bagaimana status quotation-nya, berapa nilai revenue-nya, mana yang perlu follow-up, dan mana yang berisiko cancel/outstanding?"*

---

## Commercial Metric Definitions

- **Potential Revenue**:
  Sum of budget from all owned projects with a valid budget.
- **Confirmed Revenue**:
  Sum of budget from projects where quotation status is Signed & Deal or the project/program status indicates confirmed execution.
- **Revenue Conversion Rate**:
  Confirmed Revenue / Potential Revenue x 100.
- **Average Potential Value**:
  Potential Revenue / Total Owned Projects.
- **Average Deal Value**:
  Confirmed Revenue / Total Deal.
- **Average Project Value**:
  The current MVP dashboard uses Average Potential Value unless explicitly labeled otherwise.

> [!IMPORTANT]
> **A Note on Value Metrics**: Average Potential Value and Average Deal Value are calculated differently and should not be interpreted the same way. Average Potential Value averages all opportunities (including draft, sent, and canceled projects), while Average Deal Value focuses strictly on successfully closed/signed deals.

---

## API Endpoint Details

### `GET /api/v1/dashboard/po-control-center`

#### Request Parameters:
- `po_id` (UUID, optional)
- `pm_id` (UUID, optional)
- `source_type` (str, optional) - Lead source type (e.g. Hotel, Instagram, Partner)
- `customer_category` (str, optional) - Customer category (e.g. Corporate, Agency)
- `quotation_status` (str, optional) - Draft, Sent, Follow Up, Revision, Signed & Deal, Cancel
- `program_status` (str, optional) - Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, Closed, Cancel
- `payment_status` (str, optional) - Not Invoiced, Invoice Sent, Partial Paid, Paid, Outstanding, Overdue
- `project_status` (str, optional) - Open, Active, Reporting, Closed, Canceled
- `date_from` (date, optional)
- `date_to` (date, optional)
- `event_window` (str, optional, default "all") - today, next_7_days, next_14_days, this_month, overdue, all
- `include_closed` (bool, optional, default False)
- `include_canceled` (bool, optional, default False)

#### Response Structure:
Returns a structured JSON payload mapping exactly to `POControlCenterResponse`:
- `summary`: Key financial metrics (total projects, deal/cancel count & rates, potential vs confirmed revenue, outstanding count, invoices sent, paid counts, follow-up needed).
- `quotation_summary`: Status distribution counters.
- `revenue_summary`: Project value metrics (average, highest, lowest budgets, revenue conversion rate).
- `follow_up_priorities`: Chronological priority recommendations based on urgency levels.
- `owned_projects`: Project listings detailing customer, source/vendor, budget, statuses, and custom actions.
- `po_performance`: Program Owner performance indicators (workloads, deal rates, revenues, and outstanding payments).
- `source_contribution`: Lead contribution statistics grouped by `source_type`, `vendor_name`, and `sales_name`.
- `commercial_risks`: Warnings grouped by exception types:
  - `cancel_without_reason`
  - `signed_deal_without_budget`
  - `outstanding_payment`
  - `invoice_sent_not_paid`
  - `missing_po`
  - `missing_source`

---

## Commercial Follow-up Priority Logic

Follow-up priority adalah indikator bantu untuk membantu PO melihat project yang membutuhkan perhatian. Prioritas ini bukan keputusan final otomatis dan tetap perlu divalidasi oleh tim One Spirit berdasarkan konteks operasional dan komersial.

- **Critical**:
  - Signed & Deal project with missing budget (`budget == 0` or null).
  - Project status Canceled but `cancel_reason` is missing/empty.
  - Confirmed project with `Outstanding` or `Overdue` payment status.
  - Invoice Sent and overdue (due date < today) but not Paid/partially paid.
- **High**:
  - Proposal in Draft/Sent/Follow Up/Revision with event date approaching (within 14 days).
  - Potential high-value project (budget >= Rp 100M) not yet Signed & Deal.
  - Project marked Signed & Deal but missing an assigned Program Manager (`pm_id` is null).
- **Medium**:
  - Draft quotation with customer and event details filled (ready for commercial submission).
  - Confirmed project missing an event source, external sales, or vendor name.
  - Missing customer category on CRM.
  - Confirmed project with event dates that have no uploaded documentation/files.
- **Low**:
  - Normal active project with no immediate commercial risks.

---

## Frontend Layout & Design

The PO Control Center is implemented at `/po-control-center` in [PoControlCenter.vue](../frontend/src/views/PoControlCenter.vue) using the project's glassmorphic dark-theme design system.

### Key Sections:
- **Filters**: Responsive 2-row layout containing filters for PO, PM, Source Type, Customer Category, Date range, Quotation/Program/Payment Statuses, Event Window, and Closed/Canceled checkboxes.
- **KPI Summary Grid**: Visual metrics cards showing deal/cancel rates, revenues, outstanding values, and follow-ups.
- **Tab Panel Navigation**:
  - **Prioritas Follow-up**: Detailed lists of recommended follow-up actions colored by priority (Critical/Red, High/Amber, Medium/Blue, Low/Gray).
  - **Daftar Proyek PO**: Master project data grid with direct status indicators and action items.
  - **Kinerja Komersial**: Structured sub-grids displaying:
    - Quotation and status distribution.
    - Revenue statistics (average/highest/lowest values).
    - Individual PO commercial workloads.
    - Vendor partner/lead source performance and conversions.
  - **Risiko Komersial**: Detailed panels listing projects matching specific commercial warning exemptions (e.g. Rp 0 budgets, missing cancel reasons, overdue payments).

---

## Verification & Testing

### Backend Unit Tests
We have added a complete suite of unit tests in [test_po_control_center.py](../backend/app/tests/test_po_control_center.py). Run them inside the backend container:
```bash
docker exec onespirit_backend pytest app/tests/test_po_control_center.py
```

### Full Frontend Build Check
Validate that there are no compile-time or routing syntax errors:
```bash
docker exec onespirit_frontend npm run build
```

---

## Recommended Next Sprint

### Sprint 11 — Source & Vendor Performance Center

Focus:
- Source/vendor analytics and performance tracking
- External sales contribution reporting
- Source conversion rate and cancel rate metrics
- Source confirmed revenue vs potential revenue statistics
- Lead performance analysis (hotel vs direct vs repeater vs partner vs instagram vs web)
- Source quality indicators
