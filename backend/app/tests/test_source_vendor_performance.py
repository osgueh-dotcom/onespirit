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

SQLALCHEMY_DATABASE_URL = "sqlite:////tmp/test_source_vendor.db"

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
        company_name="Source Vendor Client",
        category="Corporate",
        address="Performance Way 77"
    )
    db_session.add(cust)

    # Create event sources
    es1 = EventSource(
        source_type="Hotel",
        vendor_name="Ritz-Carlton Mega Kuningan",
        sales_name="Yudha"
    )
    es2 = EventSource(
        source_type="Partner",
        vendor_name="Mulberry Events",
        sales_name="Tina"
    )
    db_session.add(es1)
    db_session.add(es2)

    db_session.commit()
    db_session.refresh(cust)
    db_session.refresh(es1)
    db_session.refresh(es2)
    
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

def test_source_vendor_performance_endpoint(client, db):
    # 1. Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@onespirit.asia", "password": "OneSpirit2026!"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch seed models
    cust = db.query(Customer).first()
    es_hotel = db.query(EventSource).filter(EventSource.source_type == "Hotel").first()
    es_partner = db.query(EventSource).filter(EventSource.source_type == "Partner").first()
    admin_user = db.query(User).filter(User.email == "admin@onespirit.asia").first()

    today_date = date.today()

    # 2. Add projects to test calculations
    # Proyek 1: Hotel source, Deal (Confirmed), Budget Rp 150M
    p1 = {
        "title": "Hotel Deal Event",
        "customer_id": str(cust.id),
        "budget": 150000000.0,
        "revenue": 150000000.0,
        "quotation_status": "Signed & Deal",
        "program_status": "Confirmed",
        "payment_status": "Not Invoiced",
        "project_status": "Active",
        "event_date_start": today_date.isoformat(),
        "event_date_end": today_date.isoformat(),
        "program_owner_id": str(admin_user.id),
        "event_source_id": str(es_hotel.id)
    }
    client.post("/api/v1/projects", json=p1, headers=headers)

    # Proyek 2: Hotel source, Batal, Budget Rp 50M
    p2 = {
        "title": "Hotel Cancelled Event",
        "customer_id": str(cust.id),
        "budget": 50000000.0,
        "revenue": 50000000.0,
        "quotation_status": "Cancel",
        "program_status": "Cancel",
        "payment_status": "Not Invoiced",
        "project_status": "Canceled",
        "event_date_start": today_date.isoformat(),
        "program_owner_id": str(admin_user.id),
        "event_source_id": str(es_hotel.id)
    }
    client.post("/api/v1/projects", json=p2, headers=headers)

    # Proyek 3: Direct source (No EventSource ID), Pending Quotation (Draft), Budget Rp 80M
    p3 = {
        "title": "Direct Inquiry",
        "customer_id": str(cust.id),
        "budget": 80000000.0,
        "revenue": 80000000.0,
        "quotation_status": "Draft",
        "program_status": "Inquiry",
        "payment_status": "Not Invoiced",
        "project_status": "Open",
        "event_date_start": today_date.isoformat(),
        "program_owner_id": str(admin_user.id)
    }
    client.post("/api/v1/projects", json=p3, headers=headers)

    # Request Endpoint
    response = client.get("/api/v1/dashboard/source-vendor-performance?include_canceled=true", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Validate schema fields presence
    assert "summary" in data
    assert "source_performance" in data
    assert "vendor_performance" in data
    assert "po_source_performance" in data
    assert "risk_alerts" in data
    assert "data_quality" in data

    # Validate summary aggregates
    summary = data["summary"]
    assert summary["total_projects_analyzed"] >= 3
    # Confirmed revenue = Ritz-Carlton event (150M)
    assert summary["total_confirmed_revenue"] == 150000000.0
    # Potential revenue = Ritz-Carlton (150M) + Cancelled (50M) + Direct (80M) = 280M
    assert summary["total_potential_revenue"] == 280000000.0
    assert summary["total_sources"] >= 2  # Hotel and Direct

    # Validate source performance detail
    sources = data["source_performance"]
    hotel_src = [s for s in sources if s["source_type"] == "Hotel"][0]
    assert hotel_src["total_projects"] == 2
    assert hotel_src["confirmed_projects"] == 1
    assert hotel_src["cancelled_projects"] == 1
    assert hotel_src["potential_revenue"] == 200000000.0
    assert hotel_src["confirmed_revenue"] == 150000000.0
    assert hotel_src["conversion_rate"] == 50.0  # 1 confirmed out of 2
    assert hotel_src["cancel_rate"] == 50.0      # 1 cancelled out of 2

    # Validate vendor performance detail
    vendors = data["vendor_performance"]
    assert len(vendors) > 0
    ritz_vendor = [v for v in vendors if v["vendor_name"] == "Ritz-Carlton Mega Kuningan"][0]
    assert ritz_vendor["total_projects"] == 2
    assert ritz_vendor["active_projects"] == 1
    assert ritz_vendor["confirmed_projects"] == 1
    assert ritz_vendor["cancelled_projects"] == 1

    # Validate data quality report
    dq = data["data_quality"]
    assert dq["missing_source_count"] >= 1  # Project 3 has no event source ID
    assert dq["limited_vendor_data"] is True
