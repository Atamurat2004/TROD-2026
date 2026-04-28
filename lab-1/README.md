# Lab-1: Production-like Docker CRUD API

Полноценный демонстрационный проект для защиты лабораторной:

- `web` — FastAPI API для управления задачами;
- `db` — PostgreSQL с инициализацией схемы;
- оба компонента в отдельных контейнерах внутри одной Docker-сети;
- доступ снаружи открыт только к API (`8000`), база не публикует порт.

## Что сделано на уровне "как в реальном проекте"

- Слоистая архитектура: `config -> database(pool) -> repository -> service -> api`.
- Typed-схемы и валидация (`pydantic`), enum-статусы задач, пагинация и фильтрация.
- Health endpoints:
  - `GET /health/live` — liveness;
  - `GET /health/ready` — readiness с проверкой БД.
- Единообразные ошибки API (например, `404 Task not found`).
- PostgreSQL: индексы, `created_at/updated_at`, автообновление `updated_at` через trigger.
- Multi-stage Dockerfile приложения + запуск под non-root пользователем.
- Docker Compose: отдельная bridge-сеть, healthcheck для web/db, volume у БД, `restart`.
- Тесты (`pytest`): API-сценарий CRUD + сервисный слой.

## Структура

```text
lab-1/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── pyproject.toml
│   ├── src/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── errors.py
│   │   ├── main.py
│   │   ├── repository.py
│   │   ├── schemas.py
│   │   └── service.py
│   └── tests/
├── db/
│   ├── Dockerfile
│   └── init.sql
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## Быстрый старт

1) Создай `.env`:

```powershell
Copy-Item .env.example .env
```

2) Запусти систему:

```bash
docker compose up --build
```

3) Открой:

- API docs: `http://localhost:8000/docs`
- Liveness: `http://localhost:8000/health/live`
- Readiness: `http://localhost:8000/health/ready`

## API Demo Script (для показа преподавателю)

### 1. Создать задачу

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
        "title":"Prepare lab defense",
        "description":"Show docker architecture and CRUD flow",
        "priority":2,
        "due_date":"2026-05-10",
        "status":"todo"
      }'
```

### 2. Получить список (с пагинацией)

```bash
curl "http://localhost:8000/tasks?limit=10&offset=0"
```

### 3. Фильтрация и поиск

```bash
curl "http://localhost:8000/tasks?status=todo&search=Prepare"
```

### 4. Полное обновление (PUT)

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
        "title":"Prepare lab defense (updated)",
        "description":"Add docker logs and readiness checks",
        "priority":1,
        "due_date":"2026-05-12",
        "status":"in_progress"
      }'
```

### 5. Частичное обновление (PATCH)

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

### 6. Удаление

```bash
curl -i -X DELETE http://localhost:8000/tasks/1
```

## Локальные тесты

```bash
cd app
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
pytest
```

## Остановка

```bash
docker compose down
```

С полным удалением данных БД:

```bash
docker compose down -v
```

## Проверка по чеклисту задания

- Организована docker-сеть (`lab1-network`, bridge).
- Web и DB работают в отдельных контейнерах.
- Билд воспроизводимый (никаких внешних артефактов не требуется).
- `Dockerfile` приложения multi-stage.
- Доступ извне только к API (порт БД не проброшен).
- Для БД используется volume (`postgres_data`).
- Секреты не хардкодятся в `Dockerfile`/`docker-compose`, используются env-переменные.
