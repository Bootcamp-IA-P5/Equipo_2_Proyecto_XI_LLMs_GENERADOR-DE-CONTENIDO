"""
Tests unitarios para LLMService
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.llm_service import LLMService


class TestLLMService:
    """Suite de tests para LLMService"""
    
    @pytest.mark.asyncio
    async def test_groq_provider_initialization(self):
        """Test: Inicialización con Groq"""
        with patch('app.services.llm_service.ChatGroq') as mock_groq:
            service = LLMService(provider="groq")
            assert service.provider == "groq"
            mock_groq.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_ollama_provider_initialization(self):
        """Test: Inicialización con Ollama"""
        with patch('app.services.llm_service.Ollama') as mock_ollama:
            service = LLMService(provider="ollama")
            assert service.provider == "ollama"
            mock_ollama.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_with_groq(self):
        """Test: Generación de contenido con Groq"""
        with patch('app.services.llm_service.ChatGroq') as mock_groq:
            # Configurar mock
            mock_llm = MagicMock()
            mock_llm.ainvoke = AsyncMock(return_value=MagicMock(content="Test response"))
            mock_groq.return_value = mock_llm
            
            service = LLMService(provider="groq")
            result = await service.generate("Test prompt")
            
            assert result == "Test response"
            mock_llm.ainvoke.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_handles_error(self):
        """Test: Manejo de errores en generación"""
        with patch('app.services.llm_service.ChatGroq') as mock_groq:
            mock_llm = MagicMock()
            mock_llm.ainvoke = AsyncMock(side_effect=Exception("API Error"))
            mock_groq.return_value = mock_llm
            
            service = LLMService(provider="groq")
            
            with pytest.raises(Exception):
                await service.generate("Test prompt")
    
    def test_invalid_provider(self):
        """Test: Provider inválido lanza excepción"""
        with pytest.raises(ValueError):
            LLMService(provider="invalid_provider")
