"""
Servicio RAG para contenido científico divulgativo
"""
from typing import List
from app.rag.vector_store import VectorStore
from app.services.llm_service import LLMService


class ScienceRAGService:
    """Servicio para generar contenido científico divulgativo con RAG"""
    
    SCIENCE_PROMPT_TEMPLATE = """Eres un divulgador científico experto que hace la ciencia accesible y fascinante para el público general. 

## 🎯 TU MISIÓN
Crear contenido divulgativo sobre:  **{topic}**

## 📚 CONTEXTO CIENTÍFICO (Papers de arXiv)
Los siguientes son extractos de papers científicos relevantes que debes usar como base factual:

{context}

## 🌐 IDIOMA
Redacta el contenido en:  **{language}**

## 📱 PLATAFORMA:  {platform}

## 👥 AUDIENCIA:  Público general sin formación científica especializada

## ✅ DIRECTRICES DE DIVULGACIÓN
1. **Simplifica sin trivializar**: Explica conceptos complejos con analogías cotidianas
2. **Usa ejemplos concretos**: Relaciona con experiencias del día a día
3. **Evita jerga técnica**: Si usas un término técnico, explícalo inmediatamente
4. **Genera curiosidad**: Plantea preguntas que enganchen al lector
5. **Sé preciso**: Basa tus afirmaciones en los papers proporcionados
6. **Cita las fuentes**: Menciona brevemente de dónde viene la información

## 📤 FORMATO
Genera contenido listo para publicar, atractivo y educativo. 
NO incluyas meta-comentarios sobre el contenido. 

{additional_instructions}
"""

    def __init__(self, llm_provider: str = "groq"):
        self.vector_store = VectorStore(collection_name="science_papers")
        self.llm_service = LLMService(provider=llm_provider)
    
    async def generate_content(
        self,
        topic: str,
        scientific_area: str,
        platform: str = "blog",
        language:  str = "Spanish",
        additional_instructions: str = ""
    ) -> dict:
        """Genera contenido divulgativo usando RAG"""
        
        # 1. Buscar papers relevantes en el vector store
        relevant_docs = self.vector_store.search(topic, n_results=5)
        
        # 2. Si no hay suficientes resultados, indexar desde arXiv
        if len(relevant_docs) < 3:
            indexed = self.vector_store.index_from_arxiv(
                query=topic,
                category=scientific_area,
                max_papers=15
            )
            # Buscar de nuevo
            relevant_docs = self.vector_store.search(topic, n_results=5)
        
        # 3. Construir contexto
        context = self._build_context(relevant_docs)
        
        # 4. Generar prompt
        prompt = self.SCIENCE_PROMPT_TEMPLATE.format(
            topic=topic,
            context=context,
            language=language,
            platform=platform,
            additional_instructions=additional_instructions
        )
        
        # 5. Generar contenido
        content = await self.llm_service.generate(prompt)
        
        # 6. Retornar con fuentes
        return {
            "content":  content,
            "sources": [
                {
                    "title": doc["metadata"]["title"],
                    "authors": doc["metadata"]["authors"],
                    "url": doc["metadata"]["pdf_url"],
                    "relevance":  round(doc["similarity"] * 100, 1)
                }
                for doc in relevant_docs
            ],
            "scientific_area": scientific_area,
            "topic": topic
        }
    
    def _build_context(self, documents: List[dict]) -> str:
        """Construye el contexto a partir de los documentos recuperados"""
        context_parts = []
        
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"""
### Fuente {i}:  {doc['metadata']['title']}
**Autores**:  {doc['metadata']['authors']}
**Fecha**: {doc['metadata']['published']}

{doc['content'][: 1500]}...
""")
        
        return "\n".join(context_parts)