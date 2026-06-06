from datetime import date, timedelta
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.modules.projects.models import Project, ProjectInstrument
from app.modules.auth.models import User
from app.modules.projects.service import calculate_project_readiness, check_project_validation_warnings

def get_pm_control_center_data(
    db: Session,
    pm_id: Optional[str] = None,
    po_id: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    readiness_min: Optional[float] = None,
    readiness_max: Optional[float] = None,
    include_closed: bool = False,
    include_canceled: bool = False,
    instrument_status: Optional[str] = None,
    event_window: str = "all"
) -> Dict[str, Any]:
    today = date.today()
    
    # 1. Base Query with joined loads to avoid N+1 query overhead
    query = db.query(Project).filter(Project.deleted_at == None).options(
        joinedload(Project.customer),
        joinedload(Project.program_manager),
        joinedload(Project.program_owner),
        joinedload(Project.instruments),
        joinedload(Project.documents)
    )
    
    # 2. Status exclusion checks (default behavior)
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
        
    # 3. Filter PO & PM penugasan
    if pm_id:
        try:
            parsed_pm = UUID(pm_id)
            query = query.filter(Project.program_manager_id == parsed_pm)
        except ValueError:
            pass
    if po_id:
        try:
            parsed_po = UUID(po_id)
            query = query.filter(Project.program_owner_id == parsed_po)
        except ValueError:
            pass
            
    # 4. Filter Date Range
    if date_from:
        query = query.filter(Project.event_date_start >= date_from)
    if date_to:
        query = query.filter(Project.event_date_start <= date_to)
        
    # 5. Filter Event Window
    if event_window == "today":
        # Event start <= today <= event end (or event start == today if end missing)
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
    
    # 6. Parse min/max values
    r_min = readiness_min
    if r_min is not None and r_min > 1.0:
        r_min = r_min / 100.0
    r_max = readiness_max
    if r_max is not None and r_max > 1.0:
        r_max = r_max / 100.0
        
    # Filter list in memory for readiness scores & instrument status to avoid complex SQL joins
    filtered_projects = []
    project_readiness_map = {}
    
    for p in all_projects:
        # Filter non-deleted instruments
        active_insts = [inst for inst in p.instruments if not inst.deleted_at]
        
        # Filter by instrument status if requested
        if instrument_status:
            has_status = any(inst.status == instrument_status for inst in active_insts)
            if not has_status:
                continue
                
        readiness = calculate_project_readiness(p)
        score = readiness["project_readiness_score"]
        
        if r_min is not None and score < r_min:
            continue
        if r_max is not None and score > r_max:
            continue
            
        filtered_projects.append(p)
        project_readiness_map[p.id] = readiness
        
    # 7. Calculate Aggregated Operational Summary
    events_today_count = 0
    upcoming_7_days_count = 0
    overdue_events_count = 0
    not_ready_projects_count = 0
    overdue_instruments_count = 0
    need_revision_instruments_count = 0
    total_readiness_score = 0.0
    
    upcoming_events = []
    not_ready_projects = []
    overdue_instruments = []
    need_revision_instruments = []
    priority_actions = []
    
    pm_workload_aggregates = {} # pm_id -> dict
    
    for p in filtered_projects:
        readiness = project_readiness_map[p.id]
        score = readiness["project_readiness_score"]
        rate = readiness["instrument_completion_rate"]
        
        # Readiness score accumulation
        total_readiness_score += score
        
        # Calculate event countdown
        days_until = None
        if p.event_date_start:
            days_until = (p.event_date_start - today).days
            
        is_today = False
        if p.event_date_start:
            if p.event_date_end:
                is_today = p.event_date_start <= today <= p.event_date_end
            else:
                is_today = p.event_date_start == today
                
        is_overdue_event = False
        if p.event_date_end and p.event_date_end < today and p.program_status not in ["Completed", "Closed", "Cancel"]:
            is_overdue_event = True
            
        # Counters
        if is_today:
            events_today_count += 1
        if days_until is not None and 0 <= days_until <= 7:
            upcoming_7_days_count += 1
        if is_overdue_event:
            overdue_events_count += 1
        if score < 0.8:
            not_ready_projects_count += 1
            
        # Instrument checklists
        active_insts = [inst for inst in p.instruments if not inst.deleted_at]
        inst_dict = {inst.instrument_type: inst for inst in active_insts}
        
        missing_items = []
        for itype in ["CL", "ROS", "CK", "PNL"]:
            inst = inst_dict.get(itype)
            if not inst or inst.status != "Done":
                missing_items.append(itype)
                
        # Recommended action helpers
        rec_action = "Lengkapi instrumen operasional sebelum event."
        if p.program_status == "Inquiry":
            rec_action = "Tunjuk PO/PM dan siapkan penawaran awal."
        elif p.program_status == "Preparation":
            rec_action = "Selesaikan instrumen CL/ROS/CK yang belum Done."
        elif p.program_status == "Ready":
            rec_action = "Lakukan final briefing kru dan jalankan rundown."
        elif p.program_status == "Running":
            rec_action = "Monitoring eksekusi rundown event di lapangan."
        elif p.program_status in ["Completed", "Reporting"]:
            rec_action = "Unggah berkas PNL dan tagih sisa pembayaran."
            
        # Priority logic mapping
        prio = "Low"
        prio_reasons = []
        
        # Critical priority checks
        if is_today and score < 0.8:
            prio = "Critical"
            prio_reasons.append("Event dilaksanakan hari ini tetapi kesiapan < 80%.")
        elif is_overdue_event:
            prio = "Critical"
            prio_reasons.append("Jadwal pelaksanaan event sudah lewat tetapi belum Complete.")
            
        # High priority checks
        if prio != "Critical":
            if days_until is not None and 0 <= days_until <= 7 and score < 0.8:
                prio = "High"
                prio_reasons.append("Event dalam waktu 7 hari ke depan tetapi kesiapan < 80%.")
            elif any(inst.due_date and inst.due_date < today and inst.status not in ["Done", "Not Required"] for inst in active_insts):
                prio = "High"
                prio_reasons.append("Ada instrumen checklist yang melewati jatuh tempo (Overdue).")
            elif any(inst.status == "Need Revision" for inst in active_insts):
                prio = "High"
                prio_reasons.append("Terdapat instrumen yang membutuhkan revisi (Need Revision).")
            elif p.program_status in ["Ready", "Running"] and (("ROS" in missing_items) or ("CK" in missing_items)):
                prio = "High"
                prio_reasons.append("Rundown (ROS) atau Checklist (CK) belum Done untuk proyek aktif.")
                
        # Medium priority checks
        if prio not in ["Critical", "High"]:
            if days_until is not None and 0 <= days_until <= 14 and score < 0.9:
                prio = "Medium"
                prio_reasons.append("Event dalam waktu 14 hari tetapi kesiapan < 90%.")
            elif p.quotation_status == "Signed & Deal" and (("CL" in missing_items) or ("PNL" in missing_items)):
                prio = "Medium"
                prio_reasons.append("Missing CL atau PNL untuk Quotation Signed & Deal.")
            elif p.program_status in ["Completed", "Reporting"] and not p.documents:
                prio = "Medium"
                prio_reasons.append("Event selesai tetapi belum mengunggah dokumen/foto.")
                
        # Build PM Names
        pm_name = p.program_manager.full_name if p.program_manager else "-"
        po_name = p.program_owner.full_name if p.program_owner else "-"
        customer_name = p.customer.company_name if p.customer else "-"
        
        # Populate Listings
        # 1. Upcoming event item
        if days_until is not None and days_until <= 14:
            upcoming_events.append({
                "project_id": p.id,
                "project_code": p.project_code,
                "customer_name": customer_name,
                "program_name": p.program_name or p.title,
                "event_date_start": p.event_date_start,
                "event_date_end": p.event_date_end,
                "days_until_event": days_until,
                "po_name": po_name,
                "pm_name": pm_name,
                "program_status": p.program_status,
                "project_status": p.project_status,
                "readiness_score": score * 100.0,
                "instrument_completion_rate": rate * 100.0,
                "priority_level": prio,
                "recommended_action": rec_action
            })
            
        # 2. Not Ready Project item
        if score < 0.8:
            not_ready_projects.append({
                "project_id": p.id,
                "project_code": p.project_code,
                "customer_name": customer_name,
                "event_date_start": p.event_date_start,
                "pm_name": pm_name,
                "readiness_score": score * 100.0,
                "missing_items": missing_items,
                "recommended_action": f"Lengkapi: {', '.join(missing_items)} sebelum H-1 event." if missing_items else rec_action
            })
            
        # 3. Individual Instruments Overdue/Revision loops
        for inst in active_insts:
            if inst.due_date and inst.due_date < today and inst.status not in ["Done", "Not Required"]:
                overdue_instruments_count += 1
                days_overdue = (today - inst.due_date).days
                overdue_instruments.append({
                    "project_id": p.id,
                    "project_code": p.project_code,
                    "customer_name": customer_name,
                    "instrument_type": inst.instrument_type,
                    "instrument_label": inst.title or inst.instrument_type,
                    "status": inst.status,
                    "due_date": inst.due_date,
                    "days_overdue": days_overdue,
                    "pm_name": pm_name,
                    "recommended_action": f"Ubah status instrumen {inst.instrument_type} ke Done."
                })
            elif inst.status == "Need Revision":
                need_revision_instruments_count += 1
                need_revision_instruments.append({
                    "project_id": p.id,
                    "project_code": p.project_code,
                    "customer_name": customer_name,
                    "instrument_type": inst.instrument_type,
                    "notes": inst.notes or "Revisi dibutuhkan.",
                    "pm_name": pm_name,
                    "recommended_action": f"Periksa instruksi dan perbaiki instrumen {inst.instrument_type}."
                })
                
        # 4. Generate Priority Actions
        if prio_reasons:
            priority_actions.append({
                "priority_level": prio,
                "project_id": p.id,
                "project_code": p.project_code or "UNCODED",
                "title": p.title or p.program_name or p.project_code or "Untitled Project",
                "description": prio_reasons[0],
                "recommended_action": rec_action,
                "reason": ", ".join(prio_reasons)
            })
            
        # PM Workload aggregation prep
        if p.program_manager:
            pm = p.program_manager
            if pm.id not in pm_workload_aggregates:
                pm_workload_aggregates[pm.id] = {
                    "pm_id": pm.id,
                    "pm_name": pm.full_name,
                    "initial_code": pm.initial_code or pm.email.split("@")[0].upper()[:3],
                    "total_projects": 0,
                    "upcoming_events_7_days": 0,
                    "not_ready_projects": 0,
                    "overdue_instruments": 0,
                    "need_revision_instruments": 0,
                    "total_readiness": 0.0
                }
                
            pm_aggr = pm_workload_aggregates[pm.id]
            pm_aggr["total_projects"] += 1
            pm_aggr["total_readiness"] += score
            
            if days_until is not None and 0 <= days_until <= 7:
                pm_aggr["upcoming_events_7_days"] += 1
            if score < 0.8:
                pm_aggr["not_ready_projects"] += 1
                
            for inst in active_insts:
                if inst.due_date and inst.due_date < today and inst.status not in ["Done", "Not Required"]:
                    pm_aggr["overdue_instruments"] += 1
                elif inst.status == "Need Revision":
                    pm_aggr["need_revision_instruments"] += 1

    # 8. Sort listings
    # Sort Priority Actions by urgency
    prio_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    priority_actions.sort(key=lambda x: prio_order.get(x["priority_level"], 4))
    
    # Sort Upcoming Events by event date (ascending)
    upcoming_events.sort(key=lambda x: x["event_date_start"] if x["event_date_start"] else date.max)
    
    # Sort Not Ready Projects by readiness score (ascending)
    not_ready_projects.sort(key=lambda x: x["readiness_score"])
    
    # Sort Overdue Instruments by days overdue (descending)
    overdue_instruments.sort(key=lambda x: x["days_overdue"], reverse=True)
    
    # Compile PM Workload list
    pm_workload_list = []
    for pm_data in pm_workload_aggregates.values():
        total_p = pm_data["total_projects"]
        avg_score = (pm_data["total_readiness"] / total_p) * 100.0 if total_p > 0 else 0.0
        pm_workload_list.append({
            "pm_id": pm_data["pm_id"],
            "pm_name": pm_data["pm_name"],
            "initial_code": pm_data["initial_code"],
            "total_projects": total_p,
            "upcoming_events_7_days": pm_data["upcoming_events_7_days"],
            "not_ready_projects": pm_data["not_ready_projects"],
            "overdue_instruments": pm_data["overdue_instruments"],
            "need_revision_instruments": pm_data["need_revision_instruments"],
            "average_readiness_score": avg_score
        })
        
    # Sort workload list by project count (descending)
    pm_workload_list.sort(key=lambda x: x["total_projects"], reverse=True)
    
    # Calculate global averages
    total_p_filtered = len(filtered_projects)
    avg_readiness = (total_readiness_score / total_p_filtered) * 100.0 if total_p_filtered > 0 else 0.0
    
    return {
        "summary": {
            "total_active_projects": total_p_filtered,
            "events_today": events_today_count,
            "upcoming_events_7_days": upcoming_7_days_count,
            "overdue_events": overdue_events_count,
            "not_ready_projects": not_ready_projects_count,
            "overdue_instruments": overdue_instruments_count,
            "need_revision_instruments": need_revision_instruments_count,
            "average_readiness_score": avg_readiness
        },
        "upcoming_events": upcoming_events,
        "not_ready_projects": not_ready_projects,
        "overdue_instruments": overdue_instruments,
        "need_revision_instruments": need_revision_instruments,
        "pm_workload": pm_workload_list,
        "priority_actions": priority_actions
    }
