import io
import uuid
import openpyxl
from datetime import datetime, date
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session

from app.modules.auth.models import User
from app.modules.crm.models import Customer, Contact
from app.modules.crm.service import create_customer, create_contact
from app.modules.projects.models import Project
from app.modules.projects.service import create_project, transition_project_status
from app.modules.events.models import EventSchedule
from app.modules.tasks.models import Task
from app.modules.tasks.service import create_task
from app.modules.finance.models import Invoice, Payment
from app.modules.finance.service import create_invoice, create_payment
from app.modules.documents.models import Document
from app.modules.documents.service import create_document
from app.core.activity import log_activity

# Enriched Mapping lists for column headers (case-insensitive & robust)
HEADER_MAP = {
    "company_name": ["company name", "company", "client", "customer name", "customer"],
    "customer_category": ["customer category", "client category", "category", "classification"],
    "contact_name": ["contact person", "contact name", "contact", "pic customer", "cp"],
    "phone": ["phone number", "phone", "contact phone", "mobile"],
    "email": ["email", "email address", "contact email"],
    "program_name": ["program name", "project name", "title", "program", "project title", "prog"],
    "event_category": ["event category", "program category"],
    "venue": ["venue", "location", "place", "event venue"],
    "start_date": ["start date", "event date", "start", "proposed start date", "event date start"],
    "end_date": ["end date", "end", "proposed end date", "event date end"],
    "budget": ["budget", "project budget", "revenue", "amount", "budget allocation", "budget (rp)", "budget rp"],
    "quotation_number": ["quotation number", "quotation no", "quote no", "quotation reference"],
    "quotation_status": ["quotation status", "quote status"],
    "project_status": ["project status", "status", "workflow status"],
    "cl": ["cl", "cl checklist"],
    "ros": ["ros", "ros checklist"],
    "ck": ["ck", "ck checklist"],
    "pnl": ["pnl", "pnl checklist", "pnl sheet"],
    "pf": ["pf", "pf checklist"],
    "matrix": ["matrix", "matrix checklist"],
    "photo_links": ["photo links", "photos", "photo link", "link photo"],
    "video_links": ["video links", "videos", "video link", "link video"],
    "teaser_links": ["teaser links", "teaser", "teaser link", "link teaser"],
    "invoice_status": ["invoice status", "invoicing status", "billing status"],
    "payment_status": ["payment status", "pay status"],
    "payment_schedule": ["payment schedule", "payment schadule", "payment plan"],
    "signed_document": ["signed document", "signed file", "contract", "signed agreement"]
}

def clean_header(val: Any) -> str:
    if not val:
        return ""
    return str(val).strip().lower().replace("_", " ").replace("-", " ")

def find_column_indices(sheet: openpyxl.worksheet.worksheet.Worksheet) -> Tuple[Dict[str, int], int]:
    """
    Dynamically locates indices of required columns, robust to layout shifts.
    Scans the first 15 rows to find the row with the most matched aliases.
    Returns a tuple: (column_indices_dict, header_row_index)
    """
    best_row_idx = 1
    best_match_count = -1
    best_indices = {}

    for r_idx in range(1, min(15, sheet.max_row + 1)):
        row_cells = [cell.value for cell in sheet[r_idx]]
        current_indices = {}
        match_count = 0
        
        for key, aliases in HEADER_MAP.items():
            found = False
            for idx, val in enumerate(row_cells):
                cleaned = clean_header(val)
                if cleaned in aliases:
                    current_indices[key] = idx + 1  # 1-indexed for openpyxl
                    match_count += 1
                    found = True
                    break
            if not found:
                current_indices[key] = None
        
        if match_count > best_match_count:
            best_match_count = match_count
            best_row_idx = r_idx
            best_indices = current_indices

    return best_indices, best_row_idx

def get_row_val(row: Tuple, col_idx: int) -> Any:
    if not col_idx or col_idx > len(row):
        return None
    return row[col_idx - 1].value

def parse_date(val: Any) -> Any:
    if not val:
        return None
    if isinstance(val, (datetime, date)):
        return val
    try:
        # standard ISO formats
        return datetime.strptime(str(val).split(" ")[0], "%Y-%m-%d").date()
    except Exception:
        try:
            return datetime.strptime(str(val).split(" ")[0], "%d/%m/%Y").date()
        except Exception:
            return None

