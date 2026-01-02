from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio
from ib_insync import IB, Stock, Order as IBOrder, LimitOrder, MarketOrder, StopOrder
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from backend.core.config import settings
import uuid

class ExecutionEngine:
    def __init__(self):
        self.ib = None
        self.alpaca = None
        self.paper_mode = settings.ENABLE_PAPER_TRADING
        self.live_mode = settings.ENABLE_LIVE_TRADING
        self.orders_cache: Dict[str, Dict] = {}
        self.positions_cache: Dict[str, Dict] = {}
        
        if settings.ALPACA_API_KEY:
            self.alpaca = TradingClient(
                api_key=settings.ALPACA_API_KEY,
                secret_key=settings.ALPACA_SECRET_KEY,
                paper=self.paper_mode
            )

    async def connect_ib(self):
        if not self.ib:
            self.ib = IB()
            try:
                await self.ib.connectAsync(
                    settings.IB_HOST,
                    settings.IB_PORT,
                    clientId=settings.IB_CLIENT_ID
                )
            except Exception as e:
                print(f"IB connection failed: {e}")
                self.ib = None

    async def place_order(
        self,
        user_id: str,
        symbol: str,
        qty: float,
        side: str,
        order_type: str = "market",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        time_in_force: str = "day",
        extended_hours: bool = False,
        client_order_id: Optional[str] = None,
        order_class: Optional[str] = None,
        take_profit: Optional[Dict] = None,
        stop_loss: Optional[Dict] = None,
        trail_price: Optional[float] = None,
        trail_percent: Optional[float] = None
    ) -> Dict[str, Any]:
        order_id = client_order_id or str(uuid.uuid4())
        
        order_data = {
            "id": order_id,
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "type": order_type,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "time_in_force": time_in_force,
            "status": "pending",
            "filled_qty": 0,
            "filled_avg_price": 0,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "user_id": user_id
        }
        
        if self.alpaca:
            try:
                order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
                tif = TimeInForce.DAY if time_in_force.lower() == "day" else TimeInForce.GTC
                
                if order_type.lower() == "market":
                    request = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=order_side,
                        time_in_force=tif
                    )
                elif order_type.lower() == "limit":
                    request = LimitOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=order_side,
                        time_in_force=tif,
                        limit_price=limit_price
                    )
                elif order_type.lower() == "stop":
                    request = StopOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=order_side,
                        time_in_force=tif,
                        stop_price=stop_price
                    )
                else:
                    request = MarketOrderRequest(
                        symbol=symbol,
                        qty=qty,
                        side=order_side,
                        time_in_force=tif
                    )
                
                alpaca_order = self.alpaca.submit_order(request)
                
                order_data.update({
                    "id": alpaca_order.id,
                    "status": alpaca_order.status.value,
                    "broker": "alpaca"
                })
            except Exception as e:
                order_data["status"] = "rejected"
                order_data["reject_reason"] = str(e)
        
        elif self.ib:
            try:
                await self.connect_ib()
                contract = Stock(symbol, 'SMART', 'USD')
                
                if order_type.lower() == "market":
                    ib_order = MarketOrder(side.upper(), qty)
                elif order_type.lower() == "limit":
                    ib_order = LimitOrder(side.upper(), qty, limit_price)
                elif order_type.lower() == "stop":
                    ib_order = StopOrder(side.upper(), qty, stop_price)
                else:
                    ib_order = MarketOrder(side.upper(), qty)
                
                trade = self.ib.placeOrder(contract, ib_order)
                
                order_data.update({
                    "id": str(trade.order.orderId),
                    "status": trade.orderStatus.status,
                    "broker": "interactive_brokers"
                })
            except Exception as e:
                order_data["status"] = "rejected"
                order_data["reject_reason"] = str(e)
        
        else:
            order_data["status"] = "filled"
            order_data["filled_qty"] = qty
            order_data["filled_avg_price"] = limit_price or 100.0
            order_data["broker"] = "paper"
        
        self.orders_cache[order_id] = order_data
        return order_data

    async def get_orders(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        if self.alpaca:
            try:
                alpaca_orders = self.alpaca.get_orders()
                return [
                    {
                        "id": order.id,
                        "symbol": order.symbol,
                        "qty": float(order.qty),
                        "side": order.side.value,
                        "type": order.order_type.value,
                        "status": order.status.value,
                        "filled_qty": float(order.filled_qty or 0),
                        "filled_avg_price": float(order.filled_avg_price or 0),
                        "limit_price": float(order.limit_price) if order.limit_price else None,
                        "stop_price": float(order.stop_price) if order.stop_price else None,
                        "created_at": order.created_at.isoformat(),
                        "updated_at": order.updated_at.isoformat() if order.updated_at else None
                    }
                    for order in alpaca_orders[:limit]
                ]
            except Exception as e:
                print(f"Error fetching orders: {e}")
        
        return [order for order in self.orders_cache.values() if order["user_id"] == user_id][:limit]

    async def get_order(self, order_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        if self.alpaca:
            try:
                order = self.alpaca.get_order_by_id(order_id)
                return {
                    "id": order.id,
                    "symbol": order.symbol,
                    "qty": float(order.qty),
                    "side": order.side.value,
                    "type": order.order_type.value,
                    "status": order.status.value,
                    "filled_qty": float(order.filled_qty or 0),
                    "filled_avg_price": float(order.filled_avg_price or 0),
                    "limit_price": float(order.limit_price) if order.limit_price else None,
                    "created_at": order.created_at.isoformat()
                }
            except Exception:
                pass
        
        return self.orders_cache.get(order_id)

    async def update_order(
        self,
        order_id: str,
        user_id: str,
        qty: Optional[float] = None,
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
        trail: Optional[float] = None
    ) -> Dict[str, Any]:
        if self.alpaca:
            try:
                from alpaca.trading.requests import ReplaceOrderRequest
                request = ReplaceOrderRequest(
                    qty=qty,
                    limit_price=limit_price
                )
                order = self.alpaca.replace_order_by_id(order_id, request)
                return {
                    "id": order.id,
                    "status": order.status.value,
                    "qty": float(order.qty)
                }
            except Exception as e:
                raise Exception(f"Failed to update order: {e}")
        
        if order_id in self.orders_cache:
            if qty:
                self.orders_cache[order_id]["qty"] = qty
            if limit_price:
                self.orders_cache[order_id]["limit_price"] = limit_price
            return self.orders_cache[order_id]
        
        raise Exception("Order not found")

    async def cancel_order(self, order_id: str, user_id: str):
        if self.alpaca:
            try:
                self.alpaca.cancel_order_by_id(order_id)
            except Exception as e:
                raise Exception(f"Failed to cancel order: {e}")
        
        if order_id in self.orders_cache:
            self.orders_cache[order_id]["status"] = "canceled"

    async def cancel_all_orders(self, user_id: str):
        if self.alpaca:
            try:
                self.alpaca.cancel_orders()
            except Exception as e:
                raise Exception(f"Failed to cancel orders: {e}")
        
        for order_id in self.orders_cache:
            if self.orders_cache[order_id]["user_id"] == user_id:
                self.orders_cache[order_id]["status"] = "canceled"

    async def get_positions(self, user_id: str) -> List[Dict[str, Any]]:
        if self.alpaca:
            try:
                positions = self.alpaca.get_all_positions()
                return [
                    {
                        "symbol": pos.symbol,
                        "qty": float(pos.qty),
                        "side": "long" if float(pos.qty) > 0 else "short",
                        "avg_entry_price": float(pos.avg_entry_price),
                        "market_value": float(pos.market_value),
                        "cost_basis": float(pos.cost_basis),
                        "unrealized_pl": float(pos.unrealized_pl),
                        "unrealized_plpc": float(pos.unrealized_plpc),
                        "current_price": float(pos.current_price)
                    }
                    for pos in positions
                ]
            except Exception as e:
                print(f"Error fetching positions: {e}")
        
        return list(self.positions_cache.values())

    async def get_position(self, symbol: str, user_id: str) -> Optional[Dict[str, Any]]:
        if self.alpaca:
            try:
                pos = self.alpaca.get_open_position(symbol)
                return {
                    "symbol": pos.symbol,
                    "qty": float(pos.qty),
                    "side": "long" if float(pos.qty) > 0 else "short",
                    "avg_entry_price": float(pos.avg_entry_price),
                    "market_value": float(pos.market_value),
                    "unrealized_pl": float(pos.unrealized_pl),
                    "current_price": float(pos.current_price)
                }
            except Exception:
                pass
        
        return self.positions_cache.get(symbol)

    async def close_position(self, symbol: str, user_id: str, qty: Optional[float] = None):
        if self.alpaca:
            try:
                if qty:
                    self.alpaca.close_position(symbol, close_options={"qty": str(qty)})
                else:
                    self.alpaca.close_position(symbol)
            except Exception as e:
                raise Exception(f"Failed to close position: {e}")
        
        if symbol in self.positions_cache:
            del self.positions_cache[symbol]

    async def close_all_positions(self, user_id: str):
        if self.alpaca:
            try:
                self.alpaca.close_all_positions()
            except Exception as e:
                raise Exception(f"Failed to close positions: {e}")
        
        self.positions_cache.clear()
