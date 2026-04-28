from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Query, Request
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.database import Database
from src.errors import TaskNotFoundError
from src.repository import TaskRepository
from src.schemas import ErrorResponse, TaskCreate, TaskListResponse, TaskRead, TaskReplace, TaskStatus, TaskUpdate
from src.service import TaskService

settings = get_settings()
database = Database(settings=settings)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.app_env != "test":
        database.connect()
    yield
    if settings.app_env != "test":
        database.disconnect()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
    description="Task management API for Docker lab demonstration.",
)


def get_task_service() -> TaskService:
    return TaskService(TaskRepository(database))


@app.exception_handler(TaskNotFoundError)
async def handle_not_found(_: Request, exc: TaskNotFoundError):
    return JSONResponse(status_code=404, content=ErrorResponse(detail=str(exc)).model_dump())


@app.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def readiness() -> dict[str, str]:
    return {"status": "ok" if database.ping() else "degraded"}


@app.get("/tasks", response_model=TaskListResponse, tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=255),
    limit: int = Query(default=settings.default_limit, ge=1, le=settings.max_limit),
    offset: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_task_service),
):
    return service.list_tasks(status=status, search=search, limit=limit, offset=offset)


@app.get("/tasks/{task_id}", response_model=TaskRead, responses={404: {"model": ErrorResponse}}, tags=["tasks"])
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_task(task_id)


@app.post("/tasks", response_model=TaskRead, status_code=201, tags=["tasks"])
def create_task(payload: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(payload)


@app.put("/tasks/{task_id}", response_model=TaskRead, responses={404: {"model": ErrorResponse}}, tags=["tasks"])
def replace_task(task_id: int, payload: TaskReplace, service: TaskService = Depends(get_task_service)):
    return service.replace_task(task_id, payload)


@app.patch("/tasks/{task_id}", response_model=TaskRead, responses={404: {"model": ErrorResponse}}, tags=["tasks"])
def patch_task(task_id: int, payload: TaskUpdate, service: TaskService = Depends(get_task_service)):
    return service.update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=204, responses={404: {"model": ErrorResponse}}, tags=["tasks"])
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete_task(task_id)
