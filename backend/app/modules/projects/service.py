from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.projects.models import Project, ProjectStatusLog, ProjectActivityLog, ProjectInstrument
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate, ProjectInstrumentCreate, ProjectInstrumentUpdate
from app.modules.crm import service as crm_service
from app.modules.crm.schemas import CustomerCreate
from app.core.activity import log_activity
from app.core.database import db_commit_safety
from datetime import date, datetime, timezone

import uuid

def get_project(db: Session, project_id: str) -> Optional[Project]:
    parsed_id = project_id
    if isinstance(project_id, str):
        try:
            parsed_id = uuid.UUID(project_id)
        except ValueError:
            pass
    return db.query(Project).filter(Project.id == parsed_id, Project.deleted_at == None).first()

def get_projects(
    db: Session, 
    status: Optional[str] = None, 
    skip: int = 0, 
    limit: int = 100,
    po_id: Optional[uuid.UUID] = None,
    pm_id: Optional[uuid.UUID] = None,
    source_id: Optional[uuid.UUID] = None,
    quotation_status: Optional[str] = None,
    program_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    project_status: Optional[str] = None
) -> List[Project]:
    query = db.query(Project).filter(Project.deleted_at == None)
    if status:
        query = query.filter(Project.status == status)
    if po_id:
        query = query.filter(Project.program_owner_id == po_id)
    if pm_id:
        query = query.filter(Project.program_manager_id == pm_id)
    if source_id:
        query = query.filter(Project.event_source_id == source_id)
    if quotation_status:
        query = query.filter(Project.quotation_status == quotation_status)
    if program_status:
        query = query.filter(Project.program_status == program_status)
    if payment_status:
        query = query.filter(Project.payment_status == payment_status)
    if project_status:
        query = query.filter(Project.project_status == project_status)
    return query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

def check_project_validation_warnings(project: Project) -> List[str]:
    warnings = []
    
    # 1. Event end date before start date
    if project.event_date_start and project.event_date_end:
        if project.event_date_end < project.event_date_start:
            warnings.append("Event end date cannot be before the event start date.")
    
    # 2. Budget missing or negative
    if project.budget is None or project.budget < 0:
        warnings.append("Project budget allocation is missing or negative.")
        
    # 3. Quotation status Cancel without cancel_reason
    if (project.quotation_status or "").lower() == "cancel":
        if not project.cancel_reason or not project.cancel_reason.strip():
            warnings.append("Quotation status is 'Cancel' but no cancel reason is provided.")
            
    # 4. Quotation status Signed & Deal with missing/zero budget
    if (project.quotation_status or "").lower() in ["signed & deal", "signed", "deal", "approved"]:
        if not project.budget or project.budget <= 0:
            warnings.append("Quotation is signed/approved but the budget is missing or zero.")
            
    # 5. Project status Closed while payment_status is not Paid
    if (project.project_status or "").lower() == "closed":
        if (project.payment_status or "").lower() != "paid":
            warnings.append("Project is 'Closed' but payment status is not 'Paid'.")
            
    # 6. Program status Closed/Completed while documentation is missing
    if (project.program_status or "").lower() in ["completed", "closed"]:
        if not project.documents or len(project.documents) == 0:
            warnings.append("Event is completed/closed but no operational documentation is attached.")
            
    # 7 & 8. paid_amount checks
    paid = project.paid_amount
    budget = float(project.budget) if project.budget else 0.0
    
    if (project.payment_status or "").lower() == "paid":
        if not paid or paid <= 0:
            warnings.append("Payment status is marked as 'Paid' but total collected amount is zero or missing.")
            
    if paid > budget and budget > 0:
        warnings.append(f"Total payment collected (Rp {paid:,.0f}) exceeds the allocated budget (Rp {budget:,.0f}).")
        
    # Project Instruments Validation warnings (Sprint 6 & 7)
    instruments = {inst.instrument_type: inst for inst in project.instruments if not inst.deleted_at}
    today = date.today()
    
    # CL missing or not Done for confirmed project
    if (project.program_status or "").lower() in ["confirmed", "preparation", "ready", "running", "completed", "reporting", "closed"]:
        cl = instruments.get("CL")
        if not cl or (cl.status or "").lower() != "done":
            warnings.append("Contract/Confirmation Letter (CL) is missing or not marked as 'Done' for this confirmed project.")
            
    # CL missing or not Done for Signed & Deal project
    if (project.quotation_status or "").lower() in ["signed & deal", "signed", "deal", "approved"]:
        cl = instruments.get("CL")
        if not cl or (cl.status or "").lower() != "done":
            warnings.append("Contract/Confirmation Letter (CL) is missing or not marked as 'Done' for this Signed & Deal project.")
            
    # ROS not Done when Program Status is Ready, Running, Completed, Reporting, or Closed
    if (project.program_status or "").lower() in ["ready", "running", "completed", "reporting", "closed"]:
        ros = instruments.get("ROS")
        if not ros or (ros.status or "").lower() != "done":
            warnings.append("Rundown of Show (ROS) is missing or not marked as 'Done' for this project (Status: Ready/Running/Completed/Reporting/Closed).")
            
    # CK not Done when Program Status is Ready, Running, Completed, Reporting, or Closed
    if (project.program_status or "").lower() in ["ready", "running", "completed", "reporting", "closed"]:
        ck = instruments.get("CK")
        if not ck or (ck.status or "").lower() != "done":
            warnings.append("Check List (CK) is missing or not marked as 'Done' for this project (Status: Ready/Running/Completed/Reporting/Closed).")
            
    # PNL missing for Signed & Deal project
    if (project.quotation_status or "").lower() in ["signed & deal", "signed", "deal", "approved"]:
        pnl = instruments.get("PNL")
        if not pnl or not pnl.document_url:
            warnings.append("Profit & Loss (PNL) document link is missing for this Signed & Deal project.")
            
    # Instrument has status Need Revision
    for inst in project.instruments:
        if not inst.deleted_at and inst.status == "Need Revision":
            warnings.append(f"Instrument {inst.instrument_type} ('{inst.title}') requires revision.")
            
    # Instrument has due date passed and status is not Done
    for inst in project.instruments:
        if not inst.deleted_at and inst.due_date and inst.due_date < today and inst.status != "Done" and inst.status != "Not Required":
            warnings.append(f"Instrument {inst.instrument_type} ('{inst.title}') is overdue (due date: {inst.due_date} was passed).")
            
    # PNL sensitive visibility access warning
    pnl = instruments.get("PNL")
    if pnl:
        warnings.append("PNL access warning: PNL document is sensitive and should be restricted to Management/Finance/Admin in production.")
        
    return warnings

