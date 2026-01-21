"""
Rutas específicas para contenido financiero
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.financial_service import FinancialService

router = APIRouter(prefix="/financial", tags=["Financial"])


class MarketSummaryResponse(BaseModel):
    data: dict
    timestamp: str


class StockInfoRequest(BaseModel):
    symbol: str


class NewsResponse(BaseModel):
    news:  List[dict]


@router.get("/market-summary", response_model=MarketSummaryResponse)
async def get_market_summary():
    """Obtiene resumen de los principales índices"""
    from datetime import datetime
    
    return MarketSummaryResponse(
        data=FinancialService.get_market_summary(),
        timestamp=datetime.now().isoformat()
    )


@router.post("/stock-info")
async def get_stock_info(request: StockInfoRequest):
    """Obtiene información de una acción específica"""
    return FinancialService.get_stock_info(request.symbol)


@router.get("/news", response_model=NewsResponse)
async def get_financial_news(limit:  int = 10):
    """Obtiene últimas noticias financieras"""
    return NewsResponse(news=FinancialService.get_financial_news(limit))