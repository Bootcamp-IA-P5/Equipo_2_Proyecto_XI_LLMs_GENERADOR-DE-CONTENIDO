"""
Agente para contenido científico divulgativo con RAG
"""
from app.services.graph_rag_service import GraphRAGService


class ScienceAgent:
    """Agente especializado en divulgación científica con RAG"""
    
    description = "Agente científico con acceso a papers de arXiv y grafo de conocimiento"
    
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
        
        return {
            "content": result["content"],
            "topic": topic,
            "platform": platform,
            "sources": result.get("sources", []),
            "graph_concepts": result.get("graph_concepts", []),
            "scientific_area":  scientific_area
        }
