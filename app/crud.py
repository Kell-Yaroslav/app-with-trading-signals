from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Role, User, Setting, Coin, UserCoin, Position


# ─────────── Role ───────────
def create_role(session: Session, name: str, description: str = None) -> Role:
    role = Role(name=name, description=description)
    session.add(role)
    session.commit()
    session.refresh(role)
    return role


def get_role_by_name(session: Session, name: str) -> Role | None:
    return session.scalar(select(Role).where(Role.name == name))


def get_all_roles(session: Session) -> list[Role]:
    return list(session.scalars(select(Role)))


def delete_role(session: Session, role_id: int) -> bool:
    role = session.get(Role, role_id)
    if not role:
        return False
    session.delete(role)
    session.commit()
    return True


# ─────────── User ───────────
def create_user(session: Session, username: str, email: str,
                password_hash: str, role_id: int) -> User:
    user = User(username=username, email=email,
                password_hash=password_hash, role_id=role_id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> User | None:
    return session.scalar(select(User).where(User.username == username))


def get_all_users(session: Session) -> list[User]:
    return list(session.scalars(select(User)))


def update_user(session: Session, user_id: int, **kwargs) -> User | None:
    user = session.get(User, user_id)
    if not user:
        return None
    for key, value in kwargs.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True


# ─────────── Setting ───────────
def create_setting(session: Session, user_id: int, **kwargs) -> Setting:
    setting = Setting(user_id=user_id, **kwargs)
    session.add(setting)
    session.commit()
    session.refresh(setting)
    return setting


def get_setting_by_user(session: Session, user_id: int) -> Setting | None:
    return session.scalar(select(Setting).where(Setting.user_id == user_id))


def update_setting(session: Session, user_id: int, **kwargs) -> Setting | None:
    setting = get_setting_by_user(session, user_id)
    if not setting:
        return None
    for key, value in kwargs.items():
        setattr(setting, key, value)
    session.commit()
    session.refresh(setting)
    return setting


# ─────────── Coin ───────────
def create_coin(session: Session, symbol: str, name: str, exchange: str) -> Coin:
    coin = Coin(symbol=symbol, name=name, exchange=exchange)
    session.add(coin)
    session.commit()
    session.refresh(coin)
    return coin


def get_coin_by_symbol(session: Session, symbol: str) -> Coin | None:
    return session.scalar(select(Coin).where(Coin.symbol == symbol))


def get_all_coins(session: Session) -> list[Coin]:
    return list(session.scalars(select(Coin).where(Coin.is_active == True)))


def delete_coin(session: Session, coin_id: int) -> bool:
    coin = session.get(Coin, coin_id)
    if not coin:
        return False
    session.delete(coin)
    session.commit()
    return True


# ─────────── UserCoin ───────────
def add_coin_to_user(session: Session, user_id: int, coin_id: int) -> UserCoin | None:
    exists = session.scalar(
        select(UserCoin).where(UserCoin.user_id == user_id, UserCoin.coin_id == coin_id)
    )
    if exists:
        return None
    uc = UserCoin(user_id=user_id, coin_id=coin_id)
    session.add(uc)
    session.commit()
    session.refresh(uc)
    return uc


def get_user_coins(session: Session, user_id: int) -> list[UserCoin]:
    return list(session.scalars(select(UserCoin).where(UserCoin.user_id == user_id)))


def remove_coin_from_user(session: Session, user_id: int, coin_id: int) -> bool:
    uc = session.scalar(
        select(UserCoin).where(UserCoin.user_id == user_id, UserCoin.coin_id == coin_id)
    )
    if not uc:
        return False
    session.delete(uc)
    session.commit()
    return True


# ─────────── Position ───────────
def create_position(session: Session, usercoin_id: int,
                    entry_price: float, entry_time: datetime | None = None) -> Position:
    pos = Position(
        usercoin_id=usercoin_id,
        entry_price=entry_price,
        entry_time=entry_time or datetime.utcnow(),
    )
    session.add(pos)
    session.commit()
    session.refresh(pos)
    return pos


def close_position(session: Session, position_id: int,
                   exit_price: float, exit_type: str) -> Position | None:
    pos = session.get(Position, position_id)
    if not pos or pos.exit_time is not None:
        return None
    pos.exit_price = exit_price
    pos.exit_time = datetime.utcnow()
    pos.exit_type = exit_type
    pos.profit_percent = float(
        (exit_price - float(pos.entry_price)) / float(pos.entry_price) * 100
    )
    session.commit()
    session.refresh(pos)
    return pos


def get_user_positions(session: Session, user_id: int) -> list[Position]:
    return list(session.scalars(
        select(Position)
        .join(UserCoin, Position.usercoin_id == UserCoin.id)
        .where(UserCoin.user_id == user_id)
    ))