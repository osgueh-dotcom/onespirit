import logging
import secrets
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app.core.database import db_commit_safety
from app.core.config import settings
from app.modules.auth.models import Role, User
from app.modules.auth.schemas import UserCreate, UserUpdate, RoleCreate

logger = logging.getLogger(__name__)

def get_user(db: Session, user_id: str):
    try:
        user_uuid = user_id if isinstance(user_id, UUID) else UUID(str(user_id))
    except ValueError:
        return None
    return db.query(User).filter(User.id == user_uuid, User.deleted_at == None).first()

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
        role_id=user_in.role_id,
        initial_code=user_in.initial_code
    )
    db.add(db_user)
    db_commit_safety(db)
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data = user_in.model_dump(exclude_unset=True)
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
    staff_permissions = ["crm:read", "projects:read", "projects:write", "events:read", "events:write", "tasks:read", "tasks:write", "documents:read", "documents:write"]
    role_definitions = {
        "Super Admin": ["admin"],
        "Admin": ["admin"],
        "Management": ["crm:read", "crm:write", "projects:read", "projects:write", "events:read", "events:write", "finance:read", "finance:write", "documents:read", "documents:write", "tasks:read", "tasks:write"],
        "PO": ["crm:read", "crm:write", "projects:read", "projects:write", "events:read", "finance:read", "documents:read", "documents:write", "tasks:read"],
        "PM": ["crm:read", "projects:read", "projects:write", "events:read", "events:write", "documents:read", "documents:write", "tasks:read", "tasks:write"],
        "Finance": ["projects:read", "finance:read", "finance:write", "documents:read"],
        "Staff": staff_permissions
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
    admin_email = settings.ADMIN_EMAIL
    admin_user = get_user_by_email(db, admin_email)
    if not admin_user:
        admin_role = created_roles["Super Admin"]
        admin_create = UserCreate(
            email=admin_email,
            password=settings.ADMIN_PASSWORD,
            full_name="System Super Admin",
            is_active=True,
            role_id=admin_role.id
        )
        create_user(db, admin_create)
        logger.info("Seeded Super Admin user: %s", admin_email)

    # 2b. Demo User
    if settings.SEED_DEMO_USER:
        demo_email = settings.DEMO_USER_EMAIL or settings.DEMO_EMAIL
        demo_password = settings.DEMO_USER_PASSWORD or settings.DEMO_PASSWORD
        demo_user = get_user_by_email(db, demo_email)
        if not demo_password:
            logger.warning("Demo user seed skipped because no demo password is configured.")
        elif not demo_user:
            demo_role = created_roles["Management"]
            demo_create = UserCreate(
                email=demo_email,
                password=demo_password,
                full_name="Client Demo User",
                is_active=True,
                role_id=demo_role.id
            )
            create_user(db, demo_create)
            logger.info("Seeded Demo user: %s", demo_email)

    # 3. Seed placeholder internal users for Excel PO/PM verification
    initials_to_seed = [
        "JIP", "AR", "BR", "SBK", "SR", "TF", "JC", "SYS", "MWB", "RA", "OME", "SB", "UT", "MDL"
    ]
    staff_role = created_roles.get("Staff")
    if staff_role and settings.SEED_PLACEHOLDER_USERS:
        for initials in initials_to_seed:
            existing_user = db.query(User).filter(User.initial_code == initials, User.deleted_at == None).first()
            if not existing_user:
                user_create = UserCreate(
                    email=f"{initials.lower()}@onespirit.asia",
                    password=f"{secrets.token_urlsafe(32)}Aa1!#",
                    full_name=initials,
                    is_active=False,
                    role_id=staff_role.id,
                    initial_code=initials
                )
                create_user(db, user_create)
                logger.info("Seeded placeholder staff user: %s", initials)
