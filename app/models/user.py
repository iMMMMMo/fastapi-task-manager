from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


class UserBase(SQLModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
