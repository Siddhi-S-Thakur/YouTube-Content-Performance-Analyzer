from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """Health check endpoint to verify that the backend application is running."""
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "environment": settings.APP_ENV,
        "version": "0.1.0",
    }
