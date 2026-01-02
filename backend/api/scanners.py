from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from backend.core.security import get_current_user
from backend.services.scanner import Scanner
from backend.schemas.scanners import ScanRequest, ScanResult, ScannerPreset

router = APIRouter()
scanner = Scanner()

@router.post("/scan", response_model=List[ScanResult])
async def run_scan(
    scan_request: ScanRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    results = await scanner.scan(
        filters=scan_request.filters,
        universe=scan_request.universe,
        limit=scan_request.limit
    )
    return results

@router.get("/presets", response_model=List[ScannerPreset])
async def get_scanner_presets(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    presets = await scanner.get_presets()
    return presets

@router.post("/presets", status_code=201)
async def create_scanner_preset(
    preset: ScannerPreset,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    await scanner.save_preset(current_user["user_id"], preset)
    return {"status": "success", "preset": preset.name}

@router.get("/movers/gainers")
async def get_gainers(
    limit: int = 20,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    gainers = await scanner.get_top_gainers(limit)
    return gainers

@router.get("/movers/losers")
async def get_losers(
    limit: int = 20,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    losers = await scanner.get_top_losers(limit)
    return losers

@router.get("/movers/volume")
async def get_most_active(
    limit: int = 20,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    most_active = await scanner.get_most_active(limit)
    return most_active
