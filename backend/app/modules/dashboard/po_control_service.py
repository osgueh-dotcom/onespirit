from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.modules.projects.models import Project
from app.modules.auth.models import User
from app.modules.event_sources.models import EventSource
from app.modules.crm.models import Customer

def get_po_control_center_data(
    db: Session,
    po_id: Optional[str] = None,
    pm_id: Optional[str] = None,
    source_type: Optional[str] = None,
    customer_category: Optional[str] = None,
    quotation_status: Optional[str] = None,
    program_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    project_status: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    event_window: str = "all",
    include_closed: bool = False,
    include_canceled: bool = False
) -> Dict[str, Any]:
    today = date.today()

    # 1. Base Query with joined loads
    query = db.query(Project).filter(Project.deleted_at == None).options(
        joinedload(Project.customer),
        joinedload(Project.program_manager),
        joinedload(Project.program_owner),
        joinedload(Project.event_source),
        joinedload(Project.invoices),
        joinedload(Project.documents)
    )

    # 2. Exclude Closed / Canceled by default
    if not include_closed:
        query = query.filter(
            Project.program_status != "Closed",
            Project.project_status != "Closed"
        )
    if not include_canceled:
        query = query.filter(
            Project.program_status != "Cancel",
            Project.project_status != "Canceled",
            Project.quotation_status != "Cancel"
        )

    # 3. Apply Filters
    if po_id:
        try:
            parsed_po = UUID(po_id)
            query = query.filter(Project.program_owner_id == parsed_po)
        except ValueError:
            pass

    if pm_id:
        try:
            parsed_pm = UUID(pm_id)
            query = query.filter(Project.program_manager_id == parsed_pm)
        except ValueError:
            pass

    if source_type:
        query = query.join(EventSource, Project.event_source_id == EventSource.id).filter(EventSource.source_type == source_type)

    if customer_category:
        query = query.join(Customer, Project.customer_id == Customer.id).filter(Customer.category == customer_category)

    if quotation_status:
        query = query.filter(Project.quotation_status == quotation_status)

    if program_status:
        query = query.filter(Project.program_status == program_status)

    if payment_status:
        query = query.filter(Project.payment_status == payment_status)

    if project_status:
        query = query.filter(Project.project_status == project_status)

    if date_from:
        query = query.filter(Project.event_date_start >= date_from)

    if date_to:
        query = query.filter(Project.event_date_start <= date_to)

    # 4. Event Window Filters
    if event_window == "today":
        query = query.filter(
            Project.event_date_start <= today,
            or_(Project.event_date_end >= today, Project.event_date_end == None, Project.event_date_start == today)
        )
    elif event_window == "next_7_days":
        query = query.filter(Project.event_date_start >= today, Project.event_date_start <= today + timedelta(days=7))
    elif event_window == "next_14_days":
        query = query.filter(Project.event_date_start >= today, Project.event_date_start <= today + timedelta(days=14))
    elif event_window == "this_month":
        first_day_of_month = date(today.year, today.month, 1)
        if today.month == 12:
            last_day_of_month = date(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
        query = query.filter(Project.event_date_start >= first_day_of_month, Project.event_date_start <= last_day_of_month)
    elif event_window == "overdue":
        query = query.filter(
            Project.event_date_end < today,
            Project.program_status != "Completed",
            Project.program_status != "Closed",
            Project.program_status != "Cancel"
        )

    all_projects = query.all()

    # 5. Initialization
    total_owned = len(all_projects)
    total_deal = 0
    total_cancel = 0
    potential_revenue = 0.0
    confirmed_revenue = 0.0
    outstanding_count = 0
    invoice_sent_count = 0
    paid_count = 0
    follow_up_needed_count = 0
    active_projects = 0
    pending_quotation_projects = 0
    cancelled_projects = 0
    outstanding_payment_amount = 0.0
    commercial_risk_count = 0

    quotation_statuses = ["Draft", "Sent", "Follow Up", "Revision", "Signed & Deal", "Cancel"]
    quot_counts = {s: 0 for s in quotation_statuses}

    project_budgets = []
    follow_up_priorities = []
    owned_projects_list = []

    po_performance_map = {}
    source_contribution_map = {}

    # Commercial Risk arrays
    cancel_without_reason_list = []
    signed_deal_without_budget_list = []
    outstanding_payment_list = []
    invoice_sent_not_paid_list = []
    missing_po_list = []
    missing_source_list = []

    confirmed_prog_statuses = {"Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed"}

    for p in all_projects:
        budget = float(p.budget) if p.budget is not None else 0.0
        project_budgets.append(budget)

        # Basic statuses
        q_status = p.quotation_status or "Draft"
        pr_status = p.program_status or "Inquiry"
        py_status = p.payment_status or "Not Invoiced"
        pj_status = p.project_status or "Open"

        # Count quotations
        if q_status in quot_counts:
            quot_counts[q_status] += 1
        else:
            quot_counts[q_status] = quot_counts.get(q_status, 0) + 1

        is_deal = (q_status == "Signed & Deal")
        is_cancel = (q_status == "Cancel" or pj_status == "Canceled" or pr_status == "Cancel")

        if is_deal:
            total_deal += 1
        if is_cancel:
            total_cancel += 1

        # Revenue logic
        potential_revenue += budget
        is_confirmed_rev = (is_deal or pr_status in confirmed_prog_statuses)
        if is_confirmed_rev:
            confirmed_revenue += budget

        # Payment details
        if py_status in ["Outstanding", "Overdue"]:
            outstanding_count += 1
        elif py_status == "Invoice Sent":
            invoice_sent_count += 1
        elif py_status == "Paid":
            paid_count += 1

        # Calculate active projects (not closed and not cancelled)
        is_closed = (pj_status == "Closed" or pr_status == "Closed")
        if not is_closed and not is_cancel:
            active_projects += 1

        # Calculate pending quotation projects
        if q_status in ["Draft", "Sent", "Follow Up", "Revision"]:
            pending_quotation_projects += 1

        # Calculate cancelled projects
        if is_cancel:
            cancelled_projects += 1

        # Calculate actual outstanding payment amount for the project (invoice amount - paid amount)
        proj_outstanding_payment = 0.0
        for inv in p.invoices:
            if inv.deleted_at is None:
                inv_amt = float(inv.amount)
                paid_amt = 0.0
                for pay in inv.payments:
                    if pay.deleted_at is None and pay.status == "approved":
                        paid_amt += float(pay.amount)
                proj_outstanding_payment += max(0.0, inv_amt - paid_amt)
        outstanding_payment_amount += proj_outstanding_payment

        # Calculate if project has commercial risks
        has_risk = False
        if is_cancel and not p.cancel_reason:
            has_risk = True
        if q_status == "Signed & Deal" and budget <= 0:
            has_risk = True
        if py_status in ["Outstanding", "Overdue"]:
            has_risk = True
        if py_status == "Invoice Sent":
            has_risk = True
        if not p.program_owner_id:
            has_risk = True
        if not p.event_source_id:
            has_risk = True
        
        if has_risk:
            commercial_risk_count += 1

        # Relationships
        po_name = p.program_owner.full_name if p.program_owner else "-"
        pm_name = p.program_manager.full_name if p.program_manager else "-"
        customer_name = p.customer.company_name if p.customer else "-"

        # Source values
        if p.event_source:
            src_type = p.event_source.source_type or "Direct"
            vendor_name = p.event_source.vendor_name or "-"
            sales_name = p.event_source.sales_name or "-"
        else:
            src_type = "Direct"
            vendor_name = "-"
            sales_name = "-"

        # Follow-up priorities logic
        priority = None
        reason = ""
        rec_action = ""

        # Critical Triggers
        if q_status == "Signed & Deal" and budget <= 0:
            priority = "Critical"
            reason = "Proyek Signed & Deal tetapi memiliki budget Rp 0/tidak terisi."
            rec_action = "Masukkan nilai budget/revenue real untuk proyek ini."
        elif is_cancel and not p.cancel_reason:
            priority = "Critical"
            reason = "Status proyek Batal (Cancel) tetapi tidak ada alasan pembatalan."
            rec_action = "Isi alasan pembatalan (cancel_reason) pada detail proyek."
        elif py_status in ["Outstanding", "Overdue"] and pr_status in confirmed_prog_statuses:
            priority = "Critical"
            reason = f"Status pembayaran proyek terkonfirmasi adalah {py_status}."
            rec_action = "Hubungi klien segera untuk penagihan pembayaran."
        elif py_status == "Invoice Sent" and any(inv.due_date and inv.due_date < today and inv.status != "paid" for inv in p.invoices):
            priority = "Critical"
            reason = "Invoice sudah terkirim dan melewati jatuh tempo (overdue) tetapi belum lunas."
            rec_action = "Lakukan follow-up pembayaran sisa tagihan kepada klien."

        # High Triggers
        elif q_status in ["Sent", "Follow Up", "Revision"] and p.event_date_start and (p.event_date_start - today).days <= 14:
            priority = "High"
            days_left = (p.event_date_start - today).days
            reason = f"Event dijadwalkan {p.event_date_start} (H-{days_left}) tetapi status penawaran masih {q_status}."
            rec_action = "Follow up klien untuk finalisasi penawaran dan tanda tangan kontrak (CL)."
        elif not is_deal and not is_cancel and budget >= 100000000.0:
            priority = "High"
            reason = f"Proyek potensial bernilai besar (Rp {budget:,.2f}) belum berstatus Signed & Deal."
            rec_action = "Prioritaskan negosiasi komersial untuk segera mengamankan deal."
        elif q_status == "Signed & Deal" and not p.program_manager_id:
            priority = "High"
            reason = "Proyek sudah Signed & Deal tetapi belum ditugaskan Program Manager (PM)."
            rec_action = "Tunjuk Program Manager (PM) untuk memulai persiapan rundown (ROS) dan checklist (CK)."

        # Medium Triggers
        elif q_status == "Draft" and p.customer_id and p.event_date_start:
            priority = "Medium"
            reason = "Draft penawaran dengan klien dan jadwal sudah terisi tetapi belum dikirim."
            rec_action = "Tinjau kelengkapan detail draft penawaran lalu kirim ke klien."
        elif not p.event_source_id and pr_status in confirmed_prog_statuses:
            priority = "Medium"
            reason = "Proyek aktif terkonfirmasi tidak memiliki event source/vendor/sales penanggung jawab."
            rec_action = "Tentukan event source / data partner untuk proyek ini."
        elif p.customer_id and p.customer and not p.customer.category:
            priority = "Medium"
            reason = "Kategori klien (customer category) pada proyek ini kosong."
            rec_action = "Lengkapi kategori klien pada modul CRM."
        elif pr_status in confirmed_prog_statuses and not p.documents:
            priority = "Medium"
            reason = "Proyek terkonfirmasi/selesai tetapi tidak memiliki dokumentasi berkas yang diunggah."
            rec_action = "Unggah berkas kontrak atau foto dokumentasi acara."

        # Low Triggers
        elif not is_cancel and pj_status != "Closed":
            priority = "Low"
            reason = "Proyek aktif berjalan normal tanpa resiko komersial terdeteksi."
            rec_action = "Monitor progress penawaran dan koordinasi persiapan berkala."

        if priority:
            follow_up_needed_count += 1
            follow_up_priorities.append({
                "priority_level": priority,
                "project_id": p.id,
                "project_code": p.project_code,
                "customer_name": customer_name,
                "program_name": p.program_name or p.title or "Untitled Project",
                "po_name": po_name,
                "pm_name": pm_name,
                "quotation_status": q_status,
                "program_status": pr_status,
                "payment_status": py_status,
                "budget": budget,
                "event_date_start": p.event_date_start,
                "reason": reason,
                "recommended_action": rec_action
            })

        # Owned Projects Details list
        owned_projects_list.append({
            "project_id": p.id,
            "project_code": p.project_code,
            "customer_name": customer_name,
            "source_type": src_type,
            "vendor_name": vendor_name,
            "sales_name": sales_name,
            "po_name": po_name,
            "pm_name": pm_name,
            "quotation_status": q_status,
            "program_status": pr_status,
            "payment_status": py_status,
            "project_status": pj_status,
            "budget": budget,
            "event_date_start": p.event_date_start,
            "follow_up_status": priority if priority else "Normal",
            "recommended_action": rec_action if rec_action else "Kondisi komersial proyek terpantau aman."
        })

        # PO Performance mapping
        if p.program_owner:
            po = p.program_owner
            if po.id not in po_performance_map:
                initial_code = po.initial_code if po.initial_code else po.email.split("@")[0].upper()[:3]
                po_performance_map[po.id] = {
                    "po_id": po.id,
                    "po_name": po.full_name,
                    "initial_code": initial_code,
                    "total_projects": 0,
                    "deal_count": 0,
                    "cancel_count": 0,
                    "confirmed_revenue": 0.0,
                    "potential_revenue": 0.0,
                    "outstanding_count": 0,
                    "follow_up_needed_count": 0
                }
            po_perf = po_performance_map[po.id]
            po_perf["total_projects"] += 1
            if is_deal:
                po_perf["deal_count"] += 1
            if is_cancel:
                po_perf["cancel_count"] += 1
            if is_confirmed_rev:
                po_perf["confirmed_revenue"] += budget
            po_perf["potential_revenue"] += budget
            if py_status in ["Outstanding", "Overdue"]:
                po_perf["outstanding_count"] += 1
            if priority:
                po_perf["follow_up_needed_count"] += 1

        # Lead Source Contribution
        src_key = (src_type, vendor_name, sales_name)
        if src_key not in source_contribution_map:
            source_contribution_map[src_key] = {
                "source_type": src_type,
                "vendor_name": vendor_name,
                "sales_name": sales_name,
                "total_projects": 0,
                "deal_count": 0,
                "cancel_count": 0,
                "confirmed_revenue": 0.0,
                "potential_revenue": 0.0
            }
        src_contr = source_contribution_map[src_key]
        src_contr["total_projects"] += 1
        if is_deal:
            src_contr["deal_count"] += 1
        if is_cancel:
            src_contr["cancel_count"] += 1
        if is_confirmed_rev:
            src_contr["confirmed_revenue"] += budget
        src_contr["potential_revenue"] += budget

        # Risk listings
        risk_proj_data = {
            "project_id": p.id,
            "project_code": p.project_code,
            "customer_name": customer_name,
            "program_name": p.program_name or p.title or "Untitled Project",
            "budget": budget,
            "quotation_status": q_status,
            "program_status": pr_status,
            "payment_status": py_status,
            "po_name": po_name,
            "pm_name": pm_name
        }

        if is_cancel and not p.cancel_reason:
            cdata = risk_proj_data.copy()
            cdata["reason"] = "Status proyek Batal (Cancel) tetapi data cancel_reason kosong."
            cancel_without_reason_list.append(cdata)

        if q_status == "Signed & Deal" and budget <= 0:
            sdata = risk_proj_data.copy()
            sdata["reason"] = "Proyek sudah Signed & Deal tetapi nilai budget kosong (Rp 0)."
            signed_deal_without_budget_list.append(sdata)

        if py_status in ["Outstanding", "Overdue"]:
            odata = risk_proj_data.copy()
            odata["reason"] = f"Proyek mengalami keterlambatan pembayaran dengan status: {py_status}."
            outstanding_payment_list.append(odata)

        if py_status == "Invoice Sent":
            idata = risk_proj_data.copy()
            idata["reason"] = "Invoice sudah dikirim tetapi belum tercatat lunas (Paid)."
            invoice_sent_not_paid_list.append(idata)

        if not p.program_owner_id:
            mdata = risk_proj_data.copy()
            mdata["reason"] = "Proyek berjalan tetapi belum ditugaskan Program Owner (PO)."
            missing_po_list.append(mdata)

        if not p.event_source_id:
            msdata = risk_proj_data.copy()
            msdata["reason"] = "Proyek tidak memiliki data lead source (Event Source) / vendor."
            missing_source_list.append(msdata)

    # 6. Sorting Follow-up Priorities
    prio_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    follow_up_priorities.sort(key=lambda x: prio_order.get(x["priority_level"], 4))

    # 7. Compile list structures
    po_performance_list = []
    for po_id_key, po_d in po_performance_map.items():
        total_p = po_d["total_projects"]
        deal_c = po_d["deal_count"]
        po_performance_list.append({
            "po_id": po_d["po_id"],
            "po_name": po_d["po_name"],
            "initial_code": po_d["initial_code"],
            "total_projects": total_p,
            "deal_count": deal_c,
            "cancel_count": po_d["cancel_count"],
            "deal_rate": (deal_c / total_p * 100.0) if total_p > 0 else 0.0,
            "confirmed_revenue": po_d["confirmed_revenue"],
            "potential_revenue": po_d["potential_revenue"],
            "average_project_value": (po_d["potential_revenue"] / total_p) if total_p > 0 else 0.0,
            "outstanding_count": po_d["outstanding_count"],
            "follow_up_needed_count": po_d["follow_up_needed_count"]
        })
    po_performance_list.sort(key=lambda x: x["total_projects"], reverse=True)

    source_contribution_list = []
    for sc_d in source_contribution_map.values():
        total_p = sc_d["total_projects"]
        source_contribution_list.append({
            "source_type": sc_d["source_type"],
            "vendor_name": sc_d["vendor_name"],
            "sales_name": sc_d["sales_name"],
            "total_projects": total_p,
            "deal_count": sc_d["deal_count"],
            "cancel_count": sc_d["cancel_count"],
            "confirmed_revenue": sc_d["confirmed_revenue"],
            "potential_revenue": sc_d["potential_revenue"],
            "average_project_value": (sc_d["potential_revenue"] / total_p) if total_p > 0 else 0.0
        })
    source_contribution_list.sort(key=lambda x: x["total_projects"], reverse=True)

    # Global summaries
    deal_rate = (total_deal / total_owned * 100.0) if total_owned > 0 else 0.0
    cancel_rate = (total_cancel / total_owned * 100.0) if total_owned > 0 else 0.0
    avg_proj_value = (potential_revenue / total_owned) if total_owned > 0 else 0.0
    conversion_rate = (confirmed_revenue / potential_revenue * 100.0) if potential_revenue > 0 else 0.0

    highest_val = max(project_budgets) if project_budgets else 0.0
    lowest_val = min(project_budgets) if project_budgets else 0.0

    return {
        "summary": {
            "total_owned_projects": total_owned,
            "total_deal": total_deal,
            "total_cancel": total_cancel,
            "deal_rate": deal_rate,
            "cancel_rate": cancel_rate,
            "potential_revenue": potential_revenue,
            "confirmed_revenue": confirmed_revenue,
            "average_project_value": avg_proj_value,
            "outstanding_count": outstanding_count,
            "invoice_sent_count": invoice_sent_count,
            "paid_count": paid_count,
            "follow_up_needed_count": follow_up_needed_count,
            "active_projects": active_projects,
            "pending_quotation_projects": pending_quotation_projects,
            "follow_up_needed_projects": follow_up_needed_count,
            "cancelled_projects": cancelled_projects,
            "outstanding_payment": outstanding_payment_amount,
            "commercial_risk_count": commercial_risk_count
        },
        "quotation_summary": {
            "count_by_status": quot_counts,
            "draft_count": quot_counts.get("Draft", 0),
            "sent_count": quot_counts.get("Sent", 0),
            "follow_up_count": quot_counts.get("Follow Up", 0),
            "revision_count": quot_counts.get("Revision", 0),
            "signed_deal_count": quot_counts.get("Signed & Deal", 0),
            "cancel_count": quot_counts.get("Cancel", 0)
        },
        "revenue_summary": {
            "potential_revenue": potential_revenue,
            "confirmed_revenue": confirmed_revenue,
            "revenue_conversion_rate": conversion_rate,
            "average_project_value": avg_proj_value,
            "highest_project_value": highest_val,
            "lowest_project_value": lowest_val
        },
        "follow_up_priorities": follow_up_priorities,
        "owned_projects": owned_projects_list,
        "po_performance": po_performance_list,
        "source_contribution": source_contribution_list,
        "commercial_risks": {
            "cancel_without_reason": cancel_without_reason_list,
            "signed_deal_without_budget": signed_deal_without_budget_list,
            "outstanding_payment": outstanding_payment_list,
            "invoice_sent_not_paid": invoice_sent_not_paid_list,
            "missing_po": missing_po_list,
            "missing_source": missing_source_list
        }
    }
