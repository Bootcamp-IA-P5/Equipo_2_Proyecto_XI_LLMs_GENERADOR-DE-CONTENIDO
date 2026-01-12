"""
Vector Store con ChromaDB para RAG
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Optional
from app.core.config import get_settings
from app.rag.arxiv_loader import ArxivLoader, ArxivDocument

settings = get_settings()


class VectorStore: 
    """Vector Store usando ChromaDB"""
    
    def __init__(self, collection_name: str = "arxiv_papers"):
        self.collection_name = collection_name
        
        # Inicializar ChromaDB
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PERSIST_DIR,
            settings=chromadb.config.Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Obtener o crear colección
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Scientific papers from arXiv"}
        )
        
        # Modelo de embeddings
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def _get_embedding(self, text:  str) -> List[float]:
        """Genera embedding para un texto"""
        return self.embedding_model.encode(text).tolist()
    
    def add_documents(self, documents:  List[ArxivDocument]) -> int:
        """Añade documentos al vector store"""
        ids = []
        embeddings = []
        metadatas = []
        texts = []
        
        for doc in documents:
            # Combinar título y resumen para el embedding
            full_text = f"{doc.title}\n\n{doc.summary}"
            
            ids.append(doc.id)
            embeddings.append(self._get_embedding(full_text))
            metadatas.append({
                "title": doc.title,
                "authors": ", ".join(doc.authors[: 3]),  # Primeros 3 autores
                "published": doc.published,
                "categories": ", ".join(doc.categories),
                "pdf_url": doc.pdf_url
            })
            texts.append(full_text)
        
        # Añadir a ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts
        )
        
        return len(documents)
    
    def search(self, query: str, n_results: int = 5) -> List[dict]:
        """Busca documentos similares"""
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Formatear resultados
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "similarity":  1 - results['distances'][0][i]  # Convertir distancia a similitud
            })
        
        return formatted
    
    def index_from_arxiv(self, query: str, category: str = None, max_papers: int = 20) -> int:
        """Indexa papers desde arXiv"""
        papers = ArxivLoader.search_papers(query, category, max_papers)
        return self.add_documents(papers)