def calculate_project_readiness(project: Project) -> dict:
    today = date.today()
    
    # 1. Filter out deleted instruments
    active_instruments = [inst for inst in project.instruments if not inst.deleted_at]
    
    # 2. Required instruments: status is not "Not Required"
    required_instruments = [inst for inst in active_instruments if inst.status != "Not Required"]
    required_count = len(required_instruments)
    
    # 3. Completed required instruments: status is "Done"
    completed_required_count = sum(1 for inst in required_instruments if inst.status == "Done")
    
    # 4. Completion rate
    completion_rate = 0.0
    if required_count > 0:
        completion_rate = completed_required_count / required_count
        
    # 5. Missing required instruments
    missing_count = required_count - completed_required_count
    
    # 6. Revision required count
    revision_count = sum(1 for inst in required_instruments if inst.status == "Need Revision")
    
    # 7. Overdue instruments: due_date in the past and status is not Done or Not Required
    overdue_count = sum(
        1 for inst in active_instruments
        if inst.due_date and inst.due_date < today and inst.status != "Done" and inst.status != "Not Required"
    )
    
    # 8. Readiness score formula
    # - instrument_completion_rate contributes 60%
    # - documentation availability contributes 20%
    # - status consistency contributes 20%
    
    # Documentation score: 1.0 if active documents exist, else 0.0
    active_docs = [doc for doc in project.documents if not doc.deleted_at]
    documentation_score = 1.0 if len(active_docs) > 0 else 0.0
    
    # Status consistency score: based on validation warnings (excluding PNL sensitivity security note)
    warnings = check_project_validation_warnings(project)
    operational_warnings = [w for w in warnings if "PNL access warning" not in w]
    status_consistency_score = max(0.0, 1.0 - 0.2 * len(operational_warnings))
    
    # Combined score
    readiness_score = (completion_rate * 0.6) + (documentation_score * 0.2) + (status_consistency_score * 0.2)
    
    return {
        "required_instruments_count": required_count,
        "completed_required_instruments_count": completed_required_count,
        "instrument_completion_rate": completion_rate,
        "missing_required_instruments_count": missing_count,
        "revision_required_count": revision_count,
        "overdue_instruments_count": overdue_count,
        "project_readiness_score": readiness_score
    }


def resolve_project_customer(db: Session, project_in: ProjectCreate, user_id: str):
    if project_in.customer_id:
        customer = crm_service.get_customer(db, customer_id=str(project_in.customer_id))
        if not customer:
            raise ValueError("Selected customer account was not found.")
        return customer, False

    customer_name = (project_in.customer_name or "").strip()
    if not customer_name:
        raise ValueError("Provide an existing customer_id or a new customer_name.")

    matches = crm_service.check_duplicate_customer(db, company_name=customer_name)
    if matches:
        return matches[0], False

    category = (project_in.customer_category or "Prospect").strip() or "Prospect"
    customer = crm_service.create_customer(
        db,
        customer_in=CustomerCreate(
            company_name=customer_name,
            category=category,
            notes="Auto-created from Project intake. Complete CRM profile and contacts before production handoff."
        ),
        user_id=user_id,
        commit=False
    )
    return customer, True


