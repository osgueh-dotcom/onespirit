from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import deps
from app.core.security import create_access_token
from app.modules.auth import service, models, schemas
from app.core.activity import log_activity

router = APIRouter(prefix="/auth", tags=["Authentication"])

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

@router.get("/users", response_model=List[schemas.UserResponse])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.PermissionChecker(["admin", "crm:read"]))
):
    """Retrieve the list of users (Admins or CRM readers only)"""
    return service.get_users(db, skip=skip, limit=limit)

@router.post("/users", response_model=schemas.UserResponse)
def create_new_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: models.User = Depends(deps.PermissionChecker(["admin"]))
):
    """Create a new user (Super Admin only)"""
    existing_user = service.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists in the system.",
        )
    db_user = service.create_user(db, user_in=user_in)
    log_activity(
        db,
        user_id=str(current_user.id),
        action="user_registered",
        entity_type="user",
        entity_id=db_user.id,
        details={"email": db_user.email, "full_name": db_user.full_name}
    )
    return db_user

@router.get("/roles", response_model=List[schemas.RoleResponse])
def read_roles(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user)
):
    """Retrieve the list of roles"""
    return service.get_roles(db)
