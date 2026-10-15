from pydantic import BaseModel, ConfigDict, Field


class SettingBase(BaseModel):
    ema_period: int = Field(gt=0)
    target_pct: float = Field(gt=0)
    stop_pct: float = Field(gt=0)
    bollinger_period: int = Field(gt=0)
    bollinger_std: float = Field(gt=0)
    check_interval: int = Field(gt=0)


class SettingCreate(SettingBase):
    pass


class SettingUpdate(BaseModel):
    ema_period: int | None = Field(default=None, gt=0)
    target_pct: float | None = Field(default=None, gt=0)
    stop_pct: float | None = Field(default=None, gt=0)
    bollinger_period: int | None = Field(default=None, gt=0)
    bollinger_std: float | None = Field(default=None, gt=0)
    check_interval: int | None = Field(default=None, gt=0)


class SettingRead(SettingBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)