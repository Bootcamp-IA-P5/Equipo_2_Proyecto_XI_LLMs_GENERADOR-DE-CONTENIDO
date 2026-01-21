"""
Schemas de Pydantic para validación de datos (actualizado)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class LanguageEnum(str, Enum):
    ES = "Spanish"
    EN = "English"
    FR = "French"
    IT = "Italian"


class PlatformEnum(str, Enum):
    BLOG = "blog"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"


class AudienceEnum(str, Enum):
    GENERAL = "general"
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    YOUNG = "young"
    CHILDREN = "children"
    BUSINESS = "business"


class LLMProviderEnum(str, Enum):
    GROQ = "groq"
    OLLAMA = "ollama"


class ContentTypeEnum(str, Enum):
    GENERAL = "general"
    FINANCIAL = "financial"
    SCIENCE = "science"


class ContentRequest(BaseModel):
    """Request para generar contenido"""
    topic: str = Field(..., min_length=3, max_length=500)
    platform: PlatformEnum
    audience: AudienceEnum = AudienceEnum.GENERAL
    additional_context: Optional[str] = Field(default="", max_length=1000)
    tone: Optional[str] = Field(default="", max_length=200)
    llm_provider: LLMProviderEnum = LLMProviderEnum.GROQ
    language: str = Field(default="Spanish")
    content_type: Optional[ContentTypeEnum] = None  # NUEVO:  Para forzar tipo de agente


class SourceInfo(BaseModel):
    """Información de una fuente"""
    title: str
    authors: Optional[str] = None
    url: Optional[str] = None
    relevance: Optional[float] = None


class ContentResponse(BaseModel):
    """Response con el contenido generado"""
    content: str
    platform: str
    audience: str
    topic: str
    llm_provider: str
    model_used: str
    image_url: Optional[str] = None
    agent_used: Optional[str] = None
    sources: Optional[List[SourceInfo]] = None
    validation_score: Optional[float] = None
    validation_warnings: Optional[List[str]] = None
    # New fields from enhanced orchestrator
    confidence_score: Optional[float] = Field(None, description="Routing confidence (0-1)")
    processing_time_ms: Optional[float] = Field(None, description="Total processing time in ms")
    routing_reason: Optional[str] = Field(None, description="Explanation of routing decision")
    from_cache: bool = Field(False, description="Whether result was served from cache")


class PlatformInfo(BaseModel):
    id: str
    name: str
    max_length: str
    description: str


class AudienceInfo(BaseModel):
    id: str
    name: str
    description: str


class ConfigResponse(BaseModel):
    platforms: List[PlatformInfo]
    audiences: List[AudienceInfo]
    llm_providers: List[str]
    content_types: Optional[List[str]] = None  # NUEVO


class HealthResponse(BaseModel):
    status: str
    version: str
