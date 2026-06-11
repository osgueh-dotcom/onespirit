# PDF Export Flow Plan

Sprint 14 plans the official PDF export flow. It does not implement large PDF export features.

---

## 1. Documents Requiring PDF Export

- CL
- ROS
- CK
- PNL
- Final project report
- Management report
- Invoice/Finance report

---

## 2. Role Access

| Document | Recommended Export Role |
|---|---|
| CL | Admin, Management, PO |
| ROS | Admin, Management, PM |
| CK | Admin, Management, PM |
| PNL | Admin, Management, Finance |
| Final project report | Admin, Management, PO, PM |
| Management report | Admin, Management |
| Invoice/Finance report | Admin, Management, Finance |

---

## 3. Data Sources

| Document | Data Source |
|---|---|
| CL | Project, customer, quotation status, related document upload |
| ROS | Project detail, event schedule, rundown entries, PM assignment |
| CK | Project instruments, tasks/checklist, readiness warnings |
| PNL | Finance invoices/payments, project budget, actual payment data |
| Final report | Project summary, CL/ROS/CK/PNL status, activity logs, payment status |
| Management report | Dashboard analytics, PO/PM performance, source/vendor analytics |

---

## 4. Template Requirements

- Company header and One Spirit Asia identity.
- Project code and project title.
- Client/customer profile.
- Date, venue, PO, and PM.
- Document status and approval metadata.
- Export timestamp.
- Page number and footer.
- Signature/approval block where required.

---

## 5. Approval Flow

- CL: PO drafts, Management/Admin approves.
- ROS: PM drafts, Management/Admin approves if required.
- CK: PM maintains, Management/Admin reviews before execution.
- PNL: Finance prepares, Management approves.
- Final report: PM/PO completes, Management signs off.

---

## 6. Filename Convention

Recommended format:

```text
ONESPIRIT_<DOCUMENT_TYPE>_<PROJECT_CODE>_<YYYYMMDD>.pdf
```

Examples:

```text
ONESPIRIT_ROS_OSA-2026-001_20260611.pdf
ONESPIRIT_PNL_OSA-2026-001_20260611.pdf
```

---

## 7. Print vs Generated PDF

| Approach | Fit |
|---|---|
| Browser print | MVP/demo, quick manual PDF save, low complexity |
| Client-side generated PDF | Useful for lightweight reports, but harder to control layout and fonts |
| Server-side generated PDF | Recommended for production official documents and audit consistency |

Current MVP can continue using browser print. Production should evaluate server-side PDF generation for official CL, ROS, CK, PNL, and final report.

---

## 8. Technical Recommendation

- Keep browser print for MVP demo.
- Define document templates first.
- Add backend endpoint only after template and approval rules are agreed.
- Store exported PDF metadata if audit trail is required.
- Recommended metadata: document type, project ID, template version, exported by, exported at, approval status, and source data version.
- Avoid generating fake PDF flows that are not connected to real project data.

---

## 9. Implementation Priority

1. Final Report.
2. Invoice/Finance report.
3. CL template.
4. ROS template.
5. CK template.
6. PNL template.
7. Management report pack.