def create_project(db: Session, project_in: ProjectCreate, created_by_id: str) -> Project:
    parsed_creator_id = None
    if created_by_id:
        if isinstance(created_by_id, str):
            try:
                parsed_creator_id = uuid.UUID(created_by_id)
            except ValueError:
                parsed_creator_id = None
        else:
            parsed_creator_id = created_by_id

    customer, customer_created = resolve_project_customer(db, project_in, user_id=created_by_id)
    proj_title = project_in.title or project_in.program_name or "Untitled Program"

    db_project = Project(
        title=proj_title,
        status=project_in.status,
        quotation_status=project_in.quotation_status,
        start_date=project_in.start_date or project_in.event_date_start,
        end_date=project_in.end_date or project_in.event_date_end,
        budget=project_in.budget,
        revenue=project_in.revenue,
        customer_id=customer.id,
        created_by_id=parsed_creator_id,
        assigned_to_id=project_in.assigned_to_id or project_in.program_manager_id,
        
        # New fields
        project_code=project_in.project_code,
        inquiry_date=project_in.inquiry_date,
        event_category=project_in.event_category,
        program_type=project_in.program_type,
        program_name=project_in.program_name or proj_title,
        quantity=project_in.quantity,
        venue=project_in.venue,
        duration=project_in.duration,
        event_date_start=project_in.event_date_start or project_in.start_date,
        event_date_end=project_in.event_date_end or project_in.end_date,
        quotation_date=project_in.quotation_date,
        quotation_number=project_in.quotation_number,
        program_status=project_in.program_status,
        payment_status=project_in.payment_status,
        project_status=project_in.project_status,
        cancel_reason=project_in.cancel_reason,
        mom_notes=project_in.mom_notes,
        general_notes=project_in.general_notes,
        
        event_source_id=project_in.event_source_id,
        program_owner_id=project_in.program_owner_id,
        program_manager_id=project_in.program_manager_id or project_in.assigned_to_id
    )
    db.add(db_project)
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Auto-create default project instruments
    ensure_default_project_instruments(db, db_project.id)
    db.refresh(db_project)
    
    # Create initial transition log
    log = ProjectStatusLog(
        project_id=db_project.id,
        status_type="program_status",
        old_status="none",
        new_status=db_project.program_status,
        from_status="none",
        to_status=db_project.program_status,
        notes="Project created",
        changed_by_user_id=parsed_creator_id,
        changed_by_id=parsed_creator_id
    )
    db.add(log)
    
    # Log project created to ProjectActivityLog
    activity = ProjectActivityLog(
        project_id=db_project.id,
        user_id=parsed_creator_id,
        action="project_created",
        notes=f"Project '{db_project.title}' initialized."
    )
    db.add(activity)
    if customer_created:
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_creator_id,
            action="customer_auto_created",
            field_name="customer_id",
            new_value=str(customer.id),
            notes=f"Customer '{customer.company_name}' auto-created from Project intake."
        ))
    db_commit_safety(db)

    if customer_created:
        log_activity(
            db,
            user_id=parsed_creator_id,
            action="customer_created_from_project",
            entity_type="customer",
            entity_id=customer.id,
            details={
                "company_name": customer.company_name,
                "category": customer.category,
                "project_id": str(db_project.id)
            }
        )
    
    # Central activity logging
    log_activity(
        db, 
        user_id=parsed_creator_id, 
        action="project_created", 
        entity_type="project", 
        entity_id=db_project.id, 
        details={"title": db_project.title, "status": db_project.program_status}
    )
    
    return db_project

def update_project(db: Session, db_project: Project, project_in: ProjectUpdate, changed_by_id: str) -> Project:
    project_data = project_in.model_dump(exclude_unset=True)
    
    parsed_changer_id = None
    if changed_by_id:
        if isinstance(changed_by_id, str):
            try:
                parsed_changer_id = uuid.UUID(changed_by_id)
            except ValueError:
                parsed_changer_id = None
        else:
            parsed_changer_id = changed_by_id

    # Track fields for project activity logging
    old_po = db_project.program_owner_id
    old_pm = db_project.program_manager_id
    old_budget = db_project.budget
    old_quote_status = db_project.quotation_status
    old_prog_status = db_project.program_status
    old_pay_status = db_project.payment_status
    old_proj_status = db_project.project_status
    old_status = db_project.status

    # Sync compatibility fields
    if "event_date_start" in project_data and project_data["event_date_start"]:
        db_project.start_date = project_data["event_date_start"]
    if "event_date_end" in project_data and project_data["event_date_end"]:
        db_project.end_date = project_data["event_date_end"]
        
    for field, value in project_data.items():
        setattr(db_project, field, value)
    
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Track changed fields and create activity logs
    if old_po != db_project.program_owner_id:
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="po_changed",
            field_name="program_owner_id",
            old_value=str(old_po) if old_po else None,
            new_value=str(db_project.program_owner_id) if db_project.program_owner_id else None,
            notes="Program Owner updated."
        ))
        
    if old_pm != db_project.program_manager_id:
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="pm_changed",
            field_name="program_manager_id",
            old_value=str(old_pm) if old_pm else None,
            new_value=str(db_project.program_manager_id) if db_project.program_manager_id else None,
            notes="Program Manager updated."
        ))
        db_project.assigned_to_id = db_project.program_manager_id
        
    if old_budget != db_project.budget:
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="budget_updated",
            field_name="budget",
            old_value=str(old_budget),
            new_value=str(db_project.budget),
            notes="Budget updated."
        ))
        
    # Status changes & status log entries
    if old_quote_status != db_project.quotation_status:
        db.add(ProjectStatusLog(
            project_id=db_project.id,
            status_type="quotation_status",
            old_status=old_quote_status,
            new_status=db_project.quotation_status,
            from_status=old_quote_status,
            to_status=db_project.quotation_status,
            notes="Quotation status updated",
            changed_by_user_id=parsed_changer_id,
            changed_by_id=parsed_changer_id
        ))
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="quotation_status_changed",
            field_name="quotation_status",
            old_value=old_quote_status,
            new_value=db_project.quotation_status
        ))

    if old_prog_status != db_project.program_status:
        db.add(ProjectStatusLog(
            project_id=db_project.id,
            status_type="program_status",
            old_status=old_prog_status,
            new_status=db_project.program_status,
            from_status=old_prog_status,
            to_status=db_project.program_status,
            notes="Program status updated",
            changed_by_user_id=parsed_changer_id,
            changed_by_id=parsed_changer_id
        ))
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="program_status_changed",
            field_name="program_status",
            old_value=old_prog_status,
            new_value=db_project.program_status
        ))
        db_project.status = db_project.program_status.lower()

    if old_pay_status != db_project.payment_status:
        db.add(ProjectStatusLog(
            project_id=db_project.id,
            status_type="payment_status",
            old_status=old_pay_status,
            new_status=db_project.payment_status,
            from_status=old_pay_status,
            to_status=db_project.payment_status,
            notes="Payment status updated",
            changed_by_user_id=parsed_changer_id,
            changed_by_id=parsed_changer_id
        ))
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="payment_status_changed",
            field_name="payment_status",
            old_value=old_pay_status,
            new_value=db_project.payment_status
        ))

    if old_proj_status != db_project.project_status:
        db.add(ProjectStatusLog(
            project_id=db_project.id,
            status_type="project_status",
            old_status=old_proj_status,
            new_status=db_project.project_status,
            from_status=old_proj_status,
            to_status=db_project.project_status,
            notes="Project status updated",
            changed_by_user_id=parsed_changer_id,
            changed_by_id=parsed_changer_id
        ))
        db.add(ProjectActivityLog(
            project_id=db_project.id,
            user_id=parsed_changer_id,
            action="project_status_changed",
            field_name="project_status",
            old_value=old_proj_status,
            new_value=db_project.project_status
        ))
        if db_project.project_status.lower() == "closed":
            db.add(ProjectActivityLog(
                project_id=db_project.id,
                user_id=parsed_changer_id,
                action="project_closed",
                notes="Project closed."
            ))
            
    db_commit_safety(db)
    
    # Central activity logging for status change
    new_status = project_data.get("status", old_status)
    new_program_status = project_data.get("program_status", old_prog_status)
    if old_status != new_status or old_prog_status != new_program_status:
        log_activity(
            db, 
            user_id=parsed_changer_id, 
            action="status_transitioned", 
            entity_type="project", 
            entity_id=db_project.id, 
            details={"title": db_project.title, "old_status": old_prog_status, "new_status": new_program_status, "source": "project_update"}
        )
        
    return db_project

