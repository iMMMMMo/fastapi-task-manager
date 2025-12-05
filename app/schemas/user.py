from sqlmodel import SQLModel
from typing import Optional


class UserCreate(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserRead(SQLModel):
    id: int
    email: str
    full_name: Optional[str] = None


class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
