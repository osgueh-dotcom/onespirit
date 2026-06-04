from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.tasks import service, schemas
from app.modules.projects import service as project_service

router = APIRouter(tags=["Task Management Module"])

@router.get("/projects/{project_id}/tasks", response_model=List[schemas.TaskResponse])
def get_project_tasks(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["tasks:read"]))
):
    """Retrieve the checklist and priority tasks assigned to a specific project"""
    project = project_service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_tasks_by_project(db, project_id=project_id)

@router.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_entry(
    task_in: schemas.TaskCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["tasks:write"]))
):
    """Allocate a brand new task within a project"""
    project = project_service.get_project(db, project_id=str(task_in.project_id))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.create_task(db, task_in=task_in, created_by_id=str(current_user.id))

@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task_by_id(
    task_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["tasks:read"]))
):
    """Get specific task criteria and assignment detail by ID"""
    task = service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task_entry(
    task_id: str,
    task_in: schemas.TaskUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["tasks:write"]))
):
    """Adjust due date, details, assignments, or drag-and-drop status of a task"""
    task = service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return service.update_task(db, db_task=task, task_in=task_in)

@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_entry(
    task_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["tasks:write"]))
):
    """Deactivate or remove a task (Soft delete)"""
    task = service.get_task(db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    service.delete_task(db, db_task=task)
    return {"message": "Task successfully archived."}
