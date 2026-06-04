from typing import List, Optional
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
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Retrieve the list of active projects, optionally filtered by status"""
    return service.get_projects(db, status=status, skip=skip, limit=limit)

@router.get("/projects/{project_id}", response_model=schemas.ProjectResponse)
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
    
    valid_statuses = ["inquiry", "quotation", "negotiation", "confirmed", "preparation", "ongoing", "completed", "canceled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status selection. Must be one of {valid_statuses}"
        )
        
    # Standardized business approval role matrix check
    user_role = current_user.role.name
    
    # 1. Canceled status requires administrative or director scope
    if new_status == "canceled" and user_role not in ["Super Admin", "Director", "Sales"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Directors, Sales, or Administrators can cancel active event projects."
        )

    # 2. Confirmed or Completed status requires PM, Sales, Director, or Admin scope
    if new_status in ["confirmed", "completed"] and user_role not in ["Super Admin", "Director", "Project Manager", "Sales"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Directors, PMs, Sales, or Administrators can confirm or complete active event projects."
        )

    # 3. Completed status requires all associated operations checklist tasks to be finished (done)
    if new_status == "completed":
        from app.modules.tasks.models import Task
        uncompleted_tasks_count = db.query(Task).filter(
            Task.project_id == project.id,
            Task.status != "done",
            Task.deleted_at == None
        ).count()
        
        if uncompleted_tasks_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition to 'completed' status. There are {uncompleted_tasks_count} uncompleted operational checklist tasks remaining."
            )
        
    return service.transition_project_status(
        db, 
        db_project=project, 
        new_status=new_status, 
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
