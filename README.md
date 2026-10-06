# App with Trading Signals — ЛР0

Лабораторная работа №0. Техническое задание на проект.

## Содержание ветки

В этой ветке находится файл:

- **`Laboratory_Work_0_app-with-trading-signals.docx`** — отчёт по лабораторной работе №0

## Что внутри отчёта

Документ содержит техническое задание на проект информационной системы мониторинга и сигнализации криптовалютного рынка:

- **Предметная область** — отслеживание технических сигналов (Bollinger Bands, MACD, EMA) на криптобирже
- **Бизнес-цель** — автоматизировать мониторинг и уведомлять трейдера о точках входа/выхода
- **Функционал приложения** — роли Трейдер и Администратор, сценарии использования
- **Архитектура** — микросервисы: API Service, Monitor Service, gRPC Service, Notification Service, Auth Service, DB Service, Frontend
- **Технологии** — FastAPI, SQLAlchemy, Pydantic, gRPC, RabbitMQ, WebSocket, JWT, PostgreSQL, Docker, Jinja2, Nginx, Chart.js
- **Схема БД** — 6 сущностей: Role, User, Setting, Coin, UserCoin, Position
- **Связи** — 1:1, 1:N и M:N

## Реализация

Кодовая часть проекта — в ветке **`ЛР1`**:

```
ЛР0  →  техническое задание (этот файл и .docx)
ЛР1  →  реализация слоя доступа к данным
```

## Репозиторий

https://github.com/Kell-Yaroslav/app-with-trading-signals
