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
from app.modules.projects.models import Project
from app.modules.event_sources.models import EventSource
from app.tests.db_utils import sqlite_test_url

SQLALCHEMY_DATABASE_URL = sqlite_test_url("test_po_control_center.db")

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
        company_name="PO Control Center Client",
        category="Corporate",
        address="Commercial St 99"
    )
    db_session.add(cust)

    # Create event source
    es = EventSource(
        source_type="Hotel",
        vendor_name="Grand Hyatt Jakarta",
        sales_name="Indra Setiawan"
    )
    db_session.add(es)

    db_session.commit()
    db_session.refresh(cust)
    db_session.refresh(es)
    
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

def test_po_control_center_endpoint(client, db):
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

    es = db.query(EventSource).first()
    assert es is not None

    # Get admin user for assignment
    admin_user = db.query(User).filter(User.email == "admin@onespirit.asia").first()
    assert admin_user is not None
    # Assign initial code to admin for PO performance testing
    admin_user.initial_code = "ADM"
    db.commit()

    today_date = date.today()

    # 2. Create sample projects
    # P1: Signed & Deal without budget (Critical risk)
    p1_payload = {
        "title": "Deal Without Budget",
        "customer_id": str(cust.id),
        "budget": 0.0,
        "revenue": 0.0,
        "quotation_status": "Signed & Deal",
        "program_status": "Confirmed",
        "payment_status": "Not Invoiced",
        "project_status": "Active",
        "event_date_start": today_date.isoformat(),
        "event_date_end": today_date.isoformat(),
        "program_manager_id": str(admin_user.id),
        "program_owner_id": str(admin_user.id),
        "event_source_id": str(es.id)
    }
    res1 = client.post("/api/v1/projects", json=p1_payload, headers=headers)
    assert res1.status_code == 201
    
    # P2: Proposal Sent, high value, event date approaching (H-5)
    p2_payload = {
        "title": "Approaching High Value Proposal",
        "customer_id": str(cust.id),
        "budget": 120000000.0,  # Rp 120M (High value >= 100M)
        "revenue": 120000000.0,
        "quotation_status": "Sent",
        "program_status": "Inquiry",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": (today_date + timedelta(days=5)).isoformat(),
        "event_date_end": (today_date + timedelta(days=6)).isoformat(),
        "program_manager_id": str(admin_user.id),
        "program_owner_id": str(admin_user.id),
        "event_source_id": str(es.id)
    }
    res2 = client.post("/api/v1/projects", json=p2_payload, headers=headers)
    assert res2.status_code == 201

    # P3: Canceled without reason (Critical risk)
    p3_payload = {
        "title": "Cancel Missing Reason",
        "customer_id": str(cust.id),
        "budget": 50000000.0,
        "revenue": 50000000.0,
        "quotation_status": "Cancel",
        "program_status": "Cancel",
        "payment_status": "Not Invoiced",
        "project_status": "Canceled",
        "event_date_start": (today_date + timedelta(days=20)).isoformat(),
        "program_owner_id": str(admin_user.id)
    }
    res3 = client.post("/api/v1/projects", json=p3_payload, headers=headers)
    assert res3.status_code == 201

    # 3. Request PO Control Center data (include_canceled=True to retrieve P3)
    cc_res = client.get("/api/v1/dashboard/po-control-center?include_canceled=true", headers=headers)
    assert cc_res.status_code == 200
    cc_data = cc_res.json()

    # Verify Response Layout
    assert "summary" in cc_data
    assert "quotation_summary" in cc_data
    assert "revenue_summary" in cc_data
    assert "follow_up_priorities" in cc_data
    assert "owned_projects" in cc_data
    assert "po_performance" in cc_data
    assert "source_contribution" in cc_data
    assert "commercial_risks" in cc_data

    # Check Summary metrics
    summary = cc_data["summary"]
    assert summary["total_owned_projects"] >= 3
    assert summary["total_deal"] >= 1
    assert summary["total_cancel"] >= 1
    assert summary["deal_rate"] > 0
    assert summary["cancel_rate"] > 0
    assert summary["active_projects"] >= 2
    assert summary["pending_quotation_projects"] >= 1
    assert summary["follow_up_needed_projects"] >= 2
    assert summary["cancelled_projects"] >= 1
    assert summary["outstanding_payment"] == 0.0
    assert summary["commercial_risk_count"] >= 2

    # Verify potential and confirmed revenue logic
    rev = cc_data["revenue_summary"]
    # Potential = P1(0) + P2(120M) + P3(50M) = 170,000,000.0
    # Confirmed = P1 (Signed & Deal, 0.0) = 0.0
    assert rev["potential_revenue"] == 170000000.0
    assert rev["confirmed_revenue"] == 0.0

    # Verify Commercial Risks detection
    risks = cc_data["commercial_risks"]
    assert len(risks["cancel_without_reason"]) >= 1
    assert len(risks["signed_deal_without_budget"]) >= 1
    # P3 has no event source
    assert len(risks["missing_source"]) >= 1

    # Verify Follow-up priorities
    priorities = cc_data["follow_up_priorities"]
    assert len(priorities) > 0
    # P1 (Deal without budget) should be critical
    has_critical = any(p["priority_level"] == "Critical" and "Rp 0" in p["reason"] for p in priorities)
    assert has_critical

    # P2 (Approaching Sent proposal H-5) should be high priority
    has_high = any(p["priority_level"] == "High" and "H-5" in p["reason"] for p in priorities)
    assert has_high

    # PO performance checks
    po_perf = cc_data["po_performance"]
    assert len(po_perf) > 0
    assert po_perf[0]["initial_code"] == "ADM"
    assert po_perf[0]["total_projects"] >= 3

    # Source contribution checks
    source_contrib = cc_data["source_contribution"]
    assert len(source_contrib) > 0
    hotel_contrib = [s for s in source_contrib if s["source_type"] == "Hotel"]
    assert len(hotel_contrib) >= 1
    assert hotel_contrib[0]["vendor_name"] == "Grand Hyatt Jakarta"
    assert hotel_contrib[0]["sales_name"] == "Indra Setiawan"

    # 4. Request with filters (e.g. quotation_status="Signed & Deal")
    filtered_res = client.get("/api/v1/dashboard/po-control-center?quotation_status=Signed%20%26%20Deal", headers=headers)
    assert filtered_res.status_code == 200
    filtered_data = filtered_res.json()
    assert filtered_data["summary"]["total_owned_projects"] == 1
    assert filtered_data["owned_projects"][0]["quotation_status"] == "Signed & Deal"
