from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.projects import service, schemas

router = APIRouter(tags=["Project Workflow Module"])

@router.get("/projects", response_model=List[schemas.ProjectResponse])
def get_all_projects(
    db: Session = Depends(deps.get_db),
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    po_id: Optional[UUID] = None,
    pm_id: Optional[UUID] = None,
    source_id: Optional[UUID] = None,
    quotation_status: Optional[str] = None,
    program_status: Optional[str] = None,
    payment_status: Optional[str] = None,
    project_status: Optional[str] = None,
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Retrieve the list of active projects, optionally filtered by various attributes"""
    return service.get_projects(
        db, 
        status=status, 
        skip=skip, 
        limit=limit,
        po_id=po_id,
        pm_id=pm_id,
        source_id=source_id,
        quotation_status=quotation_status,
        program_status=program_status,
        payment_status=payment_status,
        project_status=project_status
    )

@router.get("/projects/{project_id}", response_model=schemas.ProjectDetailResponse)
def get_project_by_id(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Get project details by ID"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    project.validation_warnings = service.check_project_validation_warnings(project)
    return project

@router.post("/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_entry(
    project_in: schemas.ProjectCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Initialize a brand new event project"""
    return service.create_project(db, project_in=project_in, created_by_id=str(current_user.id))

@router.put("/projects/{project_id}", response_model=schemas.ProjectResponse)
def update_project_entry(
    project_id: str,
    project_in: schemas.ProjectUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Update detailed attributes of an event project"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.update_project(db, db_project=project, project_in=project_in, changed_by_id=str(current_user.id))

@router.post("/projects/{project_id}/transition", response_model=schemas.ProjectResponse)
def transition_project_workflow(
    project_id: str,
    new_status: str,
    notes: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Transition a project's operational status and record transition history with strict approval gates"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Map input status to the new Program Status taxonomy case-insensitively
    valid_statuses_map = {
        "inquiry": "Inquiry", "confirmed": "Confirmed", "preparation": "Preparation",
        "ready": "Ready", "running": "Running", "completed": "Completed",
        "reporting": "Reporting", "closed": "Closed", "cancel": "Cancel",
        "canceled": "Cancel", "negotiation": "Inquiry"
    }
    normalized_status = valid_statuses_map.get(new_status.lower(), new_status)
    
    valid_statuses = ["Inquiry", "Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed", "Cancel"]
    if normalized_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status selection. Must be one of {valid_statuses}"
        )
        
    # Standardized business approval role matrix check
    user_role = current_user.role.name
    
    # 1. Cancel status requires administrative or management scope
    if normalized_status == "Cancel" and user_role not in ["Super Admin", "Management", "Director"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Directors, Management, or Administrators can cancel active event projects."
        )

    # 2. Confirmed or Completed status requires PM, Staff, Management, or Admin scope
    is_pm_assigned = project.program_manager_id == current_user.id
    if normalized_status in ["Confirmed", "Completed"] and not (is_pm_assigned or user_role in ["Super Admin", "Management", "Director", "Staff"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Management, Staff, the assigned Program Manager, or Administrators can confirm or complete active event projects."
        )

    # 3. Completed status requires all associated operations checklist tasks to be finished (done)
    if normalized_status == "Completed":
        from app.modules.tasks.models import Task
        uncompleted_tasks_count = db.query(Task).filter(
            Task.project_id == project.id,
            Task.status != "done",
            Task.deleted_at == None
        ).count()
        
        if uncompleted_tasks_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition to 'Completed' status. There are {uncompleted_tasks_count} uncompleted operational checklist tasks remaining."
            )
        
    return service.transition_project_status(
        db, 
        db_project=project, 
        new_status=normalized_status, 
        notes=notes, 
        changed_by_id=str(current_user.id)
    )

@router.get("/projects/{project_id}/logs", response_model=List[schemas.ProjectStatusLogResponse])
def get_project_status_logs(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Fetch status logs and audit trails of project state shifts"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_project_logs(db, project_id=project_id)

@router.patch("/projects/{project_id}/status", response_model=schemas.ProjectResponse)
def patch_project_status(
    project_id: str,
    payload: schemas.ProjectStatusUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Generic status update endpoint to shift quotation, program, payment, or project status"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Gate validation for generic endpoint
    user_role = current_user.role.name
    if payload.status_type == "program_status":
        valid_statuses = ["Inquiry", "Confirmed", "Preparation", "Ready", "Running", "Completed", "Reporting", "Closed", "Cancel"]
        if payload.new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid program status selection. Must be one of {valid_statuses}"
            )
        if payload.new_status == "Cancel" and user_role not in ["Super Admin", "Management", "Director"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Directors, Management, or Administrators can cancel active event projects."
            )
        is_pm_assigned = project.program_manager_id == current_user.id
        if payload.new_status in ["Confirmed", "Completed"] and not (is_pm_assigned or user_role in ["Super Admin", "Management", "Director", "Staff"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only Management, Staff, the assigned Program Manager, or Administrators can confirm or complete active event projects."
            )

    try:
        return service.update_project_status_generic(
            db,
            db_project=project,
            status_type=payload.status_type,
            new_status=payload.new_status,
            notes=payload.notes,
            changed_by_id=str(current_user.id)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
def delete_project_entry(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Remove a project from active logs (Soft delete)"""
    project = service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    service.delete_project(db, db_project=project)
    return {"message": "Project successfully archived."}
