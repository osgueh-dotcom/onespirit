import io
import pytest
import openpyxl
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin
from app.modules.auth.models import User
from app.modules.crm.models import Customer, Contact
from app.modules.projects.models import Project
from app.modules.tasks.models import Task
from app.tests.db_utils import sqlite_test_url

# Local fixtures for self-contained testing execution
SQLALCHEMY_DATABASE_URL = sqlite_test_url("test_imports.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    seed_roles_and_admin(db_session)
    yield db_session
    db_session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def create_mock_excel() -> bytes:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Workflow"

    # Define headers
    headers = [
        "Company Name", "Customer Category", "Contact Person", "Phone Number", "Email",
        "Program Name", "Event Category", "Venue", "Start Date", "End Date",
        "Budget", "Quotation Number", "Quotation Status", "Project Status",
        "CL", "ROS", "CK", "PNL", "PF", "Matrix",
        "Photo Links", "Video Links", "Teaser Links"
    ]
    ws.append(headers)

    # Valid row
    ws.append([
        "Gojek Indonesia", "Corporate", "Ahmad PIC", "08123456", "ahmad@gojek.com",
        "Gojek Gathering & Team Building", "Gathering", "Dago Highlands Bandung",
        "2026-07-01", "2026-07-03", "125000000", "OSA-Q-2026-8888", "approved", "confirmed",
        "1", "yes", "0", "check", "no", "done",
        "https://photos.onespirit.asia/gojek", "https://videos.onespirit.asia/gojek", ""
    ])

    # Invalid row (missing company and program name)
    ws.append([
        "", "", "", "", "",
        "", "", "", "", "",
        "", "", "", "", "",
        "", "", "", "", "",
        "", "", ""
    ])

    out = io.BytesIO()
    wb.save(out)
    return out.getvalue()

def test_imports_endpoints(client):
    # 1. Login as Super Admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Generate mock sheet bytes
    excel_bytes = create_mock_excel()

    # 2. Test stateless validation preview
    files = {"file": ("workflow_sync.xlsx", excel_bytes, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    val_response = client.post("/api/v1/imports/validate", files=files, headers=headers)
    assert val_response.status_code == 200
    
    val_data = val_response.json()
    assert val_data["total_rows"] == 1
    assert val_data["valid_rows_count"] == 1
    assert val_data["invalid_rows_count"] == 0
    assert val_data["new_customers_count"] == 1
    assert val_data["new_projects_count"] == 1
    assert len(val_data["preview_rows"]) == 1
    
    # 3. Test transaction commit execution
    excel_bytes_commit = create_mock_excel()
    files_commit = {"file": ("workflow_sync.xlsx", excel_bytes_commit, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    
    commit_response = client.post("/api/v1/imports/commit", files=files_commit, headers=headers)
    assert commit_response.status_code == 200
    
    commit_data = commit_response.json()
    assert commit_data["errors"] == []
    assert commit_data["success"] is True
    assert commit_data["created_count"] > 0
