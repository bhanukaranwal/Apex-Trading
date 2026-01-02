from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from backend.core.security import get_current_user
from backend.services.risk_engine import RiskEngine
from backend.schemas.portfolio import Portfolio, AccountInfo, PortfolioAnalytics

router = APIRouter()
risk_engine = RiskEngine()

@router.get("/account", response_model=AccountInfo)
async def get_account(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    account = await risk_engine.get_account_info(current_user["user_id"])
    return account

@router.get("/summary", response_model=Portfolio)
async def get_portfolio_summary(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    portfolio = await risk_engine.get_portfolio_summary(current_user["user_id"])
    return portfolio

@router.get("/analytics", response_model=PortfolioAnalytics)
async def get_portfolio_analytics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    analytics = await risk_engine.get_portfolio_analytics(current_user["user_id"])
    return analytics

@router.get("/risk-metrics")
async def get_risk_metrics(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    metrics = await risk_engine.calculate_risk_metrics(current_user["user_id"])
    return metrics

@router.get("/greeks")
async def get_portfolio_greeks(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    greeks = await risk_engine.calculate_portfolio_greeks(current_user["user_id"])
    return greeks
