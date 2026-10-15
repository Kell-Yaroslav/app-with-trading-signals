"""Эндпоинты для подписок на монеты."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User
from api_service.dependencies import get_session, get_current_user
from api_service.schemas.user_coin import UserCoinRead, UserCoinCreate


router = APIRouter(prefix="/api/user-coins", tags=["user-coins"])


@router.get("/me", response_model=list[UserCoinRead])
def get_my_subscriptions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Мои подписки."""
    return crud.get_user_coins(session, current_user.id)


@router.post("/me", response_model=UserCoinRead, status_code=status.HTTP_201_CREATED)
def subscribe_to_coin(
    data: UserCoinCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Подписаться на монету."""
    uc = crud.add_coin_to_user(session, current_user.id, data.coin_id)
    if not uc:
        raise HTTPException(
            status_code=400, detail="Подписка уже есть или монета не найдена"
        )
    return uc


@router.delete("/me/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
def unsubscribe_from_coin(
    coin_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Отписаться от монеты."""
    ok = crud.remove_coin_from_user(session, current_user.id, coin_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return None


@router.get("/{user_id}", response_model=list[UserCoinRead])
def get_subscriptions_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Подписки пользователя: trader — свои, admin — любого."""
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return crud.get_user_coins(session, user_id)