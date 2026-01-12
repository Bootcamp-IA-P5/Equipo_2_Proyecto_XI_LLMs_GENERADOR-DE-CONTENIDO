"""
Cargador de documentos científicos desde arXiv
"""
import arxiv
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ArxivDocument: 
    """Documento de arXiv"""
    id: str
    title: str
    authors: List[str]
    summary: str
    published: str
    categories: List[str]
    pdf_url: str
    

class ArxivLoader:
    """Cargador de papers de arXiv"""
    
    # Categorías científicas principales
    CATEGORIES = {
        "ai":  "cs.AI",
        "machine_learning": "cs.LG",
        "nlp": "cs.CL",
        "computer_vision": "cs.CV",
        "quantum_physics": "quant-ph",
        "astrophysics": "astro-ph",
        "biomedicine": "q-bio",
        "mathematics": "math",
        "physics": "physics",
    }
    
    @classmethod
    def search_papers(
        cls,
        query: str,
        category: Optional[str] = None,
        max_results: int = 10
    ) -> List[ArxivDocument]: 
        """Busca papers en arXiv"""
        
        # Construir query con categoría si se especifica
        search_query = query
        if category and category in cls.CATEGORIES:
            search_query = f"cat:{cls.CATEGORIES[category]} AND {query}"
        
        # Realizar búsqueda
        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        documents = []
        for result in search.results():
            doc = ArxivDocument(
                id=result.entry_id,
                title=result.title,
                authors=[author.name for author in result.authors],
                summary=result.summary,
                published=result.published.strftime("%Y-%m-%d"),
                categories=result.categories,
                pdf_url=result.pdf_url
            )
            documents.append(doc)
        
        return documents
    
    @classmethod
    def get_paper_by_id(cls, arxiv_id: str) -> Optional[ArxivDocument]: 
        """Obtiene un paper específico por su ID"""
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(search.results())
            
            return ArxivDocument(
                id=result.entry_id,
                title=result.title,
                authors=[author.name for author in result.authors],
                summary=result.summary,
                published=result.published.strftime("%Y-%m-%d"),
                categories=result.categories,
                pdf_url=result.pdf_url
            )
        except Exception: 
            return None