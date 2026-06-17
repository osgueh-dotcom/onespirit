from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.projects.schemas import UserBriefResponse

class RundownItem(BaseModel):
    time: str
    activity: str
    pic: str
    notes: Optional[str] = None

class EventScheduleBase(BaseModel):
    venue_name: str
    address: Optional[str] = None
    map_link: Optional[str] = None
    start_time: datetime
    end_time: datetime
    rundown: List[RundownItem] = []

class EventScheduleCreate(EventScheduleBase):
    project_id: UUID
    pic_id: Optional[UUID] = None

class EventScheduleUpdate(BaseModel):
    venue_name: Optional[str] = None
    address: Optional[str] = None
    map_link: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    rundown: Optional[List[RundownItem]] = None
    pic_id: Optional[UUID] = None

class EventScheduleResponse(EventScheduleBase):
    id: UUID
    project_id: UUID
    pic_id: Optional[UUID] = None
    pic: Optional[UserBriefResponse] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
