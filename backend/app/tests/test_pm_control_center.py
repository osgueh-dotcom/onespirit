import pytest
from datetime import date, timedelta
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.models import User
from app.modules.auth.service import seed_roles_and_admin
from app.modules.crm.models import Customer
from app.modules.projects.models import Project, ProjectInstrument

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test_pm_control_center.db"

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
        company_name="PM Control Center Client",
        category="Corporate",
        address="Operations St 55"
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

def test_pm_control_center_endpoint(client, db):
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

    # Get admin user for assignment
    admin_user = db.query(User).filter(User.email == "admin@onespirit.asia").first()
    assert admin_user is not None

    # 2. Create projects
    # A project happening today with low readiness (missing CL/ROS/CK)
    today_date = date.today()
    p1_payload = {
        "title": "PM Control Event Today",
        "customer_id": str(cust.id),
        "budget": 25000000.0,
        "revenue": 30000000.0,
        "quotation_status": "Signed & Deal",
        "program_status": "Ready",
        "payment_status": "Not Invoiced",
        "project_status": "Active",
        "event_date_start": today_date.isoformat(),
        "event_date_end": today_date.isoformat(),
        "program_manager_id": str(admin_user.id),
        "program_owner_id": str(admin_user.id)
    }
    res1 = client.post("/api/v1/projects", json=p1_payload, headers=headers)
    assert res1.status_code == 201
    p1_id = res1.json()["id"]

    # A project happening in 5 days (upcoming)
    p2_payload = {
        "title": "PM Control Event Upcoming",
        "customer_id": str(cust.id),
        "budget": 45000000.0,
        "revenue": 50000000.0,
        "quotation_status": "Draft",
        "program_status": "Preparation",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": (today_date + timedelta(days=5)).isoformat(),
        "event_date_end": (today_date + timedelta(days=6)).isoformat(),
        "program_manager_id": str(admin_user.id)
    }
    res2 = client.post("/api/v1/projects", json=p2_payload, headers=headers)
    assert res2.status_code == 201
    p2_id = res2.json()["id"]

    # Set up an overdue instrument for p2
    p2_db_inst = db.query(ProjectInstrument).filter(
        ProjectInstrument.project_id == UUID(p2_id),
        ProjectInstrument.instrument_type == "ROS"
    ).first()
    assert p2_db_inst is not None
    p2_db_inst.due_date = today_date - timedelta(days=2)
    p2_db_inst.status = "In Progress"
    db.commit()

    # 3. Request PM Control Center data
    cc_res = client.get("/api/v1/dashboard/pm-control-center", headers=headers)
    assert cc_res.status_code == 200
    cc_data = cc_res.json()

    # Verify response layout
    assert "summary" in cc_data
    assert "upcoming_events" in cc_data
    assert "not_ready_projects" in cc_data
    assert "overdue_instruments" in cc_data
    assert "need_revision_instruments" in cc_data
    assert "pm_workload" in cc_data
    assert "priority_actions" in cc_data

    # Check summaries
    summary = cc_data["summary"]
    assert summary["total_active_projects"] >= 2
    assert summary["events_today"] >= 1
    assert summary["upcoming_events_7_days"] >= 1
    
    # Overdue instrument checks
    assert summary["overdue_instruments"] >= 1
    overdue_insts = cc_data["overdue_instruments"]
    assert len(overdue_insts) >= 1
    assert overdue_insts[0]["instrument_type"] == "ROS"
    assert overdue_insts[0]["days_overdue"] == 2

    # Priority Action Checks
    actions = cc_data["priority_actions"]
    assert len(actions) > 0
    # The event today with low readiness score should be Critical or High priority
    has_critical = any(a["priority_level"] == "Critical" for a in actions)
    has_high = any(a["priority_level"] == "High" for a in actions)
    assert has_critical or has_high

    # PM Workload Checks
    workload = cc_data["pm_workload"]
    assert len(workload) > 0
    assert workload[0]["pm_name"] == admin_user.full_name
    assert workload[0]["total_projects"] >= 2
    assert workload[0]["upcoming_events_7_days"] >= 1
    assert workload[0]["overdue_instruments"] >= 1

    # 4. Try filtering by event window
    cc_today = client.get("/api/v1/dashboard/pm-control-center?event_window=today", headers=headers)
    assert cc_today.status_code == 200
    today_events = cc_today.json()["upcoming_events"]
    # We should have at least the today event
    assert len(today_events) >= 1
