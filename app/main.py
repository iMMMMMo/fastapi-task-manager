from fastapi import FastAPI
from sqlmodel import SQLModel

from app.db.session import sync_engine
from app.models import user, project, task

from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.routers.auth import router as auth_router

app = FastAPI(
    title="FastAPI Task Manager",
    version="0.3.0",
)

@app.on_event("startup")
def on_startup():
    """Create tables and ensure models are registered."""
    SQLModel.metadata.create_all(sync_engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(projects_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
