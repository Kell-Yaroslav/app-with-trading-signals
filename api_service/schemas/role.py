"""Pydantic-схемы для Role."""
from pydantic import BaseModel, ConfigDict


class RoleRead(BaseModel):
    """Роль — ответ клиенту."""
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)