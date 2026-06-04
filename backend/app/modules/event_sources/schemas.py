from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class EventSourceBase(BaseModel):
    source_type: str
    vendor_name: Optional[str] = None
    sales_name: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True

class EventSourceCreate(EventSourceBase):
    pass

class EventSourceUpdate(BaseModel):
    source_type: Optional[str] = None
    vendor_name: Optional[str] = None
    sales_name: Optional[str] = None
    contact: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class EventSourceResponse(EventSourceBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
