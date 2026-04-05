from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.models.user import Role


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    role: Role | None = None
    is_active: bool | None = None


class UserListParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)
    role: Role | None = None
    is_active: bool | None = None
    search: str | None = None
