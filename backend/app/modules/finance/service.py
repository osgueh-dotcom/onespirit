from datetime import date
from decimal import Decimal
from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.finance.models import Invoice, Payment
from app.modules.finance.schemas import InvoiceCreate, InvoiceUpdate, PaymentCreate, PaymentUpdate
from app.core.activity import log_activity
from app.core.database import db_commit_safety

def get_invoice(db: Session, invoice_id: str) -> Optional[Invoice]:
    return db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.deleted_at == None).first()

def get_invoice_by_number(db: Session, invoice_number: str) -> Optional[Invoice]:
    return db.query(Invoice).filter(Invoice.invoice_number == invoice_number, Invoice.deleted_at == None).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 100) -> List[Invoice]:
    return db.query(Invoice).filter(Invoice.deleted_at == None).offset(skip).limit(limit).all()

def get_invoices_by_project(db: Session, project_id: str) -> List[Invoice]:
    return db.query(Invoice).filter(Invoice.project_id == project_id, Invoice.deleted_at == None).all()

def sync_invoice_status(db: Session, invoice: Invoice):
    """Dynamically adjust invoice status depending on cumulative approved payments"""
    old_status = invoice.status
    approved_payments = db.query(Payment).filter(
        Payment.invoice_id == invoice.id,
        Payment.status == "approved",
        Payment.deleted_at == None
    ).all()
    
    total_paid = sum(p.amount for p in approved_payments)
    
    if total_paid <= 0:
        if invoice.due_date < date.today():
            invoice.status = "overdue"
        else:
            invoice.status = "unpaid"
    elif total_paid >= invoice.amount:
        invoice.status = "paid"
    else:
        invoice.status = "partial"
        
    db_commit_safety(db)
    
    # Log status updates if synced/modified
    if old_status != invoice.status:
        log_activity(
            db, 
            user_id=None, 
            action="invoice_status_synced", 
            entity_type="invoice", 
            entity_id=invoice.id, 
            details={"invoice_number": invoice.invoice_number, "old_status": old_status, "new_status": invoice.status, "project_id": str(invoice.project_id)}
        )

def create_invoice(db: Session, invoice_in: InvoiceCreate) -> Invoice:
    db_invoice = Invoice(
        project_id=invoice_in.project_id,
        invoice_number=invoice_in.invoice_number,
        amount=invoice_in.amount,
        issue_date=invoice_in.issue_date,
        due_date=invoice_in.due_date,
        status=invoice_in.status,
        notes=invoice_in.notes
    )
    db.add(db_invoice)
    db_commit_safety(db)
    db.refresh(db_invoice)
    sync_invoice_status(db, db_invoice)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=None, 
        action="invoice_issued", 
        entity_type="invoice", 
        entity_id=db_invoice.id, 
        details={"invoice_number": db_invoice.invoice_number, "amount": float(db_invoice.amount), "project_id": str(db_invoice.project_id)}
    )
    
    return db_invoice

def update_invoice(db: Session, db_invoice: Invoice, invoice_in: InvoiceUpdate) -> Invoice:
    invoice_data = invoice_in.dict(exclude_unset=True)
    for field, value in invoice_data.items():
        setattr(db_invoice, field, value)
    db_commit_safety(db)
    db.refresh(db_invoice)
    sync_invoice_status(db, db_invoice)
    return db_invoice

def delete_invoice(db: Session, db_invoice: Invoice) -> Invoice:
    db_invoice.soft_delete()
    # Cascade soft delete to payments
    for payment in db_invoice.payments:
        payment.soft_delete()
    db_commit_safety(db)
    return db_invoice


# Payment CRUD
def get_payment(db: Session, payment_id: str) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.id == payment_id, Payment.deleted_at == None).first()

def get_payments_by_invoice(db: Session, invoice_id: str) -> List[Payment]:
    return db.query(Payment).filter(Payment.invoice_id == invoice_id, Payment.deleted_at == None).all()

def create_payment(db: Session, payment_in: PaymentCreate) -> Payment:
    db_payment = Payment(
        invoice_id=payment_in.invoice_id,
        amount=payment_in.amount,
        payment_date=payment_in.payment_date,
        reference_number=payment_in.reference_number,
        proof_url=payment_in.proof_url,
        status=payment_in.status
    )
    db.add(db_payment)
    db_commit_safety(db)
    db.refresh(db_payment)
    
    # Recalculate linked invoice status
    sync_invoice_status(db, db_payment.invoice)
    
    # Central activity logging
    log_activity(
        db, 
        user_id=None, 
        action="payment_receipt_posted", 
        entity_type="invoice", 
        entity_id=db_payment.invoice_id, 
        details={"amount": float(db_payment.amount), "reference_number": db_payment.reference_number, "status": db_payment.status, "invoice_number": db_payment.invoice.invoice_number}
    )
    
    return db_payment

def update_payment(db: Session, db_payment: Payment, payment_in: PaymentUpdate) -> Payment:
    payment_data = payment_in.dict(exclude_unset=True)
    for field, value in payment_data.items():
        setattr(db_payment, field, value)
    db_commit_safety(db)
    db.refresh(db_payment)
    
    # Recalculate linked invoice status
    sync_invoice_status(db, db_payment.invoice)
    return db_payment

def delete_payment(db: Session, db_payment: Payment) -> Payment:
    invoice = db_payment.invoice
    db_payment.soft_delete()
    db_commit_safety(db)
    
    # Recalculate linked invoice status
    sync_invoice_status(db, invoice)
    return db_payment
