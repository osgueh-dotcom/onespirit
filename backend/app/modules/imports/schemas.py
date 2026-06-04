from typing import List, Dict, Any
from pydantic import BaseModel

class ImportPreviewResponse(BaseModel):
    total_rows: int
    valid_rows_count: int
    invalid_rows_count: int
    new_customers_count: int
    new_projects_count: int
    conflicts_count: int
    warnings: List[Dict[str, Any]]
    preview_rows: List[Dict[str, Any]]

    class Config:
        from_attributes = True

class ImportCommitResponse(BaseModel):
    success: bool
    created_count: int
    updated_count: int
    errors: List[str]

    class Config:
        from_attributes = True
