from fastapi import FastAPI
from app.api.endpoints import tasks, system, auth

app = FastAPI(
    title="Task Manager API",
    description="Professional Task Management System",
    version="1.0.0"
)


app.include_router(system.router, tags=["System"])
app.include_router(tasks.router, tags=["Tasks"])  
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])