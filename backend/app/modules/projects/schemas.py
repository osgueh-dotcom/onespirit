from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from app.modules.crm.schemas import CustomerResponse
from app.modules.event_sources.schemas import EventSourceResponse

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
    from_status: Optional[str] = None
    to_status: Optional[str] = None
    notes: Optional[str] = None
    changed_by: Optional[UserBriefResponse] = None
    status_type: Optional[str] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    changed_by_user_id: Optional[UUID] = None
    changed_by_user: Optional[UserBriefResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = "inquiry"  # Deprecated
    quotation_status: str = "Draft"
    start_date: Optional[date] = None  # Deprecated
    end_date: Optional[date] = None  # Deprecated
    budget: Decimal = Decimal("0.00")
    revenue: Decimal = Decimal("0.00")

    # New Domain Refactor Fields
    project_code: Optional[str] = None
    inquiry_date: Optional[date] = None
    event_category: Optional[str] = None
    program_type: Optional[str] = None
    program_name: Optional[str] = None
    quantity: Optional[int] = None
    venue: Optional[str] = None
    duration: Optional[str] = None
    event_date_start: Optional[date] = None
    event_date_end: Optional[date] = None
    quotation_date: Optional[date] = None
    quotation_number: Optional[str] = None
    
    program_status: str = "Inquiry"
    payment_status: str = "Not Invoiced"
    project_status: str = "Open"
    
    cancel_reason: Optional[str] = None
    mom_notes: Optional[str] = None
    general_notes: Optional[str] = None

class ProjectCreate(ProjectBase):
    customer_id: UUID
    assigned_to_id: Optional[UUID] = None
    event_source_id: Optional[UUID] = None
    program_owner_id: Optional[UUID] = None
    program_manager_id: Optional[UUID] = None

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

    project_code: Optional[str] = None
    inquiry_date: Optional[date] = None
    event_category: Optional[str] = None
    program_type: Optional[str] = None
    program_name: Optional[str] = None
    quantity: Optional[int] = None
    venue: Optional[str] = None
    duration: Optional[str] = None
    event_date_start: Optional[date] = None
    event_date_end: Optional[date] = None
    quotation_date: Optional[date] = None
    quotation_number: Optional[str] = None
    
    program_status: Optional[str] = None
    payment_status: Optional[str] = None
    project_status: Optional[str] = None
    
    cancel_reason: Optional[str] = None
    mom_notes: Optional[str] = None
    general_notes: Optional[str] = None

    event_source_id: Optional[UUID] = None
    program_owner_id: Optional[UUID] = None
    program_manager_id: Optional[UUID] = None

class ProjectStatusUpdate(BaseModel):
    status_type: str
    new_status: str
    notes: Optional[str] = None
    force: Optional[bool] = False

class ProjectReadinessCheckRequest(BaseModel):
    status_type: str
    target_status: str
    notes: Optional[str] = None

class ProjectReadinessCheckResponse(BaseModel):
    project_id: UUID
    status_type: str
    target_status: str
    allowed: bool
    severity: str # "info" | "warning" | "critical"
    can_override: bool
    readiness_score: float
    instrument_completion_rate: float
    warnings: List[str]
    blockers: List[str]
    recommendations: List[str]


class ProjectDocumentResponse(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    file_path: str
    file_type: str
    storage_type: str
    notes: Optional[str] = None
    document_type: Optional[str] = None
    url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectActivityLogResponse(BaseModel):
    id: UUID
    project_id: UUID
    user_id: Optional[UUID] = None
    user: Optional[UserBriefResponse] = None
    action: str
    field_name: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

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

    event_source_id: Optional[UUID] = None
    event_source: Optional[EventSourceResponse] = None
    program_owner_id: Optional[UUID] = None
    program_owner: Optional[UserBriefResponse] = None
    program_manager_id: Optional[UUID] = None
    program_manager: Optional[UserBriefResponse] = None
    
    paid_amount: Decimal = Decimal("0.00")
    
    project_readiness_score: Optional[float] = 0.0
    instrument_completion_rate: Optional[float] = 0.0

    class Config:
        from_attributes = True

class ProjectInstrumentCreate(BaseModel):
    project_id: UUID
    instrument_type: str
    status: Optional[str] = "Not Started"
    title: Optional[str] = None
    document_url: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None

class ProjectInstrumentUpdate(BaseModel):
    status: Optional[str] = None
    title: Optional[str] = None
    document_url: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None

class ProjectInstrumentRead(BaseModel):
    id: UUID
    project_id: UUID
    instrument_type: str
    status: str
    title: Optional[str] = None
    document_url: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[date] = None
    completed_date: Optional[date] = None
    updated_by_user_id: Optional[UUID] = None
    updated_by_user: Optional[UserBriefResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectDetailResponse(ProjectResponse):
    documents: List[ProjectDocumentResponse] = []
    status_logs: List[ProjectStatusLogResponse] = []
    activity_logs: List[ProjectActivityLogResponse] = []
    validation_warnings: List[str] = []
    instruments: List[ProjectInstrumentRead] = []
    
    # Readiness score & calculations
    required_instruments_count: int = 0
    completed_required_instruments_count: int = 0
    instrument_completion_rate: Optional[float] = 0.0
    missing_required_instruments_count: int = 0
    revision_required_count: int = 0
    overdue_instruments_count: int = 0
    project_readiness_score: Optional[float] = 0.0

