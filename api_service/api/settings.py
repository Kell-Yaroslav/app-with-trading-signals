"""Эндпоинты для работы с настройками."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from api_service.dependencies import get_session, get_current_user
from api_service.schemas.setting import SettingRead, SettingCreate, SettingUpdate


router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/me", response_model=SettingRead)
def get_my_settings(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Мои настройки."""
    setting = crud.get_setting_by_user(session, current_user.id)
    if not setting:
        raise HTTPException(status_code=404, detail="Настройки не найдены")
    return setting


@router.post("/me", response_model=SettingRead, status_code=status.HTTP_201_CREATED)
def create_my_settings(
    data: SettingCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Создать свои настройки."""
    existing = crud.get_setting_by_user(session, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Настройки уже существуют")
    return crud.create_setting(session, current_user.id, **data.model_dump())


@router.put("/me", response_model=SettingRead)
def update_my_settings(
    data: SettingUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Обновить свои настройки."""
    updated = crud.update_setting(
        session, current_user.id, **data.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Настройки не найдены")
    return updated


@router.get("/{user_id}", response_model=SettingRead)
def get_settings_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Настройки пользователя: trader — свои, admin — любого."""
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    setting = crud.get_setting_by_user(session, user_id)
    if not setting:
        raise HTTPException(status_code=404, detail="Настройки не найдены")
    return setting