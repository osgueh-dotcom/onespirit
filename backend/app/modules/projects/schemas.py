from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.crm.schemas import CustomerResponse

# Simple user response to avoid circular references
class UserBriefResponse(BaseModel):
    id: UUID
    full_name: str
    email: str

    class Config:
        from_attributes = True

# Status Log Schemas
class ProjectStatusLogResponse(BaseModel):
    id: UUID
    project_id: UUID
    from_status: str
    to_status: str
    notes: Optional[str] = None
    changed_by: UserBriefResponse
    created_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    status: str = "inquiry"
    quotation_status: str = "draft"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Decimal = Decimal("0.00")
    revenue: Decimal = Decimal("0.00")

class ProjectCreate(ProjectBase):
    customer_id: UUID
    assigned_to_id: Optional[UUID] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    quotation_status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[Decimal] = None
    revenue: Optional[Decimal] = None
    customer_id: Optional[UUID] = None
    assigned_to_id: Optional[UUID] = None

class ProjectResponse(ProjectBase):
    id: UUID
    customer_id: UUID
    customer: CustomerResponse
    created_by_id: UUID
    created_by: UserBriefResponse
    assigned_to_id: Optional[UUID] = None
    assigned_to: Optional[UserBriefResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
