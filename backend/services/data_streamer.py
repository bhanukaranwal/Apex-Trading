import asyncio
from typing import Dict, List, Optional, Set
from datetime import datetime
import aiohttp
from polygon import WebSocketClient, RESTClient
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockQuotesRequest
from alpaca.data.timeframe import TimeFrame
from backend.core.config import settings

class DataStreamer:
    def __init__(self):
        self.polygon_rest = RESTClient(settings.POLYGON_API_KEY) if settings.POLYGON_API_KEY else None
        self.alpaca_client = StockHistoricalDataClient(
            settings.ALPACA_API_KEY,
            settings.ALPACA_SECRET_KEY
        ) if settings.ALPACA_API_KEY else None
        
        self.subscriptions: Set[str] = set()
        self.latest_quotes: Dict[str, Dict] = {}
        self.ws_client = None
        self._running = False

    async def start(self):
        self._running = True
        if settings.POLYGON_API_KEY:
            asyncio.create_task(self._polygon_websocket_loop())

    async def stop(self):
        self._running = False
        if self.ws_client:
            await self.ws_client.close()

    async def subscribe(self, symbols: List[str]):
        self.subscriptions.update(symbols)

    async def unsubscribe(self, symbols: List[str]):
        self.subscriptions.difference_update(symbols)

    async def get_quote(self, symbol: str) -> Optional[Dict]:
        if symbol in self.latest_quotes:
            return self.latest_quotes[symbol]
        
        if self.polygon_rest:
            try:
                quote = self.polygon_rest.get_last_quote(symbol)
                return {
                    "symbol": symbol,
                    "bid": quote.bid_price,
                    "ask": quote.ask_price,
                    "bid_size": quote.bid_size,
                    "ask_size": quote.ask_size,
                    "timestamp": quote.sip_timestamp
                }
            except Exception:
                pass
        
        return None

    async def get_quotes(self, symbols: List[str]) -> List[Dict]:
        quotes = []
        for symbol in symbols:
            quote = await self.get_quote(symbol)
            if quote:
                quotes.append(quote)
        return quotes

    async def get_historical_bars(
        self,
        symbol: str,
        timeframe: str,
        start: datetime,
        end: datetime,
        limit: int = 1000
    ) -> List[Dict]:
        if not self.alpaca_client:
            return []
        
        timeframe_map = {
            "1Min": TimeFrame.Minute,
            "5Min": TimeFrame(5, "Min"),
            "15Min": TimeFrame(15, "Min"),
            "1H": TimeFrame.Hour,
            "1D": TimeFrame.Day
        }
        
        try:
            request = StockBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=timeframe_map.get(timeframe, TimeFrame.Minute),
                start=start,
                end=end,
                limit=limit
            )
            bars = self.alpaca_client.get_stock_bars(request)
            
            result = []
            for bar in bars[symbol]:
                result.append({
                    "timestamp": bar.timestamp.isoformat(),
                    "open": float(bar.open),
                    "high": float(bar.high),
                    "low": float(bar.low),
                    "close": float(bar.close),
                    "volume": int(bar.volume)
                })
            return result
        except Exception as e:
            print(f"Error fetching bars: {e}")
            return []

    async def get_option_chain(self, symbol: str, expiration: Optional[str] = None) -> Optional[Dict]:
        if not self.polygon_rest:
            return None
        
        try:
            contracts = self.polygon_rest.list_options_contracts(
                underlying_ticker=symbol,
                expiration_date=expiration
            )
            
            chain = {
                "symbol": symbol,
                "expiration": expiration,
                "calls": [],
                "puts": []
            }
            
            for contract in contracts:
                option_data = {
                    "strike": contract.strike_price,
                    "contract": contract.ticker,
                    "bid": 0,
                    "ask": 0,
                    "last": 0,
                    "volume": 0,
                    "open_interest": 0,
                    "implied_volatility": 0
                }
                
                if contract.contract_type == "call":
                    chain["calls"].append(option_data)
                else:
                    chain["puts"].append(option_data)
            
            return chain
        except Exception as e:
            print(f"Error fetching option chain: {e}")
            return None

    async def get_market_depth(self, symbol: str) -> Optional[Dict]:
        return {
            "symbol": symbol,
            "bids": [{"price": 100.0, "size": 100} for _ in range(10)],
            "asks": [{"price": 100.5, "size": 100} for _ in range(10)]
        }

    async def get_time_and_sales(
        self,
        symbol: str,
        start: Optional[datetime],
        end: Optional[datetime],
        limit: int = 500
    ) -> List[Dict]:
        if not self.polygon_rest:
            return []
        
        try:
            trades = self.polygon_rest.list_trades(
                symbol,
                timestamp_gte=int(start.timestamp() * 1000) if start else None,
                timestamp_lte=int(end.timestamp() * 1000) if end else None,
                limit=limit
            )
            
            return [
                {
                    "timestamp": trade.sip_timestamp,
                    "price": trade.price,
                    "size": trade.size,
                    "conditions": trade.conditions or []
                }
                for trade in trades
            ]
        except Exception:
            return []

    async def get_snapshot(self, symbol: str) -> Optional[Dict]:
        quote = await self.get_quote(symbol)
        return {
            "symbol": symbol,
            "quote": quote,
            "prev_close": 100.0,
            "change": 0.5,
            "change_percent": 0.5,
            "volume": 1000000,
            "vwap": 100.25
        }

    async def get_latest_quotes(self) -> Dict[str, Dict]:
        return self.latest_quotes.copy()

    async def _polygon_websocket_loop(self):
        while self._running:
            try:
                await asyncio.sleep(1)
            except Exception as e:
                print(f"WebSocket error: {e}")
                await asyncio.sleep(5)
