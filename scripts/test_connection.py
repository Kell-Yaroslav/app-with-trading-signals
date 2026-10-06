from app.database import engine, SessionLocal
from sqlalchemy import text, inspect
from app.models import Base


def test_connection():
    """Проверка 1: соединение с PostgreSQL работает."""
    print("\n[1] Подключение к PostgreSQL...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
        print(f"    PostgreSQL: {version.split(',')[0]}")
    except Exception as e:
        print(f"    Ошибка подключения: {e}")
        return False
    return True


def test_database_exists():
    """Проверка 2: БД crypto_monitor существует и доступна."""
    print("\n[2] Проверка текущей БД...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database();"))
            db_name = result.scalar()
        print(f"    Текущая БД: {db_name}")
        return True
    except Exception as e:
        print(f"    Ошибка: {e}")
        return False


def test_tables_exist():
    """Проверка 3: все 6 таблиц из моделей созданы в БД."""
    print("\n[3] Проверка таблиц в БД...")

    expected_tables = set(Base.metadata.tables.keys())
    print(f"    Модели ожидают {len(expected_tables)} таблиц: {sorted(expected_tables)}")

    inspector = inspect(engine)
    actual_tables = set(inspector.get_table_names())
    actual_tables.discard("alembic_version")

    print(f"    В БД найдено {len(actual_tables)} таблиц: {sorted(actual_tables)}")

    missing = expected_tables - actual_tables
    extra = actual_tables - expected_tables

    if missing:
        print(f"    Отсутствуют: {missing}")
        return False
    if extra:
        print(f"    Лишние: {extra}")

    print(f"    Все таблицы на месте")
    return True




def main():
    """Запустить все проверки."""
    print("=" * 60)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К БД")
    print("=" * 60)

    checks = [
        test_connection(),
        test_database_exists(),
        test_tables_exist(),
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ")
    else:
        print("ЕСТЬ ОШИБКИ, СМ. ВЫШЕ")
    print("=" * 60)


if __name__ == "__main__":
    main()