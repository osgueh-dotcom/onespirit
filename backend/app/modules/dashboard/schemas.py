from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import date

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
    revenue_received: float
    collection_rate: float
    outstanding_amount: float
    revenue_conversion_rate: float
    average_project_value: float
    total_data_quality_issues: int


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
    # Sprint 8 operational readiness fields
    upcoming_projects_7_days: int = 0
    projects_not_ready: int = 0
    average_readiness_score: float = 0.0
    overdue_instruments_count: int = 0
    need_revision_count: int = 0

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

class InstrumentSummarySchema(BaseModel):
    missing_cl: int
    missing_ros: int
    missing_ck: int
    missing_pnl: int
    instruments_need_revision: int
    instruments_overdue: int
    average_instrument_completion_rate: float

class ReadinessSummarySchema(BaseModel):
    projects_ready_count: int
    projects_not_ready_count: int
    average_readiness_score: float
    upcoming_events_7_days: int
    overdue_events: int
    events_missing_readiness_items: int
    total_overdue_instruments: int
    total_need_revision_instruments: int

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
    instrument_summary: InstrumentSummarySchema
    readiness_summary: ReadinessSummarySchema

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class PMControlCenterSummary(BaseModel):
    total_active_projects: int
    events_today: int
    upcoming_events_7_days: int
    overdue_events: int
    not_ready_projects: int
    overdue_instruments: int
    need_revision_instruments: int
    average_readiness_score: float

    class Config:
        from_attributes = True


