"""Pydantic-схемы для User."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from api_service.schemas.role import RoleRead


class UserCreate(BaseModel):
    """Регистрация нового пользователя."""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)


class UserRead(BaseModel):
    """Пользователь — ответ клиенту."""
    id: int
    username: str
    email: str
    role_id: int
    created_at: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserReadWithRole(UserRead):
    """Пользователь с ролью — для админа."""
    role: RoleRead | None = None


class UserUpdate(BaseModel):
    """Обновление пользователя."""
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=4, max_length=100)
    is_active: bool | None = None
    role_id: int | None = None