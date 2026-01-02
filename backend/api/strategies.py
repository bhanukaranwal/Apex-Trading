from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from backend.core.security import get_current_user
from backend.services.backtester import Backtester
from backend.schemas.strategies import Strategy, StrategyCreate, BacktestRequest, BacktestResult

router = APIRouter()
backtester = Backtester()

@router.post("/", response_model=Strategy, status_code=status.HTTP_201_CREATED)
async def create_strategy(
    strategy_data: StrategyCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    strategy = await backtester.create_strategy(
        user_id=current_user["user_id"],
        name=strategy_data.name,
        description=strategy_data.description,
        code=strategy_data.code,
        parameters=strategy_data.parameters
    )
    return strategy

@router.get("/", response_model=List[Strategy])
async def get_strategies(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    strategies = await backtester.get_user_strategies(current_user["user_id"])
    return strategies

@router.get("/{strategy_id}", response_model=Strategy)
async def get_strategy(
    strategy_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    strategy = await backtester.get_strategy(strategy_id, current_user["user_id"])
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

@router.post("/{strategy_id}/backtest", response_model=BacktestResult)
async def run_backtest(
    strategy_id: int,
    backtest_request: BacktestRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    result = await backtester.run_backtest(
        strategy_id=strategy_id,
        user_id=current_user["user_id"],
        symbols=backtest_request.symbols,
        start_date=backtest_request.start_date,
        end_date=backtest_request.end_date,
        initial_capital=backtest_request.initial_capital,
        commission=backtest_request.commission
    )
    return result

@router.post("/{strategy_id}/deploy")
async def deploy_strategy(
    strategy_id: int,
    symbols: List[str],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    await backtester.deploy_strategy(strategy_id, current_user["user_id"], symbols)
    return {"status": "deployed", "strategy_id": strategy_id, "symbols": symbols}

@router.delete("/{strategy_id}/deploy")
async def stop_strategy(
    strategy_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    await backtester.stop_strategy(strategy_id, current_user["user_id"])
    return {"status": "stopped", "strategy_id": strategy_id}
