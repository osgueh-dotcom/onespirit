from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import deps
from app.modules.auth.models import User
from app.modules.event_sources import service, schemas

router = APIRouter(prefix="/event-sources", tags=["Event Source Module"])

@router.get("", response_model=List[schemas.EventSourceResponse])
def get_all_event_sources(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Retrieve list of all active event sources"""
    return service.get_event_sources(db, skip=skip, limit=limit)

@router.get("/{source_id}", response_model=schemas.EventSourceResponse)
def get_event_source_by_id(
    source_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:read"]))
):
    """Get detailed attributes of an event source"""
    source = service.get_event_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event source not found"
        )
    return source

@router.post("", response_model=schemas.EventSourceResponse, status_code=status.HTTP_201_CREATED)
def create_event_source_entry(
    source_in: schemas.EventSourceCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Create a new event source"""
    return service.create_event_source(db, source_in=source_in)

@router.put("/{source_id}", response_model=schemas.EventSourceResponse)
def update_event_source_entry(
    source_id: str,
    source_in: schemas.EventSourceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Update event source attributes"""
    source = service.get_event_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event source not found"
        )
    return service.update_event_source(db, db_source=source, source_in=source_in)

@router.delete("/{source_id}", status_code=status.HTTP_200_OK)
def delete_event_source_entry(
    source_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["projects:write"]))
):
    """Archive an event source (Soft delete)"""
    source = service.get_event_source(db, source_id=source_id)
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event source not found"
        )
    service.delete_event_source(db, db_source=source)
    return {"message": "Event source successfully archived."}
