from sqlalchemy import Boolean, Column, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import BaseModelMixin

class Role(Base, BaseModelMixin):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, index=True, nullable=False)
    permissions = Column(JSON, nullable=False, default=list)  # List of permission strings

    users = relationship("User", back_populates="role")

class User(Base, BaseModelMixin):
    __tablename__ = "users"

    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    role_id = Column(ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False)
    role = relationship("Role", back_populates="users")
    initial_code = Column(String(10), unique=True, index=True, nullable=True)
