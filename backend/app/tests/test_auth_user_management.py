import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.deps import get_db
from app.core.security import verify_password
from app.main import app
from app.modules.auth.models import User
from app.modules.auth.service import seed_roles_and_admin
from app.tests.db_utils import sqlite_test_url

SQLALCHEMY_DATABASE_URL = sqlite_test_url("test_auth_user_management.db")

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
    try:
        seed_roles_and_admin(db_session)
        yield db_session
    finally:
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
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def login(client, email="admin@onespirit.asia", password="OneSpirit2026!"):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def role_id_by_name(client, headers, role_name="Finance"):
    response = client.get("/api/v1/auth/roles", headers=headers)
    assert response.status_code == 200
    roles = response.json()
    return next(role["id"] for role in roles if role["name"] == role_name)


def test_admin_create_user_success_and_password_hash_not_returned(client, db):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)

    response = client.post(
        "/api/v1/auth/users",
        json={
            "email": "access_create@onespirit.asia",
            "full_name": "Access Create",
            "password": "AccessCreate2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "access_create@onespirit.asia"
    assert "hashed_password" not in data
    assert "password" not in data

    user = db.query(User).filter(User.email == "access_create@onespirit.asia").first()
    assert user is not None
    assert user.hashed_password != "AccessCreate2026!"
    assert verify_password("AccessCreate2026!", user.hashed_password)


def test_admin_create_user_rejects_duplicate_email(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    payload = {
        "email": "access_duplicate@onespirit.asia",
        "full_name": "Access Duplicate",
        "password": "AccessDuplicate2026!",
        "role_id": role_id,
        "is_active": True,
    }

    first_response = client.post("/api/v1/auth/users", json=payload, headers=admin_headers)
    second_response = client.post("/api/v1/auth/users", json=payload, headers=admin_headers)

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email sudah digunakan."


def test_create_user_denied_for_non_admin(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    finance_email = "access_finance@onespirit.asia"

    create_finance = client.post(
        "/api/v1/auth/users",
        json={
            "email": finance_email,
            "full_name": "Access Finance",
            "password": "AccessFinance2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )
    assert create_finance.status_code == 200

    finance_headers = login(client, finance_email, "AccessFinance2026!")
    denied_response = client.post(
        "/api/v1/auth/users",
        json={
            "email": "access_denied@onespirit.asia",
            "full_name": "Access Denied",
            "password": "AccessDenied2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=finance_headers,
    )

    assert denied_response.status_code == 403
    assert client.get("/api/v1/auth/users", headers=finance_headers).status_code == 403
    assert client.get("/api/v1/auth/users/options", headers=finance_headers).status_code == 200


def test_change_own_password_success(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    user_email = "access_password_success@onespirit.asia"

    create_response = client.post(
        "/api/v1/auth/users",
        json={
            "email": user_email,
            "full_name": "Access Password Success",
            "password": "OldPassword2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )
    assert create_response.status_code == 200

    user_headers = login(client, user_email, "OldPassword2026!")
    change_response = client.patch(
        "/api/v1/auth/me/password",
        json={
            "current_password": "OldPassword2026!",
            "new_password": "NewPassword2026!",
            "confirm_password": "NewPassword2026!",
        },
        headers=user_headers,
    )

    assert change_response.status_code == 200
    assert "berhasil" in change_response.json()["message"]
    assert client.post(
        "/api/v1/auth/login",
        data={"username": user_email, "password": "OldPassword2026!"},
    ).status_code == 400
    assert client.post(
        "/api/v1/auth/login",
        data={"username": user_email, "password": "NewPassword2026!"},
    ).status_code == 200


def test_change_own_password_fails_if_current_password_wrong(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    user_email = "access_password_wrong@onespirit.asia"

    create_response = client.post(
        "/api/v1/auth/users",
        json={
            "email": user_email,
            "full_name": "Access Password Wrong",
            "password": "WrongCurrent2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )
    assert create_response.status_code == 200

    user_headers = login(client, user_email, "WrongCurrent2026!")
    change_response = client.patch(
        "/api/v1/auth/me/password",
        json={
            "current_password": "NotTheCurrent2026!",
            "new_password": "AnotherPassword2026!",
            "confirm_password": "AnotherPassword2026!",
        },
        headers=user_headers,
    )

    assert change_response.status_code == 400
    assert change_response.json()["detail"] == "Password lama tidak sesuai."


def test_admin_reset_password(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    user_email = "access_reset@onespirit.asia"

    create_response = client.post(
        "/api/v1/auth/users",
        json={
            "email": user_email,
            "full_name": "Access Reset",
            "password": "BeforeReset2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    reset_response = client.patch(
        f"/api/v1/auth/users/{user_id}/password",
        json={
            "new_password": "AfterReset2026!",
            "confirm_password": "AfterReset2026!",
        },
        headers=admin_headers,
    )

    assert reset_response.status_code == 200
    assert client.post(
        "/api/v1/auth/login",
        data={"username": user_email, "password": "AfterReset2026!"},
    ).status_code == 200


def test_admin_can_deactivate_user_but_not_self(client):
    admin_headers = login(client)
    role_id = role_id_by_name(client, admin_headers)
    user_email = "access_status@onespirit.asia"

    create_response = client.post(
        "/api/v1/auth/users",
        json={
            "email": user_email,
            "full_name": "Access Status",
            "password": "AccessStatus2026!",
            "role_id": role_id,
            "is_active": True,
        },
        headers=admin_headers,
    )
    assert create_response.status_code == 200
    user_id = create_response.json()["id"]

    deactivate_response = client.patch(
        f"/api/v1/auth/users/{user_id}/status",
        json={"is_active": False},
        headers=admin_headers,
    )
    assert deactivate_response.status_code == 200
    assert deactivate_response.json()["is_active"] is False

    inactive_login = client.post(
        "/api/v1/auth/login",
        data={"username": user_email, "password": "AccessStatus2026!"},
    )
    assert inactive_login.status_code == 400

    me_response = client.get("/api/v1/auth/me", headers=admin_headers)
    assert me_response.status_code == 200
    self_deactivate_response = client.patch(
        f"/api/v1/auth/users/{me_response.json()['id']}/status",
        json={"is_active": False},
        headers=admin_headers,
    )
    assert self_deactivate_response.status_code == 400