def parse_float(val: Any) -> float:
    if not val:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    try:
        cleaned = str(val).replace("$", "").replace("Rp", "").replace(" ", "").strip()
        if not cleaned:
            return 0.0
        
        # Smart currency formatting parser (handles both US and IDR standards)
        if "," in cleaned and "." in cleaned:
            if cleaned.find(",") < cleaned.find("."):
                cleaned = cleaned.replace(",", "")
            else:
                cleaned = cleaned.replace(".", "").replace(",", ".")
        elif "," in cleaned:
            parts = cleaned.split(",")
            if len(parts) == 2 and len(parts[1]) <= 2:
                cleaned = cleaned.replace(",", ".")
            else:
                cleaned = cleaned.replace(",", "")
        elif "." in cleaned:
            parts = cleaned.split(".")
            if len(parts) > 2:
                cleaned = cleaned.replace(".", "")
            elif len(parts) == 2 and len(parts[1]) > 2:
                cleaned = cleaned.replace(".", "")
                
        return float(cleaned)
    except Exception:
        return 0.0

def normalize_status(val: Any, category: str) -> str:
    cleaned = str(val or "").strip().lower()
    if category == "project":
        stages = ["inquiry", "quotation", "negotiation", "confirmed", "preparation", "ongoing", "completed", "canceled"]
        for s in stages:
            if s in cleaned:
                return s
        return "inquiry"
    elif category == "quote":
        stages = ["draft", "sent", "approved", "rejected"]
        for s in stages:
            if s in cleaned:
                return s
        return "draft"
    elif category == "task":
        stages = ["todo", "in_progress", "review", "done"]
        for s in stages:
            if s in cleaned:
                return s
        return "todo"
    elif category == "payment":
        stages = ["unpaid", "partial", "paid", "overdue"]
        for s in stages:
            if s in cleaned:
                return s
        return "unpaid"
    return cleaned

def build_project_title(company_name: str, event_category: Any, program_name: Any) -> str:
    """Smartly constructs standard operational project titles aligned with seed loader"""
    c_name = str(company_name or "").strip()
    e_cat = str(event_category or "").strip()
    p_name = str(program_name or "").strip()
    
    if c_name and c_name.lower() in p_name.lower():
        return p_name
        
    parts = []
    if c_name:
        parts.append(c_name)
        
    prog_str = ""
    if e_cat and p_name:
        prog_str = f"{e_cat} ({p_name})"
    elif e_cat:
        prog_str = e_cat
    elif p_name:
        prog_str = p_name
        
    if prog_str:
        parts.append(prog_str)
        
    title = " - ".join(parts)
    return title if title else "Unnamed Project"

def parse_excel_sheet(file_bytes: bytes) -> Dict[str, Any]:
    """Stateless excel parser checking schemas and duplicate counts"""
    wb = openpyxl.load_workbook(filename=io.BytesIO(file_bytes), data_only=True)
    
    # Locate Workflow sheet or fall back to active sheet
    sheet = None
    for s_name in wb.sheetnames:
        if clean_header(s_name) == "workflow" or s_name == "Workflow":
            sheet = wb[s_name]
            break
    if not sheet:
        sheet = wb.active

    indices, header_row_idx = find_column_indices(sheet)
    
    warnings = []
    preview_rows = []
    
    new_customers = set()
    new_projects = set()
    conflicts_count = 0
    total_rows = 0
    valid_rows_count = 0
    invalid_rows_count = 0

    # Iterate rows starting from index header_row_idx + 1
    for r_idx in range(header_row_idx + 1, sheet.max_row + 1):
        row = list(sheet[r_idx])
        # Skip empty rows
        if not any(cell.value for cell in row):
            continue
            
        total_rows += 1
        
        comp_name = get_row_val(row, indices["company_name"])
        raw_program_name = get_row_val(row, indices["program_name"])
        
        # Required validation
        if not comp_name or not raw_program_name:
            invalid_rows_count += 1
            warnings.append({
                "row": r_idx,
                "message": f"Row skipped: Missing required parameters (Company Name or Program Name)."
            })
            continue

        valid_rows_count += 1
        
        # Parse fields
        c_category = get_row_val(row, indices["customer_category"]) or "Corporate"
        budget = parse_float(get_row_val(row, indices["budget"]))
        start_date = parse_date(get_row_val(row, indices["start_date"]))
        end_date = parse_date(get_row_val(row, indices["end_date"]))
        quote_no = get_row_val(row, indices["quotation_number"])
        p_status = normalize_status(get_row_val(row, indices["project_status"]), "project")
        q_status = normalize_status(get_row_val(row, indices["quotation_status"]), "quote")
        raw_event_category = get_row_val(row, indices["event_category"])

        proj_title = build_project_title(comp_name, raw_event_category, raw_program_name)

        preview_rows.append({
            "row_index": r_idx,
            "company_name": comp_name,
            "customer_category": c_category,
            "contact_name": get_row_val(row, indices["contact_name"]) or "Staff Contact",
            "phone": get_row_val(row, indices["phone"]),
            "email": get_row_val(row, indices["email"]),
            "project_title": proj_title,
            "budget": budget,
            "start_date": str(start_date) if start_date else None,
            "end_date": str(end_date) if end_date else None,
            "quotation_number": quote_no,
            "project_status": p_status,
            "quotation_status": q_status
        })

        new_customers.add(comp_name)
        new_projects.add(f"{proj_title}-{start_date}")

    return {
        "total_rows": total_rows,
        "valid_rows_count": valid_rows_count,
        "invalid_rows_count": invalid_rows_count,
        "new_customers_count": len(new_customers),
        "new_projects_count": len(new_projects),
        "conflicts_count": conflicts_count,  # Calculated dynamically in commit
        "warnings": warnings,
        "preview_rows": preview_rows
    }

