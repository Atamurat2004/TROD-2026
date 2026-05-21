# CI/CD (GitHub Actions)

Практическая работа по CI/CD — часть **lab-1**: код, Docker и настройки проверок в одном каталоге.

## Файлы

| Файл | Назначение |
|------|------------|
| `../app/pyproject.toml` | Ruff, pytest, coverage (порог **50%**) |
| `../app/requirements-dev.txt` | pytest, ruff, httpx, pytest-cov |
| `github-ci.yml` | Шаблон workflow для отдельного репозитория |

В монорепозитории `TROD-2026`: [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml).

## Отдельный репозиторий

Используйте [**lab-2/`**](../lab-2/README.md) — там готовый репозиторий для GitHub с `.github/workflows/ci.yml`.

Секреты: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.

## Демонстрация упавших пайплайнов

Ветки в `TROD-2026`: `demo/ci-fail-lint`, `demo/ci-fail-coverage`.
