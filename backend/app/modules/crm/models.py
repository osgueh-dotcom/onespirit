from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Customer(Base, BaseModelMixin):
    __tablename__ = "customers"

    company_name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(50), nullable=False)  # Corporate, Agency, Partner, etc.
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    contacts = relationship("Contact", back_populates="customer", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="customer")

class Contact(Base, BaseModelMixin):
    __tablename__ = "contacts"

    customer_id = Column(ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    position = Column(String(100), nullable=True)  # Marketing Manager, Event Coordinator, etc.

    customer = relationship("Customer", back_populates="contacts")
