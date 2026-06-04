from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.events.models import EventSchedule
from app.modules.events.schemas import EventScheduleCreate, EventScheduleUpdate
from app.core.database import db_commit_safety

def get_event_schedule(db: Session, event_id: str) -> Optional[EventSchedule]:
    return db.query(EventSchedule).filter(EventSchedule.id == event_id, EventSchedule.deleted_at == None).first()

def get_event_schedules_by_project(db: Session, project_id: str) -> List[EventSchedule]:
    return db.query(EventSchedule).filter(EventSchedule.project_id == project_id, EventSchedule.deleted_at == None).all()

def create_event_schedule(db: Session, event_in: EventScheduleCreate) -> EventSchedule:
    # Convert rundown objects to dicts for JSON column saving
    rundown_data = [item.dict() for item in event_in.rundown]
    
    db_event = EventSchedule(
        project_id=event_in.project_id,
        venue_name=event_in.venue_name,
        address=event_in.address,
        map_link=event_in.map_link,
        start_time=event_in.start_time,
        end_time=event_in.end_time,
        rundown=rundown_data,
        pic_id=event_in.pic_id
    )
    db.add(db_event)
    db_commit_safety(db)
    db.refresh(db_event)
    return db_event

def update_event_schedule(db: Session, db_event: EventSchedule, event_in: EventScheduleUpdate) -> EventSchedule:
    event_data = event_in.dict(exclude_unset=True)
    if "rundown" in event_data and event_data["rundown"] is not None:
        event_data["rundown"] = [item.dict() for item in event_data["rundown"]]
        
    for field, value in event_data.items():
        setattr(db_event, field, value)
        
    db_commit_safety(db)
    db.refresh(db_event)
    return db_event

def delete_event_schedule(db: Session, db_event: EventSchedule) -> EventSchedule:
    db_event.soft_delete()
    db_commit_safety(db)
    return db_event
