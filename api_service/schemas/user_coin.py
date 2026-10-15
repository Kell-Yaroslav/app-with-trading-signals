from datetime import datetime
from pydantic import BaseModel, ConfigDict
from api_service.schemas.coin import CoinRead


class UserCoinCreate(BaseModel):
    coin_id: int


class UserCoinRead(BaseModel):
    id: int
    user_id: int
    coin_id: int
    added_at: datetime
    coin: CoinRead | None = None

    model_config = ConfigDict(from_attributes=True)