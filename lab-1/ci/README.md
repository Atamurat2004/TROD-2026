# CI/CD (в составе lab-1)

Практическая работа по CI/CD — **часть lab-1**: код, Docker и настройки проверок в одном каталоге.

## Файлы

| Файл | Назначение |
|------|------------|
| `../app/pyproject.toml` | Ruff, pytest, coverage (порог **50%**) |
| `../app/requirements-dev.txt` | pytest, ruff, httpx, pytest-cov |
| `gitlab-ci.yml` | Шаблон GitLab CI для **отдельного** репозитория |
| `github-ci.yml` | Шаблон GitHub Actions для **отдельного** репозитория |

В монорепозитории `TROD-2026` пайплайны в корне: [`.gitlab-ci.yml`](../../.gitlab-ci.yml), [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml).

## Отдельный репозиторий (как просил преподаватель)

Скопируйте **всё содержимое** `lab-1/` в корень нового репозитория:

```text
<новый-репо>/
├── app/                    # код + Dockerfile + pyproject.toml + tests
├── db/
├── nginx/
├── docker-compose.yml
├── .env.example
├── .gitlab-ci.yml          ← из lab-1/ci/gitlab-ci.yml
├── .github/workflows/ci.yml ← из lab-1/ci/github-ci.yml
└── README.md
```

Секреты CI: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (masked).

## Демонстрация упавших пайплайнов

Ветки в монорепозитории (запушьте и откройте Actions / Pipelines):

| Ветка | Ожидаемый сбой |
|-------|----------------|
| `demo/ci-fail-lint` | job **lint** — ошибка Ruff |
| `demo/ci-fail-coverage` | job **test** — coverage &lt; 50% |

Ссылки на прогоны добавьте в отчёт после `git push origin demo/ci-fail-lint demo/ci-fail-coverage`.
