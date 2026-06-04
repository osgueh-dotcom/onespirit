from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr

# Contact schemas
class ContactBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None

class ContactCreate(ContactBase):
    customer_id: UUID

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    customer_id: Optional[UUID] = None

class ContactResponse(ContactBase):
    id: UUID
    customer_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Customer schemas
class CustomerBase(BaseModel):
    company_name: str
    category: str  # Corporate, Agency, Partner, etc.
    address: Optional[str] = None
    notes: Optional[str] = None
    normalized_name: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    company_name: Optional[str] = None
    category: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    normalized_name: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: UUID
    contacts: List[ContactResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
