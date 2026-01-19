"""
Tests unitarios para ContentAgent
"""
import pytest
from unittest.mock import patch
from app.agents.content_agent import ContentAgent


class TestContentAgent:
    """Suite de tests para ContentAgent"""
    
    @pytest.fixture
    def agent(self, mock_llm_service):
        """Crea instancia de ContentAgent con LLM mockeado"""
        with patch('app.agents.content_agent.LLMService') as mock:
            mock.return_value = mock_llm_service
            return ContentAgent(llm_provider="groq")
    
    @pytest.mark.asyncio
    async def test_generate_basic_content(self, agent, content_request_data, mock_llm_service):
        """Test: Generación básica de contenido"""
        # Arrange
        expected_content = "Tweet sobre IA: Los LLMs están revolucionando el desarrollo..."
        mock_llm_service.generate.return_value = expected_content
        
        # Act
        result = await agent.generate(**content_request_data)
        
        # Assert
        assert result is not None
        assert result["content"] == expected_content
        assert result["topic"] == content_request_data["topic"]
        assert result["platform"] == content_request_data["platform"]
        assert result["audience"] == content_request_data["audience"]
        mock_llm_service.generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_different_platforms(self, agent, mock_llm_service):
        """Test: Generación para diferentes plataformas"""
        platforms = ["twitter", "linkedin", "instagram", "facebook"]
        
        for platform in platforms:
            mock_llm_service.generate.reset_mock()
            result = await agent.generate(
                topic="Test Topic",
                platform=platform,
                audience="general",
                language="Spanish"
            )
            
            assert result["platform"] == platform
            mock_llm_service.generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_with_empty_topic(self, agent):
        """Test: Manejo de topic vacío"""
        # Este test verifica que se maneje correctamente
        result = await agent.generate(
            topic="",
            platform="twitter",
            audience="general",
            language="Spanish"
        )
        
        assert result["topic"] == ""
        # El agente debería generar algo aunque el topic esté vacío
    
    @pytest.mark.asyncio
    async def test_generate_with_tone(self, agent, mock_llm_service):
        """Test: Generación con tone específico"""
        tones = ["profesional", "casual", "humorístico", "técnico"]
        
        for tone in tones:
            mock_llm_service.generate.reset_mock()
            await agent.generate(
                topic="AI Testing",
                platform="linkedin",
                audience="developers",
                language="Spanish",
                tone=tone
            )
            
            mock_llm_service.generate.assert_called_once()
            # Verificar que el prompt incluye el tone
            call_args = mock_llm_service.generate.call_args[0][0]
            assert tone.lower() in call_args.lower() or "ton" in call_args.lower()
    
    @pytest.mark.asyncio
    async def test_generate_with_additional_context(self, agent, mock_llm_service):
        """Test: Generación con contexto adicional"""
        additional_context = "Incluir estadísticas recientes y casos de uso"
        
        await agent.generate(
            topic="Machine Learning",
            platform="blog",
            audience="estudiantes",
            language="Spanish",
            additional_context=additional_context
        )
        
        # Verificar que se llamó al LLM
        mock_llm_service.generate.assert_called_once()
        
        # Verificar que el contexto se pasó en el prompt
        call_args = mock_llm_service.generate.call_args[0][0]
        assert "estadísticas" in call_args.lower() or "casos de uso" in call_args.lower()
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self):
        """Test: Inicialización del agente"""
        with patch('app.agents.content_agent.LLMService') as mock:
            agent = ContentAgent(llm_provider="groq")
            assert agent.llm_service is not None
            mock.assert_called_once_with(provider="groq")
    
    @pytest.mark.asyncio
    async def test_generate_response_structure(self, agent, mock_llm_service):
        """Test: Estructura de respuesta correcta"""
        result = await agent.generate(
            topic="Test",
            platform="twitter",
            audience="general",
            language="English"
        )
        
        # Verificar estructura del resultado
        assert isinstance(result, dict)
        assert "content" in result
        assert "topic" in result
        assert "platform" in result
        assert "audience" in result
        assert "language" in result
    
    def test_agent_description(self):
        """Test: Agente tiene descripción"""
        assert ContentAgent.description is not None
        assert len(ContentAgent.description) > 0
        assert "contenido" in ContentAgent.description.lower()
