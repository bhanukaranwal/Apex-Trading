import { useEffect, useState } from 'react'
import { ChartContainer } from '@/components/ChartContainer'
import { DOMLadder } from '@/components/DOMLadder'
import { TimeAndSales } from '@/components/TimeAndSales'
import { OrderTicket } from '@/components/OrderTicket'
import { Watchlist } from '@/components/Watchlist'
import { PositionsList } from '@/components/PositionsList'
import { OrdersList } from '@/components/OrdersList'
import { useTradingStore } from '@/lib/store/tradingStore'
import { marketDataWS } from '@/lib/websocket'

export function TradingDashboard() {
  const selectedSymbol = useTradingStore((state) => state.selectedSymbol)
  const [quote, setQuote] = useState<any>(null)

  useEffect(() => {
    marketDataWS.connect()

    const handleQuote = (data: any) => {
      if (data.symbol === selectedSymbol) {
        setQuote(data.data)
      }
    }

    marketDataWS.subscribe('quote', handleQuote)
    marketDataWS.send({ action: 'subscribe', symbols: [selectedSymbol] })

    return () => {
      marketDataWS.unsubscribe('quote', handleQuote)
    }
  }, [selectedSymbol])

  return (
    <div className="h-screen flex flex-col bg-slate-950">
      <header className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-4 justify-between">
        <div className="flex items-center gap-6">
          <h2 className="text-xl font-bold text-white">{selectedSymbol}</h2>
          {quote && (
            <div className="flex items-center gap-4 text-sm">
              <span className="text-2xl font-mono font-bold text-white">
                ${quote.last?.toFixed(2) || '0.00'}
              </span>
              <span className={`font-semibold ${quote.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                {quote.change >= 0 ? '+' : ''}{quote.change?.toFixed(2)} ({quote.change_percent?.toFixed(2)}%)
              </span>
            </div>
          )}
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-400">
          <span>Vol: {quote?.volume?.toLocaleString() || '0'}</span>
          <span>Bid: {quote?.bid?.toFixed(2) || '0.00'} x {quote?.bid_size || 0}</span>
          <span>Ask: {quote?.ask?.toFixed(2) || '0.00'} x {quote?.ask_size || 0}</span>
        </div>
      </header>

      <div className="flex-1 grid grid-cols-12 gap-2 p-2 overflow-hidden">
        <div className="col-span-2 space-y-2">
          <Watchlist />
          <OrderTicket />
        </div>

        <div className="col-span-7 space-y-2">
          <div className="h-[calc(60vh-1rem)] workspace-panel bg-slate-900">
            <ChartContainer symbol={selectedSymbol} />
          </div>
          <div className="h-[calc(40vh-1rem)] grid grid-cols-2 gap-2">
            <PositionsList />
            <OrdersList />
          </div>
        </div>

        <div className="col-span-3 space-y-2">
          <DOMLadder symbol={selectedSymbol} />
          <TimeAndSales symbol={selectedSymbol} />
        </div>
      </div>
    </div>
  )
}
