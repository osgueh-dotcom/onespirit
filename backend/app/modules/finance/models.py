from sqlalchemy import Column, ForeignKey, String, Text, Date, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Invoice(Base, BaseModelMixin):
    __tablename__ = "invoices"

    project_id = Column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("Project", back_populates="invoices")

    invoice_number = Column(String(50), unique=True, index=True, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False, default=0.00)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    status = Column(String(50), nullable=False, default="unpaid")  # unpaid, partial, paid, overdue
    notes = Column(Text, nullable=True)

    payments = relationship("Payment", back_populates="invoice", cascade="all, delete-orphan")

class Payment(Base, BaseModelMixin):
    __tablename__ = "payments"

    invoice_id = Column(ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    invoice = relationship("Invoice", back_populates="payments")

    amount = Column(Numeric(15, 2), nullable=False, default=0.00)
    payment_date = Column(Date, nullable=False)
    
    reference_number = Column(String(100), nullable=True)
    proof_url = Column(String(255), nullable=True)  # link to image/pdf upload proof
    
    status = Column(String(50), nullable=False, default="approved")  # pending, approved, rejected
