from sqlalchemy import inspect, text
from app.database import engine


def show_table(name: str):
    """Показать таблицу и её данные."""
    inspector = inspect(engine)

    # Структура таблицы
    print(f"\n{'=' * 70}")
    print(f"ТАБЛИЦА: {name}")
    print('=' * 70)

    print("\nКолонки:")
    for col in inspector.get_columns(name):
        nullable = "" if col["nullable"] else " NOT NULL"
        print(f"  {col['name']:20} {str(col['type']):20}{nullable}")

    # Данные
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {name};"))
        rows = result.fetchall()

        print(f"\nДанные ({len(rows)} записей):")
        if not rows:
            print("  (пусто)")
            return

        # Заголовки
        headers = result.keys()
        print("  " + " | ".join(f"{h:15}" for h in headers))
        print("  " + "-" * (18 * len(headers)))

        # Строки
        for row in rows:
            print("  " + " | ".join(f"{str(v):15}" for v in row))


def main():
    """Показать все таблицы проекта."""
    tables = ["roles", "users", "settings", "coins", "user_coins", "positions", "alembic_version"]

    for name in tables:
        try:
            show_table(name)
        except Exception as e:
            print(f"\nОшибка таблицы {name}: {e}")


if __name__ == "__main__":
    main()