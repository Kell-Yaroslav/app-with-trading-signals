"""Точка входа API Service.

Запуск:
    uvicorn api_service.main:app --reload
"""
from fastapi import FastAPI

from api_service.api import auth, users, roles

app = FastAPI(
    title="Crypto Monitor API",
    description="REST API для системы мониторинга криптовалютного рынка",
    version="0.1.0",
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(roles.router)

@app.get("/")
def root():
    """Корневой эндпоинт — проверка, что сервер работает."""
    return {"status": "ok", "message": "Crypto Monitor API"}


@app.get("/health")
def health_check():
    """Проверка работоспособности."""
    return {"status": "healthy"}