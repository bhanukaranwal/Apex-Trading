from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class OrderCreate(BaseModel):
    symbol: str
    qty: float
    side: str
    type: str = "market"
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    time_in_force: str = "day"
    extended_hours: bool = False
    client_order_id: Optional[str] = None
    order_class: Optional[str] = None
    take_profit: Optional[Dict] = None
    stop_loss: Optional[Dict] = None
    trail_price: Optional[float] = None
    trail_percent: Optional[float] = None

class Order(BaseModel):
    id: str
    symbol: str
    qty: float
    side: str
    type: str
    status: str
    filled_qty: float
    filled_avg_price: float
    limit_price: Optional[float]
    stop_price: Optional[float]
    created_at: str
    updated_at: Optional[str]

class OrderUpdate(BaseModel):
    qty: Optional[float] = None
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    trail: Optional[float] = None

class OrderCancel(BaseModel):
    order_id: str
