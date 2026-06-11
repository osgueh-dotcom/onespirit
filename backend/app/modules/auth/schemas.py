from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator
import re

def check_password_complexity(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password minimal 8 karakter.")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password harus mengandung huruf besar.")
    if not re.search(r"[a-z]", v):
        raise ValueError("Password harus mengandung huruf kecil.")
    if not re.search(r"\d", v):
        raise ValueError("Password harus mengandung angka.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
        raise ValueError("Password harus mengandung simbol.")
    return v

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

# Role schemas
class RoleBase(BaseModel):
    name: str
    permissions: List[str]

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role_id: UUID
    initial_code: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return check_password_complexity(v)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[UUID] = None
    is_active: Optional[bool] = None
    initial_code: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return check_password_complexity(v)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminUserCreate(UserBase):
    password: str
    role_id: Optional[UUID] = None
    role: Optional[str] = None
    role_name: Optional[str] = None
    initial_code: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return check_password_complexity(v)

    @model_validator(mode="after")
    def validate_role_reference(self) -> "AdminUserCreate":
        if not self.role_id and not self.role and not self.role_name:
            raise ValueError("Role wajib dipilih.")
        return self

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return check_password_complexity(v)

    @model_validator(mode="after")
    def validate_passwords(self) -> "ChangePasswordRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Password baru dan konfirmasi tidak sama.")
        if self.current_password == self.new_password:
            raise ValueError("Password baru tidak boleh sama dengan password lama.")
        return self

class AdminPasswordResetRequest(BaseModel):
    new_password: str
    confirm_password: str

    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        return check_password_complexity(v)

    @model_validator(mode="after")
    def validate_passwords(self) -> "AdminPasswordResetRequest":
        if self.new_password != self.confirm_password:
            raise ValueError("Password baru dan konfirmasi tidak sama.")
        return self

class UserStatusUpdate(BaseModel):
    is_active: bool

class MessageResponse(BaseModel):
    message: str

class UserResponse(UserBase):
    id: UUID
    role_id: UUID
    role: Optional[RoleResponse] = None
    initial_code: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
