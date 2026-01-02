from pydantic import BaseModel
from typing import List, Dict, Any

class ScanRequest(BaseModel):
    filters: List[Dict[str, Any]]
    universe: str = "SP500"
    limit: int = 50

class ScanResult(BaseModel):
    symbol: str
    price: float
    change_percent: float
    volume: int
    rsi: float
    macd: float
    signal_strength: float
    timestamp: str

class ScannerPreset(BaseModel):
    name: str
    filters: List[Dict[str, Any]]
