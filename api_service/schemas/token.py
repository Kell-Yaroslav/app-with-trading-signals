"""Pydantic-схемы для JWT-токенов."""
from pydantic import BaseModel


class Token(BaseModel):
    """Ответ на логин — JWT-токен."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные внутри JWT-токена."""
    username: str | None = None
    user_id: int | None = None
    role: str | None = None