def transition_project_status(
    db: Session, 
    db_project: Project, 
    new_status: str, 
    notes: Optional[str], 
    changed_by_id: str
) -> Project:
    old_status = db_project.program_status
    if old_status == new_status:
        return db_project
        
    parsed_changer_id = None
    if changed_by_id:
        if isinstance(changed_by_id, str):
            try:
                parsed_changer_id = uuid.UUID(changed_by_id)
            except ValueError:
                parsed_changer_id = None
        else:
            parsed_changer_id = changed_by_id

    # Update both legacy status and new program_status for compatibility
    db_project.program_status = new_status
    db_project.status = new_status.lower()
    
    db_commit_safety(db)
    
    # Log transition to ProjectStatusLog
    log = ProjectStatusLog(
        project_id=db_project.id,
        status_type="program_status",
        old_status=old_status,
        new_status=new_status,
        from_status=old_status,
        to_status=new_status,
        notes=notes or f"Status shifted from {old_status} to {new_status}",
        changed_by_user_id=parsed_changer_id,
        changed_by_id=parsed_changer_id
    )
    db.add(log)
    
    # Write to ProjectActivityLog
    db.add(ProjectActivityLog(
        project_id=db_project.id,
        user_id=parsed_changer_id,
        action="program_status_changed",
        field_name="program_status",
        old_value=old_status,
        new_value=new_status,
        notes=notes
    ))
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=parsed_changer_id, 
        action="status_transitioned", 
        entity_type="project", 
        entity_id=db_project.id, 
        details={"title": db_project.title, "old_status": old_status, "new_status": new_status, "notes": notes or ""}
    )
    
    return db_project

def delete_project(db: Session, db_project: Project) -> Project:
    db_project.soft_delete()
    db_commit_safety(db)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=None, 
        action="project_archived", 
        entity_type="project", 
        entity_id=db_project.id, 
        details={"title": db_project.title}
    )
    
    return db_project

