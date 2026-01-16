"""
Servicio Graph RAG para contenido científico avanzado
"""
from typing import List
from app.rag.graph_store import KnowledgeGraph
from app.rag.vector_store import VectorStore
from app.services.llm_service import LLMService


class GraphRAGService:
    """Servicio que combina Vector RAG con Knowledge Graph"""
    
    GRAPH_RAG_PROMPT = """Eres un divulgador científico experto con acceso a un grafo de conocimiento. 

## 🎯 TEMA: {topic}

## 📊 CONOCIMIENTO ESTRUCTURADO (Grafo de Conocimiento)
Las siguientes son relaciones verificadas entre conceptos científicos:

{graph_context}

## 📚 CONTEXTO DE PAPERS (Vector RAG)
{vector_context}

## 🌐 IDIOMA:  {language}
## 📱 PLATAFORMA: {platform}

## ✅ INSTRUCCIONES
1.  Usa el grafo de conocimiento para estructurar las conexiones entre conceptos
2. Usa los papers para detalles y datos específicos
3. Explica las relaciones entre conceptos de forma clara
4. Haz el contenido accesible para público general
5. Cita conceptos del grafo cuando establezcas conexiones

## 📤 GENERA EL CONTENIDO: 
"""

    def __init__(self, llm_provider: str = "groq"):
        self.knowledge_graph = KnowledgeGraph()
        self.vector_store = VectorStore(collection_name="science_papers")
        self.llm_service = LLMService(provider=llm_provider)
        
        # Inicializar grafo con conocimiento base
        self._initialize_base_knowledge()
    
    def _initialize_base_knowledge(self):
        """Inicializa el grafo con conocimiento científico base"""
        # Ejemplo: Conceptos de IA
        self.knowledge_graph.add_entity("machine_learning", "concept", 
            {"definition": "Campo de la IA que permite a las máquinas aprender de datos"})
        self.knowledge_graph.add_entity("deep_learning", "concept",
            {"definition": "Subcampo de ML usando redes neuronales profundas"})
        self.knowledge_graph.add_entity("neural_networks", "technology",
            {"definition": "Modelos computacionales inspirados en el cerebro"})
        self.knowledge_graph.add_entity("transformers", "technology",
            {"definition":  "Arquitectura basada en mecanismos de atención"})
        self.knowledge_graph.add_entity("gpt", "technology",
            {"definition":  "Generative Pre-trained Transformer"})
        self.knowledge_graph.add_entity("attention_mechanism", "concept",
            {"definition": "Mecanismo que permite enfocarse en partes relevantes"})
        
        # Relaciones
        self.knowledge_graph.add_relation("deep_learning", "machine_learning", "is_subfield_of")
        self.knowledge_graph.add_relation("neural_networks", "deep_learning", "enables")
        self.knowledge_graph.add_relation("transformers", "neural_networks", "is_type_of")
        self.knowledge_graph.add_relation("gpt", "transformers", "based_on")
        self.knowledge_graph.add_relation("attention_mechanism", "transformers", "core_component_of")
    
    async def generate_content(
        self,
        topic: str,
        platform: str = "blog",
        language: str = "Spanish",
        related_concepts: List[str] = None
    ) -> dict:
        """Genera contenido usando Graph RAG"""
        
        # 1. Obtener contexto del grafo
        concepts = related_concepts or self._extract_concepts(topic)
        graph_context = self.knowledge_graph.get_context_for_query(concepts)
        
        # 2. Obtener contexto de papers (Vector RAG)
        vector_results = self.vector_store.search(topic, n_results=3)
        vector_context = "\n".join([
            f"**{doc['metadata']['title']}**:  {doc['content'][: 500]}..."
            for doc in vector_results
        ])
        
        # 3. Generar prompt
        prompt = self.GRAPH_RAG_PROMPT.format(
            topic=topic,
            graph_context=graph_context if graph_context else "No se encontraron relaciones directas.",
            vector_context=vector_context if vector_context else "No se encontraron papers relevantes.",
            language=language,
            platform=platform
        )
        
        # 4. Generar contenido
        content = await self.llm_service.generate(prompt)
        
        return {
            "content": content,
            "graph_concepts": concepts,
            "sources": [doc['metadata'] for doc in vector_results],
            "topic": topic
        }
    
    def _extract_concepts(self, topic: str) -> List[str]:
        """Extrae conceptos clave del topic (simplificado)"""
        # En producción, usar NER o el LLM
        topic_lower = topic.lower()
        known_concepts = list(self.knowledge_graph.graph.nodes())
        
        return [c for c in known_concepts if c.replace("_", " ") in topic_lower]