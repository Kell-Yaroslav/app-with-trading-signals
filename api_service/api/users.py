"""Эндпоинты для работы с пользователями."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from api_service.dependencies import get_session, get_current_user, require_admin
from api_service.schemas.user import UserRead, UserReadWithRole, UserUpdate
from api_service.auth.password import hash_password


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserRead)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Мой профиль.

    Требует JWT-токен в заголовке Authorization.
    Возвращает данные текущего пользователя.
    """
    return current_user


@router.get("/me/with-role", response_model=UserReadWithRole)
def get_my_profile_with_role(
    current_user: User = Depends(get_current_user),
):
    """Мой профиль с ролью."""
    return current_user


@router.get("", response_model=list[UserReadWithRole])
def get_all_users(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """
    Все пользователи — только для администратора.
    """
    return crud.get_all_users(session)


@router.get("/{user_id}", response_model=UserReadWithRole)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Пользователь по id.

    - Admin — любого пользователя.
    - Trader — только себя.
    """
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Обновить пользователя.

    - Admin — любого.
    - Trader — только себя (без role_id / is_active).
    """
    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    is_admin = current_user.role.name == "admin"
    is_self = current_user.id == user_id

    if not is_admin and not is_self:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещён",
        )

    # Trader не может менять role_id и is_active
    update_data = user_data.model_dump(exclude_unset=True)
    if not is_admin:
        update_data.pop("role_id", None)
        update_data.pop("is_active", None)

    # Если меняется пароль — хешируем
    if "password" in update_data:
        update_data["password_hash"] = hash_password(update_data.pop("password"))

    updated = crud.update_user(session, user_id, **update_data)
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """
    Удалить пользователя — только для администратора.
    """
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить самого себя",
        )

    user = crud.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    crud.delete_user(session, user_id)
    return None