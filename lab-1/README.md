# Lab-1: Sports Store Inventory (Docker)

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