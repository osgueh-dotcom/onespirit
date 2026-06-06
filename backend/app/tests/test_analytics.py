import pytest
from datetime import date
from uuid import UUID
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.core.database import Base
from app.core.deps import get_db
from app.modules.auth.service import seed_roles_and_admin
from app.modules.auth.models import User, Role
from app.modules.crm.models import Customer
from app.modules.event_sources.models import EventSource
from app.modules.projects.models import Project
from app.modules.documents.models import Document
from app.modules.finance.models import Invoice, Payment

# Use in-memory SQLite for extremely fast unit tests
SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test_analytics.db"

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

def test_analytics_endpoint_empty(client):
    # 1. Login to retrieve bearer token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get analytics when DB has no projects
    response = client.get("/api/v1/dashboard/analytics", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["executive"]["total_projects"] == 0
    assert data["executive"]["total_inquiry"] == 0
    assert data["executive"]["inquiry_stage_count"] == 0
    assert data["executive"]["confirmed_revenue"] == 0.0
    assert data["executive"]["revenue_received"] == 0.0
    assert data["executive"]["collection_rate"] == 0.0
    assert data["executive"]["outstanding_amount"] == 0.0
    assert data["executive"]["deal_rate"] == 0.0
    assert data["executive"]["total_data_quality_issues"] == 0
    assert data["target"]["achievement_rate"] == 0.0
    assert len(data["po_performance"]) == 0
    assert len(data["pm_workload"]) == 0
    assert data["data_quality"]["missing_po"] == 0
    
    # Verify empty instrument summary
    assert data["instrument_summary"]["missing_cl"] == 0
    assert data["instrument_summary"]["missing_ros"] == 0
    assert data["instrument_summary"]["missing_ck"] == 0
    assert data["instrument_summary"]["missing_pnl"] == 0
    assert data["instrument_summary"]["instruments_need_revision"] == 0
    assert data["instrument_summary"]["instruments_overdue"] == 0
    assert data["instrument_summary"]["average_instrument_completion_rate"] == 0.0

def test_analytics_calculations(client, db: Session):
    # 1. Login to retrieve bearer token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Retrieve roles/users/sources/customers to associate with test projects
    admin_user = db.query(User).filter(User.email == "admin@onespirit.asia").first()
    assert admin_user is not None
    
    # Create PO and PM placeholder users
    staff_role = db.query(Role).filter(Role.name == "Staff").first()
    po_user = User(
        email="po_test@onespirit.local",
        full_name="Program Owner Test",
        initial_code="POT",
        hashed_password="hashed_placeholder_123",
        role_id=staff_role.id
    )
    pm_user = User(
        email="pm_test@onespirit.local",
        full_name="Program Manager Test",
        initial_code="PMT",
        hashed_password="hashed_placeholder_123",
        role_id=staff_role.id
    )
    db.add(po_user)
    db.add(pm_user)
    db.commit()
    
    # Create Customer
    customer = Customer(
        company_name="Analytics Client Corp",
        category="Corporate",
        address="Jakarta"
    )
    db.add(customer)
    db.commit()
    
    # Create Event Source
    event_source = EventSource(
        source_type="Hotel",
        vendor_name="Hotel Hilton",
        sales_name="Hilton Sales",
        contact="081234567"
    )
    db.add(event_source)
    db.commit()
    
    # Create projects with varying states
    # Project 1: Deal & Confirmed status, budget 100M
    proj1 = Project(
        title="Project One (Deal)",
        budget=100000000.0,
        quotation_status="Signed & Deal",
        program_status="Confirmed",
        payment_status="Invoice Sent",
        project_status="Active",
        customer_id=customer.id,
        event_source_id=event_source.id,
        created_by_id=admin_user.id,
        program_owner_id=po_user.id,
        program_manager_id=pm_user.id,
        event_date_start=date(2026, 6, 1),
        event_date_end=date(2026, 6, 2)
    )
    
    # Project 2: Inquiry status, budget 50M (potential, not confirmed)
    proj2 = Project(
        title="Project Two (Inquiry)",
        budget=50000000.0,
        quotation_status="Draft",
        program_status="Inquiry",
        payment_status="Not Invoiced",
        project_status="Open",
        customer_id=customer.id,
        created_by_id=admin_user.id,
        event_date_start=date(2026, 6, 10)
    )
    
    # Project 3: Canceled status, budget 30M
    proj3 = Project(
        title="Project Three (Canceled)",
        budget=30000000.0,
        quotation_status="Cancel",
        program_status="Cancel",
        payment_status="Not Invoiced",
        project_status="Canceled",
        customer_id=customer.id,
        created_by_id=admin_user.id,
        program_owner_id=po_user.id,
        event_date_start=date(2027, 7, 1)
    )
    
    db.add_all([proj1, proj2, proj3])
    db.commit()
    
    # Add a document to Project 1 so it isn't flagged as documentation_missing
    doc1 = Document(
        project_id=proj1.id,
        title="Signed Quotation",
        file_path="contracts/deal.pdf",
        file_type="pdf",
        storage_type="local"
    )
    db.add(doc1)
    db.commit()
    
    # Add mock invoice and payment for Project 1 (Confirmed revenue = 100M, collected = 60M)
    inv1 = Invoice(
        project_id=proj1.id,
        invoice_number="INV-2026-001",
        amount=100000000.0,
        issue_date=date(2026, 6, 2),
        due_date=date(2026, 7, 2),
        status="paid"
    )
    db.add(inv1)
    db.commit()
    
    pay1 = Payment(
        invoice_id=inv1.id,
        amount=60000000.0,
        payment_date=date(2026, 6, 3),
        reference_number="PAY-REF-001",
        status="approved"
    )
    db.add(pay1)
    db.commit()
    
    # 3. Query all projects analytics
    res = client.get("/api/v1/dashboard/analytics", headers=headers)
    assert res.status_code == 200
    data = res.json()
    
    exec_data = data["executive"]
    assert exec_data["total_projects"] == 3
    assert exec_data["total_inquiry"] == 3
    assert exec_data["inquiry_stage_count"] == 1
    assert exec_data["total_deal"] == 1
    assert exec_data["total_cancel"] == 1
    assert exec_data["potential_revenue"] == 180000000.0
    assert exec_data["confirmed_revenue"] == 100000000.0
    assert exec_data["revenue_received"] == 60000000.0
    assert exec_data["collection_rate"] == 60.0
    assert exec_data["outstanding_amount"] == 40000000.0
    assert exec_data["deal_rate"] == pytest.approx(33.33, 0.1)
    assert exec_data["cancel_rate"] == pytest.approx(33.33, 0.1)
    assert exec_data["revenue_conversion_rate"] == pytest.approx(55.55, 0.1)
    assert exec_data["total_data_quality_issues"] == 8

    # Target checks
    target_data = data["target"]
    assert target_data["year"] == 2025
    assert target_data["revenue_target"] == 9200000000.0
    assert target_data["achievement_rate"] == pytest.approx(100000000.0 / 9200000000.0 * 100.0, 0.1)
    
    # Quotation status distribution check
    quot_data = data["quotation"]
    assert quot_data["count_by_status"]["Signed & Deal"] == 1
    assert quot_data["count_by_status"]["Draft"] == 1
    assert quot_data["count_by_status"]["Cancel"] == 1
    
    # PO Performance check
    po_perf = data["po_performance"]
    assert len(po_perf) == 1
    assert po_perf[0]["initial_code"] == "POT"
    assert po_perf[0]["total_projects"] == 2
    assert po_perf[0]["deal_count"] == 1
    assert po_perf[0]["cancel_count"] == 1
    assert po_perf[0]["confirmed_revenue"] == 100000000.0
    
    # PM Workload check
    pm_work = data["pm_workload"]
    assert len(pm_work) == 1
    assert pm_work[0]["initial_code"] == "PMT"
    assert pm_work[0]["total_projects"] == 1
    assert pm_work[0]["active_count"] == 1
    
    # Data Quality Audits check
    dq_data = data["data_quality"]
    assert dq_data["missing_po"] == 1
    assert dq_data["missing_pm"] == 2
    assert dq_data["cancel_without_reason"] == 1
    assert dq_data["documentation_missing"] == 2
    assert dq_data["unknown_source"] == 2
    
    # Verify instrument summary metrics
    inst_summary = data["instrument_summary"]
    assert inst_summary["missing_cl"] == 1
    assert inst_summary["missing_pnl"] == 1
    assert inst_summary["missing_ros"] == 0
    assert inst_summary["missing_ck"] == 0
    assert inst_summary["instruments_need_revision"] == 0
    assert inst_summary["instruments_overdue"] == 0
    assert inst_summary["average_instrument_completion_rate"] == 0.0
    
    # 4. Test Filters
    # Filter by Year 2026
    res_year = client.get("/api/v1/dashboard/analytics?year=2026", headers=headers)
    assert res_year.json()["executive"]["total_projects"] == 2
    
    # Filter by Month 7 (July)
    res_month = client.get("/api/v1/dashboard/analytics?month=7", headers=headers)
    assert res_month.json()["executive"]["total_projects"] == 1
    
    # Filter by PO ID
    res_po = client.get(f"/api/v1/dashboard/analytics?po_id={po_user.id}", headers=headers)
    assert res_po.json()["executive"]["total_projects"] == 2
