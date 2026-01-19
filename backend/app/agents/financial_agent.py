"""
Agente para contenido financiero con datos en tiempo real
"""
from app.services.llm_service import get_llm_service
from app.services.financial_service import FinancialService


class FinancialAgent:
    """Agente especializado en contenido financiero con datos actualizados"""
    
    description = "Agente financiero con acceso a datos de mercado en tiempo real"
    
    FINANCIAL_PROMPT = """Eres un analista financiero y creador de contenido especializado en mercados.

## 📊 DATOS DE MERCADO EN TIEMPO REAL
{market_data}

## 🎯 TEMA A DESARROLLAR
{topic}

## 🌐 IDIOMA:  {language}
## 📱 PLATAFORMA: {platform}
## 👥 AUDIENCIA: {audience}

## ✅ DIRECTRICES
1. Usa los datos de mercado proporcionados para dar contexto actual
2. Incluye cifras y porcentajes específicos de los datos
3. Sé objetivo y equilibrado (no dar consejos de inversión directos)
4. Añade disclaimer si es necesario
5. Haz el contenido accesible pero profesional
6. Relaciona las noticias con el tema si es relevante

## ⚠️ IMPORTANTE
Incluye siempre:  "Este contenido es informativo y no constituye asesoramiento financiero."

## 📤 GENERA EL CONTENIDO: 
"""

    def __init__(self, llm_provider: str = "groq"):
        self.llm_service = get_llm_service(provider=llm_provider)
    
    async def generate(
        self,
        topic: str,
        platform:  str,
        audience: str,
        language: str = "Spanish",
        **kwargs
    ) -> dict:
        """Genera contenido financiero con datos actualizados"""
        
        # Obtener datos financieros en tiempo real
        market_data = FinancialService.build_financial_context(topic)
        
        prompt = self.FINANCIAL_PROMPT.format(
            market_data=market_data,
            topic=topic,
            language=language,
            platform=platform,
            audience=audience
        )
        
        content = await self.llm_service.generate(prompt)
        
        return {
            "content": content,
            "topic": topic,
            "platform": platform,
            "market_summary": FinancialService.get_market_summary(),
            "data_timestamp": "Real-time"
        }
