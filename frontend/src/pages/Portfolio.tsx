import { useEffect, useState } from 'react'
import { portfolioAPI } from '@/lib/api'
import { TrendingUp, DollarSign, PieChart, AlertTriangle } from 'lucide-react'
import { PieChart as RechartsPie, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts'

export function Portfolio() {
  const [account, setAccount] = useState<any>(null)
  const [summary, setSummary] = useState<any>(null)
  const [analytics, setAnalytics] = useState<any>(null)
  const [riskMetrics, setRiskMetrics] = useState<any>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [accountRes, summaryRes, analyticsRes, riskRes] = await Promise.all([
          portfolioAPI.getAccount(),
          portfolioAPI.getSummary(),
          portfolioAPI.getAnalytics(),
          portfolioAPI.getRiskMetrics(),
        ])
        setAccount(accountRes.data)
        setSummary(summaryRes.data)
        setAnalytics(analyticsRes.data)
        setRiskMetrics(riskRes.data)
      } catch (error) {
        console.error('Error fetching portfolio data:', error)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  const COLORS = ['#3b82f6', '#22c55e', '#a855f7', '#f59e0b', '#ef4444']

  return (
    <div className="h-screen overflow-auto bg-slate-950 p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Portfolio Dashboard</h1>

      <div className="grid grid-cols-4 gap-4 mb-6">
        <div className="workspace-panel bg-slate-900 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Portfolio Value</span>
            <DollarSign size={20} className="text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            ${summary?.account_value?.toLocaleString() || '0'}
          </div>
          <div className={`text-sm mt-1 ${summary?.total_pl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {summary?.total_pl >= 0 ? '+' : ''}${summary?.total_pl?.toFixed(2) || '0'} ({summary?.total_pl_percent?.toFixed(2) || '0'}%)
          </div>
        </div>

        <div className="workspace-panel bg-slate-900 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Buying Power</span>
            <TrendingUp size={20} className="text-green-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            ${summary?.buying_power?.toLocaleString() || '0'}
          </div>
          <div className="text-sm text-slate-400 mt-1">
            Cash: ${summary?.cash?.toLocaleString() || '0'}
          </div>
        </div>

        <div className="workspace-panel bg-slate-900 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Positions</span>
            <PieChart size={20} className="text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {summary?.positions_count || 0}
          </div>
          <div className="text-sm text-slate-400 mt-1">
            Value: ${summary?.positions_value?.toLocaleString() || '0'}
          </div>
        </div>

        <div className="workspace-panel bg-slate-900 p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-slate-400 text-sm">Day P&L</span>
            <AlertTriangle size={20} className="text-yellow-400" />
          </div>
          <div className={`text-2xl font-bold ${summary?.day_pl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {summary?.day_pl >= 0 ? '+' : ''}${summary?.day_pl?.toFixed(2) || '0'}
          </div>
          <div className="text-sm text-slate-400 mt-1">
            Today's performance
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="workspace-panel bg-slate-900 p-4">
          <h3 className="font-semibold text-slate-300 mb-4">Exposure by Sector</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RechartsPie>
              <Pie
                data={Object.entries(analytics?.exposure_by_sector || {}).map(([name, value]) => ({
                  name,
                  value,
                }))}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }: any) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {Object.keys(analytics?.exposure_by_sector || {}).map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
            </RechartsPie>
          </ResponsiveContainer>
        </div>

        <div className="workspace-panel bg-slate-900 p-4">
          <h3 className="font-semibold text-slate-300 mb-4">Risk Metrics</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Value at Risk (95%)</span>
              <span className="text-white font-semibold">${riskMetrics?.var_95?.toFixed(2) || '0'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Value at Risk (99%)</span>
              <span className="text-white font-semibold">${riskMetrics?.var_99?.toFixed(2) || '0'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Max Drawdown</span>
              <span className="text-red-400 font-semibold">{(riskMetrics?.max_drawdown * 100)?.toFixed(2) || '0'}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Portfolio Beta</span>
              <span className="text-white font-semibold">{riskMetrics?.beta?.toFixed(2) || '0'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Volatility</span>
              <span className="text-white font-semibold">{(riskMetrics?.volatility * 100)?.toFixed(2) || '0'}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Sharpe Ratio</span>
              <span className="text-green-400 font-semibold">{analytics?.sharpe_ratio?.toFixed(2) || '0'}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="workspace-panel bg-slate-900 p-4">
        <h3 className="font-semibold text-slate-300 mb-4">Asset Allocation</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={Object.entries(analytics?.exposure_by_asset_type || {}).map(([name, value]) => ({
            name,
            value,
          }))}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="name" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }} />
            <Bar dataKey="value" fill="#3b82f6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
