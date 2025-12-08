from sqlmodel import Session
from app.models.project import Project
from app.core.exceptions import PermissionDeniedException
from app.repositories.project_repo import ProjectRepository


class ProjectService:

    @staticmethod
    def create(db: Session, owner_id: int, data):
        project = Project(**data.model_dump(), owner_id=owner_id)
        return ProjectRepository.create(db, project)

    @staticmethod
    def get(db: Session, project_id: int, user_id: int):
        project = ProjectRepository.get_by_id(db, project_id)
        if project.owner_id != user_id:
            raise PermissionDeniedException()
        return project

    @staticmethod
    def list(db: Session, user_id: int, limit: int, offset: int):
        return ProjectRepository.list(db, user_id, limit, offset)

    @staticmethod
    def update(db: Session, project_id: int, user_id: int, data: dict):
        project = ProjectService.get(db, project_id, user_id=user_id)
        return ProjectRepository.update(db, project, data)

    @staticmethod
    def delete(db: Session, project_id: int, user_id: int):
        project = ProjectService.get(db, project_id, user_id)
        ProjectRepository.delete(db, project)
