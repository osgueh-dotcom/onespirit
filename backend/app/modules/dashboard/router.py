from datetime import datetime, date, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.core import deps
from app.modules.auth.models import User
from app.modules.crm.models import Customer
from app.modules.projects.models import Project
from app.modules.events.models import EventSchedule
from app.modules.tasks.models import Task
from app.modules.finance.models import Invoice, Payment
from app.models.activity import ActivityLog
from app.modules.dashboard.schemas import DashboardAnalyticsResponse, PMControlCenterResponse, POControlCenterResponse
from app.modules.dashboard.service import get_dashboard_analytics
from uuid import UUID

router = APIRouter(prefix="/dashboard", tags=["Premium Dashboard Analytics Hub"])

# Helper function to apply reactive filters across entity joins
def apply_project_filters(
    query,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[str] = None,
    sales: Optional[str] = None,
    pm: Optional[str] = None,
    event_category: Optional[str] = None,
    partner: Optional[str] = None
):
    if start_date:
        query = query.filter(Project.start_date >= start_date)
    if end_date:
        query = query.filter(Project.start_date <= end_date)
    if status:
        query = query.filter(Project.status == status)
    if sales:
        query = query.filter(Project.created_by_id == sales)
    if pm:
        query = query.filter(Project.assigned_to_id == pm)
    if event_category:
        query = query.filter(Project.title.ilike(f"%{event_category}%"))
    if partner:
        query = query.join(Customer, Project.customer_id == Customer.id).filter(Customer.category.ilike(f"%{partner}%"))
    return query

