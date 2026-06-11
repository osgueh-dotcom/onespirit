import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin
from app.tests.db_utils import sqlite_test_url

# Use in-memory SQLite for extremely fast unit tests
SQLALCHEMY_DATABASE_URL = sqlite_test_url("test_api.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(scope="module")
def db():
    # Setup test tables
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    
    # Seed roles and admin
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

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "online"

def test_login_endpoint(client):
    # Try with seeded admin credentials
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_dashboard_endpoint(client):
    # 1. Login to retrieve bearer token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # 2. Query dashboard
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/dashboard", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "ongoing_projects" in data
    assert "pipeline_funnel" in data
    assert "monthly_trends" in data
    assert "team_workload" in data
    assert "recent_activities" in data

def test_password_complexity_validator(client):
    # 1. Login to retrieve bearer token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch role ID to assign to new user
    user_me_res = client.get("/api/v1/auth/me", headers=headers)
    assert user_me_res.status_code == 200
    role_id = user_me_res.json()["role_id"]

    # 2. Try creating user with weak password (e.g. no special char, short, etc.)
    weak_payloads = [
        {"email": "weak1@onespirit.asia", "password": "123", "full_name": "Weak One", "role_id": role_id},
        {"email": "weak2@onespirit.asia", "password": "weakpassword", "full_name": "Weak Two", "role_id": role_id},
        {"email": "weak3@onespirit.asia", "password": "WeakPassword123", "full_name": "Weak Three", "role_id": role_id},
    ]

    for payload in weak_payloads:
        res = client.post("/api/v1/auth/users", json=payload, headers=headers)
        assert res.status_code == 422

    # 3. Try creating user with strong password (meets all complexity rules)
    strong_payload = {
        "email": "strong@onespirit.asia",
        "password": "StrongPassword2026!",
        "full_name": "Strong User",
        "role_id": role_id
    }
    res = client.post("/api/v1/auth/users", json=strong_payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "strong@onespirit.asia"

def test_project_transition_gates(client, db):
    # 1. Get Finance Role from DB
    from app.modules.auth.models import Role
    finance_role = db.query(Role).filter(Role.name == "Finance").first()
    assert finance_role is not None

    # 2. Login as Super Admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Create a Finance User (to check 403 authorization boundary)
    finance_email = "finance_test@onespirit.asia"
    finance_payload = {
        "email": finance_email,
        "password": "FinanceUser2026!",
        "full_name": "Finance Officer",
        "role_id": str(finance_role.id)
    }
    create_res = client.post("/api/v1/auth/users", json=finance_payload, headers=admin_headers)
    assert create_res.status_code == 200

    # 4. Create a Customer and a Project
    cust_payload = {
        "company_name": "Test Transition Company",
        "category": "Corporate",
        "address": "Jakarta"
    }
    cust_res = client.post("/api/v1/customers", json=cust_payload, headers=admin_headers)
    assert cust_res.status_code == 201
    cust_id = cust_res.json()["id"]

    proj_payload = {
        "title": "Transition Test Project",
        "status": "inquiry",
        "customer_id": cust_id,
        "start_date": "2026-06-01",
        "end_date": "2026-06-02",
        "budget": 50000000
    }
    proj_res = client.post("/api/v1/projects", json=proj_payload, headers=admin_headers)
    assert proj_res.status_code == 201
    proj_id = proj_res.json()["id"]

    # 5. Login as Finance User
    finance_login = client.post(
        "/api/v1/auth/login",
        data={"username": finance_email, "password": "FinanceUser2026!"}
    )
    assert finance_login.status_code == 200
    finance_token = finance_login.json()["access_token"]
    finance_headers = {"Authorization": f"Bearer {finance_token}"}

    # 6. Attempt to transition status to "confirmed" (should be 403 Forbidden for Finance)
    transition_res = client.post(
        f"/api/v1/projects/{proj_id}/transition?new_status=confirmed&notes=Try+transition",
        headers=finance_headers
    )
    assert transition_res.status_code == 403

    # 7. Transition as Admin (should succeed)
    transition_admin_res = client.post(
        f"/api/v1/projects/{proj_id}/transition?new_status=confirmed&notes=Admin+transition",
        headers=admin_headers
    )
    assert transition_admin_res.status_code == 200
    assert transition_admin_res.json()["status"] == "confirmed"

def test_event_source_crud(client):
    # 1. Login to retrieve admin bearer token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Create Event Source
    payload = {
        "source_type": "Instagram",
        "vendor_name": "Test Vendor",
        "sales_name": "Test Sales",
        "contact": "0812345678",
        "notes": "Test notes"
    }
    create_res = client.post("/api/v1/event-sources", json=payload, headers=admin_headers)
    assert create_res.status_code == 201
    source_id = create_res.json()["id"]

    # 3. Read Event Source
    read_res = client.get(f"/api/v1/event-sources", headers=admin_headers)
    assert read_res.status_code == 200
    assert any(s["id"] == source_id for s in read_res.json())

    # 4. Update Event Source
    update_payload = {
        "source_type": "Web",
        "vendor_name": "Updated Vendor",
        "sales_name": "Updated Sales",
        "contact": "0812345678",
        "notes": "Updated notes"
    }
    update_res = client.put(f"/api/v1/event-sources/{source_id}", json=update_payload, headers=admin_headers)
    assert update_res.status_code == 200
    assert update_res.json()["source_type"] == "Web"

    # 5. Delete Event Source
    delete_res = client.delete(f"/api/v1/event-sources/{source_id}", headers=admin_headers)
    assert delete_res.status_code == 200

def test_generic_status_patch(client):
    # 1. Login as admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 2. Create Customer & Project
    cust_res = client.post("/api/v1/customers", json={"company_name": "Status Patch Client", "category": "Corporate"}, headers=admin_headers)
    cust_id = cust_res.json()["id"]

    proj_res = client.post("/api/v1/projects", json={
        "title": "Status Patch Project",
        "customer_id": cust_id,
        "budget": 10000000
    }, headers=admin_headers)
    proj_id = proj_res.json()["id"]

    # 3. Patch status generically
    patch_payload = {
        "status_type": "quotation_status",
        "new_status": "Signed & Deal",
        "notes": "Signed quotation agreement"
    }
    patch_res = client.patch(f"/api/v1/projects/{proj_id}/status", json=patch_payload, headers=admin_headers)
    assert patch_res.status_code == 200
    assert patch_res.json()["quotation_status"] == "Signed & Deal"

    # 4. Check timeline logs and validation warnings in detail view
    detail_res = client.get(f"/api/v1/projects/{proj_id}", headers=admin_headers)
    assert detail_res.status_code == 200
    detail_data = detail_res.json()
    assert any(log["status_type"] == "quotation_status" and log["new_status"] == "Signed & Deal" for log in detail_data["status_logs"])
    assert any(act["action"] == "quotation_status_changed" for act in detail_data["activity_logs"])
