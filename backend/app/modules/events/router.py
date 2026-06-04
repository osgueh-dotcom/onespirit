from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.events import service, schemas
from app.modules.projects import service as project_service

router = APIRouter(tags=["Event Management Module"])

@router.get("/projects/{project_id}/events", response_model=List[schemas.EventScheduleResponse])
def get_project_event_schedules(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["events:read"]))
):
    """Retrieve event schedules and venue rundowns assigned to a specific project"""
    project = project_service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_event_schedules_by_project(db, project_id=project_id)

@router.post("/events", response_model=schemas.EventScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_event_schedule_entry(
    event_in: schemas.EventScheduleCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["events:write"]))
):
    """Create a new event schedule rundown and link it to a project"""
    project = project_service.get_project(db, project_id=str(event_in.project_id))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.create_event_schedule(db, event_in=event_in)

@router.get("/events/{event_id}", response_model=schemas.EventScheduleResponse)
def get_event_schedule_by_id(
    event_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["events:read"]))
):
    """Get specific rundown venue details by ID"""
    event = service.get_event_schedule(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event schedule not found"
        )
    return event

@router.put("/events/{event_id}", response_model=schemas.EventScheduleResponse)
def update_event_schedule_entry(
    event_id: str,
    event_in: schemas.EventScheduleUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["events:write"]))
):
    """Modify venue schedule, mapping reference, or rundown timesheet"""
    event = service.get_event_schedule(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event schedule not found"
        )
    return service.update_event_schedule(db, db_event=event, event_in=event_in)

@router.delete("/events/{event_id}", status_code=status.HTTP_200_OK)
def delete_event_schedule_entry(
    event_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["events:write"]))
):
    """Deactivate or remove event schedule (Soft delete)"""
    event = service.get_event_schedule(db, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event schedule not found"
        )
    service.delete_event_schedule(db, db_event=event)
    return {"message": "Event schedule successfully removed."}
