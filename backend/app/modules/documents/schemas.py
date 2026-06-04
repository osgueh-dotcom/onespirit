from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.projects.schemas import UserBriefResponse

class DocumentBase(BaseModel):
    title: str
    file_path: str
    file_type: str  # pdf, image, link, teaser
    storage_type: str  # local, google_drive
    notes: Optional[str] = None

class DocumentCreate(DocumentBase):
    project_id: UUID

class DocumentResponse(DocumentBase):
    id: UUID
    project_id: UUID
    uploaded_by_id: Optional[UUID] = None
    uploaded_by: Optional[UserBriefResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
