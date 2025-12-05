from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class TaskCreate(SQLModel):
    title: str
    description: Optional[str] = None
    project_id: int
    assignee_id: Optional[int] = None
    priority: int = 3
    status: str = "todo"
    due_date: Optional[datetime] = None


class TaskRead(TaskCreate):
    id: int
    created_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[str] = None
    assignee_id: Optional[int] = None
    due_date: Optional[datetime] = None
