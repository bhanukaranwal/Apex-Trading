from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from backend.core.security import get_current_user
from backend.services.data_streamer import DataStreamer
from backend.schemas.market_data import Quote, Bar, OptionChain, TickData

router = APIRouter()
data_streamer = DataStreamer()

@router.get("/quote/{symbol}", response_model=Quote)
async def get_quote(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    quote = await data_streamer.get_quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail=f"Quote not found for {symbol}")
    return quote

@router.get("/quotes", response_model=List[Quote])
async def get_quotes(
    symbols: List[str] = Query(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    quotes = await data_streamer.get_quotes(symbols)
    return quotes

@router.get("/bars/{symbol}", response_model=List[Bar])
async def get_bars(
    symbol: str,
    timeframe: str = Query("1Min", regex="^(1Min|5Min|15Min|1H|1D)$"),
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(1000, le=50000),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    if not end:
        end = datetime.utcnow()
    if not start:
        start = end - timedelta(days=30)
    
    bars = await data_streamer.get_historical_bars(symbol, timeframe, start, end, limit)
    return bars

@router.get("/options/chain/{symbol}", response_model=OptionChain)
async def get_option_chain(
    symbol: str,
    expiration: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    chain = await data_streamer.get_option_chain(symbol, expiration)
    if not chain:
        raise HTTPException(status_code=404, detail=f"Option chain not found for {symbol}")
    return chain

@router.get("/depth/{symbol}")
async def get_market_depth(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    depth = await data_streamer.get_market_depth(symbol)
    if not depth:
        raise HTTPException(status_code=404, detail=f"Market depth not found for {symbol}")
    return depth

@router.get("/trades/{symbol}", response_model=List[TickData])
async def get_time_and_sales(
    symbol: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(500, le=10000),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    trades = await data_streamer.get_time_and_sales(symbol, start, end, limit)
    return trades

@router.get("/snapshot/{symbol}")
async def get_snapshot(
    symbol: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    snapshot = await data_streamer.get_snapshot(symbol)
    if not snapshot:
        raise HTTPException(status_code=404, detail=f"Snapshot not found for {symbol}")
    return snapshot
