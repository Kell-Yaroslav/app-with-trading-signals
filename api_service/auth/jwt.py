"""Создание и проверка JWT-токенов."""
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from api_service.config import settings


def create_access_token(data: dict[str, Any]) -> str:
    """
    Создаёт JWT-токен.

    Принимает: словарь с данными (sub, user_id, role).
    Возвращает: закодированный JWT-токен (строка).
    """
    to_encode = data.copy()

    # Время истечения токена
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRE_MINUTES
    )
    to_encode["exp"] = expire

    # Кодируем токен
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Декодирует JWT-токен.

    Принимает: JWT-строку.
    Возвращает: словарь с данными или None, если токен неверный.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None