"""
E2E Tests - User Flows Completos

Tests end-to-end que simulan flujos reales de usuario a través
de todo el sistema (frontend → API → agents → LLM → response).

Requieren que los servicios estén corriendo (docker-compose up).
"""

import pytest
import httpx
import asyncio
from typing import Dict, Any


BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


class TestCompleteUserFlows:
    """Tests E2E de flujos de usuario completos"""
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_health_check_flow(self):
        """E2E: Usuario verifica que el servicio está activo"""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            response = await client.get(f"{API_PREFIX}/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "timestamp" in data
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_content_generation_full_flow(self):
        """
        E2E: Usuario genera contenido general para Twitter
        
        Flow:
        1. Usuario accede a la app
        2. Llena formulario (topic, platform, audience)
        3. Hace POST a /content/generate
        4. Orchestrator enruta a ContentAgent
        5. ContentAgent genera con LLM
        6. Usuario recibe contenido formateado
        """
        request_data = {
            "topic": "Inteligencia Artificial en educación",
            "platform": "twitter",
            "audience": "general",
            "language": "Spanish",
            "tone": "inspirational"
        }
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            response = await client.post(
                f"{API_PREFIX}/content/generate",
                json=request_data
            )
            
            # Validar response exitoso
            assert response.status_code == 200
            data = response.json()
            
            # Validar estructura
            assert "content" in data
            assert "agent_used" in data
            assert "metadata" in data
            
            # Validar contenido
            content = data["content"]
            assert len(content) > 0
            assert len(content) <= 280  # Límite Twitter
            
            # Validar metadata
            assert data["metadata"]["platform"] == "twitter"
            assert data["metadata"]["audience"] == "general"
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_financial_analysis_full_flow(self):
        """
        E2E: Usuario genera análisis financiero con RAG
        
        Flow:
        1. Usuario solicita análisis de Apple (AAPL)
        2. POST a /financial/generate
        3. Orchestrator detecta contenido financiero
        4. FinancialAgent obtiene datos reales
        5. FinancialAgent genera análisis con RAG
        6. Usuario recibe análisis con fuentes
        """
        request_data = {
            "topic": "Apple stock analysis AAPL",
            "platform": "blog",
            "audience": "professional",
            "language": "English"
        }
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            response = await client.post(
                f"{API_PREFIX}/financial/generate",
                json=request_data
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Validar estructura completa
            assert "content" in data
            assert "agent_used" in data
            assert data["agent_used"] == "financial"
            
            # Validar contenido financiero
            content = data["content"].lower()
            assert any(word in content for word in ["stock", "market", "price", "analysis"])
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_science_content_with_arxiv_flow(self):
        """
        E2E: Usuario genera contenido científico con arXiv
        
        Flow:
        1. Usuario solicita contenido sobre Quantum Computing
        2. POST a /science/generate
        3. Orchestrator detecta contenido científico
        4. ScienceAgent busca en arXiv
        5. ScienceAgent genera con Graph RAG
        6. Usuario recibe contenido con papers citados
        """
        request_data = {
            "topic": "Quantum Computing advances",
            "platform": "blog",
            "audience": "technical",
            "language": "English"
        }
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            response = await client.post(
                f"{API_PREFIX}/science/generate",
                json=request_data
            )
            
            assert response.status_code == 200
            data = response.json()
            
            # Validar estructura
            assert "content" in data
            assert "agent_used" in data
            assert data["agent_used"] == "science"
            
            # Validar contenido científico
            content = data["content"].lower()
            assert any(word in content for word in ["quantum", "research", "computing"])
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_multi_platform_content_flow(self):
        """
        E2E: Usuario genera contenido para múltiples plataformas
        
        Simula usuario generando el mismo tema para diferentes plataformas
        y valida que el contenido se adapta a cada una.
        """
        topic = "Sostenibilidad y cambio climático"
        platforms = ["twitter", "instagram", "linkedin", "blog"]
        
        results = {}
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            for platform in platforms:
                request_data = {
                    "topic": topic,
                    "platform": platform,
                    "audience": "general",
                    "language": "Spanish"
                }
                
                response = await client.post(
                    f"{API_PREFIX}/content/generate",
                    json=request_data
                )
                
                assert response.status_code == 200
                data = response.json()
                results[platform] = data["content"]
        
        # Validar que el contenido es diferente para cada plataforma
        assert len(results) == 4
        assert results["twitter"] != results["blog"]  # Diferente longitud/estilo
        
        # Twitter debe ser más corto
        assert len(results["twitter"]) < len(results["blog"])
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_error_handling_flow(self):
        """
        E2E: Usuario envía datos inválidos y recibe error claro
        
        Flow:
        1. Usuario olvida campo requerido
        2. POST con datos incompletos
        3. API valida con Pydantic
        4. Usuario recibe error 422 descriptivo
        """
        invalid_requests = [
            {},  # Vacío
            {"topic": ""},  # Topic vacío
            {"topic": "Test", "platform": "invalid"},  # Platform inválida
        ]
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            for invalid_data in invalid_requests:
                response = await client.post(
                    f"{API_PREFIX}/content/generate",
                    json=invalid_data
                )
                
                # Debe rechazar con validation error
                assert response.status_code == 422
                data = response.json()
                assert "detail" in data
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_concurrent_requests_flow(self):
        """
        E2E: Múltiples usuarios generando contenido simultáneamente
        
        Simula carga concurrente para validar que el sistema maneja
        múltiples requests sin fallar.
        """
        request_data = {
            "topic": "Tecnología del futuro",
            "platform": "twitter",
            "audience": "general",
            "language": "Spanish"
        }
        
        async def make_request(client):
            response = await client.post(
                f"{API_PREFIX}/content/generate",
                json=request_data
            )
            return response.status_code == 200
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            # 5 requests concurrentes
            results = await asyncio.gather(
                *[make_request(client) for _ in range(5)]
            )
        
        # Todas deben ser exitosas
        assert all(results), "Algunas requests concurrentes fallaron"
        assert len(results) == 5
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_orchestrator_routing_flow(self):
        """
        E2E: Orchestrator enruta correctamente según tipo de contenido
        
        Flow:
        1. Usuario solicita diferentes tipos de contenido
        2. Orchestrator detecta el tipo apropiado
        3. Enruta al agente correcto
        4. Usuario recibe respuesta del agente esperado
        """
        test_cases = [
            {
                "request": {
                    "topic": "Apple stock market trends",
                    "platform": "blog",
                    "audience": "professional",
                    "language": "English"
                },
                "expected_agent": "financial"
            },
            {
                "request": {
                    "topic": "Quantum physics research",
                    "platform": "blog",
                    "audience": "technical",
                    "language": "English"
                },
                "expected_agent": "science"
            },
            {
                "request": {
                    "topic": "Mejores restaurantes de Madrid",
                    "platform": "instagram",
                    "audience": "general",
                    "language": "Spanish"
                },
                "expected_agent": "content"
            }
        ]
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            for case in test_cases:
                response = await client.post(
                    f"{API_PREFIX}/content/generate",
                    json=case["request"]
                )
                
                assert response.status_code == 200
                data = response.json()
                
                # Verificar que usó el agente correcto
                assert data["agent_used"] == case["expected_agent"], \
                    f"Expected {case['expected_agent']}, got {data['agent_used']}"


class TestAPIConfigEndpoints:
    """Tests E2E de endpoints de configuración"""
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_content_config_endpoint(self):
        """E2E: Usuario obtiene configuración de plataformas"""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            response = await client.get(f"{API_PREFIX}/content/config")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "platforms" in data
            assert "audiences" in data
            assert "tones" in data
            
            # Validar que incluye las plataformas esperadas
            assert "twitter" in data["platforms"]
            assert "instagram" in data["platforms"]
    
    @pytest.mark.asyncio
    @pytest.mark.e2e
    async def test_financial_config_endpoint(self):
        """E2E: Usuario obtiene configuración financiera"""
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
            response = await client.get(f"{API_PREFIX}/financial/config")
            
            assert response.status_code == 200
            data = response.json()
            
            assert "analysis_types" in data


@pytest.mark.e2e
class TestPerformanceMetrics:
    """Tests E2E de métricas de performance"""
    
    @pytest.mark.asyncio
    async def test_response_time_twitter(self):
        """E2E: Tiempo de respuesta para Twitter debe ser < 10s"""
        import time
        
        request_data = {
            "topic": "IA generativa",
            "platform": "twitter",
            "audience": "general",
            "language": "Spanish"
        }
        
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
            start_time = time.time()
            
            response = await client.post(
                f"{API_PREFIX}/content/generate",
                json=request_data
            )
            
            elapsed_time = time.time() - start_time
            
            assert response.status_code == 200
            assert elapsed_time < 10.0, f"Response took {elapsed_time:.2f}s (max 10s)"
