from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict

class ImportPreviewResponse(BaseModel):
    total_rows: int
    valid_rows_count: int
    invalid_rows_count: int
    new_customers_count: int
    new_projects_count: int
    conflicts_count: int
    warnings: List[Dict[str, Any]]
    preview_rows: List[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)

class ImportCommitResponse(BaseModel):
    success: bool
    created_count: int
    updated_count: int
    errors: List[str]
    
    total_rows: int = 0
    successful_rows: int = 0
    skipped_rows: int = 0
    warning_count: int = 0
    error_count: int = 0
    warnings_per_row: Dict[str, List[str]] = {}
    unmapped_po_pm: List[Dict[str, Any]] = []
    unknown_source_types: List[Dict[str, Any]] = []
    duplicate_customers: List[Dict[str, Any]] = []

    model_config = ConfigDict(from_attributes=True)
