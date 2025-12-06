import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db.session import get_session
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
import os
import tempfile

@pytest.fixture(name="session")
def session_fixture():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")

    """Creates a clean SQLite database for each test."""
    engine = create_engine(
    f"sqlite:///{db_path}", 
    connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    os.close(db_fd)
    engine.dispose()
    os.remove(db_path)

@pytest.fixture()
def client(session: Session):
    """Override dependency get_session so app uses the test DB."""
    def override_get_session():
        yield session
    
    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as c:
        yield c
