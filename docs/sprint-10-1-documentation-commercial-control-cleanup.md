# Sprint 10.1 — Documentation & Commercial Control Cleanup

This document outlines the tasks completed in **Sprint 10.1 — Documentation & Commercial Control Cleanup**, focusing on documentation portability, commercial metric clarity, follow-up priority disclaimers, and next sprint recommendations.

---

## Objective
The primary goals of this sprint patch are:
1. Ensure all system documentation is portable by removing absolute Windows path (`file:///`) links and converting them to relative markdown links.
2. Clarify PO Control Center financial metric definitions (potential vs confirmed revenue, conversion rates, potential vs deal average project values).
3. Standardize follow-up priority as a decision-support tool, not final business judgment.
4. Establish the maintainability backlog (component splitting) and recommendations for the next sprint.

---

## Files Reviewed
- [docs/README.md](README.md) (Updated)
- [docs/sprint-0-technical-modernization.md](sprint-0-technical-modernization.md) (Updated)
- [docs/sprint-10-po-control-center-commercial-follow-up.md](sprint-10-po-control-center-commercial-follow-up.md) (Updated)
- [docs/proposal-alignment.md](proposal-alignment.md) (Reviewed)
- [docs/mvp-scope.md](mvp-scope.md) (Reviewed)
- [docs/client-demo-flow.md](client-demo-flow.md) (Updated)
- [docs/demo-script.md](demo-script.md) (Updated)
- [docs/known-limitations-before-client-demo.md](known-limitations-before-client-demo.md) (Updated)
- [docs/backlog.md](backlog.md) (New file)
- [README.md](../README.md) (Updated)
- [frontend/src/views/PoControlCenter.vue](../frontend/src/views/PoControlCenter.vue) (Updated)

---

## file:/// Link Cleanup
All absolute local Windows paths containing `file:///E:/GVsys%20Project/` have been removed and replaced with relative markdown links, ensuring the documentation compiles and opens properly on any system or web viewer (such as GitHub or Gitlab previewers) without broken links.

---

## Commercial Metric Definitions
Definitions have been formalized in the Sprint 10 documentation:
- **Potential Revenue**: Sum of budget from all owned projects with a valid budget.
- **Confirmed Revenue**: Sum of budget from projects where quotation status is Signed & Deal or project/program status indicates confirmed execution.
- **Revenue Conversion Rate**: Confirmed Revenue / Potential Revenue x 100.
- **Average Potential Value**: Potential Revenue / Total Owned Projects.
- **Average Deal Value**: Confirmed Revenue / Total Deal.
- **Average Project Value**: The current MVP dashboard uses Average Potential Value unless explicitly labeled otherwise.

We have explicitly documented that Average Potential Value and Average Deal Value measure different aspects of the pipeline and should not be used interchangeably. The UI label in `PoControlCenter.vue` was updated to read **Rata-rata Nilai Proyek Potensial** and includes clarifying subtext.

---

## Follow-up Priority Disclaimer
To manage client expectations and frame follow-up recommendations correctly, the following disclaimer has been added to `docs/sprint-10-po-control-center-commercial-follow-up.md`, `docs/demo-script.md`, `docs/client-demo-flow.md`, and `docs/known-limitations-before-client-demo.md`:

> "Follow-up priority adalah indikator bantu untuk membantu PO melihat project yang membutuhkan perhatian. Prioritas ini bukan keputusan final otomatis dan tetap perlu divalidasi oleh tim One Spirit berdasarkan konteks operasional dan komersial."

---

## README / Docs Index Updates
1. **docs/README.md**: Added all missing sprint logs (Sprint 7 through Sprint 10.1) to the Sprint Logs index section.
2. **README.md** (root): Added a **Pusat Kontrol Utama (Current Control Centers)** section summarizing the Executive Dashboard, PM Control Center, and PO Control Center features.

---

## Backlog Added
Created [docs/backlog.md](backlog.md) detailing the frontend refactoring backlog to split the large `PoControlCenter.vue` component into nine smaller modular components under `frontend/src/components/commercial/`.

---

## Known Limitations
- Static prioritization logic based on database due dates and event windows. Actual communication activity logging (e.g. tracking call logs) is queued for future phases.

---

## Verification Checklist
- Run automated tests to check backend stability.
- Verify frontend production build (`npm run build`).
- Verify relative markdown links in all edited files.

---

## Next Sprint Recommendation
We recommend proceeding to **Sprint 11 — Source & Vendor Performance Center** to build analytics trackers for hotel partners, external sales agents, lead source conversion rates, and source-specific metrics.
