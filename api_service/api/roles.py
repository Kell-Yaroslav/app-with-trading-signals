"""Эндпоинты для работы с ролями."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User, Role
from api_service.dependencies import get_session, get_current_user
from api_service.schemas.role import RoleRead


router = APIRouter(prefix="/api/roles", tags=["roles"])


@router.get("", response_model=list[RoleRead])
def get_all_roles(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Все роли.

    Доступно любому авторизованному пользователю.
    """
    return crud.get_all_roles(session)


@router.get("/{role_id}", response_model=RoleRead)
def get_role_by_id(
    role_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Роль по id."""
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Роль не найдена",
        )
    return role