from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.projects.models import Project, ProjectStatusLog
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
    limit: int = 100
) -> List[Project]:
    query = db.query(Project).filter(Project.deleted_at == None)
    if status:
        query = query.filter(Project.status == status)
    return query.offset(skip).limit(limit).all()

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

    db_project = Project(
        title=project_in.title,
        status=project_in.status,
        quotation_status=project_in.quotation_status,
        start_date=project_in.start_date,
        end_date=project_in.end_date,
        budget=project_in.budget,
        revenue=project_in.revenue,
        customer_id=project_in.customer_id,
        created_by_id=parsed_creator_id,
        assigned_to_id=project_in.assigned_to_id
    )
    db.add(db_project)
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Create initial transition log
    log = ProjectStatusLog(
        project_id=db_project.id,
        from_status="none",
        to_status=db_project.status,
        notes="Project created",
        changed_by_id=parsed_creator_id
    )
    db.add(log)
    db_commit_safety(db)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=parsed_creator_id, 
        action="project_created", 
        entity_type="project", 
        entity_id=db_project.id, 
        details={"title": db_project.title, "status": db_project.status}
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

    # Track status change
    old_status = db_project.status
    new_status = project_data.get("status", old_status)
    
    for field, value in project_data.items():
        setattr(db_project, field, value)
    
    db_commit_safety(db)
    db.refresh(db_project)
    
    # Log transition if changed
    if old_status != new_status:
        log = ProjectStatusLog(
            project_id=db_project.id,
            from_status=old_status,
            to_status=new_status,
            notes="Project details updated",
            changed_by_id=parsed_changer_id
        )
        db.add(log)
        db_commit_safety(db)
        
        # Central activity logging for status change
        log_activity(
            db, 
            user_id=parsed_changer_id, 
            action="status_transitioned", 
            entity_type="project", 
            entity_id=db_project.id, 
            details={"title": db_project.title, "old_status": old_status, "new_status": new_status, "source": "project_update"}
        )
        
    return db_project

def transition_project_status(
    db: Session, 
    db_project: Project, 
    new_status: str, 
    notes: Optional[str], 
    changed_by_id: str
) -> Project:
    old_status = db_project.status
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

    db_project.status = new_status
    db_commit_safety(db)
    
    # Log transition
    log = ProjectStatusLog(
        project_id=db_project.id,
        from_status=old_status,
        to_status=new_status,
        notes=notes or f"Status shifted from {old_status} to {new_status}",
        changed_by_id=parsed_changer_id
    )
    db.add(log)
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

def get_project_logs(db: Session, project_id: str) -> List[ProjectStatusLog]:
    parsed_id = project_id
    if isinstance(project_id, str):
        try:
            parsed_id = uuid.UUID(project_id)
        except ValueError:
            pass
    return db.query(ProjectStatusLog).filter(ProjectStatusLog.project_id == parsed_id).order_by(ProjectStatusLog.created_at.desc()).all()
