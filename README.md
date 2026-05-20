# TROD-2026

Репозиторий практических работ по дисциплине «Технологии распределённой обработки данных».

| Каталог | Содержание |
|---------|------------|
| [**lab-1/**](lab-1/README.md) | Sports Store: FastAPI, PostgreSQL, nginx, Docker **и CI/CD** (lint, pytest, coverage ≥ 50%, push образа) |
| [**lab-3/**](lab-3/README.md) | Kafka: отзывы о спортивных товарах (порт **8081**, lab-1 — **8080**) |

Каталог `lab-2/` оставлен только как указатель: всё объединено в **lab-1** (см. [lab-2/README.md](lab-2/README.md)).

## lab-1: код + Docker + CI

В одном каталоге `lab-1/`:

- приложение и тесты — `lab-1/app/`;
- `docker-compose.yml`, `db/`, `nginx/`;
- `pyproject.toml`, `requirements-dev.txt` — в `lab-1/app/`;
- шаблоны CI для **отдельного** репозитория — `lab-1/ci/`.

Пайплайн монорепозитория (при push в `lab-1/**`):

- [`.gitlab-ci.yml`](.gitlab-ci.yml)
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

Локально (как в CI):

```powershell
cd lab-1\app
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest --cov=src --cov-fail-under=50
```

Демонстрация **упавших** пайплайнов (ветки для преподавателя):

| Ветка | Сбой |
|-------|------|
| `demo/ci-fail-lint` | не прошёл **lint** (Ruff) |
| `demo/ci-fail-coverage` | не хватило **coverage** (&lt; 50%) |

После `git push` приложите ссылки на прогоны GitHub Actions / GitLab Pipelines.

## Отдельный репозиторий для сдачи lab-1

Скопируйте содержимое `lab-1/` в корень нового репо и положите CI из `lab-1/ci/` — инструкция: [lab-1/ci/README.md](lab-1/ci/README.md).

## lab-3 (Kafka)

```powershell
cd lab-3
Copy-Item .env.example .env
docker compose up --build
```

API: `http://localhost:8081/docs` (lab-1: `http://localhost:8080/`)

## Клонирование

```bash
git clone https://github.com/Atamurat2004/TROD-2026.git
cd TROD-2026
```
