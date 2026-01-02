import asyncio
from polygon import WebSocketClient
from backend.core.config import settings

async def main():
    client = WebSocketClient(settings.POLYGON_API_KEY)
    
    def handle_msg(msg):
        print(f"Received: {msg}")
    
    client.subscribe_stock_trades(handle_msg, "AAPL", "MSFT", "GOOGL")
    
    print("Streaming live data... Press Ctrl+C to stop")
    await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
