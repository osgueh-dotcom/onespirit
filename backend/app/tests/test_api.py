import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin

# Use in-memory SQLite for extremely fast unit tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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
    # 1. Get Creative Role from DB
    from app.modules.auth.models import Role
    creative_role = db.query(Role).filter(Role.name == "Creative").first()
    assert creative_role is not None

    # 2. Login as Super Admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    admin_token = login_response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    # 3. Create a Creative User
    creative_email = "creative@onespirit.asia"
    creative_payload = {
        "email": creative_email,
        "password": "CreativeUser2026!",
        "full_name": "Creative Designer",
        "role_id": str(creative_role.id)
    }
    create_res = client.post("/api/v1/auth/users", json=creative_payload, headers=admin_headers)
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

    # 5. Login as Creative
    creative_login = client.post(
        "/api/v1/auth/login",
        data={"username": creative_email, "password": "CreativeUser2026!"}
    )
    assert creative_login.status_code == 200
    creative_token = creative_login.json()["access_token"]
    creative_headers = {"Authorization": f"Bearer {creative_token}"}

    # 6. Attempt to transition status to "confirmed" (should be 403 Forbidden for Creative)
    transition_res = client.post(
        f"/api/v1/projects/{proj_id}/transition?new_status=confirmed&notes=Try+transition",
        headers=creative_headers
    )
    assert transition_res.status_code == 403

    # 7. Transition as Admin (should succeed)
    transition_admin_res = client.post(
        f"/api/v1/projects/{proj_id}/transition?new_status=confirmed&notes=Admin+transition",
        headers=admin_headers
    )
    assert transition_admin_res.status_code == 200
    assert transition_admin_res.json()["status"] == "confirmed"
