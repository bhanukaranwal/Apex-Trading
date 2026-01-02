import { useEffect, useState } from 'react'
import { positionsAPI } from '@/lib/api'
import { useTradingStore } from '@/lib/store/tradingStore'

export function PositionsList() {
  const [positions, setPositions] = useState<any[]>([])
  const updatePositions = useTradingStore((state) => state.updatePositions)

  useEffect(() => {
    const fetchPositions = async () => {
      try {
        const response = await positionsAPI.getPositions()
        setPositions(response.data)
        updatePositions(response.data)
      } catch (error) {
        console.error('Error fetching positions:', error)
      }
    }

    fetchPositions()
    const interval = setInterval(fetchPositions, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="workspace-panel bg-slate-900">
      <div className="p-2 border-b border-slate-800">
        <h3 className="font-semibold text-sm text-slate-300">Positions</h3>
      </div>

      <div className="overflow-y-auto scrollbar-thin max-h-full">
        <table className="w-full text-xs">
          <thead className="sticky top-0 bg-slate-800">
            <tr>
              <th className="text-left px-2 py-1 text-slate-400 font-semibold">Symbol</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">Qty</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">Avg</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">Last</th>
              <th className="text-right px-2 py-1 text-slate-400 font-semibold">P&L</th>
            </tr>
          </thead>
          <tbody>
            {positions.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center py-4 text-slate-500">
                  No positions
                </td>
              </tr>
            ) : (
              positions.map((pos) => (
                <tr key={pos.symbol} className="border-b border-slate-800/50 hover:bg-slate-800/30">
                  <td className="px-2 py-1.5 text-white font-semibold">{pos.symbol}</td>
                  <td className="text-right px-2 py-1.5 text-slate-300">{pos.qty}</td>
                  <td className="text-right px-2 py-1.5 text-slate-300 font-mono">
                    ${pos.avg_entry_price?.toFixed(2)}
                  </td>
                  <td className="text-right px-2 py-1.5 text-slate-300 font-mono">
                    ${pos.current_price?.toFixed(2)}
                  </td>
                  <td className={`text-right px-2 py-1.5 font-semibold font-mono ${
                    pos.unrealized_pl >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {pos.unrealized_pl >= 0 ? '+' : ''}${pos.unrealized_pl?.toFixed(2)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
