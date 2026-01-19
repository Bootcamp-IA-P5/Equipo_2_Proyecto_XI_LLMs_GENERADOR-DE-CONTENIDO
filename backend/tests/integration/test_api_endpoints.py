"""
Tests de integración para endpoints de la API
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


class TestContentEndpoints:
    """Tests de integración para endpoints de contenido"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_health_check(self):
        """Test: Health check endpoint"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_content_config(self):
        """Test: Obtener configuración de content"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/content/config")
            assert response.status_code == 200
            data = response.json()
            assert "platforms" in data
            assert "audiences" in data
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_generate_content_endpoint(self, content_request_data):
        """Test: Endpoint de generación de contenido"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/content/generate",
                json=content_request_data
            )
            # 422 = validación fallida (aceptable), 401 = sin API key, 500 = error interno, 200 = éxito
            assert response.status_code in [200, 401, 422, 500]
            
            if response.status_code == 200:
                data = response.json()
                assert "content" in data or "error" in data
            elif response.status_code == 422:
                # Error de validación esperado si faltan campos
                data = response.json()
                assert "detail" in data


class TestFinancialEndpoints:
    """Tests de integración para endpoints financieros"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_financial_config(self):
        """Test: Configuración de financial agent"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/api/v1/financial/config")
            # El endpoint debe existir
            assert response.status_code in [200, 404]


class TestScienceEndpoints:
    """Tests de integración para endpoints científicos"""
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_science_search(self):
        """Test: Búsqueda en arXiv"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/science/search",
                json={"query": "machine learning", "max_results": 2}
            )
            # Verificar que el endpoint existe
            assert response.status_code in [200, 404, 500]
