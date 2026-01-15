"""
Orquestador del sistema multi-agente
"""
from enum import Enum
from typing import Optional
from app.agents.content_agent import ContentAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.science_agent import ScienceAgent
from app.services.image_service import ImageService


class AgentType(str, Enum):
    CONTENT = "content"
    FINANCIAL = "financial"
    SCIENCE = "science"


class AgentOrchestrator:
    """Orquestador que dirige las peticiones al agente correcto"""
    
    # Palabras clave para detectar el tipo de contenido
    FINANCIAL_KEYWORDS = [
        "mercado", "bolsa", "acciones", "inversión", "finanzas", "trading",
        "stock", "market", "investment", "crypto", "bitcoin", "economía",
        "ibex", "nasdaq", "sp500", "dow jones", "dividendos", "forex"
    ]
    
    SCIENCE_KEYWORDS = [
        "científico", "investigación", "paper", "estudio", "arxiv",
        "física", "química", "biología", "medicina", "quantum", "cuántico",
        "inteligencia artificial", "machine learning", "neurociencia",
        "astrofísica", "genética", "climate", "cambio climático"
    ]
    
    def __init__(self, llm_provider: str = "groq"):
        self.llm_provider = llm_provider
        self.agents = {
            AgentType.CONTENT: ContentAgent(llm_provider),
            AgentType.FINANCIAL: FinancialAgent(llm_provider),
            AgentType.SCIENCE: ScienceAgent(llm_provider),
        }
    
    def detect_agent_type(self, topic: str, explicit_type: Optional[str] = None) -> AgentType:
        """Detecta qué agente debe manejar la petición"""
        
        # Si se especifica explícitamente
        if explicit_type:
            try:
                return AgentType(explicit_type)
            except ValueError:
                pass
        
        topic_lower = topic.lower()
        
        # Detectar por palabras clave
        financial_score = sum(1 for kw in self.FINANCIAL_KEYWORDS if kw in topic_lower)
        science_score = sum(1 for kw in self.SCIENCE_KEYWORDS if kw in topic_lower)
        
        if financial_score > science_score and financial_score > 0:
            return AgentType.FINANCIAL
        elif science_score > financial_score and science_score > 0:
            return AgentType.SCIENCE
        else:
            return AgentType.CONTENT
    
    async def process_request(
        self,
        topic: str,
        platform: str,
        audience: str,
        language: str = "Spanish",
        content_type: Optional[str] = None,
        **kwargs
    ) -> dict:
        """Procesa una petición delegando al agente apropiado"""
        
        # 1. Detectar tipo de agente
        agent_type = self.detect_agent_type(topic, content_type)
        
        # 2. Obtener agente
        agent = self.agents[agent_type]
        
        # 3. Procesar con el agente correspondiente
        result = await agent.generate(
            topic=topic,
            platform=platform,
            audience=audience,
            language=language,
            **kwargs
        )
        
        # 4. Añadir metadata
        result["agent_used"] = agent_type.value
        result["agent_description"] = agent.description
        
        # 5. Generar imagen con Pollinations
        sizes = {
            "twitter": (1200, 675),
            "instagram": (1080, 1080),
            "linkedin": (1200, 627),
            "blog": (1200, 630)
        }
        width, height = sizes.get(platform, (1200, 630))
        
        image_url = await ImageService.generate_image(
            prompt=topic,
            width=width,
            height=height
        )
        
        if image_url:
            result["image_url"] = image_url
        
        return result