# Backward-compatible master overview endpoint
@router.get("")
def get_dashboard_summary(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None),
    current_user: User = Depends(deps.get_current_user)
):
    """Retrieve operational summaries, alerts, progress metrics, and revenues with advanced filtering"""
    now = datetime.utcnow()
    today = date.today()

    # Apply base queries
    project_query = db.query(Project).filter(Project.deleted_at == None)
    project_query = apply_project_filters(project_query, start_date, end_date, status, sales, pm, event_category, partner)
    
    total_projects = project_query.count()
    ongoing_projects = project_query.filter(Project.status.in_(["confirmed", "ongoing", "preparation"])).count()

    # Upcoming events
    event_query = db.query(EventSchedule).join(Project).filter(EventSchedule.deleted_at == None)
    event_query = apply_project_filters(event_query, start_date, end_date, status, sales, pm, event_category, partner)
    upcoming_events = event_query.filter(EventSchedule.start_time >= now, EventSchedule.start_time <= now + timedelta(days=7)).count()

    # Revenue metrics
    payments_query = db.query(Payment).join(Invoice).join(Project).filter(Payment.status == "approved", Payment.deleted_at == None)
    payments_query = apply_project_filters(payments_query, start_date, end_date, status, sales, pm, event_category, partner)
    revenue_received = float(payments_query.with_entities(func.sum(Payment.amount)).scalar() or 0)

    revenue_projected = float(project_query.with_entities(func.sum(Project.budget)).scalar() or 0)

    # Invoices metrics
    invoices_query = db.query(Invoice).join(Project).filter(Invoice.deleted_at == None, Invoice.status.in_(["unpaid", "partial", "overdue"]))
    invoices_query = apply_project_filters(invoices_query, start_date, end_date, status, sales, pm, event_category, partner)
    pending_invoices_count = invoices_query.count()
    pending_invoices_amount = float(invoices_query.with_entities(func.sum(Invoice.amount)).scalar() or 0)

    # Project status groups
    status_counts_raw = project_query.with_entities(Project.status, func.count(Project.id)).group_by(Project.status).all()
    project_status_counts = {stat: count for stat, count in status_counts_raw}
    all_stages = ["inquiry", "quotation", "negotiation", "confirmed", "preparation", "ongoing", "completed", "canceled"]
    for s in all_stages:
        if s not in project_status_counts:
            project_status_counts[s] = 0

    # Tasks progress distribution
    tasks_query = db.query(Task).join(Project).filter(Task.deleted_at == None)
    tasks_query = apply_project_filters(tasks_query, start_date, end_date, status, sales, pm, event_category, partner)
    task_counts_raw = tasks_query.with_entities(Task.status, func.count(Task.id)).group_by(Task.status).all()
    tasks_progress = {stat: count for stat, count in task_counts_raw}
    for t in ["todo", "in_progress", "review", "done"]:
        if t not in tasks_progress:
            tasks_progress[t] = 0

    # Funnel
    completed_count = project_status_counts.get("completed", 0)
    confirmed_count = completed_count + project_status_counts.get("confirmed", 0) + project_status_counts.get("preparation", 0) + project_status_counts.get("ongoing", 0)
    negotiation_count = confirmed_count + project_status_counts.get("negotiation", 0)
    quotation_count = negotiation_count + project_status_counts.get("quotation", 0)
    inquiry_count = quotation_count + project_status_counts.get("inquiry", 0)

    inquiry_pct = 100.0
    quotation_pct = round((quotation_count / inquiry_count * 100), 1) if inquiry_count > 0 else 0.0
    negotiation_pct = round((negotiation_count / quotation_count * 100), 1) if quotation_count > 0 else 0.0
    confirmed_pct = round((confirmed_count / negotiation_count * 100), 1) if negotiation_count > 0 else 0.0
    completed_pct = round((completed_count / confirmed_count * 100), 1) if confirmed_count > 0 else 0.0

    pipeline_funnel = [
        {"stage": "Inquiry", "count": inquiry_count, "percentage": inquiry_pct},
        {"stage": "Quotation", "count": quotation_count, "percentage": quotation_pct},
        {"stage": "Negotiation", "count": negotiation_count, "percentage": negotiation_pct},
        {"stage": "Confirmed", "count": confirmed_count, "percentage": confirmed_pct},
        {"stage": "Completed", "count": completed_count, "percentage": completed_pct}
    ]

    # Area trends
    monthly_trends = []
    current_year = today.year
    current_month = today.month
    
    for i in range(5, -1, -1):
        m = current_month - i
        y = current_year
        if m <= 0:
            m += 12
            y -= 1
        
        start_dt = date(y, m, 1)
        if m == 12:
            end_dt = date(y + 1, 1, 1) - timedelta(days=1)
        else:
            end_dt = date(y, m + 1, 1) - timedelta(days=1)
            
        month_name = start_dt.strftime("%b %Y")
        
        monthly_pay_query = db.query(Payment).join(Invoice).join(Project).filter(
            Payment.status == "approved",
            Payment.deleted_at == None,
            Payment.payment_date >= start_dt,
            Payment.payment_date <= end_dt
        )
        monthly_pay_query = apply_project_filters(monthly_pay_query, start_date, end_date, status, sales, pm, event_category, partner)
        sum_amount = float(monthly_pay_query.with_entities(func.sum(Payment.amount)).scalar() or 0)
        
        monthly_trends.append({
            "month": month_name,
            "amount": sum_amount
        })

    # PM Workloads
    users_with_tasks = db.query(User).filter(User.deleted_at == None).all()
    team_workload = []
    for u in users_with_tasks:
        todo_q = db.query(Task).join(Project).filter(Task.assigned_to_id == u.id, Task.status == "todo", Task.deleted_at == None)
        todo_count = apply_project_filters(todo_q, start_date, end_date, status, sales, pm, event_category, partner).count()
        
        ip_q = db.query(Task).join(Project).filter(Task.assigned_to_id == u.id, Task.status == "in_progress", Task.deleted_at == None)
        ip_count = apply_project_filters(ip_q, start_date, end_date, status, sales, pm, event_category, partner).count()
        
        rev_q = db.query(Task).join(Project).filter(Task.assigned_to_id == u.id, Task.status == "review", Task.deleted_at == None)
        rev_count = apply_project_filters(rev_q, start_date, end_date, status, sales, pm, event_category, partner).count()
        
        done_q = db.query(Task).join(Project).filter(Task.assigned_to_id == u.id, Task.status == "done", Task.deleted_at == None)
        done_count = apply_project_filters(done_q, start_date, end_date, status, sales, pm, event_category, partner).count()
        
        total_tasks = todo_count + ip_count + rev_count + done_count
        if total_tasks > 0:
            team_workload.append({
                "name": u.full_name,
                "todo": todo_count,
                "in_progress": ip_count,
                "review": rev_count,
                "done": done_count,
                "total": total_tasks
            })

    # Recent activities
    recent_logs = db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).limit(15).all()
    recent_activities = []
    for log in recent_logs:
        recent_activities.append({
            "id": str(log.id),
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": str(log.entity_id) if log.entity_id else None,
            "user_name": log.user.full_name if log.user else "System Action",
            "details": log.details,
            "created_at": log.created_at.isoformat()
        })

    # Alerts
    alerts = []
    overdue_invoices_query = db.query(Invoice).join(Project).filter(Invoice.deleted_at == None, Invoice.status == "overdue")
    overdue_invoices = apply_project_filters(overdue_invoices_query, start_date, end_date, status, sales, pm, event_category, partner).all()
    for inv in overdue_invoices:
        alerts.append({
            "type": "danger",
            "module": "finance",
            "message": f"Invoice {inv.invoice_number} is overdue! Due date was {inv.due_date}."
        })

    overdue_tasks_query = db.query(Task).join(Project).filter(Task.deleted_at == None, Task.status != "done", Task.due_date < now)
    overdue_tasks = apply_project_filters(overdue_tasks_query, start_date, end_date, status, sales, pm, event_category, partner).all()
    for task in overdue_tasks:
        alerts.append({
            "type": "warning",
            "module": "tasks",
            "message": f"Task '{task.title}' is overdue! Assigned to {task.assigned_to.full_name if task.assigned_to else 'Unassigned'}."
        })

    upcoming_events_query = db.query(EventSchedule).join(Project).filter(EventSchedule.deleted_at == None, EventSchedule.start_time >= now, EventSchedule.start_time <= now + timedelta(days=3))
    upcoming_events_list = apply_project_filters(upcoming_events_query, start_date, end_date, status, sales, pm, event_category, partner).all()
    for ev in upcoming_events_list:
        alerts.append({
            "type": "info",
            "module": "events",
            "message": f"Event at {ev.venue_name} starts soon on {ev.start_time.strftime('%Y-%m-%d %H:%M')}!"
        })

    return {
        "ongoing_projects": ongoing_projects,
        "total_projects": total_projects,
        "upcoming_events": upcoming_events,
        "pending_invoices_count": pending_invoices_count,
        "pending_invoices_amount": pending_invoices_amount,
        "revenue_received": revenue_received,
        "revenue_projected": revenue_projected,
        "project_status_counts": project_status_counts,
        "tasks_progress": tasks_progress,
        "alerts": alerts[:8],
        "pipeline_funnel": pipeline_funnel,
        "monthly_trends": monthly_trends,
        "team_workload": team_workload,
        "recent_activities": recent_activities
    }

