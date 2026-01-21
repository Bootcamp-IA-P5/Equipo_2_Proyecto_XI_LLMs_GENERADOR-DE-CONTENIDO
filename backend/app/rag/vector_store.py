"""
Vector Store con ChromaDB para RAG
Enhanced with: chunking, reranking, relevance filtering, and hybrid search
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer, CrossEncoder
from typing import List
import re
from app.core.config import get_settings
from app.rag.arxiv_loader import ArxivLoader, ArxivDocument

settings = get_settings()


class TextChunker:
    """Intelligent text chunking for better retrieval"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[dict]:
        """Split text into overlapping chunks while preserving sentence boundaries"""
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ' '.join(current_chunk)
                chunks.append({
                    "text": chunk_text,
                    "metadata": {**(metadata or {}), "chunk_index": len(chunks)},
                    "length": len(chunk_text)
                })
                
                # Keep overlap sentences
                overlap_length = 0
                overlap_sentences = []
                for s in reversed(current_chunk):
                    if overlap_length + len(s) < self.overlap:
                        overlap_sentences.insert(0, s)
                        overlap_length += len(s)
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_length = overlap_length
            
            current_chunk.append(sentence)
            current_length += sentence_length
        
        # Add remaining chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "metadata": {**(metadata or {}), "chunk_index": len(chunks)},
                "length": len(chunk_text)
            })
        
        return chunks


