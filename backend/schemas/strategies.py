from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from datetime import datetime

class StrategyCreate(BaseModel):
    name: str
    description: str
    code: str
    parameters: Dict[str, Any]

class Strategy(BaseModel):
    id: int
    user_id: str
    name: str
    description: str
    code: str
    parameters: Dict[str, Any]
    created_at: str
    status: str

class BacktestRequest(BaseModel):
    symbols: List[str]
    start_date: datetime
    end_date: datetime
    initial_capital: float = 100000
    commission: float = 0.001

class BacktestResult(BaseModel):
    strategy_id: int
    symbols: List[str]
    start_date: str
    end_date: str
    initial_capital: float
    final_value: float
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    total_trades: int
    trades: List[Dict]
    equity_curve: List[Dict]