# 1. Overview Modular Endpoint
@router.get("/overview")
def get_overview_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    project_query = db.query(Project).filter(Project.deleted_at == None)
    project_query = apply_project_filters(project_query, start_date, end_date, status, sales, pm, event_category, partner)
    
    total_projects = project_query.count()
    ongoing_projects = project_query.filter(Project.status.in_(["confirmed", "ongoing", "preparation"])).count()
    completed_projects = project_query.filter(Project.status == "completed").count()
    canceled_projects = project_query.filter(Project.status == "canceled").count()

    total_inquiries = project_query.filter(Project.status == "inquiry").count()
    deal_count = project_query.filter(Project.status.in_(["confirmed", "preparation", "ongoing", "completed"])).count()
    project_deal_ratio = round((deal_count / total_projects * 100), 1) if total_projects > 0 else 0.0

    revenue_projected = float(project_query.with_entities(func.sum(Project.budget)).scalar() or 0)
    
    payments_query = db.query(Payment).join(Invoice).join(Project).filter(Payment.status == "approved", Payment.deleted_at == None)
    payments_query = apply_project_filters(payments_query, start_date, end_date, status, sales, pm, event_category, partner)
    revenue_confirmed = float(payments_query.with_entities(func.sum(Payment.amount)).scalar() or 0)
    
    revenue_target_2025 = 9200000000.0  # Rp 9.2B Target
    revenue_target_progress = round((revenue_confirmed / revenue_target_2025 * 100), 2) if revenue_target_2025 > 0 else 0.0

    # Build active critical alerts list
    alerts = []
    overdue_tasks = db.query(Task).join(Project).filter(Task.deleted_at == None, Task.status != "done", Task.due_date < datetime.now()).all()
    for t in overdue_tasks:
        alerts.append({"type": "warning", "module": "tasks", "message": f"Overdue Checklist Task: {t.title} assigned to {t.assigned_to.full_name if t.assigned_to else 'staff'}"})

    overdue_invoices = db.query(Invoice).join(Project).filter(Invoice.deleted_at == None, Invoice.status == "overdue").all()
    for inv in overdue_invoices:
        alerts.append({"type": "danger", "module": "finance", "message": f"Invoice {inv.invoice_number} is overdue! Outstanding balance was due {inv.due_date}"})

    return {
        "total_projects": total_projects,
        "ongoing_projects": ongoing_projects,
        "completed_projects": completed_projects,
        "canceled_projects": canceled_projects,
        "total_inquiries": total_inquiries,
        "project_deal_ratio": project_deal_ratio,
        "revenue_projected": revenue_projected,
        "revenue_confirmed": revenue_confirmed,
        "revenue_target_2025": revenue_target_2025,
        "revenue_target_progress": revenue_target_progress,
        "alerts": alerts[:8]
    }

