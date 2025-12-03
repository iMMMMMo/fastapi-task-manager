from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class ProjectBase(SQLModel):
    name: str
    description: Optional[str] = None


class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="user.id")
    tasks: List["Task"] = Relationship(back_populates="project")
