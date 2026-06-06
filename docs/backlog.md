# One Spirit Backlog & Future Recommendations

This backlog outlines maintainability tasks, system refactoring, and roadmap features planned for future sprints.

---

## Frontend Maintainability Backlog

### 1. Split `PoControlCenter.vue` Component
- **Component Path**: `frontend/src/views/PoControlCenter.vue`
- **Objective**: Refactor the monolithic `PoControlCenter.vue` (currently > 1,100 lines of code) into modular, single-responsibility sub-components under `frontend/src/components/commercial/`.
- **Proposed Components**:
  - `PoControlSummaryCards.vue` - Key KPI cards (Total Projects, Deal/Cancel Rates, Revenue, Outstanding, Follow-up).
  - `PoControlFilters.vue` - Filters toolbar (PO, PM, Source Type, Category, Dates, Windows).
  - `FollowUpPriorityList.vue` - Critical/High follow-up list cards.
  - `OwnedProjectsTable.vue` - Master PO projects data table.
  - `QuotationSummary.vue` - Quotation status structure cards.
  - `CommercialRevenueSummary.vue` - Revenue statistics and conversion rates.
  - `PoPerformanceTable.vue` - Staf PO workloads and deal rate comparisons.
  - `SourceContributionTable.vue` - Partner hotel/lead source conversion list.
  - `CommercialRisksPanel.vue` - Financial warning panels (Rp 0 budgets, missing cancel reasons, overdue invoices).

---

## Recommended Next Sprint

### Sprint 11 — Source & Vendor Performance Center

Focus areas for the upcoming sprint:
1. **Source & Vendor Analytics**: Build a unified dashboard to compare hotel referrals, direct leads, repeating clients, agencies, and online sources (Instagram, web).
2. **External Sales Performance Tracking**: Monitor external sales representatives (attached to vendor/source profiles) and trace their conversion rates and revenue contribution.
3. **Source Conversion & Cancellation Rates**: Automatically calculate which sources produce the highest deal rates and which sources lead to the highest cancellations.
4. **Source Quality Indicators**: Implement audit ratings to track lead quality based on historical project readiness, timeliness of payment, and cancellation risk ratios.
