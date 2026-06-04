from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.projects.models import Project, ProjectStatusLog, ProjectActivityLog
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate
from app.core.activity import log_activity
from app.core.database import db_commit_safety

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
        
    return warnings

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

    proj_title = project_in.title or project_in.program_name or "Untitled Program"

    db_project = Project(
        title=proj_title,
        status=project_in.status,
        quotation_status=project_in.quotation_status,
        start_date=project_in.start_date or project_in.event_date_start,
        end_date=project_in.end_date or project_in.event_date_end,
        budget=project_in.budget,
        revenue=project_in.revenue,
        customer_id=project_in.customer_id,
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
    db_commit_safety(db)
    
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
    project_data = project_in.dict(exclude_unset=True)
    
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
