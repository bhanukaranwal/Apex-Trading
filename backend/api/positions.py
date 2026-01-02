from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from backend.core.security import get_current_user
from backend.services.execution_engine import ExecutionEngine
from backend.schemas.positions import Position

router = APIRouter()
execution_engine = ExecutionEngine()

@router.get("/", response_model=List[Position])
async def get_positions(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    positions = await execution_engine.get_positions(current_user["user_id"])
    return positions

@router.get("/{symbol}", response_model=Position)
async def get_position(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    position = await execution_engine.get_position(symbol, current_user["user_id"])
    if not position:
        raise HTTPException(status_code=404, detail=f"No position found for {symbol}")
    return position

@router.delete("/{symbol}", status_code=204)
async def close_position(
    symbol: str,
    qty: float = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        await execution_engine.close_position(symbol, current_user["user_id"], qty)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/", status_code=204)
async def close_all_positions(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    try:
        await execution_engine.close_all_positions(current_user["user_id"])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