def update_project_status_generic(
    db: Session,
    db_project: Project,
    status_type: str,
    new_status: str,
    notes: Optional[str],
    changed_by_id: str
) -> Project:
    valid_types = ["quotation_status", "program_status", "payment_status", "project_status"]
    if status_type not in valid_types:
        raise ValueError(f"Invalid status_type. Must be one of {valid_types}")
        
    old_status = getattr(db_project, status_type)
    if old_status == new_status:
        return db_project
        
    parsed_changer_id = None
    if changed_by_id:
        if isinstance(changed_by_id, str):
            try:
                parsed_changer_id = uuid.UUID(changed_by_id)
            except ValueError:
                parsed_changer_id = None
        else:
            parsed_changer_id = changed_by_id

    # Update field
    setattr(db_project, status_type, new_status)
    
    # If updating program status, also keep legacy field synced
    if status_type == "program_status":
        db_project.status = new_status.lower()
        
    db_commit_safety(db)
    
    # Log transition to ProjectStatusLog
    log = ProjectStatusLog(
        project_id=db_project.id,
        status_type=status_type,
        old_status=old_status,
        new_status=new_status,
        from_status=old_status if status_type == "program_status" else None,
        to_status=new_status if status_type == "program_status" else None,
        notes=notes or f"{status_type} shifted from {old_status} to {new_status}",
        changed_by_user_id=parsed_changer_id,
        changed_by_id=parsed_changer_id if status_type == "program_status" else None
    )
    db.add(log)
    
    # Write to ProjectActivityLog
    db.add(ProjectActivityLog(
        project_id=db_project.id,
        user_id=parsed_changer_id,
        action=f"{status_type}_changed",
        field_name=status_type,
        old_value=old_status,
        new_value=new_status,
        notes=notes
    ))
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=parsed_changer_id, 
        action="status_transitioned", 
        entity_type="project", 
        entity_id=db_project.id, 
        details={"title": db_project.title, "status_type": status_type, "old_status": old_status, "new_status": new_status, "notes": notes or ""}
    )
    
    return db_project

def get_project_logs(db: Session, project_id: str) -> List[ProjectStatusLog]:
    parsed_id = project_id
    if isinstance(project_id, str):
        try:
            parsed_id = uuid.UUID(project_id)
        except ValueError:
            pass
    return db.query(ProjectStatusLog).filter(ProjectStatusLog.project_id == parsed_id).order_by(ProjectStatusLog.created_at.desc()).all()

def get_project_instruments(db: Session, project_id: str) -> List[ProjectInstrument]:
    parsed_id = project_id
    if isinstance(project_id, str):
        try:
            parsed_id = uuid.UUID(project_id)
        except ValueError:
            pass
    return db.query(ProjectInstrument).filter(ProjectInstrument.project_id == parsed_id, ProjectInstrument.deleted_at == None).order_by(ProjectInstrument.created_at.asc()).all()

def create_project_instrument(db: Session, project_id: str, instrument_in: ProjectInstrumentCreate, user_id: str) -> ProjectInstrument:
    parsed_proj_id = project_id
    if isinstance(project_id, str):
        try:
            parsed_proj_id = uuid.UUID(project_id)
        except ValueError:
            pass
    parsed_user_id = user_id
    if isinstance(user_id, str):
        try:
            parsed_user_id = uuid.UUID(user_id)
        except ValueError:
            pass

    # For MVP, prevent duplicate instrument type per project unless instrument_type is OTHER
    if instrument_in.instrument_type != "OTHER":
        existing = db.query(ProjectInstrument).filter(
            ProjectInstrument.project_id == parsed_proj_id,
            ProjectInstrument.instrument_type == instrument_in.instrument_type,
            ProjectInstrument.deleted_at == None
        ).first()
        if existing:
            raise ValueError(f"Instrument of type {instrument_in.instrument_type} already exists for this project.")

    db_instrument = ProjectInstrument(
        project_id=parsed_proj_id,
        instrument_type=instrument_in.instrument_type,
        status=instrument_in.status or "Not Started",
        title=instrument_in.title or instrument_in.instrument_type,
        document_url=instrument_in.document_url,
        notes=instrument_in.notes,
        due_date=instrument_in.due_date,
        completed_date=instrument_in.completed_date,
        updated_by_user_id=parsed_user_id
    )
    db.add(db_instrument)
    
    # Log to ProjectActivityLog
    db.add(ProjectActivityLog(
        project_id=parsed_proj_id,
        user_id=parsed_user_id,
        action="instrument_created",
        field_name="instrument_type",
        new_value=instrument_in.instrument_type,
        notes=f"Instrument {instrument_in.instrument_type} created with status {db_instrument.status}"
    ))
    db_commit_safety(db)
    db.refresh(db_instrument)
    return db_instrument

