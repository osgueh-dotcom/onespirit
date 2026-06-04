from typing import Optional, List
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.core.database import db_commit_safety
from app.modules.auth.models import Role, User
from app.modules.auth.schemas import UserCreate, UserUpdate, RoleCreate

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id, User.deleted_at == None).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email, User.deleted_at == None).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.deleted_at == None).offset(skip).limit(limit).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_pw = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name,
        is_active=user_in.is_active,
        role_id=user_in.role_id
    )
    db.add(db_user)
    db_commit_safety(db)
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.dict(exclude_unset=True)
    if "password" in user_data and user_data["password"]:
        db_user.hashed_password = get_password_hash(user_data["password"])
        del user_data["password"]
    
    for field, value in user_data.items():
        setattr(db_user, field, value)
        
    db_commit_safety(db)
    db.refresh(db_user)
    return db_user

def get_roles(db: Session):
    return db.query(Role).all()

def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def create_role(db: Session, role_in: RoleCreate) -> Role:
    db_role = Role(name=role_in.name, permissions=role_in.permissions)
    db.add(db_role)
    db_commit_safety(db)
    db.refresh(db_role)
    return db_role

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def seed_roles_and_admin(db: Session):
    """Seed base roles and super admin user if they don't exist"""
    # 1. Base Roles definitions
    role_definitions = {
        "Super Admin": ["admin"],
        "Director": ["crm:read", "projects:read", "projects:write", "events:read", "finance:read", "documents:read"],
        "Sales": ["crm:read", "crm:write", "projects:read", "projects:write", "finance:read", "documents:read"],
        "Project Manager": ["crm:read", "projects:read", "projects:write", "events:read", "events:write", "tasks:read", "tasks:write", "documents:read", "documents:write"],
        "Finance": ["projects:read", "finance:read", "finance:write", "documents:read"],
        "Creative": ["projects:read", "events:read", "tasks:read", "tasks:write", "documents:read", "documents:write"],
        "Documentation Team": ["projects:read", "documents:read", "documents:write"]
    }
    
    created_roles = {}
    for name, perms in role_definitions.items():
        existing_role = get_role_by_name(db, name)
        if not existing_role:
            role_in = RoleCreate(name=name, permissions=perms)
            db_role = create_role(db, role_in)
            created_roles[name] = db_role
        else:
            created_roles[name] = existing_role
            # Update permissions if they changed
            existing_role.permissions = perms
            db_commit_safety(db)

    # 2. Super Admin User
    admin_email = "admin@onespirit.asia"
    admin_user = get_user_by_email(db, admin_email)
    if not admin_user:
        admin_role = created_roles["Super Admin"]
        admin_create = UserCreate(
            email=admin_email,
            password="OneSpirit2026!",
            full_name="System Super Admin",
            is_active=True,
            role_id=admin_role.id
        )
        create_user(db, admin_create)
        print("Successfully seeded Super Admin user: admin@onespirit.asia / OneSpirit2026!")
