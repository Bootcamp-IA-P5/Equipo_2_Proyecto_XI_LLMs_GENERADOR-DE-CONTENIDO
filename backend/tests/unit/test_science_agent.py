"""
Tests unitarios para ScienceAgent
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.agents.science_agent import ScienceAgent


class TestScienceAgent:
    """Suite de tests para ScienceAgent"""
    
    @pytest.fixture
    def agent(self):
        """Crea instancia de ScienceAgent con servicios mockeados"""
        with patch('app.agents.science_agent.GraphRAGService') as mock_graph:
            mock_graph_instance = MagicMock()
            mock_graph_instance.generate_content = AsyncMock(
                return_value={
                    "content": "Scientific content with RAG",
                    "sources": [],
                    "graph_concepts": []
                }
            )
            mock_graph.return_value = mock_graph_instance
            return ScienceAgent(llm_provider="groq")
    
    @pytest.mark.asyncio
    async def test_generate_scientific_content(self, agent):
        """Test: Generación de contenido científico con RAG"""
        result = await agent.generate(
            topic="Machine Learning",
            platform="blog",
            audience="technical",
            language="Spanish"
        )
        
        assert result is not None
        assert "content" in result
        assert result["topic"] == "Machine Learning"
        agent.graph_rag.generate_content.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test: Inicialización correcta del agente"""
        with patch('app.agents.science_agent.GraphRAGService'):
            agent = ScienceAgent(llm_provider="groq")
            assert agent.graph_rag is not None
    
    @pytest.mark.asyncio
    async def test_generate_with_different_platforms(self, agent):
        """Test: Generación para diferentes plataformas"""
        platforms = ["blog", "twitter", "linkedin"]
        
        for platform in platforms:
            agent.graph_rag.generate_content.reset_mock()
            result = await agent.generate(
                topic="Quantum Physics",
                platform=platform,
                audience="technical",
                language="Spanish"
            )
            
            assert result["platform"] == platform
            agent.graph_rag.generate_content.assert_called_once()
    
    def test_agent_description(self):
        """Test: Agente tiene descripción"""
        assert ScienceAgent.description is not None
        assert "científico" in ScienceAgent.description.lower() or "ciencia" in ScienceAgent.description.lower()
