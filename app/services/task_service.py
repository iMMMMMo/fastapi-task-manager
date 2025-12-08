from sqlmodel import Session
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.core.exceptions import PermissionDeniedException, NotFoundException
from app.repositories.task_repo import TaskRepository


class TaskService:

    @staticmethod
    def create(db: Session, owner_id: int, data):
        project = db.get(Project, data.project_id)
        if not project:
            raise NotFoundException(f"Project with id {data.project_id} does not exist")
        
        if project.owner_id != owner_id:
            raise PermissionDeniedException("You cannot add tasks to another user's project")

        if data.assignee_id is not None:
            user = db.get(User, data.assignee_id)
            if not user:
                raise NotFoundException(f"User with id {data.assignee_id} does not exist")

        task = Task(**data.model_dump(), owner_id=owner_id)
        return TaskRepository.create(db, task)

    @staticmethod
    def get(db: Session, task_id: int, user_id: int) -> Task:
        task = TaskRepository.get_by_id(db, task_id)
        if task.project.owner_id != user_id:
            raise PermissionDeniedException()
        return task

    @staticmethod
    def list(db: Session, user_id: int, limit: int, offset: int):
        return TaskRepository.list(db, user_id, limit, offset)

    @staticmethod
    def update(db: Session, task_id: int, user_id: int, data: dict):
        task = TaskService.get(db, task_id, user_id)

        if "project_id" in data:
            project = db.get(Project, data["project_id"])
            if not project:
                raise NotFoundException(f"Project with id {data['project_id']} does not exist")
            if project.owner_id != user_id:
                raise PermissionDeniedException("You cannot move task to another user's project")

        # Sprawdzenie nowego assignee (jeśli zmienia się)
        if "assignee_id" in data and data["assignee_id"] is not None:
            user = db.get(User, data["assignee_id"])
            if not user:
                raise NotFoundException(f"User with id {data['assignee_id']} does not exist")

        return TaskRepository.update(db, task, data)

    @staticmethod
    def delete(db: Session, task_id: int, user_id: int):
        task = TaskService.get(db, task_id, user_id)
        TaskRepository.delete(db, task)