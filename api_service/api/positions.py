"""Эндпоинты для работы с позициями."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User, Position, UserCoin
from api_service.dependencies import get_session, get_current_user
from api_service.schemas.position import PositionRead, PositionCreate, PositionClose


router = APIRouter(prefix="/api/positions", tags=["positions"])


@router.get("/me", response_model=list[PositionRead])
def get_my_positions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Мои позиции."""
    return crud.get_user_positions(session, current_user.id)


@router.post("/me", response_model=PositionRead, status_code=status.HTTP_201_CREATED)
def open_position(
    data: PositionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Открыть позицию."""
    uc = session.get(UserCoin, data.usercoin_id)
    if not uc or uc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Подписка вам не принадлежит")
    return crud.create_position(
        session, data.usercoin_id, entry_price=data.entry_price
    )


@router.post("/{position_id}/close", response_model=PositionRead)
def close_position(
    position_id: int,
    data: PositionClose,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Закрыть позицию."""
    pos = session.get(Position, position_id)
    if not pos:
        raise HTTPException(status_code=404, detail="Позиция не найдена")
    uc = session.get(UserCoin, pos.usercoin_id)
    if current_user.role.name != "admin" and uc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    closed = crud.close_position(
        session, position_id, data.exit_price, data.exit_type
    )
    if not closed:
        raise HTTPException(status_code=400, detail="Позиция уже закрыта")
    return closed


@router.get("/{user_id}", response_model=list[PositionRead])
def get_positions_by_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Позиции пользователя: trader — свои, admin — любого."""
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return crud.get_user_positions(session, user_id)