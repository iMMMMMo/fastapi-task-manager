from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone


if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.project import Task


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    projects: List["Project"] = Relationship(back_populates="owner")
    assigned_tasks: List["Task"] = Relationship(back_populates="assignee")
