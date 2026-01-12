"""
Rutas para generación de contenido (actualizado con multi-agente)
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ContentRequest, 
    ContentResponse, 
    ConfigResponse,
    PlatformInfo,
    AudienceInfo
)
from app.agents.orchestrator import AgentOrchestrator
from app.core.prompts import PLATFORM_CONFIGS, AUDIENCE_CONFIGS
from app.core.guardrails import ContentGuardrails
from app.core.tracing import setup_langsmith

router = APIRouter(prefix="/content", tags=["Content"])

# Configurar LangSmith al cargar el módulo
setup_langsmith()


@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """
    Genera contenido usando el sistema multi-agente
    """
    try:
        # Inicializar orquestador
        orchestrator = AgentOrchestrator(llm_provider=request.llm_provider.value)
        
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
            validation_score=validation.score
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        content_types=["general", "financial", "science"]  # NUEVO
    )