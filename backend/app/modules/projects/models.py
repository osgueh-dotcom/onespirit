from sqlalchemy import Column, ForeignKey, String, Text, Date, Numeric, DateTime, Integer
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Project(Base, BaseModelMixin):
    __tablename__ = "projects"

    title = Column(String(150), nullable=True)
    status = Column(String(50), nullable=True, default="inquiry")  # Deprecated in favor of program_status/project_status
    start_date = Column(Date, nullable=True)  # Deprecated in favor of event_date_start
    end_date = Column(Date, nullable=True)  # Deprecated in favor of event_date_end
    budget = Column(Numeric(15, 2), nullable=False, default=0.00)
    revenue = Column(Numeric(15, 2), nullable=False, default=0.00)

    # New Domain Refactor Fields
    project_code = Column(String(50), nullable=True)
    inquiry_date = Column(Date, nullable=True)
    event_category = Column(String(100), nullable=True)
    program_type = Column(String(100), nullable=True)
    program_name = Column(String(150), nullable=True)
    quantity = Column(Integer, nullable=True)
    venue = Column(String(150), nullable=True)
    duration = Column(String(50), nullable=True)
    event_date_start = Column(Date, nullable=True)
    event_date_end = Column(Date, nullable=True)
    quotation_date = Column(Date, nullable=True)
    quotation_number = Column(String(100), nullable=True)
    
    quotation_status = Column(String(50), nullable=False, default="Draft")  # Draft, Sent, Follow Up, Revision, Signed & Deal, Cancel
    program_status = Column(String(50), nullable=False, default="Inquiry")  # Inquiry, Confirmed, Preparation, Ready, Running, Completed, Reporting, Closed, Cancel
    payment_status = Column(String(50), nullable=False, default="Not Invoiced")  # Not Invoiced, Invoice Sent, Partial Paid, Paid, Outstanding, Overdue
    project_status = Column(String(50), nullable=False, default="Open")  # Open, Active, Reporting, Closed, Canceled
    
    cancel_reason = Column(Text, nullable=True)
    mom_notes = Column(Text, nullable=True)
    general_notes = Column(Text, nullable=True)

    customer_id = Column(ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False)
    customer = relationship("Customer", back_populates="projects")

    created_by_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])

    assigned_to_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])

    # Assignable relationships for PO, PM, and EventSource
    event_source_id = Column(ForeignKey("event_sources.id", ondelete="SET NULL"), nullable=True)
    event_source = relationship("EventSource")

    program_owner_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    program_owner = relationship("User", foreign_keys=[program_owner_id])

    program_manager_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    program_manager = relationship("User", foreign_keys=[program_manager_id])

    status_logs = relationship("ProjectStatusLog", back_populates="project", cascade="all, delete-orphan")
    activity_logs = relationship("ProjectActivityLog", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    event_schedules = relationship("EventSchedule", back_populates="project", cascade="all, delete-orphan")

    @property
    def paid_amount(self) -> float:
        total = 0.0
        for inv in self.invoices:
            for pay in inv.payments:
                if pay.status == "approved":
                    total += float(pay.amount)
        return total

class ProjectStatusLog(Base, BaseModelMixin):
    __tablename__ = "project_status_logs"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="status_logs")

    # Keep legacy fields for backward compatibility
    from_status = Column(String(50), nullable=True)
    to_status = Column(String(50), nullable=True)
    changed_by_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    changed_by = relationship("User", foreign_keys=[changed_by_id])

    # New detailed fields for status timeline
    status_type = Column(String(50), nullable=True)  # quotation_status, program_status, payment_status, project_status
    old_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=True)
    changed_by_user_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    changed_by_user = relationship("User", foreign_keys=[changed_by_user_id])
    
    notes = Column(Text, nullable=True)

class ProjectActivityLog(Base, BaseModelMixin):
    __tablename__ = "project_activity_logs"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="activity_logs")

    user_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user = relationship("User")

    action = Column(String(50), nullable=False)  # project_created, pm_changed, etc.
    field_name = Column(String(50), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
