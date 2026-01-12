"""
Rutas de health check
"""
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.core.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION
    )