from datetime import date
from typing import Optional, Dict, Any, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.modules.projects.models import Project
from app.modules.auth.models import User
from app.modules.crm.models import Customer
from app.modules.event_sources.models import EventSource
from app.modules.finance.models import Invoice, Payment


def get_dashboard_analytics(db: Session, filters: Dict[str, Any]) -> Dict[str, Any]:
    # Base query for active (non-deleted) projects
    query = db.query(Project).filter(Project.deleted_at == None)
    
    # Coalesce deprecated start_date with new event_date_start
    project_date = func.coalesce(Project.event_date_start, Project.start_date)
    
    # Extract filters
    year = filters.get("year")
    month = filters.get("month")
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    po_id = filters.get("po_id")
    pm_id = filters.get("pm_id")
    source_type = filters.get("source_type")
    quotation_status = filters.get("quotation_status")
    program_status = filters.get("program_status")
    payment_status = filters.get("payment_status")
    project_status = filters.get("project_status")
    customer_category = filters.get("customer_category")
    event_category = filters.get("event_category")
    program_type = filters.get("program_type")
    
    # Apply SQL filters
    if year is not None:
        query = query.filter(func.extract("year", project_date) == year)
    if month is not None:
        query = query.filter(func.extract("month", project_date) == month)
    if date_from is not None:
        query = query.filter(project_date >= date_from)
    if date_to is not None:
        query = query.filter(project_date <= date_to)
    if po_id is not None:
        query = query.filter(Project.program_owner_id == po_id)
    if pm_id is not None:
        query = query.filter(Project.program_manager_id == pm_id)
    if source_type is not None:
        query = query.join(Project.event_source).filter(EventSource.source_type == source_type)
    if quotation_status is not None:
        query = query.filter(Project.quotation_status == quotation_status)
    if program_status is not None:
        query = query.filter(Project.program_status == program_status)
    if payment_status is not None:
        query = query.filter(Project.payment_status == payment_status)
    if project_status is not None:
        query = query.filter(Project.project_status == project_status)
    if customer_category is not None:
        query = query.join(Project.customer).filter(Customer.category == customer_category)
    if event_category is not None:
        query = query.filter(Project.event_category == event_category)
    if program_type is not None:
        query = query.filter(Project.program_type == program_type)
        
    # Eagerly load all relationships for efficient in-memory analytics
    projects = query.options(
        joinedload(Project.program_owner),
        joinedload(Project.program_manager),
        joinedload(Project.customer),
        joinedload(Project.event_source),
        joinedload(Project.documents),
        joinedload(Project.instruments),
        joinedload(Project.invoices).joinedload(Invoice.payments)
    ).all()
    
    # Initialize variables for in-memory calculations
    total_projects = len(projects)
    inquiry_stage_count = 0
    total_deal = 0
    total_cancel = 0
    potential_revenue = 0.0
    confirmed_revenue = 0.0
    revenue_received = 0.0
    
    # Base status trackers initialized with 0
    quotation_statuses = ["Draft", "Sent", "Follow Up", "Revision", "Signed & Deal", "Cancel"]
    quot_counts = {s: 0 for s in quotation_statuses}
    
    program_statuses = ["Inquiry", "Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed", "Cancel"]
    prog_counts = {s: 0 for s in program_statuses}
    
    payment_statuses = ["Not Invoiced", "Invoice Sent", "Partial Paid", "Paid", "Outstanding", "Overdue"]
    pay_counts = {s: 0 for s in payment_statuses}
    
    project_statuses = ["Open", "Active", "Reporting", "Closed", "Canceled"]
    proj_counts = {s: 0 for s in project_statuses}
    
    # Grouping aggregators
    po_map = {}
    pm_map = {}
    source_map = {}
    customer_map = {}
    event_cat_map = {}
    prog_type_map = {}
    
    # Data Quality Indicators
    missing_po = 0
    missing_pm = 0
    missing_customer = 0
    missing_budget = 0
    cancel_without_reason = 0
    closed_not_paid = 0
    documentation_missing = 0
    unknown_source = 0
    
    # Instrument analytics indicators (Sprint 7)
    missing_cl = 0
    missing_ros = 0
    missing_ck = 0
    missing_pnl = 0
    instruments_need_revision = 0
    instruments_overdue = 0
    total_instrument_completion_rate_sum = 0.0
    today = date.today()
    
    # Confirmed program statuses for revenue logic
    confirmed_prog_statuses = {"Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed"}
    
    for p in projects:
        budget = float(p.budget) if p.budget is not None else 0.0
        
        # Standardize and count status fields
        q_status = p.quotation_status or "Draft"
        if q_status in quot_counts:
            quot_counts[q_status] += 1
        else:
            quot_counts[q_status] = quot_counts.get(q_status, 0) + 1
            
        pr_status = p.program_status or "Inquiry"
        if pr_status in prog_counts:
            prog_counts[pr_status] += 1
        else:
            prog_counts[pr_status] = prog_counts.get(pr_status, 0) + 1
            
        py_status = p.payment_status or "Not Invoiced"
        if py_status in pay_counts:
            pay_counts[py_status] += 1
        else:
            pay_counts[py_status] = pay_counts.get(py_status, 0) + 1
            
        pj_status = p.project_status or "Open"
        if pj_status in proj_counts:
            proj_counts[pj_status] += 1
        else:
            proj_counts[pj_status] = proj_counts.get(pj_status, 0) + 1
            
        # Calculation indicators
        is_deal = (q_status == "Signed & Deal")
        is_cancel = (q_status == "Cancel" or pj_status == "Canceled")
        
        if is_deal:
            total_deal += 1
        if is_cancel:
            total_cancel += 1
        if pr_status == "Inquiry":
            inquiry_stage_count += 1
            
        # Revenue Logic
        if budget > 0:
            potential_revenue += budget
        
        is_confirmed_rev = (is_deal or pr_status in confirmed_prog_statuses)
        if is_confirmed_rev:
            confirmed_revenue += budget
            
        # Accumulate actually received cash (approved payments)
        revenue_received += p.paid_amount
            
        # PO Performance mapping
        if p.program_owner_id:
            po_id_val = p.program_owner_id
            if po_id_val not in po_map:
                po_name = p.program_owner.full_name if p.program_owner else "Unknown PO"
                initial_code = p.program_owner.initial_code if p.program_owner else None
                po_map[po_id_val] = {
                    "po_id": po_id_val,
                    "po_name": po_name,
                    "initial_code": initial_code,
                    "total_projects": 0,
                    "deal_count": 0,
                    "cancel_count": 0,
                    "confirmed_revenue": 0.0,
                    "sum_budget": 0.0,
                    "closed_count": 0
                }
            po_data = po_map[po_id_val]
            po_data["total_projects"] += 1
            if is_deal:
                po_data["deal_count"] += 1
            if is_cancel:
                po_data["cancel_count"] += 1
            if is_confirmed_rev:
                po_data["confirmed_revenue"] += budget
            po_data["sum_budget"] += budget
            if pj_status == "Closed":
                po_data["closed_count"] += 1
                
        # PM Workload mapping
        if p.program_manager_id:
            pm_id_val = p.program_manager_id
            if pm_id_val not in pm_map:
                pm_name = p.program_manager.full_name if p.program_manager else "Unknown PM"
                initial_code = p.program_manager.initial_code if p.program_manager else None
                pm_map[pm_id_val] = {
                    "pm_id": pm_id_val,
                    "pm_name": pm_name,
                    "initial_code": initial_code,
                    "total_projects": 0,
                    "active_count": 0,
                    "preparation_count": 0,
                    "running_count": 0,
                    "reporting_count": 0,
                    "closed_count": 0
                }
            pm_data = pm_map[pm_id_val]
            pm_data["total_projects"] += 1
            if pj_status == "Active":
                pm_data["active_count"] += 1
            if pr_status == "Preparation":
                pm_data["preparation_count"] += 1
            if pr_status == "Running":
                pm_data["running_count"] += 1
            if pj_status == "Reporting":
                pm_data["reporting_count"] += 1
            if pj_status == "Closed":
                pm_data["closed_count"] += 1
                
        # Event Source analytics
        s_type = p.event_source.source_type if p.event_source else "Unknown"
        if s_type not in source_map:
            source_map[s_type] = {
                "source_type": s_type,
                "total_projects": 0,
                "confirmed_revenue": 0.0,
                "potential_revenue": 0.0,
                "deal_count": 0,
                "cancel_count": 0
            }
        src_data = source_map[s_type]
        src_data["total_projects"] += 1
        src_data["potential_revenue"] += budget
        if is_confirmed_rev:
            src_data["confirmed_revenue"] += budget
        if is_deal:
            src_data["deal_count"] += 1
        if is_cancel:
            src_data["cancel_count"] += 1
            
        # Customer Category analytics
        cust_cat = p.customer.category if (p.customer and p.customer.category) else "Unknown"
        if cust_cat not in customer_map:
            customer_map[cust_cat] = {
                "customer_category": cust_cat,
                "total_projects": 0,
                "confirmed_revenue": 0.0,
                "deal_count": 0,
                "cancel_count": 0
            }
        cust_data = customer_map[cust_cat]
        cust_data["total_projects"] += 1
        if is_confirmed_rev:
            cust_data["confirmed_revenue"] += budget
        if is_deal:
            cust_data["deal_count"] += 1
        if is_cancel:
            cust_data["cancel_count"] += 1
            
        # Event Category analytics
        e_cat = p.event_category or "Unknown"
        if e_cat not in event_cat_map:
            event_cat_map[e_cat] = {
                "event_category": e_cat,
                "total_projects": 0,
                "confirmed_revenue": 0.0
            }
        ev_cat_data = event_cat_map[e_cat]
        ev_cat_data["total_projects"] += 1
        if is_confirmed_rev:
            ev_cat_data["confirmed_revenue"] += budget
            
        # Program Type analytics
        prog_t = p.program_type or "Unknown"
        if prog_t not in prog_type_map:
            prog_type_map[prog_t] = {
                "program_type": prog_t,
                "total_projects": 0,
                "confirmed_revenue": 0.0
            }
        prog_t_data = prog_type_map[prog_t]
        prog_t_data["total_projects"] += 1
        if is_confirmed_rev:
            prog_t_data["confirmed_revenue"] += budget
            
        # Data Quality Checks
        if p.program_owner_id is None:
            missing_po += 1
        if p.program_manager_id is None:
            missing_pm += 1
        if p.customer_id is None:
            missing_customer += 1
        if p.budget is None or p.budget <= 0:
            missing_budget += 1
        if q_status == "Cancel" and (not p.cancel_reason or not p.cancel_reason.strip()):
            cancel_without_reason += 1
        if pj_status == "Closed" and py_status != "Paid":
            closed_not_paid += 1
        if not p.documents or len(p.documents) == 0:
            documentation_missing += 1
        if p.event_source_id is None or s_type.lower() in ["other", "unknown"]:
            unknown_source += 1

        # Project Instruments checks (Sprint 7)
        proj_instruments = {inst.instrument_type: inst for inst in p.instruments if not inst.deleted_at}
        
        # 1. Missing CL (if program_status in confirmed_prog_statuses)
        cl_inst = proj_instruments.get("CL")
        if pr_status in confirmed_prog_statuses:
            if not cl_inst or cl_inst.status != "Done":
                missing_cl += 1
                
        # 2. Missing ROS (if program_status in ["Ready", "Running", "Completed", "Reporting", "Closed"])
        ros_inst = proj_instruments.get("ROS")
        if pr_status in ["Ready", "Running", "Completed", "Reporting", "Closed"]:
            if not ros_inst or ros_inst.status != "Done":
                missing_ros += 1
                
        # 3. Missing CK (if program_status in ["Ready", "Running", "Completed", "Reporting", "Closed"])
        ck_inst = proj_instruments.get("CK")
        if pr_status in ["Ready", "Running", "Completed", "Reporting", "Closed"]:
            if not ck_inst or ck_inst.status != "Done":
                missing_ck += 1
                
        # 4. Missing PNL (if quotation_status is Signed & Deal)
        pnl_inst = proj_instruments.get("PNL")
        if q_status == "Signed & Deal":
            if not pnl_inst or pnl_inst.status != "Done" or not pnl_inst.document_url:
                missing_pnl += 1
                
        # 5. instruments_need_revision, instruments_overdue, average_instrument_completion_rate
        req_insts = [inst for inst in p.instruments if not inst.deleted_at and inst.status != "Not Required"]
        req_count = len(req_insts)
        done_count = sum(1 for inst in req_insts if inst.status == "Done")
        proj_completion_rate = done_count / req_count if req_count > 0 else 0.0
        total_instrument_completion_rate_sum += proj_completion_rate
        
        for inst in p.instruments:
            if not inst.deleted_at:
                if inst.status == "Need Revision":
                    instruments_need_revision += 1
                if inst.due_date and inst.due_date < today and inst.status != "Done" and inst.status != "Not Required":
                    instruments_overdue += 1

    # Set total_inquiry as total_projects per requirements
    total_inquiry = total_projects
    
    # Calculate ratios and averages safely
    deal_rate = (total_deal / total_projects * 100.0) if total_projects > 0 else 0.0
    cancel_rate = (total_cancel / total_projects * 100.0) if total_projects > 0 else 0.0
    revenue_conversion_rate = (confirmed_revenue / potential_revenue * 100.0) if potential_revenue > 0 else 0.0
    average_project_value = (confirmed_revenue / total_deal) if total_deal > 0 else 0.0
    
    # Calculate finance and data quality summaries
    collection_rate = (revenue_received / confirmed_revenue * 100.0) if confirmed_revenue > 0 else 0.0
    outstanding_amount = max(0.0, confirmed_revenue - revenue_received)
    total_data_quality_issues = (
        missing_po + missing_pm + missing_customer + missing_budget +
        cancel_without_reason + closed_not_paid + documentation_missing + unknown_source
    )
    
    # Calculate target achievement rate
    revenue_target = 9200000000.0
    achievement_rate = (confirmed_revenue / revenue_target * 100.0) if revenue_target > 0 else 0.0

    # Process PO Performance list
    po_performance_list = []
    for po_id_key, d in po_map.items():
        avg_budget = (d["sum_budget"] / d["total_projects"]) if d["total_projects"] > 0 else 0.0
        po_performance_list.append({
            "po_id": d["po_id"],
            "po_name": d["po_name"],
            "initial_code": d["initial_code"],
            "total_projects": d["total_projects"],
            "deal_count": d["deal_count"],
            "cancel_count": d["cancel_count"],
            "confirmed_revenue": d["confirmed_revenue"],
            "average_budget": avg_budget,
            "closed_count": d["closed_count"]
        })
        
    # Process PM Workload list
    pm_workload_list = []
    for pm_id_key, d in pm_map.items():
        pm_workload_list.append({
            "pm_id": d["pm_id"],
            "pm_name": d["pm_name"],
            "initial_code": d["initial_code"],
            "total_projects": d["total_projects"],
            "active_count": d["active_count"],
            "preparation_count": d["preparation_count"],
            "running_count": d["running_count"],
            "reporting_count": d["reporting_count"],
            "closed_count": d["closed_count"]
        })
        
    # Convert dict mapping arrays to lists
    source_analytics_list = list(source_map.values())
    customer_analytics_list = list(customer_map.values())
    event_category_analytics_list = list(event_cat_map.values())
    program_type_analytics_list = list(prog_type_map.values())
    
    average_instrument_completion_rate = (total_instrument_completion_rate_sum / total_projects * 100.0) if total_projects > 0 else 0.0
    
    return {
        "executive": {
            "total_projects": total_projects,
            "total_inquiry": total_inquiry,
            "inquiry_stage_count": inquiry_stage_count,
            "total_deal": total_deal,
            "total_cancel": total_cancel,
            "deal_rate": deal_rate,
            "cancel_rate": cancel_rate,
            "potential_revenue": potential_revenue,
            "confirmed_revenue": confirmed_revenue,
            "revenue_received": revenue_received,
            "collection_rate": collection_rate,
            "outstanding_amount": outstanding_amount,
            "revenue_conversion_rate": revenue_conversion_rate,
            "average_project_value": average_project_value,
            "total_data_quality_issues": total_data_quality_issues
        },
        "target": {
            "year": 2025,
            "revenue_target": revenue_target,
            "achievement_rate": achievement_rate
        },
        "quotation": {
            "count_by_status": quot_counts,
            "deal_count": total_deal,
            "cancel_count": quot_counts.get("Cancel", 0)
        },
        "program": {
            "count_by_status": prog_counts
        },
        "payment": {
            "count_by_status": pay_counts,
            "paid_count": pay_counts.get("Paid", 0),
            "outstanding_count": pay_counts.get("Outstanding", 0),
            "invoice_sent_count": pay_counts.get("Invoice Sent", 0),
            "not_invoiced_count": pay_counts.get("Not Invoiced", 0)
        },
        "project": {
            "count_by_status": proj_counts,
            "closed_count": proj_counts.get("Closed", 0),
            "reporting_count": proj_counts.get("Reporting", 0),
            "active_count": proj_counts.get("Active", 0)
        },
        "po_performance": po_performance_list,
        "pm_workload": pm_workload_list,
        "source_analytics": source_analytics_list,
        "customer_analytics": customer_analytics_list,
        "event_category_analytics": event_category_analytics_list,
        "program_type_analytics": program_type_analytics_list,
        "data_quality": {
            "missing_po": missing_po,
            "missing_pm": missing_pm,
            "missing_customer": missing_customer,
            "missing_budget": missing_budget,
            "cancel_without_reason": cancel_without_reason,
            "closed_not_paid": closed_not_paid,
            "documentation_missing": documentation_missing,
            "unknown_source": unknown_source
        },
        "instrument_summary": {
            "missing_cl": missing_cl,
            "missing_ros": missing_ros,
            "missing_ck": missing_ck,
            "missing_pnl": missing_pnl,
            "instruments_need_revision": instruments_need_revision,
            "instruments_overdue": instruments_overdue,
            "average_instrument_completion_rate": average_instrument_completion_rate
        }
    }
