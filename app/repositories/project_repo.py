from sqlmodel import Session, select
from app.models.project import Project
from app.core.exceptions import NotFoundException


class ProjectRepository:

    @staticmethod
    def get_by_id(db: Session, project_id: int) -> Project:
        project = db.get(Project, project_id)
        if not project:
            raise NotFoundException("Project not found")
        return project

    @staticmethod
    def list(db: Session, owner_id: int, limit: int, offset: int):
        statement = (
            select(Project)
            .where(Project.owner_id == owner_id)
            .limit(limit)
            .offset(offset)
        )
        return db.exec(statement).all()

    @staticmethod
    def create(db: Session, project: Project) -> Project:
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def delete(db: Session, project: Project):
        db.delete(project)
        db.commit()

    @staticmethod
    def update(db: Session, project: Project, data: dict) -> Project:
        for field, value in data.items():
            setattr(project, field, value)
        db.commit()
        db.refresh(project)
        return project
