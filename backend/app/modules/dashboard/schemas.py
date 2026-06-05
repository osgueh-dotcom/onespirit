from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

class ExecutiveSummarySchema(BaseModel):
    total_projects: int
    total_inquiry: int
    inquiry_stage_count: int
    total_deal: int
    total_cancel: int
    deal_rate: float
    cancel_rate: float
    potential_revenue: float
    confirmed_revenue: float
    revenue_conversion_rate: float
    average_project_value: float

class QuotationSummarySchema(BaseModel):
    count_by_status: Dict[str, int]
    deal_count: int
    cancel_count: int

class ProgramSummarySchema(BaseModel):
    count_by_status: Dict[str, int]

class PaymentSummarySchema(BaseModel):
    count_by_status: Dict[str, int]
    paid_count: int
    outstanding_count: int
    invoice_sent_count: int
    not_invoiced_count: int

class ProjectSummarySchema(BaseModel):
    count_by_status: Dict[str, int]
    closed_count: int
    reporting_count: int
    active_count: int

class POPerformanceSchema(BaseModel):
    po_id: UUID
    po_name: str
    initial_code: Optional[str] = None
    total_projects: int
    deal_count: int
    cancel_count: int
    confirmed_revenue: float
    average_budget: float
    closed_count: int

class PMWorkloadSchema(BaseModel):
    pm_id: UUID
    pm_name: str
    initial_code: Optional[str] = None
    total_projects: int
    active_count: int
    preparation_count: int
    running_count: int
    reporting_count: int
    closed_count: int

class SourceAnalyticsSchema(BaseModel):
    source_type: str
    total_projects: int
    confirmed_revenue: float
    potential_revenue: float
    deal_count: int
    cancel_count: int

class CustomerAnalyticsSchema(BaseModel):
    customer_category: str
    total_projects: int
    confirmed_revenue: float
    deal_count: int
    cancel_count: int

class EventCategoryAnalyticsSchema(BaseModel):
    event_category: str
    total_projects: int
    confirmed_revenue: float

class ProgramTypeAnalyticsSchema(BaseModel):
    program_type: str
    total_projects: int
    confirmed_revenue: float

class DataQualitySchema(BaseModel):
    missing_po: int
    missing_pm: int
    missing_customer: int
    missing_budget: int
    cancel_without_reason: int
    closed_not_paid: int
    documentation_missing: int
    unknown_source: int

class TargetSummarySchema(BaseModel):
    year: int
    revenue_target: float
    achievement_rate: float

class DashboardAnalyticsResponse(BaseModel):
    executive: ExecutiveSummarySchema
    target: TargetSummarySchema
    quotation: QuotationSummarySchema
    program: ProgramSummarySchema
    payment: PaymentSummarySchema
    project: ProjectSummarySchema
    po_performance: List[POPerformanceSchema]
    pm_workload: List[PMWorkloadSchema]
    source_analytics: List[SourceAnalyticsSchema]
    customer_analytics: List[CustomerAnalyticsSchema]
    event_category_analytics: List[EventCategoryAnalyticsSchema]
    program_type_analytics: List[ProgramTypeAnalyticsSchema]
    data_quality: DataQualitySchema

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
