from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

# Payment Schemas
class PaymentBase(BaseModel):
    amount: Decimal
    payment_date: date
    reference_number: Optional[str] = None
    proof_url: Optional[str] = None
    status: str = "approved"  # pending, approved, rejected

class PaymentCreate(PaymentBase):
    invoice_id: UUID

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = None
    payment_date: Optional[date] = None
    reference_number: Optional[str] = None
    proof_url: Optional[str] = None
    status: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: UUID
    invoice_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Invoice Schemas
class InvoiceBase(BaseModel):
    invoice_number: str
    amount: Decimal
    issue_date: date
    due_date: date
    status: str = "unpaid"  # unpaid, partial, paid, overdue
    notes: Optional[str] = None

class InvoiceCreate(InvoiceBase):
    project_id: UUID

class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str] = None
    amount: Optional[Decimal] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class InvoiceResponse(InvoiceBase):
    id: UUID
    project_id: UUID
    payments: List[PaymentResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
