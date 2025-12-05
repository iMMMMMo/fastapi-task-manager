from app.models.user import User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.utils.pagination import pagination_params


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_session)):
    owner_id = 1  # TEMP: Replace with actual authenticated user ID

    owner = db.get(User, owner_id)
    if not owner:
        raise HTTPException(status_code=400,detail=f"User with id {owner_id} does not exist.")
        
    project = Project(**data.dict(), owner_id=owner_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead])
def list_projects(pagination: dict = Depends(pagination_params), db: Session = Depends(get_session)):
    statement = select(Project).limit(pagination["limit"]).offset(pagination["offset"])
    results = db.exec(statement).all()
    return results


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_session)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_session)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_session)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project with id {project_id} not found")
    db.delete(project)
    db.commit()
