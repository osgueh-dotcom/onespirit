import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin
from app.modules.crm.models import Customer
from app.modules.projects.models import Project

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test_instruments.db"

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
    
    # Create a test customer
    cust = Customer(
        company_name="Test Customer Ltd",
        category="Corporate",
        address="123 Test Street"
    )
    db_session.add(cust)
    db_session.commit()
    db_session.refresh(cust)
    
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

def test_project_instruments_workflow(client, db):
    # 1. Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch customer
    cust = db.query(Customer).first()
    assert cust is not None

    # 2. Create a project
    project_payload = {
        "title": "Grand Launching Event",
        "customer_id": str(cust.id),
        "budget": 50000000.0,
        "revenue": 55000000.0,
        "quotation_status": "Draft",
        "program_status": "Inquiry",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": "2026-07-01",
        "event_date_end": "2026-07-03"
    }
    create_res = client.post("/api/v1/projects", json=project_payload, headers=headers)
    assert create_res.status_code == 201
    proj_data = create_res.json()
    proj_id = proj_data["id"]

    # 3. Verify defaults are auto-generated
    inst_res = client.get(f"/api/v1/projects/{proj_id}/instruments", headers=headers)
    assert inst_res.status_code == 200
    instruments = inst_res.json()
    assert len(instruments) == 4
    types = [i["instrument_type"] for i in instruments]
    assert "CL" in types
    assert "ROS" in types
    assert "CK" in types
    assert "PNL" in types

    # Find the CL instrument
    cl_inst = next(i for i in instruments if i["instrument_type"] == "CL")
    assert cl_inst["status"] == "Not Started"

    # 4. Get Project details and check warnings (Quotation is Draft, so no PNL missing warning yet)
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert len(detail_data["instruments"]) == 4

    # 5. Transition quotation status to Signed & Deal
    # This should trigger PNL missing warning because PNL document link is empty.
    # Note: Transitioning requires updating quotation_status. Let's do it via PUT/edit project.
    update_payload = {
        "quotation_status": "Signed & Deal",
        "program_status": "Confirmed"
    }
    update_res = client.put(f"/api/v1/projects/{proj_id}", json=update_payload, headers=headers)
    assert update_res.status_code == 200

    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=headers)
    detail_data = detail_res.json()
    warnings = detail_data["validation_warnings"]
    assert any("Profit & Loss (PNL)" in w for w in warnings)
    assert any("Contract/Confirmation Letter (CL)" in w for w in warnings)

    # 6. Update CL status to Done and PNL document URL
    cl_id = cl_inst["id"]
    patch_payload = {
        "status": "Done"
    }
    patch_res = client.patch(f"/api/v1/projects/{proj_id}/instruments/{cl_id}", json=patch_payload, headers=headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "Done"

    # Find PNL instrument and update document URL
    pnl_inst = next(i for i in instruments if i["instrument_type"] == "PNL")
    pnl_id = pnl_inst["id"]
    patch_pnl_payload = {
        "document_url": "https://drive.google.com/test-pnl-file"
    }
    patch_pnl_res = client.patch(f"/api/v1/projects/{proj_id}/instruments/{pnl_id}", json=patch_pnl_payload, headers=headers)
    assert patch_pnl_res.status_code == 200
    assert patch_pnl_res.json()["document_url"] == "https://drive.google.com/test-pnl-file"

    # 7. Check validation warnings again - CL and PNL warnings should be resolved!
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=headers)
    detail_data = detail_res.json()
    warnings = detail_data["validation_warnings"]
    assert not any("Profit & Loss (PNL)" in w for w in warnings)
    assert not any("Contract/Confirmation Letter (CL)" in w for w in warnings)

    # 8. Create a custom instrument
    custom_payload = {
        "project_id": proj_id,
        "instrument_type": "OTHER",
        "title": "Custom Event Mat",
        "status": "In Progress"
    }
    custom_res = client.post(f"/api/v1/projects/{proj_id}/instruments", json=custom_payload, headers=headers)
    assert custom_res.status_code == 201
    custom_inst = custom_res.json()
    custom_id = custom_inst["id"]
    assert custom_inst["instrument_type"] == "OTHER"
    assert custom_inst["title"] == "Custom Event Mat"

    # 9. Delete custom instrument
    del_res = client.delete(f"/api/v1/projects/{proj_id}/instruments/{custom_id}", headers=headers)
    assert del_res.status_code == 200

    # 10. Try deleting non-existent instrument
    del_fail_res = client.delete(f"/api/v1/projects/{proj_id}/instruments/{custom_id}", headers=headers)
    assert del_fail_res.status_code == 404

