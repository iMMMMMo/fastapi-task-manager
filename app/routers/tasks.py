from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.utils.pagination import pagination_params
from app.routers.auth import get_current_user


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = db.get(Project, data.project_id)
    if not project:
        raise HTTPException(status_code=400, detail=f"Project with id {data.project_id} does not exist.")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot add tasks to another user's project.")

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
def list_tasks(pagination: dict = Depends(pagination_params), db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Task).join(Project).where(Project.owner_id == current_user.id).limit(pagination["limit"]).offset(pagination["offset"])
    return db.exec(statement).all()


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    if task.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    
    update_data = data.dict(exclude_unset=True)

    if "project_id" in update_data:
        project = db.get(Project, update_data["project_id"])
        if not project:
            raise HTTPException(status_code=400, detail=f"Project with id {update_data['project_id']} does not exist.")
        
        if project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized.")

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
def delete_task(task_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    
    db.delete(task)
    db.commit()