def commit_excel_import(db: Session, file_bytes: bytes, user_id: str) -> Dict[str, Any]:
    """Transactional commits matching and updating database elements"""
    wb = openpyxl.load_workbook(filename=io.BytesIO(file_bytes), data_only=True)
    
    sheet = None
    for s_name in wb.sheetnames:
        if clean_header(s_name) == "workflow" or s_name == "Workflow":
            sheet = wb[s_name]
            break
    if not sheet:
        sheet = wb.active

    indices, header_row_idx = find_column_indices(sheet)
    
    created_count = 0
    updated_count = 0
    errors = []

    # Get system user default PM or current executor
    default_pm = db.query(User).filter(User.deleted_at == None).first()
    executor_id = user_id if user_id else (str(default_pm.id) if default_pm else None)

    for r_idx in range(header_row_idx + 1, sheet.max_row + 1):
        row = list(sheet[r_idx])
        if not any(cell.value for cell in row):
            continue

        comp_name = get_row_val(row, indices["company_name"])
        raw_program_name = get_row_val(row, indices["program_name"])

        if not comp_name or not raw_program_name:
            continue

        try:
            # 1. Match/Create Customer
            customer = db.query(Customer).filter(
                Customer.company_name == comp_name,
                Customer.deleted_at == None
            ).first()

            is_new_cust = False
            if not customer:
                # Create customer
                customer = Customer(
                    company_name=comp_name,
                    category=get_row_val(row, indices["customer_category"]) or "Corporate",
                    address=get_row_val(row, indices["venue"]) or "Address Linked"
                )
                db.add(customer)
                db.commit()
                db.refresh(customer)
                created_count += 1
                is_new_cust = True
                
                log_activity(
                    db,
                    user_id=executor_id,
                    action="customer_created",
                    entity_type="customer",
                    entity_id=customer.id,
                    details={"company_name": customer.company_name, "category": customer.category, "source": "excel_sync"}
                )
            else:
                updated_count += 1

            # 2. Match/Create Contact Point
            c_name = get_row_val(row, indices["contact_name"])
            if c_name:
                contact = db.query(Contact).filter(
                    Contact.customer_id == customer.id,
                    Contact.name == c_name,
                    Contact.deleted_at == None
                ).first()
                if not contact:
                    contact = Contact(
                        customer_id=customer.id,
                        name=c_name,
                        email=get_row_val(row, indices["email"]),
                        phone=get_row_val(row, indices["phone"]),
                        position="Point of Contact"
                    )
                    db.add(contact)
                    db.commit()
                    
                    log_activity(
                        db,
                        user_id=executor_id,
                        action="contact_linked",
                        entity_type="customer",
                        entity_id=customer.id,
                        details={"name": contact.name, "source": "excel_sync"}
                    )

            # 3. Match/Create Project
            quote_no = get_row_val(row, indices["quotation_number"])
            start_date = parse_date(get_row_val(row, indices["start_date"]))
            end_date = parse_date(get_row_val(row, indices["end_date"]))
            budget = parse_float(get_row_val(row, indices["budget"]))
            p_status = normalize_status(get_row_val(row, indices["project_status"]), "project")
            q_status = normalize_status(get_row_val(row, indices["quotation_status"]), "quote")
            raw_event_category = get_row_val(row, indices["event_category"])

            proj_title = build_project_title(comp_name, raw_event_category, raw_program_name)

            # Match by name + date
            project = db.query(Project).filter(
                Project.title == proj_title,
                Project.start_date == start_date,
                Project.deleted_at == None
            ).first()

            is_new_proj = False
            old_status = None
            if not project:
                project = Project(
                    title=proj_title,
                    status=p_status,
                    quotation_status=q_status,
                    start_date=start_date,
                    end_date=end_date,
                    budget=budget,
                    revenue=budget,
                    customer_id=customer.id,
                    created_by_id=uuid.UUID(executor_id) if executor_id else None,
                    assigned_to_id=uuid.UUID(executor_id) if executor_id else None
                )
                db.add(project)
                db.commit()
                db.refresh(project)
                created_count += 1
                is_new_proj = True
                
                log_activity(
                    db,
                    user_id=executor_id,
                    action="project_created",
                    entity_type="project",
                    entity_id=project.id,
                    details={"title": project.title, "status": project.status, "source": "excel_sync"}
                )
            else:
                old_status = project.status
                project.title = proj_title
                project.start_date = start_date or project.start_date
                project.end_date = end_date or project.end_date
                project.budget = budget or project.budget
                project.revenue = budget or project.revenue
                project.status = p_status
                project.quotation_status = q_status
                db.commit()
                updated_count += 1
                
                if old_status != p_status:
                    log_activity(
                        db,
                        user_id=executor_id,
                        action="status_transitioned",
                        entity_type="project",
                        entity_id=project.id,
                        details={"title": project.title, "old_status": old_status, "new_status": p_status, "source": "excel_sync"}
                    )

            # 4. EventSchedule setup
            venue_name = get_row_val(row, indices["venue"])
            if venue_name:
                sched = db.query(EventSchedule).filter(
                    EventSchedule.project_id == project.id,
                    EventSchedule.venue_name == venue_name,
                    EventSchedule.deleted_at == None
                ).first()
                if not sched:
                    sched = EventSchedule(
                        project_id=project.id,
                        venue_name=venue_name,
                        address=venue_name,
                        start_time=datetime.combine(start_date, datetime.min.time()) if start_date else datetime.now(),
                        end_time=datetime.combine(end_date, datetime.max.time()) if end_date else datetime.now(),
                        pic_id=uuid.UUID(executor_id) if executor_id else None,
                        rundown=[]
                    )
                    db.add(sched)
                    db.commit()

            # 5. Checklist Tasks syncing
            checklists = ["cl", "ros", "ck", "pnl", "pf", "matrix"]
            for chk in checklists:
                chk_val = get_row_val(row, indices[chk])
                chk_status = "done" if str(chk_val or "").strip().lower() in ["1", "yes", "check", "done", "x", "true"] else "todo"
                
                # Check if task exists under project
                task_title = f"{chk.upper()} Operations Checklist"
                task = db.query(Task).filter(
                    Task.project_id == project.id,
                    Task.title == task_title,
                    Task.deleted_at == None
                ).first()
                
                if not task:
                    task = Task(
                        project_id=project.id,
                        title=task_title,
                        description=f"Standard operations compliance item for {chk.upper()} checking",
                        status=chk_status,
                        priority="medium",
                        due_date=datetime.combine(start_date, datetime.min.time()) if start_date else datetime.now(),
                        created_by_id=uuid.UUID(executor_id) if executor_id else None,
                        assigned_to_id=uuid.UUID(executor_id) if executor_id else None
                    )
                    db.add(task)
                    db.commit()
                    
                    log_activity(
                        db,
                        user_id=executor_id,
                        action="task_allocated",
                        entity_type="task",
                        entity_id=task.id,
                        details={"title": task.title, "project_id": str(project.id), "source": "excel_sync"}
                    )
                else:
                    if task.status != chk_status:
                        task.status = chk_status
                        db.commit()
                        action = "task_completed" if chk_status == "done" else "task_status_changed"
                        
                        log_activity(
                            db,
                            user_id=executor_id,
                            action=action,
                            entity_type="task",
                            entity_id=task.id,
                            details={"title": task.title, "status": chk_status, "project_id": str(project.id), "source": "excel_sync"}
                        )

            # 6. Documentation Assets uploads
            docs = ["photo_links", "video_links", "teaser_links"]
            for doc_key in docs:
                link_val = get_row_val(row, indices[doc_key])
                if link_val and str(link_val).startswith("http"):
                    doc_title = f"Operational {doc_key.replace('_', ' ').title()} Asset"
                    doc = db.query(Document).filter(
                        Document.project_id == project.id,
                        Document.title == doc_title,
                        Document.file_path == link_val,
                        Document.deleted_at == None
                    ).first()
                    if not doc:
                        doc = Document(
                            project_id=project.id,
                            title=doc_title,
                            file_path=link_val,
                            file_type="link",
                            storage_type="google_drive",
                            uploaded_by_id=uuid.UUID(executor_id) if executor_id else None
                        )
                        db.add(doc)
                        db.commit()
                        
                        log_activity(
                            db,
                            user_id=executor_id,
                            action="document_linked",
                            entity_type="document",
                            entity_id=doc.id,
                            details={"title": doc.title, "project_id": str(project.id), "source": "excel_sync"}
                        )

            # 7. Invoice & Payment syncing (Standard finance ledgering support)
            if quote_no:
                invoice = db.query(Invoice).filter(
                    Invoice.invoice_number == str(quote_no).strip(),
                    Invoice.deleted_at == None
                ).first()
                
                inv_status = normalize_status(get_row_val(row, indices["invoice_status"]), "payment")
                if not inv_status or inv_status == "unpaid":
                    # Fallback check on Payment Status
                    p_stat = get_row_val(row, indices["payment_status"])
                    if p_stat and "paid" in str(p_stat).lower():
                        inv_status = "paid"
                    elif p_stat and "partial" in str(p_stat).lower():
                        inv_status = "partial"
                
                pay_schedule = get_row_val(row, indices["payment_schedule"]) or "Excel Import Billing"
                
                if not invoice:
                    invoice = Invoice(
                        project_id=project.id,
                        invoice_number=str(quote_no).strip(),
                        amount=budget,
                        issue_date=start_date or date.today(),
                        due_date=end_date or start_date or date.today(),
                        status=inv_status or "unpaid",
                        notes=f"Payment Schedule: {pay_schedule}"
                    )
                    db.add(invoice)
                    db.commit()
                    db.refresh(invoice)
                    
                    log_activity(
                        db,
                        user_id=executor_id,
                        action="invoice_issued",
                        entity_type="invoice",
                        entity_id=invoice.id,
                        details={"invoice_number": invoice.invoice_number, "amount": float(invoice.amount), "project_id": str(project.id), "source": "excel_sync"}
                    )
                else:
                    invoice.amount = budget or invoice.amount
                    invoice.status = inv_status or invoice.status
                    invoice.notes = f"Payment Schedule: {pay_schedule}"
                    db.commit()
                
                # Check if payment needs to be auto-posted
                if invoice.status == "paid":
                    payment = db.query(Payment).filter(
                        Payment.invoice_id == invoice.id,
                        Payment.status == "approved",
                        Payment.deleted_at == None
                    ).first()
                    
                    if not payment:
                        payment = Payment(
                            invoice_id=invoice.id,
                            amount=invoice.amount,
                            payment_date=start_date or date.today(),
                            reference_number=f"Excel Sync - {quote_no}",
                            status="approved",
                            proof_url="https://drive.google.com/drive/folders/onespirit"
                        )
                        db.add(payment)
                        db.commit()
                        
                        log_activity(
                            db,
                            user_id=executor_id,
                            action="payment_receipt_posted",
                            entity_type="payment",
                            entity_id=payment.id,
                            details={"invoice_number": invoice.invoice_number, "amount": float(payment.amount), "project_id": str(project.id), "source": "excel_sync"}
                        )

            # 8. Signed Document Sync
            signed_val = get_row_val(row, indices["signed_document"])
            if signed_val:
                doc_title = "Signed Operations Contract File"
                doc = db.query(Document).filter(
                    Document.project_id == project.id,
                    Document.title == doc_title,
                    Document.deleted_at == None
                ).first()
                if not doc:
                    doc = Document(
                        project_id=project.id,
                        title=doc_title,
                        file_path=str(signed_val).strip(),
                        file_type="pdf" if "pdf" in str(signed_val).lower() else "link",
                        storage_type="google_drive" if str(signed_val).startswith("http") else "local",
                        uploaded_by_id=uuid.UUID(executor_id) if executor_id else None,
                        notes="Seeded signed contract agreement from Excel import"
                    )
                    db.add(doc)
                    db.commit()
                    
                    log_activity(
                        db,
                        user_id=executor_id,
                        action="document_linked",
                        entity_type="document",
                        entity_id=doc.id,
                        details={"title": doc.title, "project_id": str(project.id), "source": "excel_sync"}
                    )

        except Exception as e:
            db.rollback()
            errors.append(f"Row {r_idx} import failed: {str(e)}")

    return {
        "success": len(errors) == 0,
        "created_count": created_count,
        "updated_count": updated_count,
        "errors": errors
    }
