from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.utils.pagination import pagination_params
from app.models.user import User
from app.routers.auth import get_current_user


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: ProjectCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = Project(**data.model_dump(), owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead])
def list_projects(pagination: dict = Depends(pagination_params), db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    statement = select(Project).where(Project.owner_id == current_user.id).limit(pagination["limit"]).offset(pagination["offset"])
    results = db.exec(statement).all()
    return results


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found.")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found.")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found.")
    
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized.")
    
    db.delete(project)
    db.commit()