def update_project_instrument(db: Session, instrument_id: str, instrument_in: ProjectInstrumentUpdate, user_id: str) -> ProjectInstrument:
    parsed_inst_id = instrument_id
    if isinstance(instrument_id, str):
        try:
            parsed_inst_id = uuid.UUID(instrument_id)
        except ValueError:
            pass
    parsed_user_id = user_id
    if isinstance(user_id, str):
        try:
            parsed_user_id = uuid.UUID(user_id)
        except ValueError:
            pass

    db_instrument = db.query(ProjectInstrument).filter(ProjectInstrument.id == parsed_inst_id, ProjectInstrument.deleted_at == None).first()
    if not db_instrument:
        raise ValueError("Instrument not found.")

    # Track fields changed for logging
    old_status = db_instrument.status
    old_doc_url = db_instrument.document_url
    old_notes = db_instrument.notes
    old_due_date = db_instrument.due_date
    old_completed_date = db_instrument.completed_date

    update_data = instrument_in.model_dump(exclude_unset=True)

    if "status" in update_data:
        db_instrument.status = update_data["status"]
        if update_data["status"].lower() == "done" and not db_instrument.completed_date:
            db_instrument.completed_date = date.today()
            
    if "title" in update_data:
        db_instrument.title = update_data["title"]
    if "document_url" in update_data:
        db_instrument.document_url = update_data["document_url"]
    if "notes" in update_data:
        db_instrument.notes = update_data["notes"]
    if "due_date" in update_data:
        db_instrument.due_date = update_data["due_date"]
    if "completed_date" in update_data:
        db_instrument.completed_date = update_data["completed_date"]

    db_instrument.updated_by_user_id = parsed_user_id
    db_instrument.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    # Log specific updates to ProjectActivityLog
    if "status" in update_data and old_status != db_instrument.status:
        action = "instrument_status_changed"
        if db_instrument.status == "Not Required":
            action = "instrument_marked_not_required"
        elif db_instrument.status == "Need Revision":
            action = "instrument_marked_need_revision"
            
        db.add(ProjectActivityLog(
            project_id=db_instrument.project_id,
            user_id=parsed_user_id,
            action=action,
            field_name=f"{db_instrument.instrument_type}_status",
            old_value=old_status,
            new_value=db_instrument.status,
            notes=f"Instrument {db_instrument.instrument_type} status updated to {db_instrument.status}"
        ))
        
    if "document_url" in update_data and old_doc_url != db_instrument.document_url:
        db.add(ProjectActivityLog(
            project_id=db_instrument.project_id,
            user_id=parsed_user_id,
            action="instrument_document_url_updated",
            field_name=f"{db_instrument.instrument_type}_document_url",
            old_value=old_doc_url,
            new_value=db_instrument.document_url,
            notes=f"Instrument {db_instrument.instrument_type} document URL updated"
        ))
        
    if "notes" in update_data and old_notes != db_instrument.notes:
        db.add(ProjectActivityLog(
            project_id=db_instrument.project_id,
            user_id=parsed_user_id,
            action="instrument_notes_updated",
            field_name=f"{db_instrument.instrument_type}_notes",
            old_value=old_notes,
            new_value=db_instrument.notes,
            notes=f"Instrument {db_instrument.instrument_type} notes updated"
        ))

    if "due_date" in update_data and old_due_date != db_instrument.due_date:
        db.add(ProjectActivityLog(
            project_id=db_instrument.project_id,
            user_id=parsed_user_id,
            action="instrument_due_date_changed",
            field_name=f"{db_instrument.instrument_type}_due_date",
            old_value=str(old_due_date) if old_due_date else None,
            new_value=str(db_instrument.due_date) if db_instrument.due_date else None,
            notes=f"Instrument {db_instrument.instrument_type} due date updated to {db_instrument.due_date}"
        ))

    if "completed_date" in update_data and old_completed_date != db_instrument.completed_date:
        db.add(ProjectActivityLog(
            project_id=db_instrument.project_id,
            user_id=parsed_user_id,
            action="instrument_completed_date_changed",
            field_name=f"{db_instrument.instrument_type}_completed_date",
            old_value=str(old_completed_date) if old_completed_date else None,
            new_value=str(db_instrument.completed_date) if db_instrument.completed_date else None,
            notes=f"Instrument {db_instrument.instrument_type} completed date updated to {db_instrument.completed_date}"
        ))

    db_commit_safety(db)
    db.refresh(db_instrument)
    return db_instrument

def delete_project_instrument(db: Session, instrument_id: str) -> bool:
    parsed_inst_id = instrument_id
    if isinstance(instrument_id, str):
        try:
            parsed_inst_id = uuid.UUID(instrument_id)
        except ValueError:
            pass
    db_instrument = db.query(ProjectInstrument).filter(ProjectInstrument.id == parsed_inst_id, ProjectInstrument.deleted_at == None).first()
    if not db_instrument:
        return False
    db_instrument.soft_delete()
    db_commit_safety(db)
    return True

def ensure_default_project_instruments(db: Session, project_id: uuid.UUID) -> List[ProjectInstrument]:
    default_types = ["CL", "ROS", "CK", "PNL"]
    created_instruments = []
    
    # We fetch existing active instruments first to avoid duplicate creation
    existing_types = {
        inst.instrument_type for inst in db.query(ProjectInstrument).filter(
            ProjectInstrument.project_id == project_id,
            ProjectInstrument.deleted_at == None
        ).all()
    }
    
    for itype in default_types:
        if itype not in existing_types:
            db_inst = ProjectInstrument(
                project_id=project_id,
                instrument_type=itype,
                status="Not Started",
                title=itype,
                document_url=None,
                notes=None
            )
            db.add(db_inst)
            created_instruments.append(db_inst)
            
    if created_instruments:
        db.add(ProjectActivityLog(
            project_id=project_id,
            action="instrument_defaults_generated",
            notes=f"Default instruments generated: {', '.join([i.instrument_type for i in created_instruments])}"
        ))
        db_commit_safety(db)
        
    return created_instruments

def categorize_warning(warning: str) -> str:
    warning_lower = warning.lower()
    if "pnl access warning" in warning_lower:
        return "security"
    elif any(term in warning_lower for term in ["budget", "payment", "paid", "invoice", "pnl document"]):
        return "finance"
    elif any(term in warning_lower for term in ["document", "documentation"]):
        return "documentation"
    elif any(term in warning_lower for term in ["instrument", "cl is missing", "cl not marked", "ros is missing", "ros not marked", "ck is missing", "ck not marked"]):
        return "instrument"
    elif any(term in warning_lower for term in ["event end date", "budget allocation is missing"]):
        return "operational"
    else:
        return "data_quality"

