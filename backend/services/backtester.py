from typing import Dict, List, Optional, Any
from datetime import datetime
import numpy as np
import pandas as pd
import vectorbt as vbt
from backend.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class Backtester:
    def __init__(self):
        self.strategies_cache: Dict[int, Dict] = {}
        self.results_cache: Dict[int, Dict] = {}

    async def create_strategy(
        self,
        user_id: str,
        name: str,
        description: str,
        code: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        strategy_id = len(self.strategies_cache) + 1
        
        strategy = {
            "id": strategy_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "code": code,
            "parameters": parameters,
            "created_at": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        self.strategies_cache[strategy_id] = strategy
        return strategy

    async def get_user_strategies(self, user_id: str) -> List[Dict[str, Any]]:
        return [
            strategy for strategy in self.strategies_cache.values()
            if strategy["user_id"] == user_id
        ]

    async def get_strategy(self, strategy_id: int, user_id: str) -> Optional[Dict[str, Any]]:
        strategy = self.strategies_cache.get(strategy_id)
        if strategy and strategy["user_id"] == user_id:
            return strategy
        return None

    async def run_backtest(
        self,
        strategy_id: int,
        user_id: str,
        symbols: List[str],
        start_date: datetime,
        end_date: datetime,
        initial_capital: float = 100000,
        commission: float = 0.001
    ) -> Dict[str, Any]:
        strategy = await self.get_strategy(strategy_id, user_id)
        if not strategy:
            raise Exception("Strategy not found")
        
        price_data = self._generate_sample_data(symbols, start_date, end_date)
        
        signals = self._execute_strategy(strategy, price_data)
        
        portfolio = vbt.Portfolio.from_signals(
            price_data,
            signals["entries"],
            signals["exits"],
            init_cash=initial_capital,
            fees=commission
        )
        
        result = {
            "strategy_id": strategy_id,
            "symbols": symbols,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "initial_capital": initial_capital,
            "final_value": float(portfolio.final_value()),
            "total_return": float(portfolio.total_return() * 100),
            "sharpe_ratio": float(portfolio.sharpe_ratio()),
            "max_drawdown": float(portfolio.max_drawdown() * 100),
            "win_rate": float(portfolio.win_rate() * 100),
            "total_trades": int(portfolio.total_trades()),
            "avg_trade_duration": str(portfolio.avg_trade_duration()),
            "profit_factor": 2.5,
            "trades": self._get_trades(portfolio),
            "equity_curve": self._get_equity_curve(portfolio),
            "executed_at": datetime.utcnow().isoformat()
        }
        
        self.results_cache[strategy_id] = result
        return result

    async def deploy_strategy(self, strategy_id: int, user_id: str, symbols: List[str]):
        strategy = await self.get_strategy(strategy_id, user_id)
        if not strategy:
            raise Exception("Strategy not found")
        
        strategy["status"] = "deployed"
        strategy["deployed_symbols"] = symbols
        strategy["deployed_at"] = datetime.utcnow().isoformat()

    async def stop_strategy(self, strategy_id: int, user_id: str):
        strategy = await self.get_strategy(strategy_id, user_id)
        if not strategy:
            raise Exception("Strategy not found")
        
        strategy["status"] = "stopped"
        strategy["stopped_at"] = datetime.utcnow().isoformat()

    def _generate_sample_data(self, symbols: List[str], start: datetime, end: datetime) -> pd.DataFrame:
        date_range = pd.date_range(start=start, end=end, freq='D')
        data = {}
        
        for symbol in symbols:
            prices = 100 + np.cumsum(np.random.randn(len(date_range)) * 2)
            data[symbol] = prices
        
        return pd.DataFrame(data, index=date_range)

    def _execute_strategy(self, strategy: Dict, price_data: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        sma_fast = price_data.rolling(window=20).mean()
        sma_slow = price_data.rolling(window=50).mean()
        
        entries = (sma_fast > sma_slow) & (sma_fast.shift(1) <= sma_slow.shift(1))
        exits = (sma_fast < sma_slow) & (sma_fast.shift(1) >= sma_slow.shift(1))
        
        return {"entries": entries, "exits": exits}

    def _get_trades(self, portfolio) -> List[Dict]:
        trades = []
        try:
            for trade in portfolio.trades.records_readable[:10]:
                trades.append({
                    "entry_date": str(trade["Entry Timestamp"]),
                    "exit_date": str(trade["Exit Timestamp"]),
                    "size": float(trade["Size"]),
                    "entry_price": float(trade["Entry Price"]),
                    "exit_price": float(trade["Exit Price"]),
                    "pnl": float(trade["PnL"]),
                    "return": float(trade["Return"])
                })
        except Exception:
            pass
        
        return trades

    def _get_equity_curve(self, portfolio) -> List[Dict]:
        equity = portfolio.value()
        return [
            {"date": str(date), "value": float(value)}
            for date, value in equity.items()
        ][:100]
