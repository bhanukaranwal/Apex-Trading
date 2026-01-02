from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from backend.core.security import get_current_user
from backend.services.execution_engine import ExecutionEngine
from backend.schemas.orders import OrderCreate, Order, OrderUpdate, OrderCancel

router = APIRouter()
execution_engine = ExecutionEngine()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def place_order(
    order_data: OrderCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        order = await execution_engine.place_order(
            user_id=current_user["user_id"],
            symbol=order_data.symbol,
            qty=order_data.qty,
            side=order_data.side,
            order_type=order_data.type,
            limit_price=order_data.limit_price,
            stop_price=order_data.stop_price,
            time_in_force=order_data.time_in_force,
            extended_hours=order_data.extended_hours,
            client_order_id=order_data.client_order_id,
            order_class=order_data.order_class,
            take_profit=order_data.take_profit,
            stop_loss=order_data.stop_loss,
            trail_price=order_data.trail_price,
            trail_percent=order_data.trail_percent
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[Order])
async def get_orders(
    status_filter: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    orders = await execution_engine.get_orders(
        user_id=current_user["user_id"],
        status=status_filter,
        limit=limit
    )
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    order = await execution_engine.get_order(order_id, current_user["user_id"])
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.patch("/{order_id}", response_model=Order)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        order = await execution_engine.update_order(
            order_id=order_id,
            user_id=current_user["user_id"],
            qty=order_update.qty,
            limit_price=order_update.limit_price,
            stop_price=order_update.stop_price,
            trail=order_update.trail
        )
        return order
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_order(
    order_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        await execution_engine.cancel_order(order_id, current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_all_orders(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        await execution_engine.cancel_all_orders(current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
