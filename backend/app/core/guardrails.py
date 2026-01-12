"""
Sistema de guardrails para validación y calidad del contenido
"""
import re
from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Resultado de validación"""
    is_valid: bool
    issues: List[str]
    warnings: List[str]
    score: float  # 0-100


class ContentGuardrails:
    """Guardrails para asegurar calidad y evitar alucinaciones"""
    
    # Patrones de contenido problemático
    HALLUCINATION_PATTERNS = [
        r"como modelo de lenguaje",
        r"no tengo acceso a",
        r"no puedo verificar",
        r"según mi conocimiento",
        r"hasta mi fecha de corte",
        r"as an ai",
        r"i don't have access",
        r"i cannot verify",
    ]
    
    # Contenido inapropiado
    INAPPROPRIATE_PATTERNS = [
        r"consejo (financiero|médico|legal) profesional",
        r"garantizo|garantiza|garantizamos",
        r"100% seguro",
        r"sin riesgo",
    ]
    
    # Límites por plataforma
    PLATFORM_LIMITS = {
        "twitter": {"max_chars": 280, "max_hashtags": 5},
        "instagram": {"max_chars": 2200, "max_hashtags": 30},
        "linkedin": {"max_chars": 3000, "max_hashtags": 5},
        "blog": {"max_chars": 50000, "max_hashtags": 10},
    }
    
    @classmethod
    def validate_content(
        cls,
        content: str,
        platform:  str,
        check_hallucinations:  bool = True,
        check_length: bool = True,
        check_inappropriate: bool = True
    ) -> ValidationResult:
        """Valida el contenido generado"""
        issues = []
        warnings = []
        score = 100.0
        
        content_lower = content.lower()
        
        # 1. Detectar alucinaciones
        if check_hallucinations: 
            for pattern in cls.HALLUCINATION_PATTERNS:
                if re.search(pattern, content_lower):
                    issues.append(f"Posible alucinación detectada: patrón '{pattern}'")
                    score -= 15
        
        # 2. Verificar longitud
        if check_length and platform in cls.PLATFORM_LIMITS: 
            limits = cls.PLATFORM_LIMITS[platform]
            
            if len(content) > limits["max_chars"]: 
                issues.append(
                    f"Contenido excede límite de {platform}: "
                    f"{len(content)}/{limits['max_chars']} caracteres"
                )
                score -= 20
            
            # Contar hashtags
            hashtags = re.findall(r'#\w+', content)
            if len(hashtags) > limits["max_hashtags"]: 
                warnings.append(
                    f"Demasiados hashtags: {len(hashtags)}/{limits['max_hashtags']}"
                )
                score -= 5
        
        # 3. Contenido inapropiado
        if check_inappropriate:
            for pattern in cls.INAPPROPRIATE_PATTERNS:
                if re.search(pattern, content_lower):
                    warnings.append(f"Contenido potencialmente problemático: '{pattern}'")
                    score -= 10
        
        # 4. Verificar contenido vacío o muy corto
        if len(content.strip()) < 50:
            issues.append("Contenido demasiado corto o vacío")
            score -= 30
        
        # 5. Verificar estructura básica (para blogs)
        if platform == "blog": 
            if not re.search(r'#{1,3}\s', content):
                warnings.append("Blog sin encabezados detectados")
                score -= 5
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
            score=max(0, score)
        )
    
    @classmethod
    def sanitize_content(cls, content: str) -> str:
        """Limpia el contenido de patrones problemáticos"""
        sanitized = content
        
        # Remover patrones de alucinación
        for pattern in cls.HALLUCINATION_PATTERNS:
            sanitized = re.sub(pattern, "", sanitized, flags=re. IGNORECASE)
        
        # Limpiar espacios múltiples
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)
        sanitized = re.sub(r' {2,}', ' ', sanitized)
        
        return sanitized.strip()
    
    @classmethod
    def add_disclaimers(cls, content: str, content_type: str) -> str:
        """Añade disclaimers apropiados según el tipo de contenido"""
        disclaimers = {
            "financial": "\n\n---\n*⚠️ Este contenido es informativo y no constituye asesoramiento financiero.  Consulta con un profesional antes de tomar decisiones de inversión.*",
            "science": "\n\n---\n*📚 Contenido basado en investigación científica publicada.  Para información actualizada, consulta las fuentes originales.*",
            "health": "\n\n---\n*🏥 Este contenido es informativo y no sustituye el consejo médico profesional.*",
        }
        
        if content_type in disclaimers:
            return content + disclaimers[content_type]
        
        return content