from sqlmodel import SQLModel
from typing import Optional


class ProjectCreate(SQLModel):
    name: str
    description: Optional[str] = None


class ProjectRead(ProjectCreate):
    id: int
    owner_id: int


class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
