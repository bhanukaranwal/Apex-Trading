from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from backend.core.security import get_current_user
from backend.services.ai_signals import AISignalEngine
from backend.schemas.signals import Signal, SignalCreate, SignalConfig

router = APIRouter()
ai_engine = AISignalEngine()

@router.get("/", response_model=List[Signal])
async def get_signals(
    symbols: Optional[List[str]] = Query(None),
    signal_type: Optional[str] = None,
    min_confidence: float = 0.6,
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    signals = await ai_engine.get_signals(
        symbols=symbols,
        signal_type=signal_type,
        min_confidence=min_confidence,
        limit=limit
    )
    return signals

@router.get("/{symbol}/predictions")
async def get_price_predictions(
    symbol: str,
    horizon: int = 10,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    predictions = await ai_engine.predict_prices(symbol, horizon)
    return predictions

@router.get("/{symbol}/sentiment")
async def get_sentiment_analysis(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    sentiment = await ai_engine.analyze_sentiment(symbol)
    return sentiment

@router.get("/{symbol}/patterns")
async def detect_patterns(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    patterns = await ai_engine.detect_patterns(symbol)
    return patterns

@router.post("/config", status_code=201)
async def configure_signals(
    config: SignalConfig,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    await ai_engine.update_config(current_user["user_id"], config)
    return {"status": "success", "message": "Signal configuration updated"}
