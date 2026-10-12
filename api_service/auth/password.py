"""Хеширование и проверка паролей."""
from passlib.context import CryptContext

# Контекст для хеширования через bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хеширует пароль через bcrypt.

    Принимает: пароль в открытом виде.
    Возвращает: хеш (60 символов).
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Проверяет пароль против хеша.

    Принимает: пароль в открытом виде, хеш из БД.
    Возвращает: True если пароль верный.
    """
    return pwd_context.verify(plain_password, password_hash)