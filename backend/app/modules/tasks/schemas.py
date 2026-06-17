from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.modules.projects.schemas import UserBriefResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = "todo"
    priority: str = "medium"

class TaskCreate(TaskBase):
    project_id: UUID
    assigned_to_id: Optional[UUID] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[UUID] = None

class TaskResponse(TaskBase):
    id: UUID
    project_id: UUID
    assigned_to_id: Optional[UUID] = None
    assigned_to: Optional[UserBriefResponse] = None
    created_by_id: UUID
    created_by: UserBriefResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