# 2. Revenue Deep Intelligence Endpoint
@router.get("/revenue")
def get_revenue_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    project_query = db.query(Project).filter(Project.deleted_at == None)
    project_query = apply_project_filters(project_query, start_date, end_date, status, sales, pm, event_category, partner)
    
    revenue_projected = float(project_query.with_entities(func.sum(Project.budget)).scalar() or 0)

    payments_query = db.query(Payment).join(Invoice).join(Project).filter(Payment.status == "approved", Payment.deleted_at == None)
    payments_query = apply_project_filters(payments_query, start_date, end_date, status, sales, pm, event_category, partner)
    revenue_confirmed = float(payments_query.with_entities(func.sum(Payment.amount)).scalar() or 0)
    
    revenue_pending = max(0.0, revenue_projected - revenue_confirmed)
    revenue_target_2025 = 9200000000.0

    # Revenue trend monthly (Last 6 Months)
    today_dt = date.today()
    monthly_trends = []
    for i in range(5, -1, -1):
        m = today_dt.month - i
        y = today_dt.year
        if m <= 0:
            m += 12
            y -= 1
        start_dt = date(y, m, 1)
        end_dt = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y + 1, 1, 1) - timedelta(days=1)
        month_name = start_dt.strftime("%b %Y")
        
        trend_pay_query = db.query(Payment).join(Invoice).join(Project).filter(
            Payment.status == "approved", Payment.deleted_at == None,
            Payment.payment_date >= start_dt, Payment.payment_date <= end_dt
        )
        trend_pay_query = apply_project_filters(trend_pay_query, start_date, end_date, status, sales, pm, event_category, partner)
        sum_amount = float(trend_pay_query.with_entities(func.sum(Payment.amount)).scalar() or 0)
        monthly_trends.append({"month": month_name, "amount": sum_amount})

    # Revenue by Category (dynamic string lookup in Project Title)
    results = project_query.with_entities(Project.title, Project.budget).all()
    categories = {"Gathering": 0.0, "Entertainment": 0.0, "Production": 0.0, "Outbound/TB": 0.0, "Other": 0.0}
    for p_title, p_budget in results:
        b = float(p_budget or 0)
        t_lower = p_title.lower()
        if "gathering" in t_lower:
            categories["Gathering"] += b
        elif "entertainment" in t_lower:
            categories["Entertainment"] += b
        elif "production" in t_lower:
            categories["Production"] += b
        elif "tb" in t_lower or "team building" in t_lower or "outbound" in t_lower:
            categories["Outbound/TB"] += b
        else:
            categories["Other"] += b
    revenue_by_category = [{"category": k, "amount": v} for k, v in categories.items()]

    # Revenue by Sales (aggregating Project budget grouped by created_by_id)
    sales_raw = project_query.with_entities(Project.created_by_id, func.sum(Project.budget)).group_by(Project.created_by_id).all()
    revenue_by_sales = []
    for user_id, sum_budget in sales_raw:
        user = db.query(User).filter(User.id == user_id).first()
        name = user.full_name if user else "Unknown Creator"
        revenue_by_sales.append({"sales": name, "amount": float(sum_budget or 0)})

    # Revenue by Customer Category
    partner_raw = project_query.join(Customer).with_entities(Customer.category, func.sum(Project.budget)).group_by(Customer.category).all()
    revenue_by_partner = [{"partner": cat, "amount": float(sum_val or 0)} for cat, sum_val in partner_raw]

    return {
        "revenue_projected": revenue_projected,
        "revenue_confirmed": revenue_confirmed,
        "revenue_pending": revenue_pending,
        "revenue_target": revenue_target_2025,
        "revenue_target_progress": round((revenue_confirmed / revenue_target_2025 * 100), 2) if revenue_target_2025 > 0 else 0.0,
        "monthly_trends": monthly_trends,
        "revenue_by_category": revenue_by_category,
        "revenue_by_sales": revenue_by_sales,
        "revenue_by_partner": revenue_by_partner
    }

