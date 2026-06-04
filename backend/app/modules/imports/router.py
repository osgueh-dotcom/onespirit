from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core import deps
from app.modules.auth.models import User
from app.modules.imports import schemas, service

router = APIRouter(prefix="/imports", tags=["Workflow Excel Import Engine"])

@router.post("/validate", response_model=schemas.ImportPreviewResponse)
def validate_excel_workflow(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["admin", "projects:write"]))
):
    """Parses Excel stream without commit, executing schemas, rows matching preview, and warnings report"""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a valid Excel spreadsheet (.xlsx)."
        )
    try:
        file_bytes = file.file.read()
        preview = service.parse_excel_sheet(db, file_bytes)
        return preview
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Excel parsing failed: {str(e)}"
        )

@router.post("/commit", response_model=schemas.ImportCommitResponse)
def commit_excel_workflow(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.PermissionChecker(["admin", "projects:write"]))
):
    """Executes database transaction updates and creates entities from Excel stream safely"""
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a valid Excel spreadsheet (.xlsx)."
        )
    try:
        file_bytes = file.file.read()
        report = service.commit_excel_import(db, file_bytes, str(current_user.id))
        return report
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Excel database commit transaction failed: {str(e)}"
        )
