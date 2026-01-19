"""
Tests unitarios para FinancialAgent
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.financial_agent import FinancialAgent


class TestFinancialAgent:
    """Suite de tests para FinancialAgent"""
    
    @pytest.fixture
    def agent(self, mock_llm_service):
        """Crea instancia de FinancialAgent con servicios mockeados"""
        with patch('app.agents.financial_agent.get_llm_service') as mock_llm:
            mock_llm.return_value = mock_llm_service
            return FinancialAgent(llm_provider="groq")
    
    @pytest.mark.asyncio
    async def test_generate_financial_analysis(self, agent, mock_llm_service):
        """Test: Generación de análisis financiero"""
        # Arrange
        expected_content = "Análisis financiero de Apple Inc..."
        mock_llm_service.generate.return_value = expected_content
        
        # Act
        result = await agent.generate(
            topic="Apple Inc. Analysis",
            platform="blog",
            audience="professional",
            language="Spanish"
        )
        
        # Assert
        assert result is not None
        assert result["content"] == expected_content
        assert result["topic"] == "Apple Inc. Analysis"
        assert "market_summary" in result
        mock_llm_service.generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test: Inicialización correcta del agente"""
        with patch('app.agents.financial_agent.get_llm_service'):
            agent = FinancialAgent(llm_provider="groq")
            assert agent.llm_service is not None
    
    def test_agent_description(self):
        """Test: Agente tiene descripción"""
        assert FinancialAgent.description is not None
        assert "financiero" in FinancialAgent.description.lower()