# 3. Workflow Pipeline & Status distribution Endpoint
@router.get("/workflow")
def get_workflow_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    project_query = db.query(Project).filter(Project.deleted_at == None)
    project_query = apply_project_filters(project_query, start_date, end_date, status, sales, pm, event_category, partner)

    # Status distribution counts
    status_counts_raw = project_query.with_entities(Project.status, func.count(Project.id)).group_by(Project.status).all()
    project_status_counts = {stat: count for stat, count in status_counts_raw}
    all_stages = ["inquiry", "quotation", "negotiation", "confirmed", "preparation", "ongoing", "completed", "canceled"]
    for s in all_stages:
        if s not in project_status_counts:
            project_status_counts[s] = 0

    # Pipeline funnel counts (Cumulative representation)
    completed_count = project_status_counts.get("completed", 0)
    confirmed_count = completed_count + project_status_counts.get("confirmed", 0) + project_status_counts.get("preparation", 0) + project_status_counts.get("ongoing", 0)
    negotiation_count = confirmed_count + project_status_counts.get("negotiation", 0)
    quotation_count = negotiation_count + project_status_counts.get("quotation", 0)
    inquiry_count = quotation_count + project_status_counts.get("inquiry", 0)

    pipeline_funnel = [
        {"stage": "Inquiry", "count": inquiry_count, "percentage": 100.0},
        {"stage": "Quotation", "count": quotation_count, "percentage": round((quotation_count / inquiry_count * 100), 1) if inquiry_count > 0 else 0.0},
        {"stage": "Negotiation", "count": negotiation_count, "percentage": round((negotiation_count / quotation_count * 100), 1) if quotation_count > 0 else 0.0},
        {"stage": "Confirmed", "count": confirmed_count, "percentage": round((confirmed_count / negotiation_count * 100), 1) if negotiation_count > 0 else 0.0},
        {"stage": "Completed", "count": completed_count, "percentage": round((completed_count / confirmed_count * 100), 1) if confirmed_count > 0 else 0.0}
    ]

    total = max(1, sum(project_status_counts.values()))
    completion_rate = round((completed_count / total * 100), 1)

    return {
        "project_status_counts": project_status_counts,
        "pipeline_funnel": pipeline_funnel,
        "completion_rate": completion_rate
    }

# 4. Event Scheduling Density & Upcoming calendar listings Endpoint
@router.get("/events")
def get_event_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    now = datetime.now()
    
    # Event schedules join Project
    event_query = db.query(EventSchedule).join(Project).filter(EventSchedule.deleted_at == None)
    event_query = apply_project_filters(event_query, start_date, end_date, status, sales, pm, event_category, partner)
    
    # Upcoming runs next 30 days
    upcoming_events_raw = event_query.filter(EventSchedule.start_time >= now).order_by(EventSchedule.start_time.asc()).limit(10).all()
    upcoming_events = []
    for ev in upcoming_events_raw:
        upcoming_events.append({
            "id": str(ev.id),
            "project_title": ev.project.title,
            "venue_name": ev.venue_name,
            "start_time": ev.start_time.isoformat(),
            "end_time": ev.end_time.isoformat() if ev.end_time else None
        })

    # Density listing by month (Event Calendar)
    density_raw = event_query.with_entities(func.to_char(EventSchedule.start_time, 'YYYY-MM'), func.count(EventSchedule.id)).group_by(func.to_char(EventSchedule.start_time, 'YYYY-MM')).all()
    event_density = [{"month": m, "count": cnt} for m, cnt in density_raw]

    # Top venues load
    venue_raw = event_query.with_entities(EventSchedule.venue_name, func.count(EventSchedule.id)).group_by(EventSchedule.venue_name).order_by(func.count(EventSchedule.id).desc()).limit(5).all()
    venue_counts = [{"venue": v, "count": c} for v, c in venue_raw if v]

    return {
        "upcoming_events": upcoming_events,
        "event_density": event_density,
        "venue_counts": venue_counts
    }

