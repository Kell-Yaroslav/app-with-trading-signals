# App with Trading Signals

Система мониторинга криптовалютного рынка с автоматическим отслеживанием технических сигналов.

**Лабораторная работа №2** — REST API на FastAPI.

---

## Содержание

- [О проекте](#о-проекте)
- [Стек технологий](#стек-технологий)
- [Структура проекта](#структура-проекта)
- [Запуск](#запуск)
- [API Service](#api-service)
- [Тестовые пользователи](#тестовые-пользователи)
- [Права доступа](#права-доступа)
- [JWT-аутентификация](#jwt-аутентификация)
- [Работа с Git](#работа-с-git)

---

## О проекте

Информационная система для мониторинга криптовалютного рынка. Отслеживает технические индикаторы (Bollinger Bands, MACD, EMA) и уведомляет трейдера о точках входа и выхода из позиции.

**Бизнес-цель:** не пропускать торговые сигналы и получать уведомления.

**Что реализовано:**
- **ЛР1** — слой доступа к данным: 6 ORM-моделей, 24 CRUD-функции, миграции Alembic
- **ЛР2** — REST API на FastAPI: регистрация, логин через JWT, CRUD-эндпоинты, разграничение прав

---

## Стек технологий

### ЛР1 — доступ к данным

- **PostgreSQL 17** — реляционная СУБД
- **SQLAlchemy 2.1** — ORM
- **Alembic 1.20** — миграции
- **psycopg2-binary** — драйвер PostgreSQL
- **python-dotenv** — чтение `.env`

### ЛР2 — REST API

- **FastAPI 0.143** — веб-фреймворк
- **Uvicorn 0.54** — ASGI-сервер
- **Pydantic 2.14** — валидация данных
- **python-jose 3.5** — JWT-токены
- **passlib + bcrypt** — хеширование паролей
- **python-multipart** — форма логина (OAuth2)
- **email-validator** — валидация email

---

## Структура проекта

```
app-with-trading-signals/
├── app/                          # ЛР1 — слой доступа к данным
│   ├── __init__.py
│   ├── database.py               # Подключение к PostgreSQL
│   ├── models.py                 # 6 ORM-моделей
│   └── crud.py                   # 24 CRUD-функции
│
├── api_service/                  # ЛР2 — REST API
│   ├── __init__.py
│   ├── main.py                   # Точка входа FastAPI
│   ├── config.py                 # Настройки из .env
│   ├── dependencies.py           # get_session, get_current_user, require_admin
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py               # POST /register, /login
│   │   ├── users.py              # CRUD users
│   │   └── roles.py              # CRUD roles
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── password.py           # Bcrypt-хеширование
│   │   └── jwt.py                # Создание/проверка токенов
│   └── schemas/
│       ├── __init__.py
│       ├── user.py               # UserCreate, UserRead, UserUpdate
│       ├── role.py               # RoleRead
│       ├── token.py              # Token, TokenData
│       └── coin.py               # CoinCreate, CoinRead
│
├── alembic/                      # Миграции
│   └── versions/
│
├── scripts/                      # Утилиты
│   ├── seed.py                   # Тестовые данные (bcrypt)
│   ├── demo.py                   # Демонстрация CRUD
│   ├── clear_db.py               # Очистка БД
│   ├── show_tables.py            # Просмотр таблиц
│   └── test_connection.py        # Тест подключения
│
├── .env                          # Переменные окружения (не в Git)
├── .env.example                  # Шаблон
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Запуск

### 1. Требования

- PostgreSQL 17
- Python 3.10+
- Git

### 2. Клонирование

```bash
git clone https://github.com/Kell-Yaroslav/app-with-trading-signals.git
cd app-with-trading-signals
git checkout ЛР2
```

### 3. Виртуальное окружение

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Зависимости

```bash
pip install -r requirements.txt
```

### 5. База данных

```bash
psql -U postgres -c "CREATE DATABASE crypto_monitor ENCODING 'UTF8';"
```

### 6. Настройка `.env`

Скопируй `.env.example` в `.env`:

```bash
copy .env.example .env
```

Впиши свой пароль и сгенерируй JWT-ключ:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**`.env`:**
```
DATABASE_URL=postgresql+psycopg2://postgres:1234@localhost:5432/crypto_monitor
JWT_SECRET_KEY=<сгенерированный ключ>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

### 7. Миграции

```bash
alembic upgrade head
```

### 8. Тестовые данные

```bash
python -m scripts.seed
```

### 9. Запуск API

```bash
uvicorn api_service.main:app --reload
```

**Swagger UI:** http://localhost:8000/docs

---

## API Service

### Аутентификация

| Метод | Эндпоинт | Что делает | Доступ |
|---|---|---|---|
| POST | `/api/auth/register` | Регистрация | Публичный |
| POST | `/api/auth/login` | Логин, возвращает JWT | Публичный |

### Пользователи

| Метод | Эндпоинт | Что делает | Доступ |
|---|---|---|---|
| GET | `/api/users/me` | Свой профиль | JWT |
| GET | `/api/users/me/with-role` | Свой профиль + роль | JWT |
| GET | `/api/users` | Все пользователи | Admin |
| GET | `/api/users/{user_id}` | По id | Admin / себя |
| PUT | `/api/users/{user_id}` | Обновить | Admin / себя |
| DELETE | `/api/users/{user_id}` | Удалить | Admin |

### Роли

| Метод | Эндпоинт | Что делает | Доступ |
|---|---|---|---|
| GET | `/api/roles` | Список ролей | JWT |
| GET | `/api/roles/{role_id}` | Роль по id | JWT |

### Публичные

| Метод | Эндпоинт | Что делает |
|---|---|---|
| GET | `/` | Корневой — проверка работы |
| GET | `/health` | Проверка работоспособности |

---

## Тестовые пользователи

Из `scripts/seed.py`. **Единый пароль — `1234`.**

| Username | Email | Пароль | Роль |
|---|---|---|---|
| `admin` | admin@mail.ru | 1234 | admin |
| `ivan` | ivan@mail.ru | 1234 | trader |
| `petr` | petr@mail.ru | 1234 | trader |

---

## Права доступа

| Действие | Trader | Admin |
|---|---|---|
| Регистрация | ✅ | ✅ |
| Логин | ✅ | ✅ |
| Просмотр своих данных | ✅ | ✅ |
| Просмотр чужих данных | ❌ 403 | ✅ |
| Редактирование своих данных | ✅ | ✅ |
| Редактирование чужих данных | ❌ 403 | ✅ |
| Просмотр списка пользователей | ❌ 403 | ✅ |
| Удаление пользователя | ❌ 403 | ✅ |
| CRUD своих `settings` | ✅ | ✅ |
| CRUD чужих `settings` | ❌ | ✅ |
| CRUD своих `user_coins` | ✅ | ✅ |
| CRUD чужих `user_coins` | ❌ | ✅ |
| CRUD своих `positions` | ✅ | ✅ |
| CRUD чужих `positions` | ❌ | ✅ |
| Создание/удаление `coins` | ❌ 403 | ✅ |

---

## JWT-аутентификация

### Что кладём в токен

```json
{
  "sub": "ivan",
  "user_id": 2,
  "role": "trader",
  "exp": 1234567890
}
```

- `sub` — username
- `user_id` — id пользователя
- `role` — роль для быстрой проверки прав
- `exp` — время истечения

### Как использовать

1. **Логин:** `POST /api/auth/login` с form-data `username` и `password`
2. **Получить токен:**
   ```json
   {
     "access_token": "eyJ...",
     "token_type": "bearer"
   }
   ```
3. **Отправлять токен в каждом запросе:**
   ```
   Authorization: Bearer <access_token>
   ```

### В Swagger UI

1. Нажми **Authorize** справа сверху
2. Введи username и password
3. Нажми **Authorize**
4. Появится зелёный замок 🔒 — все защищённые запросы автоматически включают токен

---

## Работа с Git

### Ветки

- **`ЛР0`** — техническое задание и схема БД
- **`ЛР1`** — реализация слоя доступа к данным
- **`ЛР2`** — REST API (текущая)

### Синхронизация

```bash
# Перед началом работы
git pull origin ЛР2

# После изменений
git add <файлы>
git commit -m "..."
git push
```

### Перед push

```bash
# Подтянуть свежие изменения с сервера
git pull --rebase origin ЛР2

# Если нет конфликтов
git push
```

---

## Авторы

- **Перевертова Анастасия** — подключение к БД, ORM-модели (ЛР1), вторая часть API (ЛР2)
- **Келль Ярослав** — CRUD, seed, Alembic (ЛР1), первая часть API (ЛР2)

---

## Репозиторий

https://github.com/Kell-Yaroslav/app-with-trading-signals