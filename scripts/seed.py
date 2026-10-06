from app.database import SessionLocal, engine
from app.models import Base
from app import crud


def seed():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        # Проверяем, не заполнена ли БД
        if crud.get_role_by_name(session, "trader"):
            print("БД уже заполнена. Пропускаем seed.")
            return

        # 1. Роли
        role_trader = crud.create_role(session, "trader", "Трейдер")
        role_admin  = crud.create_role(session, "admin",  "Администратор")

        # 2. Пользователи
        admin = crud.create_user(session, "admin", "admin@mail.ru", "hash_a", role_admin.id)
        ivan  = crud.create_user(session, "ivan",  "ivan@mail.ru",  "hash_i", role_trader.id)
        petr  = crud.create_user(session, "petr",  "petr@mail.ru",  "hash_p", role_trader.id)

        # 3. Настройки
        crud.create_setting(session, admin.id, ema_period=20, target_pct=2.0, stop_pct=1.0)
        crud.create_setting(session, ivan.id,  ema_period=20, target_pct=3.0, stop_pct=1.5)
        crud.create_setting(session, petr.id,  ema_period=50, target_pct=2.5, stop_pct=2.0)

        # 4. Монеты
        btc = crud.create_coin(session, "BTCUSDT", "Bitcoin",  "kucoin")
        eth = crud.create_coin(session, "ETHUSDT", "Ethereum", "kucoin")
        sol = crud.create_coin(session, "SOLUSDT", "Solana",   "bybit")

        # 5. Подписки
        crud.add_coin_to_user(session, ivan.id, btc.id)
        crud.add_coin_to_user(session, ivan.id, eth.id)
        crud.add_coin_to_user(session, petr.id, btc.id)
        crud.add_coin_to_user(session, petr.id, sol.id)
        crud.add_coin_to_user(session, admin.id, btc.id)

        # 6. Позиции
        ivan_btc = crud.get_user_coins(session, ivan.id)[0]
        petr_btc = crud.get_user_coins(session, petr.id)[0]

        p1 = crud.create_position(session, ivan_btc.id, entry_price=60000)
        p2 = crud.create_position(session, petr_btc.id, entry_price=60500)

        crud.close_position(session, p1.id, exit_price=62000, exit_type="TARGET")

        print("Тестовые данные успешно добавлены")
    finally:
        session.close()


if __name__ == "__main__":
    seed()