class VectorStore: 
    """
    Enhanced Vector Store using ChromaDB
    Features: chunking, reranking, relevance filtering, hybrid search
    """
    
    # Reranking model for improved relevance
    RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    
    def __init__(self, collection_name: str = "arxiv_papers", enable_reranking: bool = True):
        self.collection_name = collection_name
        self.enable_reranking = enable_reranking
        self.chunker = TextChunker(chunk_size=512, overlap=50)
        
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
        
        # Modelo de embeddings (bi-encoder for retrieval)
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        
        # Cross-encoder for reranking (lazy loaded)
        self._reranker = None
    
    @property
    def reranker(self):
        """Lazy load reranker to save memory"""
        if self._reranker is None and self.enable_reranking:
            try:
                self._reranker = CrossEncoder(self.RERANKER_MODEL)
            except Exception:
                self.enable_reranking = False
        return self._reranker
    
    def _get_embedding(self, text: str) -> List[float]:
        """Genera embedding para un texto"""
        return self.embedding_model.encode(text).tolist()
    
    def _rerank_results(self, query: str, results: List[dict], top_k: int = 5) -> List[dict]:
        """Rerank results using cross-encoder for better relevance"""
        if not self.enable_reranking or not results or self.reranker is None:
            return results[:top_k]
        
        # Prepare pairs for reranking
        pairs = [(query, doc["content"]) for doc in results]
        
        # Get reranking scores
        scores = self.reranker.predict(pairs)
        
        # Add scores and sort
        for i, doc in enumerate(results):
            doc["rerank_score"] = float(scores[i])
        
        # Sort by rerank score (higher is better)
        reranked = sorted(results, key=lambda x: x["rerank_score"], reverse=True)
        
        return reranked[:top_k]
    
    def _filter_by_relevance(self, results: List[dict], min_similarity: float = 0.3) -> List[dict]:
        """Filter out low-relevance results"""
        return [doc for doc in results if doc.get("similarity", 0) >= min_similarity]

    def add_documents(self, documents: List[ArxivDocument], use_chunking: bool = True) -> int:
        """Añade documentos al vector store con chunking opcional"""
        ids = []
        embeddings = []
        metadatas = []
        texts = []
        
        for doc in documents:
            base_metadata = {
                "title": doc.title,
                "authors": ", ".join(doc.authors[:3]),
                "published": doc.published,
                "categories": ", ".join(doc.categories),
                "pdf_url": doc.pdf_url,
                "paper_id": doc.id
            }
            
            full_text = f"{doc.title}\n\n{doc.summary}"
            
            if use_chunking and len(full_text) > 600:
                # Chunk long documents
                chunks = self.chunker.chunk_text(full_text, base_metadata)
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{doc.id}_chunk_{i}"
                    ids.append(chunk_id)
                    embeddings.append(self._get_embedding(chunk["text"]))
                    metadatas.append(chunk["metadata"])
                    texts.append(chunk["text"])
            else:
                # Short documents: store as-is
                ids.append(doc.id)
                embeddings.append(self._get_embedding(full_text))
                metadatas.append(base_metadata)
                texts.append(full_text)
        
        # Añadir a ChromaDB (skip duplicates)
        existing_ids = set(self.collection.get()["ids"])
        new_data = [(i, e, m, t) for i, e, m, t in zip(ids, embeddings, metadatas, texts) if i not in existing_ids]
        
        if new_data:
            new_ids, new_embeddings, new_metadatas, new_texts = zip(*new_data)
            self.collection.add(
                ids=list(new_ids),
                embeddings=list(new_embeddings),
                metadatas=list(new_metadatas),
                documents=list(new_texts)
            )
        
        return len(new_data)
    
    def search(
        self, 
        query: str, 
        n_results: int = 5,
        min_similarity: float = 0.3,
        use_reranking: bool = True,
        filter_categories: List[str] = None
    ) -> List[dict]:
        """
        Enhanced search with reranking and relevance filtering
        
        Args:
            query: Search query
            n_results: Number of results to return
            min_similarity: Minimum similarity threshold (0-1)
            use_reranking: Whether to use cross-encoder reranking
            filter_categories: Optional category filter (e.g., ["cs.AI", "cs.LG"])
        """
        # Retrieve more candidates for reranking
        retrieve_k = n_results * 3 if use_reranking else n_results
        
        query_embedding = self._get_embedding(query)
        
        # Build where clause for filtering
        where_clause = None
        if filter_categories:
            # ChromaDB where clause for category filtering
            where_clause = {"categories": {"$in": filter_categories}}
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=retrieve_k,
            include=["documents", "metadatas", "distances"],
            where=where_clause
        )
        
        # Handle empty results
        if not results['ids'] or not results['ids'][0]:
            return []
        
        # Formatear resultados
        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "similarity": 1 - results['distances'][0][i]
            })
        
        # Filter by minimum similarity
        formatted = self._filter_by_relevance(formatted, min_similarity)
        
        # Rerank if enabled
        if use_reranking and self.enable_reranking:
            formatted = self._rerank_results(query, formatted, top_k=n_results)
        else:
            formatted = formatted[:n_results]
        
        return formatted
    
    def hybrid_search(
        self,
        query: str,
        keywords: List[str] = None,
        n_results: int = 5
    ) -> List[dict]:
        """
        Hybrid search combining semantic similarity with keyword matching
        
        Args:
            query: Natural language query
            keywords: Optional explicit keywords to boost
            n_results: Number of results
        """
        # Semantic search
        semantic_results = self.search(query, n_results=n_results * 2, use_reranking=False)
        
        if not keywords:
            return self._rerank_results(query, semantic_results, top_k=n_results)
        
        # Boost results containing keywords
        for doc in semantic_results:
            keyword_score = sum(
                1 for kw in keywords 
                if kw.lower() in doc["content"].lower()
            ) / len(keywords)
            doc["keyword_score"] = keyword_score
            doc["hybrid_score"] = doc["similarity"] * 0.7 + keyword_score * 0.3
        
        # Sort by hybrid score
        semantic_results.sort(key=lambda x: x["hybrid_score"], reverse=True)
        
        return self._rerank_results(query, semantic_results[:n_results * 2], top_k=n_results)

    def index_from_arxiv(self, query: str, category: str = None, max_papers: int = 20) -> int:
        """Indexa papers desde arXiv"""
        papers = ArxivLoader.search_papers(query, category, max_papers)
        return self.add_documents(papers)
    
    def get_collection_stats(self) -> dict:
        """Get statistics about the collection"""
        all_docs = self.collection.get()
        return {
            "total_documents": len(all_docs["ids"]),
            "collection_name": self.collection_name,
            "embedding_model": settings.EMBEDDING_MODEL,
            "reranking_enabled": self.enable_reranking
        }