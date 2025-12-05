from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone


if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.user import User


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"
    priority: int = 3
    due_date: Optional[datetime] = None


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    project_id: int = Field(foreign_key="project.id")
    assignee_id: Optional[int] = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    project: Optional["Project"] = Relationship(back_populates="tasks")
    assignee: Optional["User"] = Relationship(back_populates="assigned_tasks")
