"""
Configuración central de la aplicación
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # API
    API_TITLE:  str = "Content Generator API"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://127.0.0.1:3000"]
    
    # LLM Providers
    GROQ_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434"
    
    # Default LLM
    DEFAULT_LLM_PROVIDER: str = "groq"
    DEFAULT_GROQ_MODEL: str = "llama-3.3-70b-versatile"
    DEFAULT_OLLAMA_MODEL: str = "llama3.2"
    
    # LangSmith (Trazabilidad)
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: Optional[str] = None
    LANGCHAIN_PROJECT: str = "content-generator"
    
    # Pollinations (Imágenes IA)
    POLLINATIONS_API_KEY: Optional[str] = None
    
        # ChromaDB (RAG)
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "content_knowledge"
    
    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config: 
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()