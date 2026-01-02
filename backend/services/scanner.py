from typing import Dict, List, Any, Optional
import numpy as np
from datetime import datetime

class Scanner:
    def __init__(self):
        self.presets = {
            "momentum_breakout": {
                "name": "Momentum Breakout",
                "filters": [
                    {"field": "rsi", "operator": ">", "value": 60},
                    {"field": "volume", "operator": ">", "value": "avg_volume * 2"},
                    {"field": "price", "operator": ">", "value": "52w_high * 0.95"}
                ]
            },
            "oversold_bounce": {
                "name": "Oversold Bounce",
                "filters": [
                    {"field": "rsi", "operator": "<", "value": 30},
                    {"field": "price", "operator": ">", "value": "sma_200"}
                ]
            }
        }

    async def scan(
        self,
        filters: List[Dict[str, Any]],
        universe: str = "SP500",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        results = []
        symbols = self._get_universe_symbols(universe)
        
        for symbol in symbols[:limit]:
            metrics = await self._calculate_metrics(symbol)
            
            if self._apply_filters(metrics, filters):
                results.append({
                    "symbol": symbol,
                    "price": metrics["price"],
                    "change_percent": metrics["change_percent"],
                    "volume": metrics["volume"],
                    "rsi": metrics["rsi"],
                    "macd": metrics["macd"],
                    "signal_strength": metrics["signal_strength"],
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return sorted(results, key=lambda x: x["signal_strength"], reverse=True)

    async def get_presets(self) -> List[Dict[str, Any]]:
        return [
            {"id": key, "name": preset["name"], "filters": preset["filters"]}
            for key, preset in self.presets.items()
        ]

    async def save_preset(self, user_id: str, preset: Dict[str, Any]):
        preset_id = f"user_{user_id}_{preset['name'].lower().replace(' ', '_')}"
        self.presets[preset_id] = preset

    async def get_top_gainers(self, limit: int = 20) -> List[Dict[str, Any]]:
        gainers = []
        for i in range(limit):
            gainers.append({
                "symbol": f"GAINER{i+1}",
                "price": np.random.uniform(50, 200),
                "change": np.random.uniform(5, 20),
                "change_percent": np.random.uniform(5, 15),
                "volume": int(np.random.uniform(1000000, 50000000))
            })
        return sorted(gainers, key=lambda x: x["change_percent"], reverse=True)

    async def get_top_losers(self, limit: int = 20) -> List[Dict[str, Any]]:
        losers = []
        for i in range(limit):
            losers.append({
                "symbol": f"LOSER{i+1}",
                "price": np.random.uniform(50, 200),
                "change": -np.random.uniform(5, 20),
                "change_percent": -np.random.uniform(5, 15),
                "volume": int(np.random.uniform(1000000, 50000000))
            })
        return sorted(losers, key=lambda x: x["change_percent"])

    async def get_most_active(self, limit: int = 20) -> List[Dict[str, Any]]:
        active = []
        for i in range(limit):
            active.append({
                "symbol": f"ACTIVE{i+1}",
                "price": np.random.uniform(50, 200),
                "volume": int(np.random.uniform(10000000, 100000000)),
                "change_percent": np.random.uniform(-10, 10)
            })
        return sorted(active, key=lambda x: x["volume"], reverse=True)

    def _get_universe_symbols(self, universe: str) -> List[str]:
        universes = {
            "SP500": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "JPM", "V", "JNJ"],
            "NASDAQ100": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"],
            "ALL": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "SPY", "QQQ"]
        }
        return universes.get(universe, universes["SP500"]) * 10

    async def _calculate_metrics(self, symbol: str) -> Dict[str, Any]:
        return {
            "symbol": symbol,
            "price": np.random.uniform(100, 200),
            "change_percent": np.random.uniform(-5, 5),
            "volume": int(np.random.uniform(1000000, 10000000)),
            "rsi": np.random.uniform(20, 80),
            "macd": np.random.uniform(-2, 2),
            "signal_strength": np.random.uniform(0, 100),
            "sma_50": np.random.uniform(95, 105),
            "sma_200": np.random.uniform(90, 110)
        }

    def _apply_filters(self, metrics: Dict[str, Any], filters: List[Dict[str, Any]]) -> bool:
        for filter_item in filters:
            field = filter_item["field"]
            operator = filter_item["operator"]
            value = filter_item["value"]
            
            if field not in metrics:
                continue
            
            metric_value = metrics[field]
            
            if operator == ">" and not (metric_value > value):
                return False
            elif operator == "<" and not (metric_value < value):
                return False
            elif operator == "==" and not (metric_value == value):
                return False
        
        return True
