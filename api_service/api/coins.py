"""Эндпоинты для работы с монетами."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud
from app.models import User, Coin
from api_service.dependencies import get_session, get_current_user, require_admin
from api_service.schemas.coin import CoinRead, CoinCreate


router = APIRouter(prefix="/api/coins", tags=["coins"])


@router.get("", response_model=list[CoinRead])
def get_all_coins(session: Session = Depends(get_session)):
    """Список всех монет."""
    return crud.get_all_coins(session)


@router.get("/{coin_id}", response_model=CoinRead)
def get_coin_by_id(coin_id: int, session: Session = Depends(get_session)):
    """Монета по id."""
    coin = session.get(Coin, coin_id)
    if not coin:
        raise HTTPException(status_code=404, detail="Монета не найдена")
    return coin


@router.post("", response_model=CoinRead, status_code=status.HTTP_201_CREATED)
def create_coin(
    coin_data: CoinCreate,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Создать монету — только админ."""
    existing = crud.get_coin_by_symbol(session, coin_data.symbol)
    if existing:
        raise HTTPException(status_code=400, detail="Монета уже существует")
    return crud.create_coin(
        session=session,
        symbol=coin_data.symbol,
        name=coin_data.name,
        exchange=coin_data.exchange,
    )


@router.delete("/{coin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coin(
    coin_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Удалить монету — только админ."""
    coin = session.get(Coin, coin_id)
    if not coin:
        raise HTTPException(status_code=404, detail="Монета не найдена")
    crud.delete_coin(session, coin_id)
    return None