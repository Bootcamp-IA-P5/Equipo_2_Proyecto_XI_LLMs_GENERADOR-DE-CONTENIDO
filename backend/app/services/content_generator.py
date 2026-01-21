"""
Servicio principal de generación de contenido
"""
import urllib.parse
from app.services.llm_service import LLMService
from app.core.prompts import build_content_prompt
from app.models.schemas import ContentRequest, ContentResponse
from app.services.image_service import ImageService


class ContentGeneratorService:
    """Servicio para generar contenido para diferentes plataformas"""
    
    async def generate(self, request: ContentRequest) -> ContentResponse:
        """
        Genera contenido basado en la solicitud
        """
        # Inicializar el servicio LLM
        llm_service = LLMService(provider=request.llm_provider.value)
        
        # Construir el prompt
        prompt = build_content_prompt(
            topic=request.topic,
            platform=request.platform.value,
            audience=request.audience.value,
            additional_context=request.additional_context or "",
            tone=request.tone or "",
            language=request.language
        )
        
        # Generar contenido
        content = await llm_service.generate(prompt)

        # Tamaños por plataforma
        sizes = {
            "twitter": (1200, 675),
            "instagram":(1080, 1080),
            "linkedin": (1200, 627),
            "blog":  (1200, 630)
        }
        width, height = sizes.get(request.platform.value, (1200, 630))
        
        # Generar imagen con Pollinations
        image_url = await ImageService.generate_image(
            prompt=request.topic,
            width=width,
            height=height
        )
        
        # Fallback si falla
        if not image_url: 
            safe_text = urllib.parse.quote(request.topic[:30])
            image_url = f"https://placehold.co/{width}x{height}/4A90A4/ffffff?text={safe_text}"
        
        return ContentResponse(
            content=content,
            platform=request.platform.value,
            audience=request.audience.value,
            topic=request.topic,
            llm_provider=request.llm_provider.value,
            model_used=llm_service.model_name,
            image_url=image_url
        )