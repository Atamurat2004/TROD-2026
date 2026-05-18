# Lab-2: CI/CD-конвейер для приложения (Sports Store)

Каталог **`lab-2/`** — практическая работа по **CI/CD**. Код приложения, **Dockerfile** и **docker compose** остаются в [**lab-1**](../lab-1/README.md); здесь — линтер, тесты, coverage и описание пайплайна.

## Связь с lab-1

| Компонент | Расположение |
|-----------|--------------|
| FastAPI-приложение, БД, nginx | `lab-1/` |
| `Dockerfile` образа API | `lab-1/app/Dockerfile` |
| Unit/integration-тесты | `lab-1/app/tests/` |
| Ruff, pytest, coverage (порог **50%**) | `lab-2/pyproject.toml`, `lab-2/requirements-dev.txt` |
| GitLab CI / GitHub Actions | `../.gitlab-ci.yml`, `../.github/workflows/ci.yml` |

Изменения в `lab-1/app` или в конфигурации CI в `lab-2/` запускают один и тот же пайплайн.

## Структура lab-2

В `lab-2/` **нет** каталогов `app/` и `tests/` — это нормально: исходники и тесты лежат в `lab-1/app/`, а здесь только настройки CI.

```text
lab-2/
├── README.md
├── pyproject.toml          # ruff, pytest, coverage 
└── requirements-dev.txt    # pytest, ruff, httpx, pytest-cov
```

## Локальный запуск проверок (как в CI)

Требования: **Python 3.12+**, приложение из lab-1.

```powershell
cd lab-1\app
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt -r ..\..\lab-2\requirements-dev.txt
```

**Сборка (build):**

```powershell
python -m compileall -q src
```

**Линтер (lint):**

```powershell
ruff check . --config ..\..\lab-2\pyproject.toml
ruff format --check . --config ..\..\lab-2\pyproject.toml
```

**Тесты и coverage:**

```powershell
pytest --cov=src --cov-config=..\..\lab-2\pyproject.toml --cov-report=term --cov-report=html --cov-report=xml --cov-fail-under=50
```

Отчёт HTML: `lab-1/app/htmlcov/index.html`.

Полный стек с PostgreSQL и nginx — см. [lab-1/README.md](../lab-1/README.md):

```powershell
cd lab-1
Copy-Item .env.example .env
docker compose up --build
```

API с хоста: `http://localhost:8080/docs`, health: `http://localhost:8080/health/live`.

## Docker-образ (как в job docker_build)

Из корня репозитория или из `lab-1/app`:

```powershell
docker build -f lab-1/app/Dockerfile -t lab1-app:local lab-1/app
```

В CI образ помечается тегом **`$CI_COMMIT_SHORT_SHA`** (GitLab) или первыми 7 символами SHA (GitHub).

## CI/CD: stages и jobs

Пайплайн запускается при **merge request / pull request** и при пуше в **ветку по умолчанию** (`workflow.rules` в `.gitlab-ci.yml`).

| Stage | Job | Действие | Падение при |
|-------|-----|----------|-------------|
| build | `build` | `pip install`, `compileall src` | Ошибка зависимостей или синтаксиса |
| lint | `lint` | `ruff check`, `ruff format --check` | Нарушения ruff |
| test | `test` | `pytest` + coverage ≥ **50%** | Упавшие тесты или низкое покрытие |
| docker | `docker_build` | `docker build` → артефакт `image.tar` | Ошибка сборки образа |
| publish | `docker_push` | login + `docker push` в Docker Hub | Нет секретов / ошибка push |

Минимум **5 jobs**: `build`, `lint`, `test`, `docker_build`, `docker_push`.

### Coverage

- В логе job **test** — таблица coverage; в GitLab regex `coverage:` парсит строку `TOTAL … %`.
- Артефакты: `lab-1/app/htmlcov/`, `lab-1/app/coverage.xml` (Cobertura).
- Порог **50%**: `--cov-fail-under=50` и `[tool.coverage.report] fail_under` в `pyproject.toml`.

### Docker Hub (без хардкода)

**GitLab** — *Settings → CI/CD → Variables* (рекомендуется **Masked**):

| Переменная | Описание |
|------------|----------|
| `DOCKERHUB_USERNAME` | Логин Docker Hub |
| `DOCKERHUB_TOKEN` | Access Token или пароль |
| `DOCKER_IMAGE_NAME` (опц.) | Имя репозитория на Hub (по умолчанию `lab1-app`) |

Теги push: **`$CI_COMMIT_SHORT_SHA`**, **`$CI_COMMIT_REF_SLUG`**.

**GitHub** — *Settings → Secrets and variables → Actions*:

- Secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- Variable (опц.): `DOCKER_IMAGE_NAME`

Job **docker_push** завершится с ошибкой, если секреты не заданы.

### GitLab Runner и Docker-in-Docker

Jobs **docker_build** / **docker_push** используют `docker:27-dind`. Runner должен поддерживать DinD (часто нужен **privileged** executor).

### Почему пайплайн «реально» падает

- Сломанная установка или `compileall` → **build** красный.
- Ruff → ненулевой exit code → **lint** красный.
- Pytest или coverage &lt; 50% → **test** красный.
- Ошибка `docker build` → **docker_build** красный.
- Отсутствие `DOCKERHUB_*` → **docker_push** красный.

## GitHub Actions

Файл [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) дублирует этапы для PR и push в `main`/`master`. Триггер по путям: `lab-1/**`, `lab-2/**`, файлы workflow.