def evaluate_project_readiness_gate(project: Project, status_type: str, target_status: str) -> dict:
    warnings = []
    blockers = []
    recommendations = []
    
    # Calculate current readiness metrics
    readiness = calculate_project_readiness(project)
    readiness_score = readiness["project_readiness_score"] * 100.0  # as percentage
    instrument_completion_rate = readiness["instrument_completion_rate"] * 100.0  # as percentage
    
    # Get active instruments list (non-deleted)
    active_instruments = [inst for inst in project.instruments if not inst.deleted_at]
    instruments_dict = {inst.instrument_type: inst for inst in active_instruments}
    
    # Check date utilities
    today = date.today()
    
    # Evaluate rules based on status_type
    if status_type == "program_status":
        if target_status == "Ready":
            # CL missing or not Done
            cl = instruments_dict.get("CL")
            if not cl or cl.status != "Done":
                warnings.append("Contract/Confirmation Letter (CL) is missing or not marked as 'Done'.")
                recommendations.append("Lengkapi dan setujui Contract/Confirmation Letter (CL).")
                
            # ROS missing or not Done
            ros = instruments_dict.get("ROS")
            if not ros or ros.status != "Done":
                warnings.append("Rundown of Show (ROS) is missing or not marked as 'Done'.")
                recommendations.append("Susun dan selesaikan Rundown of Show (ROS).")
                
            # CK missing or not Done
            ck = instruments_dict.get("CK")
            if not ck or ck.status != "Done":
                warnings.append("Check List (CK) is missing or not marked as 'Done'.")
                recommendations.append("Verifikasi kesiapan via Check List (CK).")
                
            # PNL is missing or not Done for Signed & Deal project
            if project.quotation_status == "Signed & Deal":
                pnl = instruments_dict.get("PNL")
                if not pnl or pnl.status != "Done" or not pnl.document_url:
                    warnings.append("Profit & Loss (PNL) instrument is missing or not marked as 'Done' with valid document URL for this Signed & Deal project.")
                    recommendations.append("Unggah draft PNL dan set status menjadi Done.")
            
            # project has instrument Need Revision
            need_revision_list = [inst for inst in active_instruments if inst.status == "Need Revision"]
            if need_revision_list:
                warnings.append(f"Project has {len(need_revision_list)} instrument(s) needing revision.")
                recommendations.append("Revisi instrumen yang memerlukan perbaikan.")
                
            # project has overdue instruments
            overdue_list = [
                inst for inst in active_instruments
                if inst.due_date and inst.due_date < today and inst.status != "Done" and inst.status != "Not Required"
            ]
            if overdue_list:
                warnings.append(f"Project has {len(overdue_list)} overdue instrument(s).")
                recommendations.append("Perbarui tenggat waktu atau selesaikan instrumen yang telat.")
                
            # event_date_start is missing
            if not project.event_date_start:
                warnings.append("Event start date is missing.")
                recommendations.append("Tentukan tanggal mulai event di detail project.")
                
            # PM is missing
            if not project.program_manager_id:
                warnings.append("Program Manager (PM) is not assigned.")
                recommendations.append("Tunjuk PM untuk mengelola eksekusi event.")
                
            # PO is missing
            if not project.program_owner_id:
                warnings.append("Program Owner (PO) is not assigned.")
                recommendations.append("Tunjuk PO untuk kepemilikan program.")
                
        elif target_status == "Running":
            # project_status is Canceled is a critical blocker
            if project.project_status == "Canceled":
                blockers.append("Cannot run an event that is marked as Canceled.")
                recommendations.append("Aktifkan kembali project (ubah project_status dari Canceled) sebelum menjalankan event.")
                
            # readiness_score < 80
            if readiness_score < 80.0:
                warnings.append(f"Project readiness score ({readiness_score:.1f}%) is below the operational threshold of 80%.")
                recommendations.append("Lengkapi checklist operational dan unggah dokumen pendukung untuk meningkatkan score.")
                
            # ROS is not Done
            ros = instruments_dict.get("ROS")
            if not ros or ros.status != "Done":
                warnings.append("Rundown of Show (ROS) is not marked as 'Done'. Running event requires a finalized rundown.")
                recommendations.append("Finalisasi Rundown of Show (ROS).")
                
            # CK is not Done
            ck = instruments_dict.get("CK")
            if not ck or ck.status != "Done":
                warnings.append("Check List (CK) is not marked as 'Done'. Running event requires completed pre-execution checks.")
                recommendations.append("Selesaikan pre-execution checklist.")
                
            # any required instrument is Need Revision
            need_revision_list = [inst for inst in active_instruments if inst.status == "Need Revision"]
            if need_revision_list:
                warnings.append(f"Project has {len(need_revision_list)} instrument(s) marked as 'Need Revision'.")
                recommendations.append("Selesaikan revisi instrumen.")
                
            # event date is missing
            if not project.event_date_start:
                warnings.append("Event start date is missing.")
                recommendations.append("Isi tanggal mulai event.")
            else:
                # event date is in the future by more than 7 days (premature run)
                days_until = (project.event_date_start - today).days
                if days_until > 7:
                    warnings.append(f"Event is scheduled to start in {days_until} days. Running this event now might be premature.")
                    recommendations.append("Verifikasi apakah eksekusi dipercepat.")
                    
        elif target_status == "Completed":
            # documentation is missing
            active_docs = [d for d in project.documents if not d.deleted_at]
            if not active_docs or len(active_docs) == 0:
                warnings.append("No active documents are uploaded. Event completion requires post-event reports/documentation.")
                recommendations.append("Unggah dokumentasi/Laporan Pertanggungjawaban (LPJ).")
                
            # project still has overdue instruments
            overdue_list = [
                inst for inst in active_instruments
                if inst.due_date and inst.due_date < today and inst.status != "Done" and inst.status != "Not Required"
            ]
            if overdue_list:
                warnings.append(f"Project has {len(overdue_list)} overdue instrument(s).")
                recommendations.append("Tandai instrumen yang sudah selesai atau update statusnya.")
                
            # ROS/CK are not Done
            ros = instruments_dict.get("ROS")
            if not ros or ros.status != "Done":
                warnings.append("Rundown of Show (ROS) was not completed.")
            ck = instruments_dict.get("CK")
            if not ck or ck.status != "Done":
                warnings.append("Check List (CK) was not completed.")
                
            # event_date_end is missing
            if not project.event_date_end:
                warnings.append("Event end date is missing.")
                recommendations.append("Isi tanggal berakhir event.")
            elif project.event_date_end > today:
                # event_date_end is in the future
                warnings.append(f"Event end date ({project.event_date_end}) is in the future. Completing the event now is premature.")
                recommendations.append("Tunggu hingga event selesai dijalankan sesuai jadwal.")
                
        elif target_status == "Closed":
            # payment_status is not Paid
            if project.payment_status != "Paid":
                warnings.append("Payment status is not 'Paid'. Closing requires full payment settlement.")
                recommendations.append("Lakukan penagihan invoice atau verifikasi approval pembayaran.")
                
            # documentation is missing
            active_docs = [d for d in project.documents if not d.deleted_at]
            if not active_docs or len(active_docs) == 0:
                warnings.append("No active documents are uploaded.")
                recommendations.append("Unggah LPJ/Dokumentasi penutupan.")
                
            # reporting status is unclear (not Reporting or Completed or Closed)
            if project.program_status not in ["Reporting", "Completed", "Closed"]:
                warnings.append(f"Current program status is '{project.program_status}'. Standard flow requires Completed/Reporting stage before Closing.")
                recommendations.append("Selesaikan tahapan pelaporan (Reporting) sebelum menutup.")
                
            # PNL missing or not Done
            pnl = instruments_dict.get("PNL")
            if not pnl or pnl.status != "Done" or not pnl.document_url:
                warnings.append("PNL document is missing or not marked as 'Done'. Closing requires finalized Profit & Loss statement.")
                recommendations.append("Finalisasi PNL sheet.")
                
    elif status_type == "project_status":
        if target_status == "Closed":
            # payment_status is not Paid
            if project.payment_status != "Paid":
                warnings.append("Payment status is not 'Paid'. Closing requires full payment settlement.")
                recommendations.append("Selesaikan outstanding invoice.")
                
            # program_status is not Completed/Reporting/Closed
            if project.program_status not in ["Completed", "Reporting", "Closed"]:
                warnings.append(f"Program status is '{project.program_status}'. Event execution should be Completed or Reporting before closing.")
                
            # documentation is missing
            active_docs = [d for d in project.documents if not d.deleted_at]
            if not active_docs or len(active_docs) == 0:
                warnings.append("No active operational documents uploaded.")
                
            # PNL is missing or not Done
            pnl = instruments_dict.get("PNL")
            if not pnl or pnl.status != "Done" or not pnl.document_url:
                warnings.append("PNL document is missing or not finalized.")
                
            # project has unresolved Need Revision instruments
            need_revision_list = [inst for inst in active_instruments if inst.status == "Need Revision"]
            if need_revision_list:
                warnings.append(f"Project has {len(need_revision_list)} instrument(s) with 'Need Revision' status.")
                
        elif target_status == "Canceled":
            # cancel_reason is missing
            if not project.cancel_reason or not project.cancel_reason.strip():
                warnings.append("Cancel reason is not provided.")
                recommendations.append("Tuliskan alasan pembatalan pada mom_notes or cancel_reason.")
                
            # project has Signed & Deal quotation
            if project.quotation_status == "Signed & Deal":
                warnings.append("Project has a 'Signed & Deal' quotation. Canceling a signed contract involves high commercial risk.")
                recommendations.append("Koordinasikan dengan manajemen sebelum membatalkan kontrak deal.")
                
            # payment_status is Paid or Partial Paid
            if project.payment_status in ["Paid", "Partial Paid"]:
                warnings.append(f"Project has already received payment (Status: {project.payment_status}). Canceling requires processing refunds/finance review.")
                recommendations.append("Hubungi departemen Finance untuk settlement invoice/refund.")

    # Determine allowed, severity, and can_override
    if blockers:
        allowed = False
        severity = "critical"
        can_override = True
    elif warnings:
        allowed = True
        severity = "warning"
        can_override = True
    else:
        allowed = True
        severity = "info"
        can_override = True
        
    return {
        "allowed": allowed,
        "severity": severity,
        "warnings": warnings,
        "blockers": blockers,
        "recommendations": recommendations,
        "readiness_score": readiness_score,
        "instrument_completion_rate": instrument_completion_rate,
        "can_override": can_override
    }