class PMControlCenterUpcomingEvent(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    program_name: Optional[str] = None
    event_date_start: Optional[date] = None
    event_date_end: Optional[date] = None
    days_until_event: Optional[int] = None
    po_name: Optional[str] = None
    pm_name: Optional[str] = None
    program_status: str
    project_status: str
    readiness_score: float
    instrument_completion_rate: float
    priority_level: str
    recommended_action: str

    class Config:
        from_attributes = True


class PMControlCenterNotReadyProject(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    event_date_start: Optional[date] = None
    pm_name: Optional[str] = None
    readiness_score: float
    missing_items: List[str]
    recommended_action: str

    class Config:
        from_attributes = True


class PMControlCenterOverdueInstrument(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    instrument_type: str
    instrument_label: Optional[str] = None
    status: str
    due_date: Optional[date] = None
    days_overdue: int
    pm_name: Optional[str] = None
    recommended_action: str

    class Config:
        from_attributes = True


class PMControlCenterNeedRevisionInstrument(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    instrument_type: str
    notes: Optional[str] = None
    pm_name: Optional[str] = None
    recommended_action: str

    class Config:
        from_attributes = True


class PMControlCenterPMWorkload(BaseModel):
    pm_id: UUID
    pm_name: str
    initial_code: Optional[str] = None
    total_projects: int
    upcoming_events_7_days: int
    not_ready_projects: int
    overdue_instruments: int
    need_revision_instruments: int
    average_readiness_score: float

    class Config:
        from_attributes = True


class PMControlCenterPriorityAction(BaseModel):
    priority_level: str
    project_id: UUID
    project_code: Optional[str] = None
    title: str
    description: str
    recommended_action: str
    reason: str

    class Config:
        from_attributes = True


class PMControlCenterResponse(BaseModel):
    summary: PMControlCenterSummary
    upcoming_events: List[PMControlCenterUpcomingEvent]
    not_ready_projects: List[PMControlCenterNotReadyProject]
    overdue_instruments: List[PMControlCenterOverdueInstrument]
    need_revision_instruments: List[PMControlCenterNeedRevisionInstrument]
    pm_workload: List[PMControlCenterPMWorkload]
    priority_actions: List[PMControlCenterPriorityAction]

    class Config:
        from_attributes = True


class POControlCenterSummary(BaseModel):
    total_owned_projects: int
    total_deal: int
    total_cancel: int
    deal_rate: float
    cancel_rate: float
    potential_revenue: float
    confirmed_revenue: float
    average_project_value: float
    outstanding_count: int
    invoice_sent_count: int
    paid_count: int
    follow_up_needed_count: int
    active_projects: int
    pending_quotation_projects: int
    follow_up_needed_projects: int
    cancelled_projects: int
    outstanding_payment: float
    commercial_risk_count: int

    class Config:
        from_attributes = True


class POControlCenterQuotationSummary(BaseModel):
    count_by_status: Dict[str, int]
    draft_count: int
    sent_count: int
    follow_up_count: int
    revision_count: int
    signed_deal_count: int
    cancel_count: int

    class Config:
        from_attributes = True


class POControlCenterRevenueSummary(BaseModel):
    potential_revenue: float
    confirmed_revenue: float
    revenue_conversion_rate: float
    average_project_value: float
    highest_project_value: float
    lowest_project_value: float

    class Config:
        from_attributes = True


class POControlCenterFollowUpPriority(BaseModel):
    priority_level: str
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    program_name: Optional[str] = None
    po_name: Optional[str] = None
    pm_name: Optional[str] = None
    quotation_status: str
    program_status: str
    payment_status: str
    budget: float
    event_date_start: Optional[date] = None
    reason: str
    recommended_action: str

    class Config:
        from_attributes = True


class POControlCenterOwnedProject(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    source_type: Optional[str] = None
    vendor_name: Optional[str] = None
    sales_name: Optional[str] = None
    po_name: Optional[str] = None
    pm_name: Optional[str] = None
    quotation_status: str
    program_status: str
    payment_status: str
    project_status: str
    budget: float
    event_date_start: Optional[date] = None
    follow_up_status: Optional[str] = None
    recommended_action: str

    class Config:
        from_attributes = True


class POControlCenterPOPerformance(BaseModel):
    po_id: UUID
    po_name: str
    initial_code: Optional[str] = None
    total_projects: int
    deal_count: int
    cancel_count: int
    deal_rate: float
    confirmed_revenue: float
    potential_revenue: float
    average_project_value: float
    outstanding_count: int
    follow_up_needed_count: int

    class Config:
        from_attributes = True


class POControlCenterSourceContribution(BaseModel):
    source_type: str
    vendor_name: Optional[str] = None
    sales_name: Optional[str] = None
    total_projects: int
    deal_count: int
    cancel_count: int
    confirmed_revenue: float
    potential_revenue: float
    average_project_value: float

    class Config:
        from_attributes = True


class POControlCenterRiskProject(BaseModel):
    project_id: UUID
    project_code: Optional[str] = None
    customer_name: Optional[str] = None
    program_name: Optional[str] = None
    budget: float
    quotation_status: str
    program_status: str
    payment_status: str
    po_name: Optional[str] = None
    pm_name: Optional[str] = None
    reason: Optional[str] = None

    class Config:
        from_attributes = True


class POControlCenterCommercialRisks(BaseModel):
    cancel_without_reason: List[POControlCenterRiskProject]
    signed_deal_without_budget: List[POControlCenterRiskProject]
    outstanding_payment: List[POControlCenterRiskProject]
    invoice_sent_not_paid: List[POControlCenterRiskProject]
    missing_po: List[POControlCenterRiskProject]
    missing_source: List[POControlCenterRiskProject]

    class Config:
        from_attributes = True


class POControlCenterResponse(BaseModel):
    summary: POControlCenterSummary
    quotation_summary: POControlCenterQuotationSummary
    revenue_summary: POControlCenterRevenueSummary
    follow_up_priorities: List[POControlCenterFollowUpPriority]
    owned_projects: List[POControlCenterOwnedProject]
    po_performance: List[POControlCenterPOPerformance]
    source_contribution: List[POControlCenterSourceContribution]
    commercial_risks: POControlCenterCommercialRisks

    class Config:
        from_attributes = True

