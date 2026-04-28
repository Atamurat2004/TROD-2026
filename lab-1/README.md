# Lab-1: Sports Store Inventory (Docker)

Полноценный демонстрационный проект для защиты лабораторной:

- `web` — FastAPI API + веб-страница для управления товарами спорт-магазина;
- `db` — PostgreSQL с инициализацией схемы;
- оба компонента работают в отдельных контейнерах в одной Docker-сети;
- наружу открыт только API (`8000`), БД не публикует порт.

## Что реализовано

- Слоистая архитектура: `config -> database(pool) -> repository -> service -> api`.
- Валидация входных данных (`pydantic`), фильтрация и пагинация.
- Health endpoints:
  - `GET /health/live` — жив ли сервис;
  - `GET /health/ready` — готов ли сервис + есть ли соединение с БД.
- Единый формат ошибок API (`404` и т.д.).
- PostgreSQL: индексы, поля `created_at`/`updated_at`, trigger на `updated_at`.
- Multi-stage Dockerfile и non-root пользователь в `web` контейнере.
- Docker Compose: bridge-сеть, healthcheck, volume у БД, restart policy.
- Тесты (`pytest`) для API и сервисного слоя.

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

- Web UI: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- Liveness: `http://localhost:8000/health/live`
- Readiness: `http://localhost:8000/health/ready`

## API Demo Script (товары спорт-магазина)

### 1. Добавить товар

```bash
curl -X POST http://localhost:8000/products \
  -H "Content-Type: application/json" \
  -d '{
        "title":"Nike Running Shoes",
        "description":"Footwear",
        "priority":2,
        "status":"todo"
      }'
```

`status` значения:
- `todo` = `in_stock`
- `in_progress` = `low_stock`
- `done` = `out_of_stock`

### 2. Получить список товаров

```bash
curl "http://localhost:8000/products?limit=10&offset=0"
```

### 3. Поиск/фильтрация

```bash
curl "http://localhost:8000/products?status=todo&search=Nike"
```

### 4. Частично обновить товар (PATCH)

```bash
curl -X PATCH http://localhost:8000/products/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

### 5. Удалить товар

```bash
curl -i -X DELETE http://localhost:8000/products/1
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

Полная очистка (включая данные БД):

```bash
docker compose down -v
```

## Проверка по чеклисту задания

- Есть docker-сеть (`lab1-network`, bridge).
- Web и DB в разных контейнерах.
- Билд воспроизводим на чистом окружении.
- `Dockerfile` приложения multi-stage.
- Внешний доступ только к API, без проброса порта БД.
- У БД настроен volume (`postgres_data`).
- Секреты не хардкодятся в Dockerfile/compose, берутся из env.