def test_sprint_7_instrument_refinements(client, db):
    from datetime import date, timedelta
    from app.modules.auth.schemas import UserCreate
    from app.modules.auth.service import create_user
    from app.modules.auth.models import Role, User

    # 1. Login as admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # Fetch customer
    cust = db.query(Customer).first()
    assert cust is not None

    # Create a project
    project_payload = {
        "title": "Sprint 7 Launch Project",
        "customer_id": str(cust.id),
        "budget": 20000000.0,
        "revenue": 22000000.0,
        "quotation_status": "Draft",
        "program_status": "Inquiry",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": "2026-08-01",
        "event_date_end": "2026-08-03"
    }
    create_res = client.post("/api/v1/projects", json=project_payload, headers=admin_headers)
    assert create_res.status_code == 201
    proj_id = create_res.json()["id"]

    # Retrieve project detail, check readiness scores are initialized
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=admin_headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["required_instruments_count"] == 4
    assert detail_data["completed_required_instruments_count"] == 0
    assert detail_data["instrument_completion_rate"] == 0.0
    
    # 2. Update status of CL to Done, check completed_date is set to today
    instruments = detail_data["instruments"]
    cl_inst = next(i for i in instruments if i["instrument_type"] == "CL")
    cl_id = cl_inst["id"]
    
    patch_res = client.patch(
        f"/api/v1/projects/{proj_id}/instruments/{cl_id}",
        json={"status": "Done"},
        headers=admin_headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "Done"
    assert patch_res.json()["completed_date"] == str(date.today())

    # 3. Update status of CL to In Progress, check completed_date is NOT cleared (retains today's date)
    patch_res = client.patch(
        f"/api/v1/projects/{proj_id}/instruments/{cl_id}",
        json={"status": "In Progress"},
        headers=admin_headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["status"] == "In Progress"
    assert patch_res.json()["completed_date"] == str(date.today())

    # 4. Set status of CL to Need Revision, verify revision warning is triggered
    patch_res = client.patch(
        f"/api/v1/projects/{proj_id}/instruments/{cl_id}",
        json={"status": "Need Revision"},
        headers=admin_headers
    )
    assert patch_res.status_code == 200
    
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=admin_headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert detail_data["revision_required_count"] == 1
    warnings = detail_data["validation_warnings"]
    assert any("requires revision" in w for w in warnings)

    # 5. Set due date in the past, verify overdue warning
    yesterday = date.today() - timedelta(days=1)
    patch_res = client.patch(
        f"/api/v1/projects/{proj_id}/instruments/{cl_id}",
        json={"due_date": str(yesterday)},
        headers=admin_headers
    )
    assert patch_res.status_code == 200
    
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=admin_headers)
    detail_data = detail_res.json()
    assert detail_data["overdue_instruments_count"] == 1
    warnings = detail_data["validation_warnings"]
    assert any("is overdue" in w for w in warnings)

    # 6. PNL sensitivity behavior checking:
    # First update PNL document_url as admin
    pnl_inst = next(i for i in instruments if i["instrument_type"] == "PNL")
    pnl_id = pnl_inst["id"]
    patch_res = client.patch(
        f"/api/v1/projects/{proj_id}/instruments/{pnl_id}",
        json={"document_url": "https://drive.google.com/sensitive-pnl-sheet"},
        headers=admin_headers
    )
    assert patch_res.status_code == 200
    assert patch_res.json()["document_url"] == "https://drive.google.com/sensitive-pnl-sheet"

    # Create a Staff user to verify masking
    staff_role = db.query(Role).filter(Role.name == "Staff").first()
    assert staff_role is not None
    staff_email = "test-staff@onespirit.asia"
    existing_staff = db.query(User).filter(User.email == staff_email).first()
    if not existing_staff:
        staff_create = UserCreate(
            email=staff_email,
            password="OneSpirit2026!Staff",
            full_name="Staff Tester",
            is_active=True,
            role_id=staff_role.id
        )
        create_user(db, staff_create)
    
    # Login as Staff
    staff_login = client.post(
        "/api/v1/auth/login",
        data={"username": staff_email, "password": "OneSpirit2026!Staff"}
    )
    assert staff_login.status_code == 200
    staff_token = staff_login.json()["access_token"]
    staff_headers = {"Authorization": f"Bearer {staff_token}"}

    # Query project detail as Staff, check that PNL document_url is masked (None)
    staff_detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=staff_headers)
    assert staff_detail_res.status_code == 200
    staff_detail_data = staff_detail_res.json()
    
    staff_pnl = next(i for i in staff_detail_data["instruments"] if i["instrument_type"] == "PNL")
    assert staff_pnl["document_url"] is None
    
    # Query instruments list as Staff, verify it is masked
    staff_insts_res = client.get(f"/api/v1/projects/{proj_id}/instruments", headers=staff_headers)
    assert staff_insts_res.status_code == 200
    staff_pnl_in_list = next(i for i in staff_insts_res.json() if i["instrument_type"] == "PNL")
    assert staff_pnl_in_list["document_url"] is None
