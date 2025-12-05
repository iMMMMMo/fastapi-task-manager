from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.utils.pagination import pagination_params

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_session)):
    project = db.get(Project, data.project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Project with id {data.project_id} does not exist.")

    if data.assignee_id is not None:
        user = db.get(User, data.assignee_id)
        if not user:
            raise HTTPException( status_code=400, detail=f"User with id {data.assignee_id} does not exist.")
    task = Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/", response_model=list[TaskRead])
def list_tasks(pagination: dict = Depends(pagination_params), db: Session = Depends(get_session)):
    statement = select(Task).limit(pagination["limit"]).offset(pagination["offset"])
    return db.exec(statement).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_session)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_session)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = data.dict(exclude_unset=True)

    if "project_id" in update_data:
        project = db.get(Project, update_data["project_id"])
        if not project:
            raise HTTPException(status_code=400, detail=f"Project with id {update_data['project_id']} does not exist.")

    if "assignee_id" in update_data and update_data["assignee_id"] is not None:
        user = db.get(User, update_data["assignee_id"])
        if not user:
            raise HTTPException(status_code=400, detail=f"User with id {update_data['assignee_id']} does not exist.")

    for key, value in update_data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_session)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
