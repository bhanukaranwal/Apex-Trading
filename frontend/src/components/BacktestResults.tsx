import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

interface BacktestResultsProps {
  result: any
}

export function BacktestResults({ result }: BacktestResultsProps) {
  return (
    <div className="workspace-panel bg-slate-900 p-6">
      <h2 className="text-xl font-bold text-white mb-6">Backtest Results</h2>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Total Return</div>
          <div className={`text-2xl font-bold ${result.total_return >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {result.total_return?.toFixed(2)}%
          </div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Sharpe Ratio</div>
          <div className="text-2xl font-bold text-white">{result.sharpe_ratio?.toFixed(2)}</div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Max Drawdown</div>
          <div className="text-2xl font-bold text-red-400">{result.max_drawdown?.toFixed(2)}%</div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Win Rate</div>
          <div className="text-2xl font-bold text-white">{result.win_rate?.toFixed(2)}%</div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Total Trades</div>
          <div className="text-2xl font-bold text-white">{result.total_trades}</div>
        </div>
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="text-slate-400 text-sm">Final Value</div>
          <div className="text-2xl font-bold text-white">${result.final_value?.toLocaleString()}</div>
        </div>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-semibold text-white mb-4">Equity Curve</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={result.equity_curve}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="date" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
            <Line type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div>
        <h3 className="text-lg font-semibold text-white mb-4">Recent Trades</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-800">
              <tr>
                <th className="text-left px-3 py-2 text-slate-400">Entry Date</th>
                <th className="text-left px-3 py-2 text-slate-400">Exit Date</th>
                <th className="text-right px-3 py-2 text-slate-400">Size</th>
                <th className="text-right px-3 py-2 text-slate-400">Entry</th>
                <th className="text-right px-3 py-2 text-slate-400">Exit</th>
                <th className="text-right px-3 py-2 text-slate-400">P&L</th>
              </tr>
            </thead>
            <tbody>
              {result.trades?.slice(0, 10).map((trade: any, idx: number) => (
                <tr key={idx} className="border-b border-slate-800">
                  <td className="px-3 py-2 text-slate-300">{trade.entry_date}</td>
                  <td className="px-3 py-2 text-slate-300">{trade.exit_date}</td>
                  <td className="text-right px-3 py-2 text-slate-300">{trade.size}</td>
                  <td className="text-right px-3 py-2 text-slate-300">${trade.entry_price?.toFixed(2)}</td>
                  <td className="text-right px-3 py-2 text-slate-300">${trade.exit_price?.toFixed(2)}</td>
                  <td className={`text-right px-3 py-2 font-semibold ${
                    trade.pnl >= 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    ${trade.pnl?.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
