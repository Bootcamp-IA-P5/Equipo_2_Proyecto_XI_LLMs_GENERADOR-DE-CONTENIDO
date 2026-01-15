"""
Servicio Graph RAG para contenido científico avanzado
Enhanced with: HyDE, query expansion, contextual compression, auto-learning
"""
from typing import List, Optional, Dict
import re
from app.rag.graph_store import KnowledgeGraph
from app.rag.vector_store import VectorStore
from app.services.llm_service import LLMService


class GraphRAGService:
    """
    Enhanced Graph RAG Service
    Features:
    - HyDE (Hypothetical Document Embeddings) for better retrieval
    - Query expansion for comprehensive search
    - Contextual compression to reduce noise
    - Auto-learning from retrieved documents
    """
    
    GRAPH_RAG_PROMPT = """Eres un divulgador científico experto con acceso a un grafo de conocimiento. 

## 🎯 TEMA: {topic}

## 📊 CONOCIMIENTO ESTRUCTURADO (Grafo de Conocimiento)
Las siguientes son relaciones verificadas entre conceptos científicos:

{graph_context}

## 📚 CONTEXTO DE PAPERS (Vector RAG)
{vector_context}

## 🌐 IDIOMA: {language}
## 📱 PLATAFORMA: {platform}

## ✅ INSTRUCCIONES
1. Usa el grafo de conocimiento para estructurar las conexiones entre conceptos
2. Usa los papers para detalles y datos específicos
3. Explica las relaciones entre conceptos de forma clara
4. Haz el contenido accesible para público general
5. Cita conceptos del grafo cuando establezcas conexiones
6. Si hay fuentes de papers, menciónalas brevemente

## 📤 GENERA EL CONTENIDO: 
"""

    HYDE_PROMPT = """Write a short, hypothetical scientific abstract (150-200 words) that would perfectly answer this question:

Question: {query}

Write as if you're writing an abstract for a scientific paper. Include technical terms and specific details that would appear in a real paper about this topic.

Abstract:"""

    QUERY_EXPANSION_PROMPT = """Given this search query about a scientific topic, generate 3 alternative search queries that would help find relevant information.

Original query: {query}

Generate queries that:
1. Use synonyms or related technical terms
2. Focus on different aspects of the topic
3. Are more specific or more general

Return ONLY a JSON array of strings, no explanation:
["query1", "query2", "query3"]"""

    COMPRESSION_PROMPT = """Extract only the most relevant information from this context that directly relates to the query.

Query: {query}

Context:
{context}

Return a compressed version (max 500 words) containing ONLY information relevant to answering the query. Remove tangential information."""

    def __init__(self, llm_provider: str = "groq", enable_hyde: bool = True, enable_auto_learn: bool = True):
        self.knowledge_graph = KnowledgeGraph(persist_path="./knowledge_graph.json")
        self.vector_store = VectorStore(collection_name="science_papers", enable_reranking=True)
        self.llm_service = LLMService(provider=llm_provider)
        self.enable_hyde = enable_hyde
        self.enable_auto_learn = enable_auto_learn
        
        # Inicializar grafo con conocimiento base expandido
        self._initialize_base_knowledge()
    
    def _initialize_base_knowledge(self):
        """Inicializa el grafo con conocimiento científico base expandido"""
        # Skip if graph already has nodes (loaded from file)
        if self.knowledge_graph.graph.number_of_nodes() > 0:
            return
            
        # === MACHINE LEARNING & AI ===
        self.knowledge_graph.add_entity("artificial_intelligence", "concept", 
            {"name": "Artificial Intelligence", "definition": "Simulation of human intelligence in machines"})
        self.knowledge_graph.add_entity("machine_learning", "concept", 
            {"name": "Machine Learning", "definition": "Campo de la IA que permite a las máquinas aprender de datos"})
        self.knowledge_graph.add_entity("deep_learning", "concept",
            {"name": "Deep Learning", "definition": "Subcampo de ML usando redes neuronales profundas"})
        self.knowledge_graph.add_entity("neural_networks", "technology",
            {"name": "Neural Networks", "definition": "Modelos computacionales inspirados en el cerebro"})
        self.knowledge_graph.add_entity("transformers", "technology",
            {"name": "Transformers", "definition": "Arquitectura basada en mecanismos de atención"})
        self.knowledge_graph.add_entity("gpt", "technology",
            {"name": "GPT", "definition": "Generative Pre-trained Transformer"})
        self.knowledge_graph.add_entity("attention_mechanism", "concept",
            {"name": "Attention Mechanism", "definition": "Mecanismo que permite enfocarse en partes relevantes"})
        self.knowledge_graph.add_entity("llm", "technology",
            {"name": "Large Language Models", "definition": "Modelos de lenguaje con billones de parámetros"})
        self.knowledge_graph.add_entity("bert", "technology",
            {"name": "BERT", "definition": "Bidirectional Encoder Representations from Transformers"})
        self.knowledge_graph.add_entity("rag", "method",
            {"name": "RAG", "definition": "Retrieval-Augmented Generation - combines retrieval with generation"})
        self.knowledge_graph.add_entity("fine_tuning", "method",
            {"name": "Fine-tuning", "definition": "Adapting pre-trained models to specific tasks"})
        self.knowledge_graph.add_entity("prompt_engineering", "method",
            {"name": "Prompt Engineering", "definition": "Designing effective prompts for LLMs"})
        
        # === NLP ===
        self.knowledge_graph.add_entity("nlp", "concept",
            {"name": "Natural Language Processing", "definition": "Processing and understanding human language"})
        self.knowledge_graph.add_entity("embeddings", "concept",
            {"name": "Embeddings", "definition": "Dense vector representations of text"})
        self.knowledge_graph.add_entity("tokenization", "method",
            {"name": "Tokenization", "definition": "Breaking text into tokens"})
        
        # === COMPUTER VISION ===
        self.knowledge_graph.add_entity("computer_vision", "concept",
            {"name": "Computer Vision", "definition": "Enabling computers to interpret visual information"})
        self.knowledge_graph.add_entity("cnn", "technology",
            {"name": "CNN", "definition": "Convolutional Neural Networks for image processing"})
        self.knowledge_graph.add_entity("image_classification", "method",
            {"name": "Image Classification", "definition": "Categorizing images into classes"})
        
        # === REINFORCEMENT LEARNING ===
        self.knowledge_graph.add_entity("reinforcement_learning", "concept",
            {"name": "Reinforcement Learning", "definition": "Learning through trial and error with rewards"})
        self.knowledge_graph.add_entity("rlhf", "method",
            {"name": "RLHF", "definition": "Reinforcement Learning from Human Feedback"})
        
        # === RELATIONS ===
        # AI Hierarchy
        self.knowledge_graph.add_relation("machine_learning", "artificial_intelligence", "is_subfield_of")
        self.knowledge_graph.add_relation("deep_learning", "machine_learning", "is_subfield_of")
        self.knowledge_graph.add_relation("reinforcement_learning", "machine_learning", "is_subfield_of")
        self.knowledge_graph.add_relation("nlp", "artificial_intelligence", "is_subfield_of")
        self.knowledge_graph.add_relation("computer_vision", "artificial_intelligence", "is_subfield_of")
        
        # Technologies
        self.knowledge_graph.add_relation("neural_networks", "deep_learning", "enables")
        self.knowledge_graph.add_relation("transformers", "neural_networks", "is_type_of")
        self.knowledge_graph.add_relation("cnn", "neural_networks", "is_type_of")
        self.knowledge_graph.add_relation("gpt", "transformers", "based_on")
        self.knowledge_graph.add_relation("bert", "transformers", "based_on")
        self.knowledge_graph.add_relation("llm", "transformers", "based_on")
        self.knowledge_graph.add_relation("attention_mechanism", "transformers", "core_component_of")
        
        # Methods
        self.knowledge_graph.add_relation("rag", "llm", "extends")
        self.knowledge_graph.add_relation("fine_tuning", "llm", "applies_to")
        self.knowledge_graph.add_relation("prompt_engineering", "llm", "applies_to")
        self.knowledge_graph.add_relation("rlhf", "llm", "improves")
        self.knowledge_graph.add_relation("embeddings", "nlp", "enables")
        self.knowledge_graph.add_relation("tokenization", "nlp", "enables")
    
    async def _generate_hyde_query(self, query: str) -> str:
        """
        Generate a hypothetical document for better retrieval (HyDE)
        This creates a synthetic answer that's then used for embedding-based search
        """
        if not self.enable_hyde:
            return query
            
        try:
            prompt = self.HYDE_PROMPT.format(query=query)
            hypothetical_doc = await self.llm_service.generate(prompt)
            return hypothetical_doc[:1000]  # Limit length
        except Exception:
            return query
    
    async def _expand_query(self, query: str) -> List[str]:
        """Generate alternative queries for comprehensive search"""
        try:
            prompt = self.QUERY_EXPANSION_PROMPT.format(query=query)
            response = await self.llm_service.generate(prompt)
            
            # Parse JSON array
            json_match = re.search(r'\[.*?\]', response, re.DOTALL)
            if json_match:
                import json
                queries = json.loads(json_match.group())
                return [query] + queries[:3]
        except Exception:
            pass
        
        return [query]
    
    async def _compress_context(self, query: str, context: str) -> str:
        """Compress context to keep only relevant information"""
        if len(context) < 1000:
            return context
            
        try:
            prompt = self.COMPRESSION_PROMPT.format(query=query, context=context[:3000])
            compressed = await self.llm_service.generate(prompt)
            return compressed
        except Exception:
            return context[:1500]
    
    async def _auto_learn_from_results(self, results: List[dict]):
        """Extract entities from retrieved documents and add to knowledge graph"""
        if not self.enable_auto_learn or not results:
            return
            
        # Combine content from top results
        combined_text = "\n".join([
            f"{doc['metadata'].get('title', '')}: {doc['content'][:500]}"
            for doc in results[:2]
        ])
        
        if combined_text:
            await self.knowledge_graph.extract_entities_from_text(
                combined_text, 
                self.llm_service
            )
    
    async def generate_content(
        self,
        topic: str,
        platform: str = "blog",
        language: str = "Spanish",
        related_concepts: List[str] = None,
        use_hyde: bool = True,
        use_query_expansion: bool = True
    ) -> dict:
        """
        Generate content using Enhanced Graph RAG
        
        Args:
            topic: Main topic for content generation
            platform: Target platform (blog, twitter, linkedin, etc.)
            language: Output language
            related_concepts: Optional list of concepts to include
            use_hyde: Whether to use HyDE for better retrieval
            use_query_expansion: Whether to expand query for comprehensive search
        """
        
        # 1. Extract concepts from topic
        concepts = related_concepts or self._extract_concepts(topic)
        
        # 2. Get context from knowledge graph (with fuzzy matching)
        graph_context = self.knowledge_graph.get_context_for_query(concepts + [topic])
        
        # 3. Expand query for better coverage
        queries = [topic]
        if use_query_expansion:
            queries = await self._expand_query(topic)
        
        # 4. Generate HyDE query for semantic search
        search_query = topic
        if use_hyde and self.enable_hyde:
            search_query = await self._generate_hyde_query(topic)
        
        # 5. Perform hybrid search with all queries
        all_results = []
        seen_ids = set()
        
        for q in queries[:3]:  # Limit to avoid too many searches
            results = self.vector_store.hybrid_search(
                query=q,
                keywords=concepts,
                n_results=3
            )
            for doc in results:
                if doc['id'] not in seen_ids:
                    all_results.append(doc)
                    seen_ids.add(doc['id'])
        
        # Also search with HyDE query
        if search_query != topic:
            hyde_results = self.vector_store.search(search_query, n_results=2)
            for doc in hyde_results:
                if doc['id'] not in seen_ids:
                    all_results.append(doc)
                    seen_ids.add(doc['id'])
        
        # 6. Auto-learn from results (add new entities to graph)
        await self._auto_learn_from_results(all_results)
        
        # 7. Format vector context
        vector_context = "\n\n".join([
            f"📄 **{doc['metadata'].get('title', 'Unknown')}** "
            f"(Relevance: {doc.get('rerank_score', doc.get('similarity', 0)):.2f})\n"
            f"Authors: {doc['metadata'].get('authors', 'Unknown')}\n"
            f"{doc['content'][:600]}..."
            for doc in all_results[:5]
        ])
        
        # 8. Compress context if too long
        if len(vector_context) > 2500:
            vector_context = await self._compress_context(topic, vector_context)
        
        # 9. Generate prompt
        prompt = self.GRAPH_RAG_PROMPT.format(
            topic=topic,
            graph_context=graph_context if graph_context else "No se encontraron relaciones directas en el grafo.",
            vector_context=vector_context if vector_context else "No se encontraron papers relevantes.",
            language=language,
            platform=platform
        )
        
        # 10. Generate content
        content = await self.llm_service.generate(prompt)
        
        return {
            "content": content,
            "graph_concepts": concepts,
            "sources": [doc['metadata'] for doc in all_results[:5]],
            "topic": topic,
            "queries_used": queries,
            "hyde_enabled": use_hyde and self.enable_hyde,
            "graph_stats": self.knowledge_graph.get_stats()
        }
    
    def _extract_concepts(self, topic: str) -> List[str]:
        """Extract concepts using both exact matching and fuzzy search"""
        topic_lower = topic.lower()
        
        # Use fuzzy matching from knowledge graph
        concepts = self.knowledge_graph.find_similar_entities(topic_lower, threshold=0.5)
        
        # Also extract potential concepts from topic words
        words = re.findall(r'\b\w+\b', topic_lower)
        for word in words:
            if len(word) > 3:  # Skip short words
                similar = self.knowledge_graph.find_similar_entities(word, threshold=0.7)
                concepts.extend(similar)
        
        # Remove duplicates while preserving order
        seen = set()
        return [c for c in concepts if not (c in seen or seen.add(c))][:10]