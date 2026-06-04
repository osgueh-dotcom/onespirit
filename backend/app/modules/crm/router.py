from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.crm import service, schemas

router = APIRouter(tags=["CRM Module"])

# Customer Endpoints
@router.get("/customers", response_model=List[schemas.CustomerResponse])
def get_all_customers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.PermissionChecker(["crm:read"]))
):
    """Retrieve the list of customers"""
    return service.get_customers(db, skip=skip, limit=limit)

@router.get("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def get_customer_by_id(
    customer_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:read"]))
):
    """Get customer profile by ID"""
    customer = service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.post("/customers", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_entry(
    customer_in: schemas.CustomerCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Register a new customer account"""
    existing_customer = service.get_customer_by_name(db, company_name=customer_in.company_name)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A customer with this company name already exists."
        )
    return service.create_customer(db, customer_in=customer_in, user_id=str(current_user.id))

@router.put("/customers/{customer_id}", response_model=schemas.CustomerResponse)
def update_customer_entry(
    customer_id: str,
    customer_in: schemas.CustomerUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Update custom attributes of a customer"""
    customer = service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return service.update_customer(db, db_customer=customer, customer_in=customer_in)

@router.delete("/customers/{customer_id}", status_code=status.HTTP_200_OK)
def delete_customer_entry(
    customer_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Remove a customer account (Soft delete)"""
    customer = service.get_customer(db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    service.delete_customer(db, db_customer=customer)
    return {"message": "Customer profile successfully deactivated."}


# Contact Endpoints
@router.post("/contacts", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_entry(
    contact_in: schemas.ContactCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Register a new contact point of contact"""
    customer = service.get_customer(db, customer_id=str(contact_in.customer_id))
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer account not found"
        )
    return service.create_contact(db, contact_in=contact_in, user_id=str(current_user.id))

@router.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact_entry(
    contact_id: str,
    contact_in: schemas.ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Update contact attributes"""
    contact = service.get_contact(db, contact_id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    return service.update_contact(db, db_contact=contact, contact_in=contact_in)

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_200_OK)
def delete_contact_entry(
    contact_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["crm:write"]))
):
    """Deactivate or remove contact information (Soft delete)"""
    contact = service.get_contact(db, contact_id=contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found"
        )
    service.delete_contact(db, db_contact=contact)
    return {"message": "Contact point of contact successfully removed."}
