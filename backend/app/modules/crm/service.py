import re
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.crm.models import Customer, Contact
from app.modules.crm.schemas import CustomerCreate, CustomerUpdate, ContactCreate, ContactUpdate
from app.core.activity import log_activity
from app.core.database import db_commit_safety

def normalize_customer_name(name: str) -> str:
    if not name:
        return ""
    # 1. Lowercase and trim spaces
    cleaned = name.strip().lower()
    # 2. Remove punctuation
    cleaned = re.sub(r'[^\w\s]', '', cleaned)
    # 3. Collapse multiple spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def check_duplicate_customer(db: Session, company_name: str, exclude_id: Optional[str] = None) -> List[Customer]:
    normalized = normalize_customer_name(company_name)
    if not normalized:
        return []
    query = db.query(Customer).filter(Customer.normalized_name == normalized, Customer.deleted_at == None)
    if exclude_id:
        query = query.filter(Customer.id != exclude_id)
    return query.all()

# Customer CRUD
def get_customer(db: Session, customer_id: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id, Customer.deleted_at == None).first()

def get_customer_by_name(db: Session, company_name: str) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.company_name == company_name, Customer.deleted_at == None).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    return db.query(Customer).filter(Customer.deleted_at == None).offset(skip).limit(limit).all()

def create_customer(db: Session, customer_in: CustomerCreate, user_id: Optional[str] = None) -> Customer:
    db_customer = Customer(
        company_name=customer_in.company_name,
        normalized_name=normalize_customer_name(customer_in.company_name),
        category=customer_in.category,
        address=customer_in.address,
        notes=customer_in.notes
    )
    db.add(db_customer)
    db_commit_safety(db)
    db.refresh(db_customer)
    
    log_activity(
        db,
        user_id=user_id,
        action="customer_created",
        entity_type="customer",
        entity_id=db_customer.id,
        details={"company_name": db_customer.company_name, "category": db_customer.category}
    )
    
    return db_customer

def update_customer(db: Session, db_customer: Customer, customer_in: CustomerUpdate) -> Customer:
    customer_data = customer_in.dict(exclude_unset=True)
    for field, value in customer_data.items():
        setattr(db_customer, field, value)
    if "company_name" in customer_data:
        db_customer.normalized_name = normalize_customer_name(db_customer.company_name)
    db_commit_safety(db)
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, db_customer: Customer) -> Customer:
    db_customer.soft_delete()
    # Soft delete related contacts as well
    for contact in db_customer.contacts:
        contact.soft_delete()
    db_commit_safety(db)
    return db_customer


# Contact CRUD
def get_contact(db: Session, contact_id: str) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id, Contact.deleted_at == None).first()

def get_contacts_by_customer(db: Session, customer_id: str) -> List[Contact]:
    return db.query(Contact).filter(Contact.customer_id == customer_id, Contact.deleted_at == None).all()

def create_contact(db: Session, contact_in: ContactCreate, user_id: Optional[str] = None) -> Contact:
    db_contact = Contact(
        customer_id=contact_in.customer_id,
        name=contact_in.name,
        email=contact_in.email,
        phone=contact_in.phone,
        position=contact_in.position
    )
    db.add(db_contact)
    db_commit_safety(db)
    db.refresh(db_contact)
    
    log_activity(
        db,
        user_id=user_id,
        action="contact_linked",
        entity_type="customer",
        entity_id=db_contact.customer_id,
        details={"name": db_contact.name, "position": db_contact.position}
    )
    
    return db_contact

def update_contact(db: Session, db_contact: Contact, contact_in: ContactUpdate) -> Contact:
    contact_data = contact_in.dict(exclude_unset=True)
    for field, value in contact_data.items():
        setattr(db_contact, field, value)
    db_commit_safety(db)
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, db_contact: Contact) -> Contact:
    db_contact.soft_delete()
    db_commit_safety(db)
    return db_contact
