"""
Agente para contenido financiero con datos en tiempo real via MCP
"""
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.services.llm_service import LLMService


class FinancialAgent:
    """Agente especializado en contenido financiero usando MCP"""
    
    description = "Agente financiero con acceso a datos de mercado en tiempo real via MCP"
    
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
        self.llm_service = LLMService(provider=llm_provider)
    
    async def generate(
        self,
        topic: str,
        platform:  str,
        audience: str,
        language: str = "Spanish",
        **kwargs
    ) -> dict:
        """Genera contenido financiero conectando al servidor MCP"""
        
        # Configuración del servidor MCP (subproceso local)
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "app.mcp.server"],
            env=None
        )

        market_context_str = ""
        market_summary_data = {}

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    # Inicializar conexión
                    await session.initialize()
                    
                    # Llamar herramientas MCP
                    # 1. Resumen de mercado
                    summary_result = await session.call_tool("get_market_summary")
                    market_summary_data = summary_result.content[0].text
                    
                    # 2. Noticias (si aplica)
                    news_result = await session.call_tool("get_financial_news", arguments={"limit": 3})
                    news_data = news_result.content[0].text

                    # Construir string de contexto (simulando lo que hacía el servicio antes)
                    # Nota: El servidor MCP devuelve los dicts serializados, aquí los usamos para el prompt
                    market_context_str = f"Market Summary: {market_summary_data}\n\nNews: {news_data}"

        except Exception as e:
            print(f"Error MCP: {e}")
            market_context_str = "No se pudieron obtener datos financieros en tiempo real via MCP."

        
        prompt = self.FINANCIAL_PROMPT.format(
            market_data=market_context_str,
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
            "market_summary": market_summary_data, # Retornamos los datos crudos del MCP
            "data_timestamp": "Real-time (MCP)"
        }
