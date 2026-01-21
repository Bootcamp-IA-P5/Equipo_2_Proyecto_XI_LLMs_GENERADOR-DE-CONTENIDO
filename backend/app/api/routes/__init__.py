"""
Registro de todas las rutas
"""
from fastapi import APIRouter
from app.api.routes import content, health, financial, science

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(content.router)
api_router.include_router(financial.router)
api_router.include_router(science.router)