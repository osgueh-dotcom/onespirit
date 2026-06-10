# Commercial Control Logic Reference

This document explains the definitions, calculations, data sources, fallbacks, and ambiguities used to manage commercial operations in the OneSpirit Workflow System.

---

## 1. Core Definitions

### A. Potential Revenue
* **Definition**: The total estimated value of all projects owned by a Program Owner (PO), regardless of the current contract or quotation status. It represents the gross pipeline size.
* **Status Range**: All projects matching the query (including drafts, sent, follow-ups, and cancellations if explicitly included).

### B. Confirmed Revenue
* **Definition**: Revenue from projects that have successfully completed the commercial gate (Signed & Deal quotation status) or are active in operational stages.
* **Status Range**: Projects where:
  * `quotation_status` is `"Signed & Deal"`
  * **OR** `program_status` is one of: `Confirmed`, `Preparation`, `Ready`, `Running`, `Completed`, `Reporting`, `Closed`.

### C. Outstanding Payment
* **Definition**: The total unpaid balance for issued invoices, representing active receivables.
* **Calculation**: For each project's active (non-deleted) invoices, compute:
  $$\text{Invoice Amount} - \text{Total Approved Payments}$$
  The sum across all projects represents the total outstanding payment value.

### D. Pending Quotation
* **Definition**: Project opportunities currently undergoing active negotiations or proposal revisions, but not yet closed or cancelled.
* **Status Range**: Projects where `quotation_status` is one of: `Draft`, `Sent`, `Follow Up`, `Revision`.

### E. Follow-up Needed
* **Definition**: Projects flagged for urgent PO intervention due to commercial anomalies, approaching event dates without a signed contract, or unpaid invoices.
* **Status Range**: Active projects triggered by specific validation rules (defined in formulas below).

### F. Cancelled/Lost
* **Definition**: Projects that were terminated by the client or failed to sign, excluded from revenue calculations.
* **Status Range**: Projects where:
  * `quotation_status == "Cancel"` **OR**
  * `project_status == "Canceled"` **OR**
  * `program_status == "Cancel"`

### G. Commercial Risk
* **Definition**: Any operational or financial exception that indicates a threat to project profitability or administrative completeness.

---

## 2. Formulas & Calculation Methods

### Metrik Summary

1. **Total Owned Projects**:
   $$\text{Count}(P) \quad \text{where } P.\text{deleted\_at} = \text{null}$$
2. **Deal Rate**:
   $$\frac{\text{Total Deal Projects}}{\text{Total Owned Projects}} \times 100$$
3. **Cancel Rate**:
   $$\frac{\text{Total Cancelled Projects}}{\text{Total Owned Projects}} \times 100$$
4. **Potential Revenue**:
   $$\sum \text{budget}(P)$$
5. **Confirmed Revenue**:
   $$\sum \text{budget}(P) \quad \text{where } P.\text{quotation\_status} = \text{"Signed \& Deal"} \lor P.\text{program\_status} \in \text{ConfirmedStatuses}$$
6. **Outstanding Payment**:
   $$\sum (\text{invoice}.\text{amount} - \text{payment}.\text{amount}) \quad \text{where } \text{payment}.\text{status} = \text{"approved"} \land \text{invoice/payment}.\text{deleted\_at} = \text{null}$$
7. **Average Project Value**:
   $$\frac{\text{Potential Revenue}}{\text{Total Owned Projects}}$$
8. **Commercial Risk Count**:
   $$\text{Count}(P) \quad \text{where } P \text{ triggers at least one Commercial Risk rule}$$

---

## 3. Data Sources

| Metric | Database Fields | Tables Involved |
| :--- | :--- | :--- |
| **Budget / Value** | `projects.budget` | `projects` |
| **Quotation Status** | `projects.quotation_status` | `projects` |
| **Program Status** | `projects.program_status` | `projects` |
| **Payment Details** | `invoices.amount`, `payments.amount`, `payments.status` | `invoices`, `payments` |
| **Ownership** | `projects.program_owner_id`, `projects.program_manager_id` | `users` |
| **Lead Sources** | `event_sources.source_type`, `event_sources.vendor_name` | `event_sources` |

---

## 4. Fallbacks & Missing Data Handling

* **Missing Budget**: If a project's budget is `null`, it defaults to `0.0`. It is also flagged as a **Critical** or **High** priority risk if the project is already `Signed & Deal`.
* **Missing Dates**: If a project has no start date, date-based follow-up triggers (e.g. H-14 event alerts) are skipped, and the project is flagged for manual audit.
* **Missing Program Owner / Lead Source**: Defaults to `"-"` in the UI and is listed as a commercial risk.

---

## 5. Known Ambiguities

1. **Quotation Status vs Program Status**: A project may have `quotation_status` as `"Sent"` but its operational `program_status` is already set to `"Preparation"` during early coordination. For revenue compilation safety, OneSpirit counts this as **Confirmed Revenue** to align with operation commitments.
2. **Deposit vs Invoice Matching**: Payments are matched directly against invoices. Invoices not created yet but paid via deposits will not reduce the outstanding payment balance until an invoice is explicitly created and the payment is linked.
