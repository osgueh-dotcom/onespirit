from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import db_commit_safety
from app.modules.event_sources.models import EventSource
from app.modules.event_sources.schemas import EventSourceCreate, EventSourceUpdate
import uuid

def get_event_source(db: Session, source_id: str) -> Optional[EventSource]:
    parsed_id = source_id
    if isinstance(source_id, str):
        try:
            parsed_id = uuid.UUID(source_id)
        except ValueError:
            pass
    return db.query(EventSource).filter(EventSource.id == parsed_id, EventSource.deleted_at == None).first()

def get_event_sources(db: Session, skip: int = 0, limit: int = 100) -> List[EventSource]:
    return db.query(EventSource).filter(EventSource.deleted_at == None).offset(skip).limit(limit).all()

def create_event_source(db: Session, source_in: EventSourceCreate) -> EventSource:
    db_source = EventSource(
        source_type=source_in.source_type,
        vendor_name=source_in.vendor_name,
        sales_name=source_in.sales_name,
        contact=source_in.contact,
        notes=source_in.notes,
        is_active=source_in.is_active
    )
    db.add(db_source)
    db_commit_safety(db)
    db.refresh(db_source)
    return db_source

def update_event_source(db: Session, db_source: EventSource, source_in: EventSourceUpdate) -> EventSource:
    source_data = source_in.dict(exclude_unset=True)
    for field, value in source_data.items():
        setattr(db_source, field, value)
    db_commit_safety(db)
    db.refresh(db_source)
    return db_source

def delete_event_source(db: Session, db_source: EventSource) -> EventSource:
    db_source.soft_delete()
    db_commit_safety(db)
    return db_source
