"""
Agente para contenido científico divulgativo con RAG
"""
from app.services.graph_rag_service import GraphRAGService
from app.services.image_service import ImageService


class ScienceAgent:
    """Agente especializado en divulgación científica con RAG"""
    
    description = "Agente científico con acceso a papers de arXiv y grafo de conocimiento"
    
    # Tamaños de imagen por plataforma
    PLATFORM_IMAGE_SIZES = {
        "twitter": (1200, 675),
        "instagram": (1080, 1080),
        "linkedin": (1200, 627),
        "blog": (1200, 630)
    }
    
    def __init__(self, llm_provider:  str = "groq"):
        self.graph_rag = GraphRAGService(llm_provider=llm_provider)
    
    async def generate(
        self,
        topic: str,
        platform: str,
        audience: str,
        language: str = "Spanish",
        scientific_area: str = "ai",
        **kwargs
    ) -> dict:
        """Genera contenido científico divulgativo"""
        
        result = await self.graph_rag.generate_content(
            topic=topic,
            platform=platform,
            language=language
        )
        
        # Generar imagen
        width, height = self.PLATFORM_IMAGE_SIZES.get(platform, (1200, 630))
        image_url = await ImageService.generate_image(
            prompt=f"scientific research {topic}",
            width=width,
            height=height
        )
        
        return {
            "content": result["content"],
            "topic": topic,
            "platform": platform,
            "sources": result.get("sources", []),
            "graph_concepts": result.get("graph_concepts", []),
            "scientific_area":  scientific_area,
            "image_url": image_url
        }
