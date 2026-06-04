from typing import List, Optional
from sqlalchemy.orm import Session
from app.modules.documents.models import Document
from app.modules.documents.schemas import DocumentCreate
from app.core.activity import log_activity
from app.core.database import db_commit_safety

def get_document(db: Session, doc_id: str) -> Optional[Document]:
    return db.query(Document).filter(Document.id == doc_id, Document.deleted_at == None).first()

def get_documents_by_project(db: Session, project_id: str) -> List[Document]:
    return db.query(Document).filter(Document.project_id == project_id, Document.deleted_at == None).all()

def create_document(db: Session, doc_in: DocumentCreate, uploaded_by_id: str) -> Document:
    db_doc = Document(
        project_id=doc_in.project_id,
        title=doc_in.title,
        file_path=doc_in.file_path,
        file_type=doc_in.file_type,
        storage_type=doc_in.storage_type,
        notes=doc_in.notes,
        uploaded_by_id=uploaded_by_id
    )
    db.add(db_doc)
    db_commit_safety(db)
    db.refresh(db_doc)
    
    # Determine appropriate action tag based on storage_type
    action = "document_linked" if db_doc.storage_type == "google_drive" else "document_uploaded"
    
    log_activity(
        db,
        user_id=uploaded_by_id,
        action=action,
        entity_type="document",
        entity_id=db_doc.id,
        details={
            "title": db_doc.title,
            "project_id": str(db_doc.project_id),
            "file_type": db_doc.file_type,
            "storage_type": db_doc.storage_type
        }
    )
    
    return db_doc

def delete_document(db: Session, db_doc: Document) -> Document:
    db_doc.soft_delete()
    db_commit_safety(db)
    return db_doc
