from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Quote(BaseModel):
    symbol: str
    bid: float
    ask: float
    bid_size: int
    ask_size: int
    timestamp: datetime

class Bar(BaseModel):
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class OptionContract(BaseModel):
    strike: float
    contract: str
    bid: float
    ask: float
    last: float
    volume: int
    open_interest: int
    implied_volatility: float

class OptionChain(BaseModel):
    symbol: str
    expiration: Optional[str]
    calls: List[OptionContract]
    puts: List[OptionContract]

class TickData(BaseModel):
    timestamp: int
    price: float
    size: int
    conditions: List[str]
