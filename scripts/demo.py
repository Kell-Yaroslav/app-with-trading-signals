from app.database import SessionLocal
from app import crud


def demo():
    session = SessionLocal()
    try:
        print("=" * 60)
        print("ДЕМОНСТРАЦИЯ CRUD-ОПЕРАЦИЙ")
        print("=" * 60)

        print("\n[1] Все пользователи:")
        for u in crud.get_all_users(session):
            print(f"   id={u.id}, username={u.username}, role_id={u.role_id}, email={u.email}")

        print("\n[2] Все монеты:")
        for c in crud.get_all_coins(session):
            print(f"   {c.symbol} — {c.name} ({c.exchange})")

        ivan = crud.get_user_by_username(session, "ivan")
        print(f"\n[3] Монеты пользователя {ivan.username}:")
        for uc in crud.get_user_coins(session, ivan.id):
            print(f"   {uc.coin.symbol} — добавлена {uc.added_at:%Y-%m-%d}")

        setting = crud.get_setting_by_user(session, ivan.id)
        print(f"\n[4] Настройки {ivan.username}:")
        print(f"   EMA={setting.ema_period}, target={setting.target_pct}%, "
              f"stop={setting.stop_pct}%")

        print(f"\n[5] Позиции {ivan.username}:")
        for p in crud.get_user_positions(session, ivan.id):
            status = "закрыта" if p.exit_time else "открыта"
            profit = f", профит {p.profit_percent}%" if p.profit_percent else ""
            print(f"   Position #{p.id}: entry={p.entry_price}, "
                  f"exit={p.exit_price} ({status}{profit})")

        print(f"\n[6] Обновляем настройки {ivan.username}...")
        crud.update_setting(session, ivan.id, ema_period=100, target_pct=5.0)
        setting = crud.get_setting_by_user(session, ivan.id)
        print(f"   Новые: EMA={setting.ema_period}, target={setting.target_pct}%")

        print("\n[7] Создаём нового пользователя anna...")
        trader_role = crud.get_role_by_name(session, "trader")
        anna = crud.create_user(session, "anna", "anna@mail.ru", "hash_n", trader_role.id)
        crud.create_setting(session, anna.id)
        print(f"   Создан: id={anna.id}, username={anna.username}")

        print(f"\n[8] Удаляем пользователя {anna.username}...")
        ok = crud.delete_user(session, anna.id)
        print(f"   Результат: {'удалён' if ok else 'не найден'}")

        print("\n[9] Проверка: остались ли настройки anna?")
        setting = crud.get_setting_by_user(session, anna.id)
        print(f"   Настройки: {'есть' if setting else 'удалены каскадно'}")

        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
        print("=" * 60)

    finally:
        session.close()


if __name__ == "__main__":
    demo()