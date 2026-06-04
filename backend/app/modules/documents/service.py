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

def map_legacy_file_type_to_doc_type(file_type: str) -> str:
    cleaned = (file_type or "").strip().lower()
    if cleaned in ["pdf", "signed_file", "signed_file"]:
        return "SIGNED_FILE"
    if cleaned in ["image", "photo", "jpg", "png"]:
        return "PHOTO"
    if cleaned in ["video", "mp4", "avi"]:
        return "VIDEO"
    if cleaned == "teaser":
        return "TEASER"
    if cleaned == "instagram":
        return "INSTAGRAM"
    if cleaned == "youtube":
        return "YOUTUBE"
    return "OTHER"

def create_document(db: Session, doc_in: DocumentCreate, uploaded_by_id: str) -> Document:
    doc_type = doc_in.document_type
    if not doc_type:
        doc_type = map_legacy_file_type_to_doc_type(doc_in.file_type)
        
    doc_url = doc_in.url
    if not doc_url:
        doc_url = doc_in.file_path

    import uuid
    parsed_uploader_id = None
    if uploaded_by_id:
        if isinstance(uploaded_by_id, str):
            try:
                parsed_uploader_id = uuid.UUID(uploaded_by_id)
            except ValueError:
                parsed_uploader_id = None
        else:
            parsed_uploader_id = uploaded_by_id

    db_doc = Document(
        project_id=doc_in.project_id,
        title=doc_in.title,
        file_path=doc_in.file_path,
        file_type=doc_in.file_type,
        storage_type=doc_in.storage_type,
        notes=doc_in.notes,
        uploaded_by_id=parsed_uploader_id,
        document_type=doc_type,
        url=doc_url
    )
    db.add(db_doc)
    db_commit_safety(db)
    db.refresh(db_doc)
    
    # Determine appropriate action tag based on storage_type
    action = "document_linked" if db_doc.storage_type == "google_drive" else "document_uploaded"
    
    log_activity(
        db,
        user_id=parsed_uploader_id,
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
    
    # Track document added in ProjectActivityLog
    from app.modules.projects.models import ProjectActivityLog
    activity = ProjectActivityLog(
        project_id=db_doc.project_id,
        user_id=parsed_uploader_id,
        action="document_added",
        field_name="document",
        new_value=db_doc.title,
        notes=f"Document '{db_doc.title}' ({db_doc.document_type}) linked to project."
    )
    db.add(activity)
    db_commit_safety(db)
    
    return db_doc

def delete_document(db: Session, db_doc: Document) -> Document:
    db_doc.soft_delete()
    db_commit_safety(db)
    return db_doc
