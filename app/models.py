from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey,
    Numeric, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


# 1. Role
class Role(Base):
    __tablename__ = "roles"

    id          = Column(Integer, primary_key=True)
    name        = Column(String(20), unique=True, nullable=False)
    description = Column(String(255))

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


# 2. User
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True)
    username      = Column(String(50), unique=True, nullable=False)
    email         = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id       = Column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active     = Column(Boolean, default=True, nullable=False)

    role       = relationship("Role", back_populates="users")
    setting    = relationship("Setting", back_populates="user", uselist=False,
                              cascade="all, delete-orphan")
    user_coins = relationship("UserCoin", back_populates="user",
                              cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_role", "role_id"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role_id={self.role_id})>"


# 3. Setting
class Setting(Base):
    __tablename__ = "settings"

    id               = Column(Integer, primary_key=True)
    user_id          = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                              unique=True, nullable=False)
    ema_period       = Column(Integer, nullable=False, default=20)
    target_pct       = Column(Numeric(5, 2), nullable=False, default=2.00)
    stop_pct         = Column(Numeric(5, 2), nullable=False, default=1.00)
    bollinger_period = Column(Integer, nullable=False, default=20)
    bollinger_std    = Column(Numeric(4, 2), nullable=False, default=2.00)
    check_interval   = Column(Integer, nullable=False, default=300)

    user = relationship("User", back_populates="setting")

    __table_args__ = (
        CheckConstraint("ema_period > 0",       name="ck_settings_ema"),
        CheckConstraint("target_pct > 0",       name="ck_settings_target"),
        CheckConstraint("stop_pct > 0",         name="ck_settings_stop"),
        CheckConstraint("bollinger_period > 0", name="ck_settings_boll_period"),
        CheckConstraint("bollinger_std > 0",    name="ck_settings_boll_std"),
        CheckConstraint("check_interval > 0",   name="ck_settings_check"),
    )

    def __repr__(self):
        return f"<Setting(user_id={self.user_id}, ema={self.ema_period})>"


# 4. Coin
class Coin(Base):
    __tablename__ = "coins"

    id        = Column(Integer, primary_key=True)
    symbol    = Column(String(20), unique=True, nullable=False)
    name      = Column(String(100), nullable=False)
    exchange  = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    user_coins = relationship("UserCoin", back_populates="coin",
                              cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("exchange IN ('kucoin','bybit')", name="ck_coins_exchange"),
        Index("idx_coins_symbol", "symbol"),
    )

    def __repr__(self):
        return f"<Coin(id={self.id}, symbol='{self.symbol}', exchange='{self.exchange}')>"


# 5. UserCoin
class UserCoin(Base):
    __tablename__ = "user_coins"

    id       = Column(Integer, primary_key=True)
    user_id  = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    coin_id  = Column(Integer, ForeignKey("coins.id", ondelete="CASCADE"), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user      = relationship("User", back_populates="user_coins")
    coin      = relationship("Coin", back_populates="user_coins")
    positions = relationship("Position", back_populates="usercoin",
                             cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("user_id", "coin_id", name="uq_user_coin"),
        Index("idx_user_coins_user", "user_id"),
        Index("idx_user_coins_coin", "coin_id"),
    )

    def __repr__(self):
        return f"<UserCoin(user_id={self.user_id}, coin_id={self.coin_id})>"


# 6. Position
class Position(Base):
    __tablename__ = "positions"

    id             = Column(Integer, primary_key=True)
    usercoin_id    = Column(Integer, ForeignKey("user_coins.id", ondelete="CASCADE"),
                            nullable=False)
    entry_price    = Column(Numeric(20, 8), nullable=False)
    exit_price     = Column(Numeric(20, 8))
    profit_percent = Column(Numeric(10, 4))
    exit_type      = Column(String(10))
    entry_time     = Column(DateTime, nullable=False)
    exit_time      = Column(DateTime)

    usercoin = relationship("UserCoin", back_populates="positions")

    __table_args__ = (
        CheckConstraint("exit_type IN ('TARGET','STOP','MANUAL')",
                        name="ck_positions_exit_type"),
        Index("idx_positions_usercoin", "usercoin_id"),
    )

    def __repr__(self):
        return f"<Position(id={self.id}, usercoin_id={self.usercoin_id}, entry={self.entry_price})>"