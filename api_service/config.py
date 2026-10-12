"""Конфигурация API Service."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Настройки приложения, читаются из .env."""

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))


settings = Settings()