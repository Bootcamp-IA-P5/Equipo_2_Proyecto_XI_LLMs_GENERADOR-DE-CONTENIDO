"""
Tests unitarios para Orchestrator
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.orchestrator import AgentOrchestrator


class TestAgentOrchestrator:
    """Suite de tests para AgentOrchestrator"""
    
    @pytest.fixture
    def orchestrator(self):
        """Crea instancia de Orchestrator con agentes mockeados"""
        with patch('app.agents.orchestrator.ContentAgent') as mock_content, \
             patch('app.agents.orchestrator.FinancialAgent') as mock_financial, \
             patch('app.agents.orchestrator.ScienceAgent') as mock_science:
            
            # Configurar mocks
            mock_content_instance = MagicMock()
            mock_content_instance.generate = AsyncMock(return_value={"content": "content result"})
            mock_content.return_value = mock_content_instance
            
            mock_financial_instance = MagicMock()
            mock_financial_instance.generate = AsyncMock(return_value={"content": "financial result"})
            mock_financial.return_value = mock_financial_instance
            
            mock_science_instance = MagicMock()
            mock_science_instance.generate = AsyncMock(return_value={"content": "science result"})
            mock_science.return_value = mock_science_instance
            
            return AgentOrchestrator(llm_provider="groq")
    
    @pytest.mark.asyncio
    async def test_orchestrator_initialization(self):
        """Test: Inicialización correcta con todos los agentes"""
        with patch('app.agents.orchestrator.ContentAgent'), \
             patch('app.agents.orchestrator.FinancialAgent'), \
             patch('app.agents.orchestrator.ScienceAgent'):
            
            orchestrator = AgentOrchestrator(llm_provider="groq")
            
            assert orchestrator.agents is not None
            assert len(orchestrator.agents) == 3
            assert orchestrator.llm_provider == "groq"
    
    @pytest.mark.asyncio
    async def test_route_to_content_agent(self, orchestrator):
        """Test: Routing a ContentAgent para contenido general"""
        # Use explicit content_type to ensure routing
        result = await orchestrator.process_request(
            topic="Mejores restaurantes de Madrid",
            platform="twitter",
            audience="general",
            language="Spanish",
            content_type="content"
        )
        
        assert result is not None
        assert "content" in result
        assert result["agent_used"] == "content"
        assert "agent_description" in result
    
    @pytest.mark.asyncio
    async def test_route_to_financial_agent(self, orchestrator):
        """Test: Routing a FinancialAgent para contenido financiero"""
        result = await orchestrator.process_request(
            topic="Apple stock analysis",
            platform="blog",
            audience="professional",
            language="Spanish",
            content_type="financial"
        )
        
        assert result["agent_used"] == "financial"
    
    @pytest.mark.asyncio
    async def test_route_to_science_agent(self, orchestrator):
        """Test: Routing a ScienceAgent para contenido científico"""
        result = await orchestrator.process_request(
            topic="Quantum computing",
            platform="blog",
            audience="technical",
            language="Spanish",
            content_type="science"
        )
        
        assert result is not None
        assert result["agent_used"] == "science"
    
    @pytest.mark.asyncio
    async def test_default_routing(self, orchestrator):
        """Test: Routing por defecto a ContentAgent cuando se especifica explícitamente"""
        # Use explicit content_type to ensure content agent is used
        result = await orchestrator.process_request(
            topic="General topic about cooking",
            platform="instagram",
            audience="young",
            language="English",
            content_type="content"
        )
        
        assert result is not None
        # Con content_type explícito debe ir a content_agent
        assert result["agent_used"] == "content"
    
    @pytest.mark.asyncio
    async def test_orchestrator_passes_parameters(self, orchestrator):
        """Test: Orchestrator pasa todos los parámetros correctamente"""
        result = await orchestrator.process_request(
            topic="Test topic",
            platform="linkedin",
            audience="business",
            language="Spanish",
            tone="professional",
            additional_context="extra info"
        )
        
        assert result is not None
        assert "content" in result
        assert "agent_used" in result
    
    @pytest.mark.asyncio
    async def test_detect_financial_keywords(self, orchestrator):
        """Test: Detecta contenido financiero por keywords"""
        result = await orchestrator.process_request(
            topic="Análisis del mercado de acciones y bolsa",
            platform="blog",
            audience="professional",
            language="Spanish"
        )
        assert result["agent_used"] == "financial"
    
    @pytest.mark.asyncio
    async def test_detect_science_keywords(self, orchestrator):
        """Test: Detecta contenido científico por keywords"""
        result = await orchestrator.process_request(
            topic="Investigación sobre física cuántica",
            platform="blog",
            audience="technical",
            language="Spanish"
        )
        assert result["agent_used"] == "science"
