"""Pydantic-схемы для Coin."""
from pydantic import BaseModel, ConfigDict, Field


class CoinRead(BaseModel):
    """Монета — ответ клиенту."""
    id: int
    symbol: str
    name: str
    exchange: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CoinCreate(BaseModel):
    """Создание монеты — только админ."""
    symbol: str = Field(min_length=3, max_length=20)
    name: str = Field(min_length=1, max_length=100)
    exchange: str = Field(pattern="^(kucoin|bybit)$")