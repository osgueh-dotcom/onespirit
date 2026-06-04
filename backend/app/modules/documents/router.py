import os
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.core import deps
from app.core.config import settings
from app.modules.auth.models import User
from app.modules.documents import service, schemas
from app.modules.projects import service as project_service

router = APIRouter(tags=["Documentation Module"])

@router.get("/projects/{project_id}/documents", response_model=List[schemas.DocumentResponse])
def get_project_documents(
    project_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["documents:read"]))
):
    """Retrieve documents, Google Drive references, and file uploads linked to a project"""
    project = project_service.get_project(db, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return service.get_documents_by_project(db, project_id=project_id)

@router.post("/documents", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
def create_document_link(
    doc_in: schemas.DocumentCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["documents:write"]))
):
    """Link a cloud-based document (e.g. Google Drive, teaser link) to a project"""
    project = project_service.get_project(db, project_id=str(doc_in.project_id))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    if doc_in.storage_type != "google_drive":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use file upload endpoint for local files."
        )
    return service.create_document(db, doc_in=doc_in, uploaded_by_id=str(current_user.id))

@router.post("/documents/upload", response_model=schemas.DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_local_file(
    project_id: UUID = Form(...),
    title: str = Form(...),
    notes: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["documents:write"]))
):
    """Upload physical PDF, image, or presentation materials directly to local storage volume"""
    project = project_service.get_project(db, project_id=str(project_id))
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
        
    # Ensure upload folder exists
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)
        
    # Save the file securely
    file_extension = os.path.splitext(file.filename)[1]
    import uuid
    safe_filename = f"{project_id}_{str(uuid.uuid4())[:8]}{file_extension}"
    file_path = os.path.join(upload_dir, safe_filename)
    
    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to write file: {str(e)}"
        )
        
    file_type = "pdf" if file_extension.lower() == ".pdf" else "image"
    
    doc_create = schemas.DocumentCreate(
        project_id=project_id,
        title=title,
        file_path=file_path,
        file_type=file_type,
        storage_type="local",
        notes=notes
    )
    return service.create_document(db, doc_in=doc_create, uploaded_by_id=str(current_user.id))

@router.delete("/documents/{doc_id}", status_code=status.HTTP_200_OK)
def delete_document_entry(
    doc_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["documents:write"]))
):
    """Remove a linked reference or upload entry (Soft delete)"""
    doc = service.get_document(db, doc_id=doc_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    service.delete_document(db, db_doc=doc)
    return {"message": "Document successfully deleted."}
