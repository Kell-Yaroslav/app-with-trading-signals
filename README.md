# App with Trading Signals

Система мониторинга криптовалютного рынка. ЛР1 — слой доступа к данным.

## Стек

- Python 3.14
- PostgreSQL 17
- SQLAlchemy 2.1
- Alembic 1.20
- psycopg2-binary
- python-dotenv

## Структура

```
app/
├── database.py     # подключение к БД
├── models.py       # 6 ORM-моделей
└── crud.py         # 24 CRUD-функции

scripts/
├── seed.py         # тестовые данные
├── demo.py         # демонстрация CRUD
└── test_connection.py  # тест подключения

alembic/            # миграции
alembic.ini
.env.example
```

## Схема БД

**Сущности:** Role, User, Setting, Coin, UserCoin, Position.

**Связи:**

```
Role     (1) ──── (N) User
User     (1) ──── (1) Setting
User     (1) ──── (N) UserCoin
Coin     (1) ──── (N) UserCoin
UserCoin (1) ──── (N) Position
User     (M) ──── (N) Coin   [через UserCoin]
```

## Запуск

```bash
# БД
psql -U postgres -c "CREATE DATABASE crypto_monitor ENCODING 'UTF8';"

# venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# зависимости
pip install SQLAlchemy psycopg2-binary alembic python-dotenv

# .env
copy .env.example .env
# вписать свой пароль от postgres

# миграции
alembic upgrade head

# проверка
python -m scripts.test_connection

# данные
python -m scripts.seed

# демонстрация
python -m scripts.demo
```

## Скрипты

| Скрипт | Что делает |
|---|---|
| `seed.py` | Создаёт 2 роли, 3 пользователя, 3 монеты, подписки, позиции. Идемпотентен. |
| `demo.py` | Показывает 9 сценариев CRUD: чтение, обновление, создание, удаление, каскад. |
| `test_connection.py` | Проверяет подключение, БД, наличие таблиц, работу CRUD. |

## Alembic

```bash
alembic current                      # текущая версия
alembic history                      # история
alembic upgrade head                 # применить
alembic downgrade -1                 # откатить
alembic revision --autogenerate -m "msg"  # новая миграция
```

## Авторы

- Перевертова Анастасия — подключение к БД, модели
- Келль Ярослав — CRUD, seed, demo, Alembic

## Репозиторий

https://github.com/Kell-Yaroslav/app-with-trading-signals
