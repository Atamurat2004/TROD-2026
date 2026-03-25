# Практическая работа (lab-1): CI/CD для Docker-приложения

Каталог **`lab-1/`** в монорепозитории [**TROD-2026**](../README.md): веб-сервис на **FastAPI** + **Uvicorn**, Docker, **ruff**, **pytest**, **coverage** (порог **50%**), публикация отчёта покрытия, сборка и push образа в **Docker Hub**.

## Состав (внутри `lab-1/`)

| Элемент | Назначение |
|--------|------------|
| `app/main.py` | Приложение (маршруты `/`, `/health`, функция `add` для тестов) |
| `tests/` | Pytest: API (через `httpx` + ASGI) и unit-тесты |
| `requirements.txt` | Зависимости времени выполнения |
| `requirements-dev.txt` | Линтер, pytest, coverage, httpx |
| `pyproject.toml` | Настройки **ruff** и **coverage** (в т.ч. `fail_under = 50`) |
| `Dockerfile` | Сборка образа (`python:3.12-slim-bookworm`, обновление пакетов ОС, непривилегированный пользователь) |
| `../.gitlab-ci.yml` | Пайплайн GitLab (контекст сборки — этот каталог) |
| `../.github/workflows/ci.yml` | GitHub Actions для **lab-1** |

## Локальный запуск (без Docker)

Требования: **Python 3.12+**, `pip`.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements-dev.txt

# Линтер
ruff check .
ruff format --check .

# Тесты и покрытие (ниже 50% — код возврата ≠ 0)
pytest --cov=app --cov-report=term --cov-report=html --cov-report=xml --cov-fail-under=50

# Отчёт HTML: каталог htmlcov/ (откройте htmlcov/index.html в браузере)
python -m compileall -q app
```

Запуск API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Проверка: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health), документация OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Docker

Сборка и запуск:

```bash
docker build -t lab1-app:local .
docker run --rm -p 8000:8000 lab1-app:local
```

Образ слушает порт **8000**.

## CI/CD: этапы и jobs

Пайплайн запускается при **открытом merge request** и при пуше в **ветку по умолчанию** (см. `workflow.rules` в корневом `.gitlab-ci.yml`).

| Stage / job | Что делает | Условие падения |
|-------------|------------|-----------------|
| **build** | `pip install -r requirements.txt`, `compileall app` | Ошибка установки или синтаксиса |
| **lint** | `ruff check .`, `ruff format --check .` | Нарушения правил ruff |
| **test** | `pytest` + coverage, `--cov-fail-under=50` | Упавшие тесты или покрытие &lt; 50% |
| **docker_build** | `docker build`, тег `:CI_COMMIT_SHORT_SHA`, артефакт `image.tar` | Ошибка сборки образа |
| **docker_push** | `docker load`, login в Docker Hub, `docker push` | Нет секретов, ошибка login/push |

Минимум пяти job: `build`, `lint`, `test`, `docker_build`, `docker_push`.

### Покрытие (coverage)

- В логе job **test** публикуется таблица coverage; в GitLab задано `coverage:` с regex для строки `TOTAL ...`.
- Артефакты: **htmlcov/** (HTML-отчёт) и **coverage.xml** (Cobertura для встроенного отчёта GitLab).
- Падение при &lt; 50% обеспечивают флаги **`--cov-fail-under=50`** и **`[tool.coverage.report] fail_under`** в `pyproject.toml`.

### Docker Hub (без хардкода учётных данных)

В **GitLab**: *Settings → CI/CD → Variables* (рекомендуется **Masked**; для защищённых веток — **Protected**):

| Переменная | Описание |
|------------|----------|
| `DOCKERHUB_USERNAME` | Логин Docker Hub |
| `DOCKERHUB_TOKEN` | Пароль или [Access Token](https://docs.docker.com/docker-hub/access-tokens/) |
| `DOCKER_IMAGE_NAME` (опционально) | Имя репозитория на Hub (по умолчанию `lab1-app`) |

Образ пушится с тегами **`$CI_COMMIT_SHORT_SHA`** и **`$CI_COMMIT_REF_SLUG`**.

В **GitHub**: *Settings → Secrets and variables → Actions*:

- `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
- опционально variable `DOCKER_IMAGE_NAME`

### GitLab Runner и Docker-in-Docker

Job **docker_build** / **docker_push** используют сервис **docker:dind**. Исполнитель должен разрешать Docker-in-Docker (часто нужен **privileged** runner или эквивалентная настройка executor). Если сборка падает на `docker info`, уточните требования к runner у администратора GitLab.

### Почему пайплайн «реально» падает

- Сборка зависимостей или компиляция байткода — при ошибке job **build** красный.
- Ruff — ненулевой код выхода при нарушениях.
- Pytest/coverage — ненулевой код при падении тестов или покрытии ниже порога.
- **docker_push** — завершится с ошибкой, если не заданы `DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`.

## GitHub Actions

Файл в корне `.github/workflows/ci.yml` дублирует логику для **pull request** и пушей в `main`/`master`. Job **docker_push** выполняется после успешного **docker_build**; без настроенных secrets шаг проверки секретов завершится с ошибкой.

## Репозиторий на GitHub

Проект выгружается в монорепозиторий **[TROD-2026](https://github.com/Atamurat2004/TROD-2026)**. Клонирование и push — из **корня** репозитория (не из `lab-1/`):

```bash
git clone https://github.com/Atamurat2004/TROD-2026.git
cd TROD-2026
git remote add origin https://github.com/Atamurat2004/TROD-2026.git   # если ещё не добавлен
git push -u origin main
```

Для аутентификации используйте **Personal Access Token** ([настройка токена](https://github.com/settings/tokens), scope **repo**) или Git Credential Manager.

---

При необходимости замените демо-приложение своим кодом из прошлой работы по Docker, сохранив контракты: `requirements*.txt`, `Dockerfile`, тесты с покрытием ≥ 50%, конфигурацию ruff и описанные переменные CI.
