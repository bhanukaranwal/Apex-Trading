import { useEffect, useState } from 'react'
import { marketDataAPI } from '@/lib/api'

interface TimeAndSalesProps {
  symbol: string
}

interface Trade {
  timestamp: number
  price: number
  size: number
  conditions: string[]
}

export function TimeAndSales({ symbol }: TimeAndSalesProps) {
  const [trades, setTrades] = useState<Trade[]>([])

  useEffect(() => {
    const fetchTrades = async () => {
      try {
        const response = await marketDataAPI.getDepth(symbol)
        const mockTrades: Trade[] = Array.from({ length: 50 }, (_, i) => ({
          timestamp: Date.now() - i * 1000,
          price: 175 + Math.random() * 2 - 1,
          size: Math.floor(Math.random() * 500) + 100,
          conditions: [],
        }))
        setTrades(mockTrades)
      } catch (error) {
        console.error('Error fetching trades:', error)
      }
    }

    fetchTrades()
    const interval = setInterval(fetchTrades, 2000)

    return () => clearInterval(interval)
  }, [symbol])

  return (
    <div className="workspace-panel bg-slate-900 h-[calc(40vh-0.5rem)] flex flex-col">
      <div className="p-2 border-b border-slate-800">
        <h3 className="font-semibold text-sm text-slate-300">Time & Sales</h3>
      </div>

      <div className="flex-1 overflow-y-auto scrollbar-thin">
        <table className="w-full text-xs font-mono">
          <thead className="sticky top-0 bg-slate-800">
            <tr>
              <th className="text-left px-2 py-1 text-slate-400 font-semibold">Time</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">Price</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">Size</th>
            </tr>
          </thead>
          <tbody>
            {trades.map((trade, idx) => {
              const time = new Date(trade.timestamp)
              const prevPrice = idx < trades.length - 1 ? trades[idx + 1].price : trade.price
              const direction = trade.price > prevPrice ? 'up' : trade.price < prevPrice ? 'down' : 'neutral'

              return (
                <tr key={idx} className="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td className="px-2 py-1 text-slate-400">
                    {time.toLocaleTimeString('en-US', { hour12: false })}
                  </td>
                  <td className={`text-right px-2 py-1 font-semibold ${
                    direction === 'up' ? 'text-green-400' : direction === 'down' ? 'text-red-400' : 'text-slate-300'
                  }`}>
                    {trade.price.toFixed(2)}
                  </td>
                  <td className="text-right px-2 py-1 text-slate-300">
                    {trade.size.toLocaleString()}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