# 5. Finance Health & billing details Endpoint
@router.get("/finance")
def get_finance_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    invoices_query = db.query(Invoice).join(Project).filter(Invoice.deleted_at == None)
    invoices_query = apply_project_filters(invoices_query, start_date, end_date, status, sales, pm, event_category, partner)

    # Invoices aggregate
    total_invoices_count = invoices_query.count()
    unpaid_invoices_query = invoices_query.filter(Invoice.status.in_(["unpaid", "partial"]))
    unpaid_invoices_count = unpaid_invoices_query.count()
    unpaid_invoices_amount = float(unpaid_invoices_query.with_entities(func.sum(Invoice.amount)).scalar() or 0)

    overdue_invoices_query = invoices_query.filter(Invoice.status == "overdue")
    overdue_invoices_count = overdue_invoices_query.count()
    overdue_invoices_amount = float(overdue_invoices_query.with_entities(func.sum(Invoice.amount)).scalar() or 0)

    # Invoices distribution
    inv_counts_raw = invoices_query.with_entities(Invoice.status, func.count(Invoice.id)).group_by(Invoice.status).all()
    invoice_status_distribution = {stat: count for stat, count in inv_counts_raw}
    for s in ["unpaid", "partial", "paid", "overdue"]:
        if s not in invoice_status_distribution:
            invoice_status_distribution[s] = 0

    paid_count = invoice_status_distribution.get("paid", 0)
    payment_completion_rate = round((paid_count / max(1, total_invoices_count) * 100), 1)

    # Active Overdue invoice listing
    overdue_list = overdue_invoices_query.order_by(Invoice.due_date.asc()).limit(5).all()
    overdue_invoices_list = []
    for inv in overdue_list:
        overdue_invoices_list.append({
            "invoice_number": inv.invoice_number,
            "project_title": inv.project.title,
            "amount": float(inv.amount),
            "due_date": str(inv.due_date)
        })

    return {
        "unpaid_invoices_count": unpaid_invoices_count,
        "unpaid_invoices_amount": unpaid_invoices_amount,
        "overdue_invoices_count": overdue_invoices_count,
        "overdue_invoices_amount": overdue_invoices_amount,
        "invoice_status_distribution": invoice_status_distribution,
        "payment_completion_rate": payment_completion_rate,
        "overdue_invoices_list": overdue_invoices_list
    }

