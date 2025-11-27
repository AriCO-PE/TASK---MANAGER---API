from fastapi import APIRouter
from datetime import datetime 

router = APIRouter()

@router.get("/")
def read_root():
    return{
        "message": "Bienvenido a Task Manager Api ",
        "endpoints_available": 3,
        "documentation": "/docs",
    }

@router.get("/health")
def health_check():
    return{
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0", 
        "service": "Task Manager API",
    }