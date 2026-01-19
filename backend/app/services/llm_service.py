"""
Servicio para interactuar con diferentes LLMs
"""
import asyncio
from typing import Dict, Optional
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage
from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """Servicio unificado para interactuar con LLMs"""
    
    # Singleton instances per provider
    _instances: Dict[str, "LLMService"] = {}
    _lock = asyncio.Lock()
    
    def __new__(cls, provider: str = "groq") -> "LLMService":
        """Singleton pattern - return existing instance if available"""
        if provider not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[provider] = instance
        return cls._instances[provider]
    
    def __init__(self, provider: str = "groq"):
        # Only initialize once per instance
        if getattr(self, '_initialized', False):
            return
            
        self.provider = provider
        self.llm = self._initialize_llm()
        self.model_name = self._get_model_name()
        self._initialized = True
    
    @classmethod
    def get_instance(cls, provider: str = "groq") -> "LLMService":
        """Factory method to get or create an LLMService instance"""
        return cls(provider)
    
    @classmethod
    def reset_instances(cls):
        """Reset all instances (useful for testing)"""
        cls._instances.clear()
    
    def _get_model_name(self) -> str:
        if self.provider == "groq":  
            return settings.DEFAULT_GROQ_MODEL
        return settings.DEFAULT_OLLAMA_MODEL
    
    def _initialize_llm(self):
        if self.provider == "groq":  
            return ChatGroq(
                model=settings.DEFAULT_GROQ_MODEL,
                api_key=settings.GROQ_API_KEY,
                temperature=0.7,
                max_tokens=4096
            )
        elif self.provider == "ollama":  
            return Ollama(
                model=settings.DEFAULT_OLLAMA_MODEL,
                base_url=settings.OLLAMA_BASE_URL,
                temperature=0.7
            )
        else:
            raise ValueError(f"Provider '{self.provider}' no soportado")
    
    async def generate(self, prompt: str) -> str:
        """Genera contenido basado en el prompt"""
        try:
            if self.provider == "groq":  
                response = await self.llm.ainvoke([HumanMessage(content=prompt)])
                return response.content
            else: 
                # ✅ CORREGIDO: Ejecutar Ollama en un thread separado para no bloquear el event loop
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,  # Usa el executor por defecto (ThreadPoolExecutor)
                    lambda: self.llm.invoke(prompt)
                )
                return response
        except Exception as e:
            raise Exception(f"Error al generar contenido con {self.provider}:  {str(e)}")


def get_llm_service(provider: str = "groq") -> LLMService:
    """
    Factory function to get a shared LLMService instance.
    
    This ensures all components share the same LLM connection,
    reducing resource usage and improving efficiency.
    
    Args:
        provider: The LLM provider ("groq" or "ollama")
        
    Returns:
        A shared LLMService instance for the specified provider
    """
    return LLMService.get_instance(provider)