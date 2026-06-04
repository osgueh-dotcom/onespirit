from sqlalchemy import Column, ForeignKey, String, Text, Date, Numeric, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Project(Base, BaseModelMixin):
    __tablename__ = "projects"

    title = Column(String(150), nullable=False)
    status = Column(String(50), nullable=False, default="inquiry")  # inquiry, quotation, negotiation, confirmed, ongoing, completed, canceled
    quotation_status = Column(String(50), nullable=False, default="draft")  # draft, sent, approved, rejected
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    budget = Column(Numeric(15, 2), nullable=False, default=0.00)
    revenue = Column(Numeric(15, 2), nullable=False, default=0.00)

    customer_id = Column(ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False)
    customer = relationship("Customer", back_populates="projects")

    created_by_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_by = relationship("User", foreign_keys=[created_by_id])

    assigned_to_id = Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])

    status_logs = relationship("ProjectStatusLog", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="project", cascade="all, delete-orphan")
    event_schedules = relationship("EventSchedule", back_populates="project", cascade="all, delete-orphan")

class ProjectStatusLog(Base, BaseModelMixin):
    __tablename__ = "project_status_logs"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="status_logs")

    from_status = Column(String(50), nullable=False)
    to_status = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)

    changed_by_id = Column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    changed_by = relationship("User")
