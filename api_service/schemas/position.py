
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PositionCreate(BaseModel):
    usercoin_id: int
    entry_price: float = Field(gt=0)


class PositionClose(BaseModel):
    exit_price: float = Field(gt=0)
    exit_type: str = Field(pattern="^(TARGET|STOP|MANUAL)$")


class PositionRead(BaseModel):
    id: int
    usercoin_id: int
    entry_price: float
    exit_price: float | None
    profit_percent: float | None
    exit_type: str | None
    entry_time: datetime
    exit_time: datetime | None

    model_config = ConfigDict(from_attributes=True)