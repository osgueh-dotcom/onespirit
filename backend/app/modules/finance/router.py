from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import deps
from app.core.database import db_commit_safety
from app.modules.auth.models import User
from app.modules.finance import service, schemas
from app.modules.projects import service as project_service

router = APIRouter(tags=["Finance Module"])

# Invoices
@router.get("/invoices", response_model=List[schemas.InvoiceResponse])
def get_all_invoices(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.PermissionChecker(["finance:read"]))
):
    """Retrieve billing invoices catalog"""
    return service.get_invoices(db, skip=skip, limit=limit)

@router.get("/projects/{project_id}/invoices", response_model=List[schemas.InvoiceResponse])
def get_project_invoices(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:read"]))
):
    """Retrieve all invoices issued for a specific project"""
    project = project_service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_invoices_by_project(db, project_id=project_id)

@router.post("/invoices", response_model=schemas.InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice_entry(
    invoice_in: schemas.InvoiceCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Issue a new invoice linked to a project"""
    project = project_service.get_project(db, project_id=str(invoice_in.project_id))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    existing_invoice = service.get_invoice_by_number(db, invoice_number=invoice_in.invoice_number)
    if existing_invoice:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An invoice with this invoice number already exists."
        )
    return service.create_invoice(db, invoice_in=invoice_in)

@router.get("/invoices/{invoice_id}", response_model=schemas.InvoiceResponse)
def get_invoice_by_id(
    invoice_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:read"]))
):
    """Get specific invoice criteria and related payments by ID"""
    invoice = service.get_invoice(db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return invoice

@router.put("/invoices/{invoice_id}", response_model=schemas.InvoiceResponse)
def update_invoice_entry(
    invoice_id: str,
    invoice_in: schemas.InvoiceUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Update details of an invoice"""
    invoice = service.get_invoice(db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return service.update_invoice(db, db_invoice=invoice, invoice_in=invoice_in)

@router.delete("/invoices/{invoice_id}", status_code=status.HTTP_200_OK)
def delete_invoice_entry(
    invoice_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Remove or void an invoice (Soft delete)"""
    invoice = service.get_invoice(db, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    service.delete_invoice(db, db_invoice=invoice)
    return {"message": "Invoice successfully voided."}


# Payments
@router.post("/payments", response_model=schemas.PaymentResponse, status_code=status.HTTP_201_CREATED)
def record_payment_entry(
    payment_in: schemas.PaymentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Record a cash collection payment receipts sheet linked to an invoice"""
    invoice = service.get_invoice(db, invoice_id=str(payment_in.invoice_id))
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return service.create_payment(db, payment_in=payment_in)

@router.put("/payments/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment_entry(
    payment_id: str,
    payment_in: schemas.PaymentUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Update payment log info"""
    payment = service.get_payment(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return service.update_payment(db, db_payment=payment, payment_in=payment_in)

@router.delete("/payments/{payment_id}", status_code=status.HTTP_200_OK)
def delete_payment_entry(
    payment_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Deactivate or remove payment entry (Soft delete)"""
    payment = service.get_payment(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    service.delete_payment(db, db_payment=payment)
    return {"message": "Payment record successfully deleted."}

@router.post("/payments/{payment_id}/approve", response_model=schemas.PaymentResponse)
def approve_payment_receipt(
    payment_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["finance:write"]))
):
    """Approve a pending payment receipt, triggering cascading invoice status re-calculations"""
    payment = service.get_payment(db, payment_id=payment_id)
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    payment.status = "approved"
    db_commit_safety(db)
    db.refresh(payment)
    
    # Recalculate linked invoice status
    service.sync_invoice_status(db, payment.invoice)
    
    return payment
