from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/task_manager"
)

sync_engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(sync_engine) as session:
        yield session

