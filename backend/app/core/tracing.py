"""
Configuración de LangSmith para trazabilidad
"""
import os
from typing import Optional
from langsmith import Client
from app.core.config import get_settings

settings = get_settings()


def setup_langsmith() -> bool:
    """Configura LangSmith si las credenciales están disponibles"""
    if settings.LANGCHAIN_API_KEY:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
        return True
    return False


def get_langsmith_client() -> Optional[Client]:
    """Obtiene el cliente de LangSmith para consultas"""
    if settings.LANGCHAIN_API_KEY: 
        return Client()
    return None