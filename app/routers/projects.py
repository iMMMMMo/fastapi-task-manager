from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.db.session import get_session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService
from app.utils.pagination import pagination_params
from app.models.user import User
from app.routers.auth import get_current_user


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate, 
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    return ProjectService.create(db, current_user.id, data)


@router.get("/", response_model=list[ProjectRead])
def list_projects(
    pagination: dict = Depends(pagination_params), 
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    return ProjectService.list(db, current_user.id, pagination["limit"], pagination["offset"])


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(
    project_id: int, 
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    return ProjectService.get(db, project_id, current_user.id)


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, data: ProjectUpdate, 
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    return ProjectService.update(db, project_id, current_user.id, data.model_dump(exclude_unset=True))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int, 
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    ProjectService.delete(db, project_id, current_user.id)
