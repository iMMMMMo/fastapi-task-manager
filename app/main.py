from fastapi import FastAPI

from app.routers.projects import router as projects_router
from app.routers.tasks import router as tasks_router
from app.routers.auth import router as auth_router

app = FastAPI(
    title="FastAPI Task Manager",
    version="0.4.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(projects_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
