import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface GreeksChartProps {
  symbol: string
  expiration: string
}

export function GreeksChart({ symbol, expiration }: GreeksChartProps) {
  const [data, setData] = useState<any[]>([])

  useEffect(() => {
    const mockData = []
    for (let strike = 160; strike <= 190; strike += 5) {
      mockData.push({
        strike,
        delta: (strike < 175 ? 0.6 : 0.3) + (Math.random() * 0.2 - 0.1),
        gamma: 0.05 + (Math.random() * 0.03),
        theta: -(0.02 + Math.random() * 0.02),
        vega: 0.15 + (Math.random() * 0.1),
      })
    }
    setData(mockData)
  }, [symbol, expiration])

  return (
    <div className="workspace-panel bg-slate-900 h-[calc(100vh-200px)]">
      <div className="p-3 border-b border-slate-800">
        <h3 className="font-semibold text-slate-300">Greeks by Strike</h3>
      </div>
      <div className="p-4 h-[calc(100%-60px)]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="strike" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
              labelStyle={{ color: '#cbd5e1' }}
            />
            <Legend />
            <Bar dataKey="delta" fill="#3b82f6" name="Delta" />
            <Bar dataKey="gamma" fill="#22c55e" name="Gamma" />
            <Bar dataKey="vega" fill="#a855f7" name="Vega" />
            <Bar dataKey="theta" fill="#ef4444" name="Theta" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
