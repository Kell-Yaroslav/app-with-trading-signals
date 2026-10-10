"""Очистить все данные из БД."""
from sqlalchemy import text
from app.database import engine


def clear_all():
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE positions, user_coins, settings, users, coins, roles "
            "RESTART IDENTITY CASCADE;"
        ))
    print("Все данные удалены")


if __name__ == "__main__":
    clear_all()