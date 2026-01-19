"""
Servidor MCP para Datos Financieros
"""
from mcp.server.fastmcp import FastMCP
from app.services.financial_service import FinancialService

# Crear servidor MCP
mcp = FastMCP("Financial Data Server")

@mcp.tool()
def get_market_summary() -> dict:
    """
    Obtiene un resumen de los principales índices bursátiles (SP500, NASDAQ, IBEX35, etc).
    Retorna precios actuales, cambios porcentuales y dirección del mercado.
    """
    return FinancialService.get_market_summary()

@mcp.tool()
def get_stock_info(symbol: str) -> dict:
    """
    Obtiene información detallada de una acción específica o índice.
    Args:
        symbol: El símbolo del ticker (ej: AAPL, MSFT, GOOGL, ^IBEX)
    """
    return FinancialService.get_stock_info(symbol)

@mcp.tool()
def get_financial_news(limit: int = 5) -> list:
    """
    Obtiene las últimas noticias financieras de múltiples fuentes RSS confiables.
    Args:
        limit: Número máximo de noticias a retornar (default: 5)
    """
    return FinancialService.get_financial_news(limit)

if __name__ == "__main__":
    # Ejecuta el servidor usando stdio por defecto
    mcp.run()
