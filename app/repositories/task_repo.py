from sqlmodel import Session, select
from app.models.task import Task
from app.models.project import Project
from app.core.exceptions import NotFoundException


class TaskRepository:

    @staticmethod
    def get_by_id(db: Session, task_id: int) -> Task:
        task = db.get(Task, task_id)
        if not task:
            raise NotFoundException("Task not found")
        return task

    @staticmethod
    def list(db: Session, owner_id: int, limit: int, offset: int):
        statement = (
            select(Task)
            .join(Project)
            .where(Project.owner_id == owner_id)
            .limit(limit)
            .offset(offset)
        )
        return db.exec(statement).all()

    @staticmethod
    def create(db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def update(db: Session, task: Task, data: dict) -> Task:
        for field, value in data.items():
            setattr(task, field, value)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def delete(db: Session, task: Task):
        db.delete(task)
        db.commit()