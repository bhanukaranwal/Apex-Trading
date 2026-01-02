from typing import Dict, Set, Any
from fastapi import WebSocket
import asyncio
import json
from collections import defaultdict
from backend.services.data_streamer import DataStreamer

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self.subscriptions: Dict[WebSocket, Set[str]] = defaultdict(set)
        self.data_streamer: Optional[DataStreamer] = None
        self._running = False

    async def start(self):
        self.data_streamer = DataStreamer()
        await self.data_streamer.start()
        self._running = True
        asyncio.create_task(self._broadcast_loop())

    async def stop(self):
        self._running = False
        if self.data_streamer:
            await self.data_streamer.stop()

    async def connect(self, websocket: WebSocket, channel: str):
        await websocket.accept()
        self.active_connections[channel].add(websocket)

    async def disconnect(self, websocket: WebSocket, channel: str):
        self.active_connections[channel].discard(websocket)
        if websocket in self.subscriptions:
            del self.subscriptions[websocket]

    async def handle_message(self, websocket: WebSocket, data: Dict[str, Any], channel: str):
        action = data.get("action")
        
        if action == "subscribe" and channel == "market_data":
            symbols = data.get("symbols", [])
            self.subscriptions[websocket].update(symbols)
            if self.data_streamer:
                await self.data_streamer.subscribe(symbols)
            await websocket.send_json({"status": "subscribed", "symbols": symbols})
        
        elif action == "unsubscribe" and channel == "market_data":
            symbols = data.get("symbols", [])
            self.subscriptions[websocket].difference_update(symbols)
            await websocket.send_json({"status": "unsubscribed", "symbols": symbols})

    async def broadcast_to_channel(self, channel: str, message: Dict[str, Any]):
        if channel not in self.active_connections:
            return
        
        disconnected = set()
        for websocket in self.active_connections[channel]:
            try:
                await websocket.send_json(message)
            except Exception:
                disconnected.add(websocket)
        
        for websocket in disconnected:
            await self.disconnect(websocket, channel)

    async def send_to_websocket(self, websocket: WebSocket, message: Dict[str, Any]):
        try:
            await websocket.send_json(message)
        except Exception:
            pass

    async def _broadcast_loop(self):
        while self._running:
            if self.data_streamer:
                quotes = await self.data_streamer.get_latest_quotes()
                for symbol, quote in quotes.items():
                    for websocket, symbols in self.subscriptions.items():
                        if symbol in symbols:
                            await self.send_to_websocket(websocket, {
                                "type": "quote",
                                "symbol": symbol,
                                "data": quote
                            })
            await asyncio.sleep(0.1)

websocket_manager = WebSocketManager()
