import pytest
from datetime import date
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin
from app.modules.crm.models import Customer
from app.modules.projects.models import Project

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test_readiness_gates.db"

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
    
    # Create test customer
    cust = Customer(
        company_name="Readiness Client Ltd",
        category="Corporate",
        address="Readiness St 10"
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

def test_readiness_gate_endpoints(client, db):
    # 1. Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    cust = db.query(Customer).first()
    assert cust is not None

    # 2. Create project
    project_payload = {
        "title": "Readiness Gate Testing",
        "customer_id": str(cust.id),
        "budget": 10000000.0,
        "revenue": 12000000.0,
        "quotation_status": "Draft",
        "program_status": "Inquiry",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": "2026-10-01",
        "event_date_end": "2026-10-03"
    }
    create_res = client.post("/api/v1/projects", json=project_payload, headers=headers)
    assert create_res.status_code == 201
    proj_id = create_res.json()["id"]

    # 3. Test Preview Check Endpoint (POST /readiness/check)
    check_payload = {
        "status_type": "program_status",
        "target_status": "Ready"
    }
    check_res = client.post(f"/api/v1/projects/{proj_id}/readiness/check", json=check_payload, headers=headers)
    assert check_res.status_code == 200
    check_data = check_res.json()
    assert check_data["project_id"] == proj_id
    assert check_data["status_type"] == "program_status"
    assert check_data["target_status"] == "Ready"
    assert check_data["allowed"] is True
    assert check_data["severity"] == "warning"
    # Should flag missing CL, ROS, CK, PNL document warnings
    assert len(check_data["warnings"]) > 0

    # 4. Test Blocker transition scenario (Trying to run a Canceled event)
    # First, cancel the project status
    cancel_res = client.patch(
        f"/api/v1/projects/{proj_id}/status",
        json={"status_type": "project_status", "new_status": "Canceled", "notes": "Canceled test"},
        headers=headers
    )
    assert cancel_res.status_code == 200

    # Verify that transitioning program_status to "Running" is blocked
    block_check_res = client.post(
        f"/api/v1/projects/{proj_id}/readiness/check",
        json={"status_type": "program_status", "target_status": "Running"},
        headers=headers
    )
    assert block_check_res.json()["allowed"] is False
    assert block_check_res.json()["severity"] == "critical"
    assert "Canceled" in "".join(block_check_res.json()["blockers"])

    # Actually patching it without force should return 409 Conflict
    patch_fail = client.patch(
        f"/api/v1/projects/{proj_id}/status",
        json={"status_type": "program_status", "new_status": "Running", "notes": "Run it anyway", "force": False},
        headers=headers
    )
    assert patch_fail.status_code == 409
    assert "blocked" in patch_fail.json()["detail"]["message"].lower()

    # Patching it with force=True should succeed
    patch_success = client.patch(
        f"/api/v1/projects/{proj_id}/status",
        json={"status_type": "program_status", "new_status": "Running", "notes": "Forcing run", "force": True},
        headers=headers
    )
    assert patch_success.status_code == 200
    assert patch_success.json()["program_status"] == "Running"

    # 5. Check Dashboard Analytics Response Schema compatibility
    dash_res = client.get("/api/v1/dashboard/analytics", headers=headers)
    assert dash_res.status_code == 200
    dash_data = dash_res.json()
    assert "readiness_summary" in dash_data
    assert dash_data["readiness_summary"]["projects_ready_count"] is not None
    assert dash_data["readiness_summary"]["average_readiness_score"] is not None
