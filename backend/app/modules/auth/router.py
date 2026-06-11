from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import deps
from app.core.security import create_access_token, verify_password
from app.modules.auth import service, models, schemas
from app.core.activity import log_activity

router = APIRouter(prefix="/auth", tags=["Authentication"])

ROLE_ALIASES = {
    "super_admin": "Super Admin",
    "super admin": "Super Admin",
    "admin": "Super Admin",
    "management": "Management",
    "finance": "Finance",
    "po": "Staff",
    "pm": "Staff",
    "staff": "Staff",
    "demo": "Management",
}


def resolve_role(db: Session, user_in: schemas.AdminUserCreate) -> models.Role:
    if user_in.role_id:
        role = db.query(models.Role).filter(models.Role.id == user_in.role_id).first()
    else:
        requested_role = user_in.role or user_in.role_name or ""
        normalized_role = ROLE_ALIASES.get(requested_role.strip().lower(), requested_role.strip())
        role = service.get_role_by_name(db, normalized_role)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role tidak valid.",
        )
    return role


def is_admin_user(user: models.User) -> bool:
    return bool(user.role and "admin" in (user.role.permissions or []))


def active_admin_count(db: Session) -> int:
    users = db.query(models.User).filter(
        models.User.deleted_at == None,
        models.User.is_active == True
    ).all()
    return sum(1 for user in users if is_admin_user(user))

@router.post("/login", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, retrieve a JWT access token"""
    user = service.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # Central activity logging for successful login
    log_activity(
        db,
        user_id=str(user.id),
        action="user_login",
        entity_type="user",
        entity_id=user.id,
        details={"email": user.email}
    )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }

@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user)
):
    """Retrieve the logged in user profile"""
    return current_user

@router.patch("/me/password", response_model=schemas.MessageResponse)
def change_own_password(
    *,
    db: Session = Depends(deps.get_db),
    payload: schemas.ChangePasswordRequest,
    current_user: models.User = Depends(deps.get_current_user)
):
    """Allow the current user to change their own password."""
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password lama tidak sesuai.",
        )

    service.update_user(
        db,
        current_user,
        schemas.UserUpdate(password=payload.new_password)
    )
    log_activity(
        db,
        user_id=str(current_user.id),
        action="password_changed",
        entity_type="user",
        entity_id=current_user.id,
        details={"email": current_user.email}
    )
    return {"message": "Password berhasil diperbarui."}

@router.get("/users", response_model=List[schemas.UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.PermissionChecker(["admin"]))
):
    """Retrieve the list of users for admin user management."""
    return service.get_users(db, skip=skip, limit=limit)

@router.get("/users/options", response_model=List[schemas.UserResponse])
def read_user_options(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.PermissionChecker(["admin", "crm:read", "projects:read"]))
):
    """Retrieve safe user reference data for workflow filters and assignments."""
    return service.get_users(db, skip=skip, limit=limit)

@router.post("/users", response_model=schemas.UserResponse)
def create_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.AdminUserCreate,
    current_user: models.User = Depends(deps.PermissionChecker(["admin"]))
):
    """Create a new user (admin only)"""
    existing_user = service.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah digunakan.",
        )
    role = resolve_role(db, user_in)
    db_user = service.create_user(
        db,
        user_in=schemas.UserCreate(
            email=user_in.email,
            full_name=user_in.full_name,
            is_active=user_in.is_active,
            password=user_in.password,
            role_id=role.id,
            initial_code=user_in.initial_code
        )
    )
    log_activity(
        db,
        user_id=str(current_user.id),
        action="user_registered",
        entity_type="user",
        entity_id=db_user.id,
        details={"email": db_user.email, "full_name": db_user.full_name}
    )
    return db_user

@router.patch("/users/{user_id}/password", response_model=schemas.MessageResponse)
def reset_user_password(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
    payload: schemas.AdminPasswordResetRequest,
    current_user: models.User = Depends(deps.PermissionChecker(["admin"]))
):
    """Allow an admin to reset another user's password."""
    target_user = service.get_user(db, user_id=user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan.",
        )

    service.update_user(
        db,
        target_user,
        schemas.UserUpdate(password=payload.new_password)
    )
    log_activity(
        db,
        user_id=str(current_user.id),
        action="user_password_reset",
        entity_type="user",
        entity_id=target_user.id,
        details={"email": target_user.email}
    )
    return {"message": "Password user berhasil diperbarui."}

@router.patch("/users/{user_id}/status", response_model=schemas.UserResponse)
def update_user_status(
    *,
    user_id: str,
    db: Session = Depends(deps.get_db),
    payload: schemas.UserStatusUpdate,
    current_user: models.User = Depends(deps.PermissionChecker(["admin"]))
):
    """Activate or deactivate a user without deleting historical workflow data."""
    target_user = service.get_user(db, user_id=user_id)
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan.",
        )

    if target_user.id == current_user.id and not payload.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Anda tidak dapat menonaktifkan akun sendiri.",
        )

    if is_admin_user(target_user) and target_user.is_active and not payload.is_active and active_admin_count(db) <= 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Super Admin terakhir tidak boleh dinonaktifkan.",
        )

    updated_user = service.update_user(
        db,
        target_user,
        schemas.UserUpdate(is_active=payload.is_active)
    )
    log_activity(
        db,
        user_id=str(current_user.id),
        action="user_status_changed",
        entity_type="user",
        entity_id=updated_user.id,
        details={"email": updated_user.email, "is_active": updated_user.is_active}
    )
    return updated_user

@router.get("/roles", response_model=List[schemas.RoleResponse])
def read_roles(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Retrieve the list of roles"""
    return service.get_roles(db)
