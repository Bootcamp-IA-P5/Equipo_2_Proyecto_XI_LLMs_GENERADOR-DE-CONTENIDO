"""
Agente para contenido general
"""
from app.services.llm_service import get_llm_service
from app.core.prompts import build_content_prompt


class ContentAgent: 
    """Agente especializado en contenido general para redes sociales"""
    
    description = "Agente de contenido general para blogs y redes sociales"
    
    def __init__(self, llm_provider:  str = "groq"):
        self.llm_service = get_llm_service(provider=llm_provider)
    
    async def generate(
        self,
        topic: str,
        platform:  str,
        audience: str,
        language: str = "Spanish",
        tone: str = "",
        additional_context: str = "",
        **kwargs
    ) -> dict:
        """Genera contenido general"""
        
        prompt = build_content_prompt(
            topic=topic,
            platform=platform,
            audience=audience,
            additional_context=additional_context,
            tone=tone,
            language=language
        )
        
        content = await self.llm_service.generate(prompt)
        
        return {
            "content": content,
            "topic": topic,
            "platform":  platform,
            "audience": audience,
            "language": language
        }