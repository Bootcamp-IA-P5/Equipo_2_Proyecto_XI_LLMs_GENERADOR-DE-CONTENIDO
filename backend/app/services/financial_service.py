"""
Servicio para obtener información financiera actualizada
"""
import yfinance as yf
import feedparser
from datetime import datetime, timedelta
from typing import Optional
import httpx


class FinancialService:
    """Servicio para obtener datos financieros en tiempo real"""
    
    # Fuentes de noticias RSS financieras gratuitas
    RSS_FEEDS = {
        "yahoo_finance": "https://finance.yahoo.com/news/rssindex",
        "investing_com": "https://www.investing.com/rss/news.rss",
        "marketwatch": "https://feeds.marketwatch.com/marketwatch/topstories/",
        "cnbc": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    }
    
    # Índices principales
    MAIN_INDICES = {
        "SP500": "^GSPC",
        "NASDAQ": "^IXIC",
        "DOW_JONES": "^DJI",
        "IBEX35": "^IBEX",
        "EURO_STOXX": "^STOXX50E",
        "NIKKEI": "^N225",
        "FTSE100": "^FTSE",
    }
    
    @classmethod
    def get_market_summary(cls) -> dict:
        """Obtiene un resumen de los principales índices"""
        summary = {}
        
        for name, symbol in cls.MAIN_INDICES.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current = hist['Close'].iloc[-1]
                    previous = hist['Close'].iloc[-2]
                    change = ((current - previous) / previous) * 100
                    
                    summary[name] = {
                        "symbol": symbol,
                        "price": round(current, 2),
                        "change_percent": round(change, 2),
                        "direction": "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    }
            except Exception as e:
                summary[name] = {"error": str(e)}
        
        return summary
    
    @classmethod
    def get_stock_info(cls, symbol: str) -> dict:
        """Obtiene información detallada de una acción"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1mo")
            
            return {
                "symbol": symbol,
                "name": info.get("longName", symbol),
                "sector": info.get("sector", "N/A"),
                "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "52_week_high":  info.get("fiftyTwoWeekHigh"),
                "52_week_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume"),
                "description": info.get("longBusinessSummary", "")[: 500],
            }
        except Exception as e: 
            return {"error": str(e)}
    
    @classmethod
    def get_financial_news(cls, limit: int = 10) -> list:
        """Obtiene las últimas noticias financieras de múltiples fuentes"""
        all_news = []
        
        for source, url in cls.RSS_FEEDS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:5]:  # 5 por fuente
                    all_news.append({
                        "source": source,
                        "title": entry.get("title", ""),
                        "summary": entry.get("summary", "")[: 300],
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                    })
            except Exception: 
                continue
        
        # Ordenar por fecha y limitar
        return all_news[: limit]
    
    @classmethod
    def build_financial_context(cls, topic: str = "general") -> str:
        """Construye contexto financiero para el LLM"""
        context_parts = []
        
        # Resumen del mercado
        context_parts.append("## 📊 RESUMEN DEL MERCADO (Datos en tiempo real)")
        market = cls.get_market_summary()
        for name, data in market.items():
            if "error" not in data:
                context_parts.append(
                    f"- **{name}**:  {data['price']} ({data['direction']} {data['change_percent']}%)"
                )
        
        # Noticias recientes
        context_parts.append("\n## 📰 NOTICIAS FINANCIERAS RECIENTES")
        news = cls.get_financial_news(limit=5)
        for item in news:
            context_parts.append(f"- **{item['title']}** ({item['source']})")
            if item['summary']: 
                context_parts.append(f"  {item['summary'][: 150]}...")
        
        context_parts.append(f"\n*Datos actualizados: {datetime.now().strftime('%Y-%m-%d %H:%M')} UTC*")
        
        return "\n".join(context_parts)