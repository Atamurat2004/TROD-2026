from fastapi import FastAPI

app = FastAPI(title="Lab-1", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Проверка готовности сервиса."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    """Корневой маршрут."""
    return {"message": "Lab-1 distributed data processing"}


def add(a: int, b: int) -> int:
    """Чистая функция для unit-тестов и покрытия веток."""
    return a + b






