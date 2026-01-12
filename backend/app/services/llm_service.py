"""
Servicio para interactuar con diferentes LLMs
"""
import asyncio
from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage
from app.core.config import get_settings

settings = get_settings()


class LLMService:
    """Servicio unificado para interactuar con LLMs"""
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider
        self.llm = self._initialize_llm()
        self.model_name = self._get_model_name()
    
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