# 6. PM Workloads & Heatmap allocations Endpoint
@router.get("/team")
def get_team_analytics(
    db: Session = Depends(deps.get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    sales: Optional[str] = Query(None),
    pm: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    partner: Optional[str] = Query(None)
):
    users = db.query(User).filter(User.deleted_at == None).all()
    pm_workloads = []
    assignment_heatmap = []

    for u in users:
        tasks_query = db.query(Task).join(Project).filter(Task.assigned_to_id == u.id, Task.deleted_at == None)
        tasks_query = apply_project_filters(tasks_query, start_date, end_date, status, sales, pm, event_category, partner)
        
        todo = tasks_query.filter(Task.status == "todo").count()
        in_progress = tasks_query.filter(Task.status == "in_progress").count()
        review = tasks_query.filter(Task.status == "review").count()
        done = tasks_query.filter(Task.status == "done").count()
        total = todo + in_progress + review + done

        if total > 0:
            pm_workloads.append({
                "name": u.full_name,
                "todo": todo,
                "in_progress": in_progress,
                "review": review,
                "done": done,
                "total": total,
                "completion_rate": round((done / total * 100), 1)
            })

        # Event schedule counts per user (Heatmap density)
        scheds_query = db.query(EventSchedule).join(Project).filter(EventSchedule.pic_id == u.id, EventSchedule.deleted_at == None)
        scheds_query = apply_project_filters(scheds_query, start_date, end_date, status, sales, pm, event_category, partner)
        sched_count = scheds_query.count()
        assignment_heatmap.append({
            "pm_name": u.full_name,
            "events_allocated": sched_count
        })

    return {
        "pm_workloads": pm_workloads,
        "assignment_heatmap": assignment_heatmap
    }

# 7. Audit log events chronologically Endpoint
@router.get("/activity")
def get_activity_timeline(
    db: Session = Depends(deps.get_db),
    limit: int = Query(20, ge=1, le=100),
    action: Optional[str] = Query(None),
    entity_type: Optional[str] = Query(None)
):
    query = db.query(ActivityLog)
    if action:
        query = query.filter(ActivityLog.action == action)
    if entity_type:
        query = query.filter(ActivityLog.entity_type == entity_type)
        
    recent_logs = query.order_by(ActivityLog.created_at.desc()).limit(limit).all()
    activities = []
    for log in recent_logs:
        activities.append({
            "id": str(log.id),
            "action": log.action,
            "entity_type": log.entity_type,
            "entity_id": str(log.entity_id) if log.entity_id else None,
            "user_name": log.user.full_name if log.user else "System Action",
            "details": log.details,
            "created_at": log.created_at.isoformat()
        })
    return {"activities": activities}

# GET /api/v1/dashboard/analytics Endpoint
@router.get("/analytics", response_model=DashboardAnalyticsResponse)
def get_analytics(
    db: Session = Depends(deps.get_db),
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    po_id: Optional[UUID] = Query(None),
    pm_id: Optional[UUID] = Query(None),
    source_type: Optional[str] = Query(None),
    quotation_status: Optional[str] = Query(None),
    program_status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    project_status: Optional[str] = Query(None),
    customer_category: Optional[str] = Query(None),
    event_category: Optional[str] = Query(None),
    program_type: Optional[str] = Query(None),
    current_user: User = Depends(deps.get_current_user)
):
    """Retrieve structured business intelligence metrics, PO/PM workloads, category shares, and data audits"""
    filters = {
        "year": year,
        "month": month,
        "date_from": date_from,
        "date_to": date_to,
        "po_id": po_id,
        "pm_id": pm_id,
        "source_type": source_type,
        "quotation_status": quotation_status,
        "program_status": program_status,
        "payment_status": payment_status,
        "project_status": project_status,
        "customer_category": customer_category,
        "event_category": event_category,
        "program_type": program_type,
    }
    return get_dashboard_analytics(db, filters)


@router.get("/pm-control-center", response_model=PMControlCenterResponse)
def get_pm_control_center(
    db: Session = Depends(deps.get_db),
    pm_id: Optional[str] = Query(None),
    po_id: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    readiness_min: Optional[float] = Query(None),
    readiness_max: Optional[float] = Query(None),
    include_closed: bool = Query(False),
    include_canceled: bool = Query(False),
    instrument_status: Optional[str] = Query(None),
    event_window: str = Query("all"),
    current_user: User = Depends(deps.get_current_user)
):
    """Retrieve day-to-day operational schedules, checklists, instrument alerts, workloads and priority action recommendations."""
    from app.modules.dashboard import operational_service
    return operational_service.get_pm_control_center_data(
        db,
        pm_id=pm_id,
        po_id=po_id,
        date_from=date_from,
        date_to=date_to,
        readiness_min=readiness_min,
        readiness_max=readiness_max,
        include_closed=include_closed,
        include_canceled=include_canceled,
        instrument_status=instrument_status,
        event_window=event_window
    )


@router.get("/po-control-center", response_model=POControlCenterResponse)
def get_po_control_center(
    db: Session = Depends(deps.get_db),
    po_id: Optional[str] = Query(None),
    pm_id: Optional[str] = Query(None),
    source_type: Optional[str] = Query(None),
    customer_category: Optional[str] = Query(None),
    quotation_status: Optional[str] = Query(None),
    program_status: Optional[str] = Query(None),
    payment_status: Optional[str] = Query(None),
    project_status: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    event_window: str = Query("all"),
    include_closed: bool = Query(False),
    include_canceled: bool = Query(False),
    current_user: User = Depends(deps.get_current_user)
):
    """Retrieve PO Control Center commercial aggregates, quotation tracking, revenue conversion, workloads, and risks."""
    from app.modules.dashboard import po_control_service
    return po_control_service.get_po_control_center_data(
        db,
        po_id=po_id,
        pm_id=pm_id,
        source_type=source_type,
        customer_category=customer_category,
        quotation_status=quotation_status,
        program_status=program_status,
        payment_status=payment_status,
        project_status=project_status,
        date_from=date_from,
        date_to=date_to,
        event_window=event_window,
        include_closed=include_closed,
        include_canceled=include_canceled
    )

