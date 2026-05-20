# Lab-1: Sports Store Inventory (Docker)

## Структура

```text
lab-1/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt   # pytest, ruff, coverage (CI)
│   ├── pyproject.toml           # ruff, pytest, coverage ≥ 50%
│   ├── src/
│   └── tests/
├── db/
├── nginx/
├── ci/                          # шаблоны .gitlab-ci.yml / GitHub Actions
├── docker-compose.yml
├── .env.example
└── .gitignore
```

**CI/CD** входит в эту же лабораторную: в монорепозитории пайплайн в корне ([`.gitlab-ci.yml`](../.gitlab-ci.yml), [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)). Для отдельного репозитория — см. [ci/README.md](ci/README.md).

## Быстрый старт

1) Создай `.env`:

```powershell
Copy-Item .env.example .env
```

2) Запусти систему:

```bash
docker compose up --build
```

3) Открой (весь HTTP идёт через **nginx**, приложение снаружи не слушает порт `8000`):

- Web UI: `http://localhost:8080/`
- API docs: `http://localhost:8080/docs`
- Liveness: `http://localhost:8080/health/live`
- Readiness: `http://localhost:8080/health/ready`

Порт хоста задаётся в `docker-compose.yml` (`8080:80`). При необходимости замени `8080` на другой свободный порт.

## API Demo Script (товары спорт-магазина)

### 1. Добавить товар

```bash
curl -X POST http://localhost:8080/products \
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
curl "http://localhost:8080/products?limit=10&offset=0"
```

### 3. Поиск/фильтрация

```bash
curl "http://localhost:8080/products?status=todo&search=Nike"
```

### 4. Частично обновить товар (PATCH)

```bash
curl -X PATCH http://localhost:8080/products/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```

### 5. Удалить товар

```bash
curl -i -X DELETE http://localhost:8080/products/1
```

## Локальные тесты и линтер (как в CI)

Из каталога `lab-1/app`:

```powershell
cd app
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
ruff format --check .
pytest --cov=src --cov-report=term --cov-fail-under=50
```

Полный стек: `docker compose up --build` из корня `lab-1/`.

Подробнее про пайплайн и выгрузку в отдельный репозиторий: [ci/README.md](ci/README.md).

## Остановка

```bash
docker compose down
```

Полная очистка (включая данные БД):

```bash
docker compose down -v
```
