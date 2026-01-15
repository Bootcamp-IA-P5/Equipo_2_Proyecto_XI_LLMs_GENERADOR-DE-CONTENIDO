"""
Agente para contenido general
"""
from app.services.llm_service import LLMService
from app.services.image_service import ImageService
from app.core.prompts import build_content_prompt


class ContentAgent: 
    """Agente especializado en contenido general para redes sociales"""
    
    description = "Agente de contenido general para blogs y redes sociales"
    
    # Tamaños de imagen por plataforma
    PLATFORM_IMAGE_SIZES = {
        "twitter": (1200, 675),
        "instagram": (1080, 1080),
        "linkedin": (1200, 627),
        "blog": (1200, 630)
    }
    
    def __init__(self, llm_provider:  str = "groq"):
        self.llm_service = LLMService(provider=llm_provider)
    
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
        
        # Generar imagen
        width, height = self.PLATFORM_IMAGE_SIZES.get(platform, (1200, 630))
        image_url = await ImageService.generate_image(
            prompt=topic,
            width=width,
            height=height
        )
        
        return {
            "content": content,
            "topic": topic,
            "platform":  platform,
            "audience": audience,
            "language": language,
            "image_url": image_url,
            "model_used": self.llm_service.model_name
        }