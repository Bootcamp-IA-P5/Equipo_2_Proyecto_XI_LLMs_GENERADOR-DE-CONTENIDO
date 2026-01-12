"""
Aplicación principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import api_router

settings = get_settings()

app = FastAPI(
    title=settings.API_TITLE,
    version=settings. API_VERSION,
    description="API para generación de contenido con IA para diferentes plataformas",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    return {
        "message": "Content Generator API",
        "docs":  "/docs",
        "version": settings.API_VERSION
    }