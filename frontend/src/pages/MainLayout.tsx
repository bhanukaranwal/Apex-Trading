import { Outlet, Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  LineChart, 
  TrendingUp, 
  Wallet, 
  Zap, 
  Search, 
  Settings, 
  LogOut 
} from 'lucide-react'
import { useAuthStore } from '@/lib/store/authStore'

export function MainLayout() {
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/charts', icon: LineChart, label: 'Charts' },
    { path: '/options', icon: TrendingUp, label: 'Options' },
    { path: '/portfolio', icon: Wallet, label: 'Portfolio' },
    { path: '/strategies', icon: Zap, label: 'Strategies' },
    { path: '/scanners', icon: Search, label: 'Scanners' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <div className="h-screen flex bg-slate-950 text-slate-100">
      <aside className="w-16 bg-slate-900 border-r border-slate-800 flex flex-col items-center py-4">
        <div className="mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center font-bold text-white">
            A
          </div>
        </div>

        <nav className="flex-1 flex flex-col gap-2">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`p-3 rounded-lg transition-colors group relative ${
                location.pathname === item.path
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <item.icon size={20} />
              <span className="absolute left-full ml-2 px-2 py-1 bg-slate-800 text-sm rounded opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap">
                {item.label}
              </span>
            </Link>
          ))}
        </nav>

        <button
          onClick={logout}
          className="p-3 text-slate-400 hover:bg-red-900/20 hover:text-red-400 rounded-lg transition-colors"
        >
          <LogOut size={20} />
        </button>
      </aside>

      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}
