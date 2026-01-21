"""
Structured Logging Configuration

Sistema de logging estructurado en formato JSON para:
- Trazabilidad de requests con IDs únicos
- Logs parseable por herramientas de monitoreo
- Integración con LangSmith tracing
- Diferentes niveles según entorno
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
import uuid
from contextvars import ContextVar

from app.core.config import settings


# Context variable para request ID
request_id_var: ContextVar[str] = ContextVar('request_id', default='')


class StructuredFormatter(logging.Formatter):
    """
    Formateador JSON para logs estructurados
    
    Convierte logs de Python a formato JSON con campos adicionales:
    - timestamp: ISO 8601
    - level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    - message: Mensaje del log
    - request_id: ID único del request actual
    - module: Módulo Python que generó el log
    - function: Función que generó el log
    - extra: Datos adicionales
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatea el log record como JSON"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Añadir request_id si existe
        req_id = request_id_var.get()
        if req_id:
            log_data["request_id"] = req_id
        
        # Añadir exception info si existe
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Añadir campos extra
        if hasattr(record, 'extra'):
            log_data["extra"] = record.extra
        
        return json.dumps(log_data, ensure_ascii=False)


class RequestLogger:
    """
    Logger contextual para requests HTTP
    
    Genera un ID único por request y lo propaga a todos los logs.
    """
    
    def __init__(self, request_id: str = None):
        self.request_id = request_id or str(uuid.uuid4())
        request_id_var.set(self.request_id)
        self.logger = logging.getLogger("app.request")
    
    def log_request(self, method: str, path: str, **kwargs):
        """Loguea inicio de request"""
        self.logger.info(
            f"Request started: {method} {path}",
            extra={
                "event": "request_started",
                "method": method,
                "path": path,
                **kwargs
            }
        )
    
    def log_response(self, status_code: int, duration_ms: float, **kwargs):
        """Loguea fin de request con timing"""
        level = logging.INFO if status_code < 400 else logging.WARNING
        self.logger.log(
            level,
            f"Request completed: {status_code} ({duration_ms:.2f}ms)",
            extra={
                "event": "request_completed",
                "status_code": status_code,
                "duration_ms": duration_ms,
                **kwargs
            }
        )
    
    def log_error(self, error: Exception, **kwargs):
        """Loguea error en request"""
        self.logger.error(
            f"Request error: {str(error)}",
            exc_info=True,
            extra={
                "event": "request_error",
                "error_type": error.__class__.__name__,
                **kwargs
            }
        )


class AgentLogger:
    """
    Logger específico para agentes
    
    Trackea operaciones de agentes con métricas adicionales.
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = logging.getLogger(f"app.agent.{agent_name}")
    
    def log_generation_start(self, topic: str, platform: str, **kwargs):
        """Loguea inicio de generación"""
        self.logger.info(
            f"Agent {self.agent_name} starting generation",
            extra={
                "event": "generation_started",
                "agent": self.agent_name,
                "topic": topic,
                "platform": platform,
                **kwargs
            }
        )
    
    def log_generation_complete(self, duration_ms: float, content_length: int, **kwargs):
        """Loguea fin de generación con métricas"""
        self.logger.info(
            f"Agent {self.agent_name} completed generation ({duration_ms:.2f}ms)",
            extra={
                "event": "generation_completed",
                "agent": self.agent_name,
                "duration_ms": duration_ms,
                "content_length": content_length,
                **kwargs
            }
        )
    
    def log_rag_query(self, query: str, results_count: int, **kwargs):
        """Loguea query de RAG"""
        self.logger.debug(
            f"RAG query executed: {results_count} results",
            extra={
                "event": "rag_query",
                "agent": self.agent_name,
                "query": query,
                "results_count": results_count,
                **kwargs
            }
        )


def setup_logging(log_level: str = None) -> None:
    """
    Configura el sistema de logging de la aplicación
    
    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
                   Si no se especifica, usa settings.LOG_LEVEL
    """
    level = log_level or getattr(settings, 'LOG_LEVEL', 'INFO')
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Limpiar handlers existentes
    root_logger.handlers.clear()
    
    # Handler para stdout con formato JSON
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(handler)
    
    # Configurar loggers específicos
    logging.getLogger("app").setLevel(level)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    logging.info(
        "Logging configured",
        extra={
            "event": "logging_initialized",
            "log_level": level,
            "format": "json"
        }
    )


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre especificado
    
    Args:
        name: Nombre del logger (ej: "app.services.llm")
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


# Convenience functions
def log_llm_call(
    provider: str,
    model: str,
    prompt_tokens: int = None,
    completion_tokens: int = None,
    duration_ms: float = None
):
    """Helper para loguear llamadas a LLM"""
    logger = get_logger("app.llm")
    logger.info(
        f"LLM call completed: {provider}/{model}",
        extra={
            "event": "llm_call",
            "provider": provider,
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "duration_ms": duration_ms
        }
    )


def log_rag_operation(
    operation: str,
    collection: str,
    query: str = None,
    results_count: int = None,
    duration_ms: float = None
):
    """Helper para loguear operaciones de RAG"""
    logger = get_logger("app.rag")
    logger.debug(
        f"RAG operation: {operation} on {collection}",
        extra={
            "event": "rag_operation",
            "operation": operation,
            "collection": collection,
            "query": query,
            "results_count": results_count,
            "duration_ms": duration_ms
        }
    )


# Inicializar logging al importar
setup_logging()
