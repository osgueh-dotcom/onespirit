# Sprint 4 — Dashboard Presentation & Executive Reporting

Transform the dashboard from a technical analytics page into a presentation-ready executive dashboard for PT. One Spirit Asia.

## Objectives
- Realize an executive layout suitable for direct board presentation and business evaluation.
- Auto-generate an operational summary narrative in Indonesian.
- Formulate dynamic management evaluation guidelines detailing Strengths, Risks, and Actions.
- Provide a clean, printer-friendly PDF output format by hiding headers, sidebars, navigation controls, and filter grids.

---

## Dashboard Structure

### 1. Header & Context Indicator
- **Title**: Executive Dashboard
- **Subtitle**: One Spirit Workflow & Business Analytics
- Includes last updated synced timestamp and active period overview (e.g. `Tahun 2025, Juni`).
- Includes a primary **"Print / Save Report"** button that invokes the browser's PDF export dialog.

### 2. Collapsible Filter Matrix
Provides dropdown inputs to query the database dynamically. 
- Year, Month, Dates limits.
- Assigned PO, PM.
- Quotation, Program, Payment, and Project status bounds.
- Event source type, Customer category, Event categories, and Program types.

### 3. Executive Summary Narrative
Translates numerical data points into a fluent, professional Indonesian narrative:
- Mentions inquiry records, deals signed, conversion ratios, confirmed revenue, and target achievement rate (relative to Rp 9.2B Target).
- Shows highlights and alert warnings if cancellation rates exceed wajar boundaries (>30%) or if operational data issues exist.
- Safely reverts to a clean neutral empty state if no records match active filters.

### 4. Executive KPI Cards
Displays 9 primary metrics:
- **Total Inquiry**: Total inquiry/project records matching the filter.
- **Total Deal**: Count of projects that converted into "Signed & Deal" quotation status.
- **Deal Rate (%)**: Ratio of deals won to total inquiry.
- **Cancel Rate (%)**: Ratio of cancelled quotations/projects to total inquiry.
- **Potential Revenue**: Sum of budget parameters for all queried projects.
- **Confirmed Revenue**: Sum of budget parameters for projects containing deals or confirmed programs.
- **Target Achievement (%)**: Confirmed revenue relative to Rp 9.2B Target.
- **Revenue Conversion Rate (%)**: Confirmed revenue relative to potential revenue.
- **Average Project Value**: Confirmed revenue divided by deal counts.

### 5. Revenue & Target Section
Renders the radial target achievement meter alongside confirmed, potential, and conversion rate cards.

### 6. Workflow Stages Status Matrix
Renders counting metrics across all four status phases:
- **Quotation Statuses**: Draft, Sent, Follow Up, Revision, Signed & Deal, Cancel.
- **Program Statuses**: Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, Closed, Cancel.
- **Payment Statuses**: Not Invoiced, Invoice Sent, Partial Paid, Paid, Outstanding, Overdue.
- **Project Statuses**: Open, Active, Reporting, Closed, Canceled.

### 7. PO & PM Performance Grids
Tables showing work metrics, won counts, average budgets, and active workloads categorized per PO and PM initials code.

### 8. Source & Market Share
Grid representing revenue share bars for Event sources, Customer category, Event category, and Program type.

### 9. Finance & Payment Summary
Gathers payment count by status, paid counts, outstanding counts, collected cash (`revenue_received`), collection rate, and outstanding pipeline balances.

### 10. Data Integrity Audits
Identifies data anomalies like missing POs, PMs, budget parameters, customer mappings, cancel reasons, or document links. Explains how data quality affects reporting accuracy.

### 11. Management Evaluation Notes
Generates tactical feedback points:
- **Strengths**: Triggered by positive deal conversions (>=45%), target milestones, or zero-issue integrity profiles.
- **Risks**: Flags high cancellations (>50%), outstanding receivables, or data gaps.
- **Recommended Actions**: Actionable prompts to clear outstanding debts, assign Program Owners, or audit documentation.

---

## Print & Presentation Mode Details
Using CSS media queries (`@media print`), the browser layout undergoes automatic adjustments when printing or saving as a PDF:
- Hides sidebars, navigation headers, search matrices, reset buttons, and action links (`display: none !important`).
- Overrides dark-theme colors, formatting elements with dark-text (`#1a202c`) on a white background.
- Adjusts height bounds and container layouts to prevent broken tables, cropped segments, or vertical scrollbar rendering.

---

## Verification
- Run tests verifying new backend calculations: `docker exec onespirit_backend pytest`
- Check Vue builds: `npm run build`
- Run the system containers: `docker-compose up -d --build`
- Verify REST endpoint: `/api/v1/dashboard/analytics`
- Manual print preview checking (`Ctrl + P`) in the web application dashboard view.
