"""
Rutas específicas para contenido científico
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.rag.arxiv_loader import ArxivLoader
from app.services.science_rag_service import ScienceRAGService

router = APIRouter(prefix="/science", tags=["Science"])


class ArxivSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    max_results: int = 10


class ScienceContentRequest(BaseModel):
    topic: str
    scientific_area: str = "ai"
    platform: str = "blog"
    language:  str = "Spanish"
    llm_provider: str = "groq"


@router.post("/search-papers")
async def search_arxiv_papers(request: ArxivSearchRequest):
    """Busca papers en arXiv"""
    papers = ArxivLoader.search_papers(
        query=request.query,
        category=request.category,
        max_results=request.max_results
    )
    
    return {
        "papers":  [
            {
                "id": p.id,
                "title": p.title,
                "authors": p.authors,
                "summary": p.summary[: 500],
                "published":  p.published,
                "pdf_url": p.pdf_url
            }
            for p in papers
        ],
        "total":  len(papers)
    }


@router.post("/generate")
async def generate_science_content(request: ScienceContentRequest):
    """Genera contenido científico divulgativo con RAG"""
    try:
        service = ScienceRAGService(llm_provider=request.llm_provider)
        
        result = await service.generate_content(
            topic=request.topic,
            scientific_area=request.scientific_area,
            platform=request.platform,
            language=request.language
        )
        
        return result
        
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_science_categories():
    """Obtiene las categorías científicas disponibles"""
    return {
        "categories": [
            {"id": "ai", "name":  "Inteligencia Artificial"},
            {"id":  "machine_learning", "name":  "Machine Learning"},
            {"id": "nlp", "name":  "Procesamiento de Lenguaje Natural"},
            {"id": "quantum_physics", "name": "Física Cuántica"},
            {"id": "astrophysics", "name": "Astrofísica"},
            {"id": "biomedicine", "name":  "Biomedicina"},
        ]
    }