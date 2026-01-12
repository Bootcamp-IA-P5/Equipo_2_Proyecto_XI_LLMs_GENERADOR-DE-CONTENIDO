"""
Sistema de prompts para diferentes plataformas y audiencias
"""

PLATFORM_CONFIGS = {
    "blog": {
        "name": "Blog",
        "max_length": "1500-2000 palabras",
        "style": "informativo, detallado, con subtítulos y párrafos bien estructurados",
        "elements": "introducción enganchadora, desarrollo con subtítulos H2/H3, conclusión, llamada a la acción",
        "tone": "profesional pero accesible",
        "format_instructions": "Usa formato Markdown con encabezados, listas y negritas donde sea apropiado."
    },
    "twitter":  {
        "name": "Twitter/X",
        "max_length": "280 caracteres máximo",
        "style": "conciso, impactante, con gancho inicial",
        "elements": "mensaje principal directo, hashtags relevantes (máximo 3), emoji estratégico",
        "tone": "directo, engaging y memorable",
        "format_instructions":  "Un solo tweet.  Los hashtags al final.  Máximo 280 caracteres TOTAL."
    },
    "instagram": {
        "name":  "Instagram",
        "max_length": "2200 caracteres máximo, ideal 150-300 para mejor engagement",
        "style": "visual, emotivo, storytelling personal",
        "elements": "gancho en primera línea, historia o valor, emojis naturales, hashtags (10-15 relevantes), CTA",
        "tone": "cercano, auténtico y inspirador",
        "format_instructions": "Primera línea debe captar atención.  Separa hashtags con salto de línea al final."
    },
    "linkedin":  {
        "name": "LinkedIn",
        "max_length":  "700-1300 caracteres para mejor engagement",
        "style": "profesional con toque personal, insights de valor",
        "elements": "gancho inicial potente, desarrollo con puntos clave, reflexión final o pregunta",
        "tone": "experto pero humano, que invite a la conversación",
        "format_instructions": "Usa saltos de línea para facilitar lectura. Primera línea es crucial."
    }
}

AUDIENCE_CONFIGS = {
    "general": {
        "name": "Público General",
        "description": "público general sin conocimientos técnicos específicos",
        "language_level": "lenguaje cotidiano, evitar jerga técnica, ejemplos de la vida diaria"
    },
    "professional": {
        "name": "Profesionales",
        "description": "profesionales del sector con conocimientos intermedios",
        "language_level": "terminología del sector aceptable, enfoque en aplicaciones prácticas"
    },
    "technical": {
        "name": "Técnicos/Expertos",
        "description": "expertos técnicos que buscan información detallada y precisa",
        "language_level": "lenguaje técnico apropiado, profundidad en conceptos, datos específicos"
    },
    "young": {
        "name": "Jóvenes (18-25)",
        "description": "audiencia joven digitalmente nativa",
        "language_level": "lenguaje actual y dinámico, referencias culturales contemporáneas, tono fresco"
    },
    "children": {
        "name": "Infantil (8-12)",
        "description": "niños en edad escolar",
        "language_level": "lenguaje muy simple, ejemplos cotidianos y divertidos, tono educativo y amigable"
    },
    "business": {
        "name": "Empresarial",
        "description": "directivos y tomadores de decisiones empresariales",
        "language_level": "enfoque en ROI e impacto de negocio, datos y métricas, lenguaje ejecutivo"
    }
}


def build_content_prompt(
    topic: str,
    platform: str,
    audience: str,
    additional_context: str = "",
    tone: str = "",
    language: str = "Spanish" # <--- Recibimos el parámetro (por defecto Español)
) -> str:
    """
    Construye el prompt optimizado para generación de contenido
    """
    platform_config = PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS["blog"])
    audience_config = AUDIENCE_CONFIGS.get(audience, AUDIENCE_CONFIGS["general"])
    
    prompt = f"""Eres un experto creador de contenido digital con años de experiencia en {platform_config['name']}.
Tu contenido siempre genera alto engagement y aporta valor real a la audiencia.

## 🎯 TAREA
Crea contenido sobre:  **{topic}**

## 🌐 IDIOMA DE SALIDA
Redacta el contenido íntegramente en: **{language}**

## 📱 PLATAFORMA:  {platform_config['name']}
- **Longitud**:  {platform_config['max_length']}
- **Estilo**: {platform_config['style']}
- **Elementos requeridos**: {platform_config['elements']}
- **Tono base**: {platform_config['tone']}
- **Formato**:  {platform_config['format_instructions']}

## 👥 AUDIENCIA: {audience_config['name']}
- **Perfil**: {audience_config['description']}
- **Nivel de lenguaje**: {audience_config['language_level']}

## ✅ DIRECTRICES DE CALIDAD
1. El contenido debe ser ORIGINAL y evitar clichés
2. Aporta valor real:  información útil, perspectiva única o entretenimiento genuino
3. Respeta ESTRICTAMENTE los límites de longitud
4. Adapta perfectamente el tono a la audiencia
5. El gancho inicial debe captar atención inmediatamente
6. Incluye todos los elementos requeridos de la plataforma

{f"## 🎨 TONO ESPECÍFICO: {tone}" if tone else ""}
{f"## 📝 CONTEXTO ADICIONAL: {additional_context}" if additional_context else ""}

## 📤 FORMATO DE RESPUESTA
Genera ÚNICAMENTE el contenido final listo para publicar. 
NO incluyas explicaciones, introducciones ni comentarios sobre el contenido.
"""
    return prompt