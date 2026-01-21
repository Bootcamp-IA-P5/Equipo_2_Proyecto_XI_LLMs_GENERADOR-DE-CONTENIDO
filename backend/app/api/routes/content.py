"""
Rutas para generación de contenido (actualizado con multi-agente mejorado)
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.schemas import (
    ContentRequest, 
    ContentResponse, 
    ConfigResponse,
    PlatformInfo,
    AudienceInfo
)
from app.agents.orchestrator import AgentOrchestrator, AgentType
from app.core.prompts import PLATFORM_CONFIGS, AUDIENCE_CONFIGS
from app.core.guardrails import ContentGuardrails
from app.core.tracing import setup_langsmith

router = APIRouter(prefix="/content", tags=["Content"])

# Configurar LangSmith al cargar el módulo
setup_langsmith()

# Global orchestrator instance for metrics persistence
_orchestrator_instance: Optional[AgentOrchestrator] = None


def get_orchestrator(llm_provider: str = "groq") -> AgentOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator_instance
    if _orchestrator_instance is None or _orchestrator_instance.llm_provider != llm_provider:
        _orchestrator_instance = AgentOrchestrator(
            llm_provider=llm_provider,
            enable_smart_routing=True,
            enable_caching=True
        )
    return _orchestrator_instance


class BatchRequest(BaseModel):
    """Request for batch content generation"""
    requests: List[ContentRequest]
    max_concurrent: int = 3


class ChainRequest(BaseModel):
    """Request for agent chaining"""
    topic: str
    platform: str
    audience: str = "general"
    language: str = "Spanish"
    agent_sequence: List[str] = ["science", "content"]
    additional_context: Optional[str] = ""


@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Genera contenido usando el sistema multi-agente mejorado
    
    Features:
    - Smart LLM-based routing
    - Automatic fallback on errors
    - Request caching
    - Performance metrics
    """
    try:
        # Get orchestrator with caching
        orchestrator = get_orchestrator(request.llm_provider.value)
        
        # Procesar con el agente apropiado
        result = await orchestrator.process_request(
            topic=request.topic,
            platform=request.platform.value,
            audience=request.audience.value,
            language=request.language,
            tone=request.tone,
            additional_context=request.additional_context,
            content_type=getattr(request, 'content_type', None)
        )
        
        # Validar con guardrails
        validation = ContentGuardrails.validate_content(
            content=result["content"],
            platform=request.platform.value
        )
        
        # Sanitizar si hay issues menores
        if not validation.is_valid:
            result["content"] = ContentGuardrails.sanitize_content(result["content"])
            result["validation_warnings"] = validation.issues + validation.warnings
        
        # Añadir disclaimers si es contenido financiero
        if result.get("agent_used") == "financial":
            result["content"] = ContentGuardrails.add_disclaimers(
                result["content"], "financial"
            )
        
        return ContentResponse(
            content=result["content"],
            platform=request.platform.value,
            audience=request.audience.value,
            topic=request.topic,
            llm_provider=request.llm_provider.value,
            model_used=result.get("model_used", "unknown"),
            image_url=result.get("image_url"),
            agent_used=result.get("agent_used"),
            sources=result.get("sources"),
            validation_score=validation.score,
            # New fields from enhanced orchestrator
            confidence_score=result.get("confidence_score"),
            processing_time_ms=result.get("processing_time_ms"),
            routing_reason=result.get("routing_reason"),
            from_cache=result.get("from_cache", False)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/batch")
async def generate_batch(batch_request: BatchRequest):
    """
    Generate multiple content pieces in parallel
    
    Useful for:
    - Generating content for multiple platforms at once
    - Bulk content creation
    """
    try:
        orchestrator = get_orchestrator()
        
        # Convert requests to dicts
        requests = [
            {
                "topic": req.topic,
                "platform": req.platform.value,
                "audience": req.audience.value,
                "language": req.language,
                "tone": req.tone,
                "additional_context": req.additional_context,
            }
            for req in batch_request.requests
        ]
        
        results = await orchestrator.process_batch(
            requests=requests,
            max_concurrent=batch_request.max_concurrent
        )
        
        return {
            "results": results,
            "total": len(results),
            "successful": sum(1 for r in results if "error" not in r),
            "failed": sum(1 for r in results if "error" in r)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/chain")
async def generate_with_chain(chain_request: ChainRequest):
    """
    Generate content using agent chaining
    
    Example: Use Science agent for research, then Content agent for social optimization
    
    Default chain: science → content
    """
    try:
        orchestrator = get_orchestrator()
        
        # Convert agent strings to enum
        agent_sequence = []
        for agent_str in chain_request.agent_sequence:
            try:
                agent_sequence.append(AgentType(agent_str.lower()))
            except ValueError:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Invalid agent type: {agent_str}. Valid: content, financial, science"
                )
        
        result = await orchestrator.chain_agents(
            topic=chain_request.topic,
            platform=chain_request.platform,
            audience=chain_request.audience,
            language=chain_request.language,
            agent_sequence=agent_sequence,
            additional_context=chain_request.additional_context
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_metrics():
    """
    Get orchestration metrics
    
    Returns:
    - Total requests
    - Agent usage distribution
    - Average processing time
    - Cache hit rate
    - Error rate
    """
    orchestrator = get_orchestrator()
    return orchestrator.get_metrics()


@router.get("/agents")
async def get_agents():
    """
    Get information about available agents
    
    Returns list of agents with their capabilities and strengths
    """
    orchestrator = get_orchestrator()
    return orchestrator.get_agent_info()


@router.get("/config", response_model=ConfigResponse)
async def get_config():
    """Obtiene la configuración disponible"""
    platforms = [
        PlatformInfo(
            id=key,
            name=config["name"],
            max_length=config["max_length"],
            description=config["style"]
        )
        for key, config in PLATFORM_CONFIGS.items()
    ]
    
    audiences = [
        AudienceInfo(
            id=key,
            name=config["name"],
            description=config["description"]
        )
        for key, config in AUDIENCE_CONFIGS.items()
    ]
    
    return ConfigResponse(
        platforms=platforms,
        audiences=audiences,
        llm_providers=["groq", "ollama"],
        content_types=["general", "financial", "science"]
    )