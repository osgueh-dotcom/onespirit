from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.modules.projects.models import Project
from app.modules.event_sources.models import EventSource
from app.modules.auth.models import User

def get_source_vendor_performance_data(
    db: Session,
    po_id: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    include_closed: bool = False,
    include_canceled: bool = False
) -> Dict[str, Any]:
    today = date.today()

    # 1. Base Query with relations
    query = db.query(Project).filter(Project.deleted_at == None).options(
        joinedload(Project.customer),
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

    if date_from:
        query = query.filter(Project.event_date_start >= date_from)

    if date_to:
        query = query.filter(Project.event_date_start <= date_to)

    all_projects = query.all()

    # 4. Initialize maps
    source_map = {}
    vendor_map = {}
    po_source_map = {}

    missing_source_count = 0
    missing_vendor_count = 0
    total_projects_analyzed = len(all_projects)
    total_potential_revenue = 0.0
    total_confirmed_revenue = 0.0
    total_outstanding_payment = 0.0
    commercial_risk_count = 0

    confirmed_prog_statuses = {"Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed"}

    for p in all_projects:
        budget = float(p.budget) if p.budget is not None else 0.0
        total_potential_revenue += budget

        q_status = p.quotation_status or "Draft"
        pr_status = p.program_status or "Inquiry"
        py_status = p.payment_status or "Not Invoiced"
        pj_status = p.project_status or "Open"

        is_deal = (q_status == "Signed & Deal")
        is_cancel = (q_status == "Cancel" or pj_status == "Canceled" or pr_status == "Cancel")
        is_confirmed_rev = (is_deal or pr_status in confirmed_prog_statuses)

        if is_confirmed_rev:
            total_confirmed_revenue += budget

        # Active project calculation
        is_closed = (pj_status == "Closed" or pr_status == "Closed")
        is_active = (not is_closed and not is_cancel)

        # Pending quotation calculation
        is_pending_quotation = (q_status in ["Draft", "Sent", "Follow Up", "Revision"])

        # Calculate outstanding payment on this project
        proj_outstanding = 0.0
        for inv in p.invoices:
            if inv.deleted_at is None:
                inv_amt = float(inv.amount)
                paid_amt = 0.0
                for pay in inv.payments:
                    if pay.deleted_at is None and pay.status == "approved":
                        paid_amt += float(pay.amount)
                proj_outstanding += max(0.0, inv_amt - paid_amt)
        total_outstanding_payment += proj_outstanding

        # Check follow up priority triggers
        is_follow_up = False
        if q_status == "Signed & Deal" and budget <= 0:
            is_follow_up = True
        elif is_cancel and not p.cancel_reason:
            is_follow_up = True
        elif py_status in ["Outstanding", "Overdue"] and pr_status in confirmed_prog_statuses:
            is_follow_up = True
        elif py_status == "Invoice Sent" and any(inv.due_date and inv.due_date < today and inv.status != "paid" for inv in p.invoices):
            is_follow_up = True
        elif q_status in ["Sent", "Follow Up", "Revision"] and p.event_date_start and (p.event_date_start - today).days <= 14:
            is_follow_up = True
        elif not is_deal and not is_cancel and budget >= 100000000.0:
            is_follow_up = True
        elif q_status == "Signed & Deal" and not p.program_manager_id:
            is_follow_up = True
        elif q_status == "Draft" and p.customer_id and p.event_date_start:
            is_follow_up = True
        elif not p.event_source_id and pr_status in confirmed_prog_statuses:
            is_follow_up = True

        # Check commercial risk triggers
        has_risk = False
        if is_cancel and not p.cancel_reason:
            has_risk = True
        elif q_status == "Signed & Deal" and budget <= 0:
            has_risk = True
        elif py_status in ["Outstanding", "Overdue"]:
            has_risk = True
        elif py_status == "Invoice Sent":
            has_risk = True
        elif not p.program_owner_id:
            has_risk = True
        elif not p.event_source_id:
            has_risk = True
        
        if has_risk:
            commercial_risk_count += 1

        # Source type mapping
        if p.event_source:
            src_type = p.event_source.source_type or "Direct"
            vendor_name = p.event_source.vendor_name or "-"
        else:
            src_type = "Direct"
            vendor_name = "-"
            missing_source_count += 1

        if p.event_source_id and (not p.event_source.vendor_name or p.event_source.vendor_name == "-"):
            missing_vendor_count += 1

        # A. Grouping by Event Source Type
        if src_type not in source_map:
            source_map[src_type] = {
                "source_type": src_type,
                "total_projects": 0,
                "active_projects": 0,
                "confirmed_projects": 0,
                "cancelled_projects": 0,
                "pending_quotation_projects": 0,
                "potential_revenue": 0.0,
                "confirmed_revenue": 0.0,
                "outstanding_payment": 0.0,
                "follow_up_needed": 0,
                "commercial_risk": 0
            }
        s_data = source_map[src_type]
        s_data["total_projects"] += 1
        if is_active:
            s_data["active_projects"] += 1
        if is_deal:
            s_data["confirmed_projects"] += 1
        if is_cancel:
            s_data["cancelled_projects"] += 1
        if is_pending_quotation:
            s_data["pending_quotation_projects"] += 1
        s_data["potential_revenue"] += budget
        if is_confirmed_rev:
            s_data["confirmed_revenue"] += budget
        s_data["outstanding_payment"] += proj_outstanding
        if is_follow_up:
            s_data["follow_up_needed"] += 1
        if has_risk:
            s_data["commercial_risk"] += 1

        # B. Grouping by Vendor Name (only structured ones)
        if vendor_name and vendor_name != "-":
            if vendor_name not in vendor_map:
                vendor_map[vendor_name] = {
                    "vendor_name": vendor_name,
                    "total_projects": 0,
                    "active_projects": 0,
                    "confirmed_projects": 0,
                    "cancelled_projects": 0,
                    "potential_revenue": 0.0,
                    "confirmed_revenue": 0.0,
                    "risk_count": 0
                }
            v_data = vendor_map[vendor_name]
            v_data["total_projects"] += 1
            if is_active:
                v_data["active_projects"] += 1
            if is_deal:
                v_data["confirmed_projects"] += 1
            if is_cancel:
                v_data["cancelled_projects"] += 1
            v_data["potential_revenue"] += budget
            if is_confirmed_rev:
                v_data["confirmed_revenue"] += budget
            if has_risk:
                v_data["risk_count"] += 1

        # C. Grouping by PO & Source Type Combined
        po_name = p.program_owner.full_name if p.program_owner else "Unassigned"
        po_id_val = p.program_owner_id
        po_src_key = (po_name, src_type)
        if po_src_key not in po_source_map:
            po_source_map[po_src_key] = {
                "po_id": po_id_val,
                "po_name": po_name,
                "source_type": src_type,
                "total_projects": 0,
                "confirmed_projects": 0,
                "pending_projects": 0,
                "potential_revenue": 0.0,
                "confirmed_revenue": 0.0,
                "follow_up_needed": 0
            }
        pos_data = po_source_map[po_src_key]
        pos_data["total_projects"] += 1
        if is_deal:
            pos_data["confirmed_projects"] += 1
        if is_pending_quotation:
            pos_data["pending_projects"] += 1
        pos_data["potential_revenue"] += budget
        if is_confirmed_rev:
            pos_data["confirmed_revenue"] += budget
        if is_follow_up:
            pos_data["follow_up_needed"] += 1

    # 5. Compile outputs and calculations
    source_performance_list = []
    for s_name, s_data in source_map.items():
        total_p = s_data["total_projects"]
        potential_r = s_data["potential_revenue"]
        confirmed_c = s_data["confirmed_projects"]
        cancel_c = s_data["cancelled_projects"]
        
        # conversion_rate = deal projects / total projects * 100
        # cancel_rate = cancel projects / total projects * 100
        source_performance_list.append({
            "source_type": s_name,
            "total_projects": total_p,
            "active_projects": s_data["active_projects"],
            "confirmed_projects": confirmed_c,
            "cancelled_projects": cancel_c,
            "pending_quotation_projects": s_data["pending_quotation_projects"],
            "potential_revenue": potential_r,
            "confirmed_revenue": s_data["confirmed_revenue"],
            "outstanding_payment": s_data["outstanding_payment"],
            "average_project_value": (potential_r / total_p) if total_p > 0 else 0.0,
            "conversion_rate": (confirmed_c / total_p * 100.0) if total_p > 0 else 0.0,
            "cancel_rate": (cancel_c / total_p * 100.0) if total_p > 0 else 0.0,
            "follow_up_needed": s_data["follow_up_needed"],
            "commercial_risk": s_data["commercial_risk"]
        })
    source_performance_list.sort(key=lambda x: x["total_projects"], reverse=True)

    vendor_performance_list = []
    for v_name, v_data in vendor_map.items():
        total_p = v_data["total_projects"]
        potential_r = v_data["potential_revenue"]
        vendor_performance_list.append({
            "vendor_name": v_name,
            "total_projects": total_p,
            "active_projects": v_data["active_projects"],
            "confirmed_projects": v_data["confirmed_projects"],
            "cancelled_projects": v_data["cancelled_projects"],
            "potential_revenue": potential_r,
            "confirmed_revenue": v_data["confirmed_revenue"],
            "average_project_value": (potential_r / total_p) if total_p > 0 else 0.0,
            "usage_frequency": total_p,
            "risk_count": v_data["risk_count"]
        })
    vendor_performance_list.sort(key=lambda x: x["total_projects"], reverse=True)

    po_source_performance_list = []
    for pos_data in po_source_map.values():
        po_source_performance_list.append(pos_data)
    po_source_performance_list.sort(key=lambda x: x["total_projects"], reverse=True)

    # 6. Generate Alerts
    risk_alerts = []
    for src in source_performance_list:
        source_type_name = src["source_type"]
        total_p = src["total_projects"]
        cancel_rate = src["cancel_rate"]
        pending_count = src["pending_quotation_projects"]
        pending_ratio = pending_count / total_p if total_p > 0 else 0.0
        outstanding_p = src["outstanding_payment"]

        if total_p >= 2:
            if cancel_rate > 30.0:
                risk_alerts.append({
                    "level": "High",
                    "category": "high_cancellation",
                    "message": f"Source '{source_type_name}' memiliki cancellation rate tinggi: {cancel_rate:.1f}% ({src['cancelled_projects']} dari {total_p} proyek batal)."
                })
            if pending_ratio > 0.5:
                risk_alerts.append({
                    "level": "Medium",
                    "category": "high_pending_quotation",
                    "message": f"Source '{source_type_name}' memiliki rasio pending quotation tinggi: {pending_ratio*100:.1f}% ({pending_count} proyek pending)."
                })
        if outstanding_p > 50000000.0:
            risk_alerts.append({
                "level": "High",
                "category": "high_outstanding",
                "message": f"Source '{source_type_name}' memiliki outstanding pembayaran tinggi senilai Rp {outstanding_p:,.0f}."
            })

    for v in vendor_performance_list:
        v_name = v["vendor_name"]
        total_p = v["total_projects"]
        cancel_c = v["cancelled_projects"]
        cancel_rate = (cancel_c / total_p * 100.0) if total_p > 0 else 0.0
        risk_c = v["risk_count"]

        if total_p >= 2 and cancel_rate > 30.0:
            risk_alerts.append({
                "level": "High",
                "category": "high_cancellation",
                "message": f"Vendor partner '{v_name}' memiliki cancellation rate tinggi: {cancel_rate:.1f}%."
            })
        if risk_c > 0:
            risk_alerts.append({
                "level": "Medium",
                "category": "vendor_risks",
                "message": f"Vendor '{v_name}' memiliki {risk_c} proyek dengan risiko komersial/overdue."
            })

    if missing_source_count > 0:
        risk_alerts.append({
            "level": "Medium",
            "category": "missing_data",
            "message": f"{missing_source_count} proyek berjalan tidak memiliki data lead source (Event Source) terpetakan."
        })
    if missing_vendor_count > 0:
        risk_alerts.append({
            "level": "Info",
            "category": "missing_data",
            "message": f"{missing_vendor_count} proyek dengan event source tidak memiliki detail spesifikasi nama vendor partner."
        })

    # Summary analytics
    total_sources = len(source_performance_list)
    total_vendors = len(vendor_performance_list)
    
    total_confirmed_deals = sum(s["confirmed_projects"] for s in source_performance_list)
    total_analyzed = total_projects_analyzed
    avg_conversion = (total_confirmed_deals / total_analyzed * 100.0) if total_analyzed > 0 else 0.0

    # Data Quality Report
    data_quality_report = {
        "missing_source_count": missing_source_count,
        "missing_vendor_count": missing_vendor_count,
        "limited_vendor_data": True,
        "notes": [
            "Data vendor terbatas karena data vendor saat ini disimpan sebagai text field 'vendor_name' di dalam model EventSource, bukan sebagai model entitas mandiri.",
            "Proyek tanpa event source/vendor dianggap sebagai Direct/Unknown lead source.",
            "Conversion rate dihitung berdasarkan persentase jumlah proyek berstatus Signed & Deal terhadap total proyek yang dianalisis."
        ]
    }

    return {
        "summary": {
            "total_sources": total_sources,
            "total_vendors": total_vendors,
            "total_projects_analyzed": total_projects_analyzed,
            "total_potential_revenue": total_potential_revenue,
            "total_confirmed_revenue": total_confirmed_revenue,
            "total_outstanding_payment": total_outstanding_payment,
            "average_conversion_rate": avg_conversion,
            "commercial_risk_count": commercial_risk_count
        },
        "source_performance": source_performance_list,
        "vendor_performance": vendor_performance_list,
        "po_source_performance": po_source_performance_list,
        "risk_alerts": risk_alerts,
        "data_quality": data_quality_report
    }
