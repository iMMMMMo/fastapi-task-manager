from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.db.session import get_session
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService
from app.utils.pagination import pagination_params
from app.routers.auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return TaskService.create(db, current_user.id, data)


@router.get("/", response_model=list[TaskRead])
def list_tasks(
    pagination: dict = Depends(pagination_params),
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return TaskService.list(db, current_user.id, pagination["limit"], pagination["offset"])


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return TaskService.get(db, task_id, current_user.id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return TaskService.update(db, task_id, current_user.id, data.model_dump(exclude_unset=True))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    TaskService.delete(db, task_id, current_user.id)