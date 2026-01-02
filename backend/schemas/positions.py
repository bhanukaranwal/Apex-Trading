from pydantic import BaseModel

class Position(BaseModel):
    symbol: str
    qty: float
    side: str
    avg_entry_price: float
    market_value: float
    cost_basis: float
    unrealized_pl: float
    unrealized_plpc: float
    current_price: float
