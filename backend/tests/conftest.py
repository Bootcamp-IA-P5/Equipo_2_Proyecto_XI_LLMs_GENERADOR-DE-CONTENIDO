"""
Fixtures y configuración compartida para todos los tests
"""
import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

# Configurar event loop para tests async
@pytest.fixture(scope="session")
def event_loop():
    """Event loop para tests asíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Mock del LLMService
@pytest.fixture
def mock_llm_service():
    """Mock del servicio LLM"""
    service = MagicMock()
    service.generate = AsyncMock(return_value="Contenido generado por mock")
    return service


# Fixture para datos de test
@pytest.fixture
def content_request_data():
    """Datos de ejemplo para requests de contenido"""
    return {
        "topic": "Inteligencia Artificial",
        "platform": "twitter",
        "audience": "desarrolladores",
        "language": "Spanish",
        "tone": "profesional",
        "additional_context": "enfocado en LLMs"
    }


@pytest.fixture
def financial_request_data():
    """Datos de ejemplo para análisis financiero"""
    return {
        "topic": "Análisis de Apple Inc.",
        "ticker": "AAPL",
        "language": "Spanish"
    }


# Mock de configuración
@pytest.fixture
def mock_settings():
    """Mock de settings"""
    from unittest.mock import MagicMock
    settings = MagicMock()
    settings.GROQ_API_KEY = "test_key"
    settings.DEFAULT_LLM_PROVIDER = "groq"
    settings.DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"
    return settings


# Fixture para cliente HTTP async (útil para tests de integración)
@pytest.fixture
async def async_client() -> AsyncGenerator:
    """Cliente HTTP async para tests de integración"""
    from httpx import AsyncClient
    from app.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Mock para VectorStore (evita cargar sentence_transformers en tests)
@pytest.fixture(autouse=True)
def mock_sentence_transformers(monkeypatch):
    """Mock automático de sentence_transformers para evitar cuelgues"""
    import sys
    from unittest.mock import MagicMock
    
    # Solo mockear si no está ya importado
    if 'sentence_transformers' not in sys.modules:
        mock_st = MagicMock()
        sys.modules['sentence_transformers'] = mock_st
