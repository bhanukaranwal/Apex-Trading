import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        const response = await axios.post(`${API_URL}/api/v1/auth/refresh`, {
          refresh_token: refreshToken,
        })
        
        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    
    return Promise.reject(error)
  }
)

export const marketDataAPI = {
  getQuote: (symbol: string) => api.get(`/market-data/quote/${symbol}`),
  getQuotes: (symbols: string[]) => api.get('/market-data/quotes', { params: { symbols } }),
  getBars: (symbol: string, timeframe: string, start?: string, end?: string) =>
    api.get(`/market-data/bars/${symbol}`, { params: { timeframe, start, end } }),
  getOptionChain: (symbol: string, expiration?: string) =>
    api.get(`/market-data/options/chain/${symbol}`, { params: { expiration } }),
  getDepth: (symbol: string) => api.get(`/market-data/depth/${symbol}`),
}

export const ordersAPI = {
  placeOrder: (data: any) => api.post('/orders', data),
  getOrders: (status?: string) => api.get('/orders', { params: { status } }),
  getOrder: (orderId: string) => api.get(`/orders/${orderId}`),
  updateOrder: (orderId: string, data: any) => api.patch(`/orders/${orderId}`, data),
  cancelOrder: (orderId: string) => api.delete(`/orders/${orderId}`),
  cancelAllOrders: () => api.delete('/orders'),
}

export const positionsAPI = {
  getPositions: () => api.get('/positions'),
  getPosition: (symbol: string) => api.get(`/positions/${symbol}`),
  closePosition: (symbol: string, qty?: number) =>
    api.delete(`/positions/${symbol}`, { data: { qty } }),
  closeAllPositions: () => api.delete('/positions'),
}

export const portfolioAPI = {
  getAccount: () => api.get('/portfolio/account'),
  getSummary: () => api.get('/portfolio/summary'),
  getAnalytics: () => api.get('/portfolio/analytics'),
  getRiskMetrics: () => api.get('/portfolio/risk-metrics'),
  getGreeks: () => api.get('/portfolio/greeks'),
}

export const signalsAPI = {
  getSignals: (params?: any) => api.get('/signals', { params }),
  getPredictions: (symbol: string, horizon: number) =>
    api.get(`/signals/${symbol}/predictions`, { params: { horizon } }),
  getSentiment: (symbol: string) => api.get(`/signals/${symbol}/sentiment`),
  getPatterns: (symbol: string) => api.get(`/signals/${symbol}/patterns`),
}

export const strategiesAPI = {
  createStrategy: (data: any) => api.post('/strategies', data),
  getStrategies: () => api.get('/strategies'),
  getStrategy: (id: number) => api.get(`/strategies/${id}`),
  runBacktest: (id: number, data: any) => api.post(`/strategies/${id}/backtest`, data),
  deployStrategy: (id: number, symbols: string[]) =>
    api.post(`/strategies/${id}/deploy`, { symbols }),
  stopStrategy: (id: number) => api.delete(`/strategies/${id}/deploy`),
}

export const scannersAPI = {
  runScan: (data: any) => api.post('/scanners/scan', data),
  getPresets: () => api.get('/scanners/presets'),
  getGainers: (limit: number) => api.get('/scanners/movers/gainers', { params: { limit } }),
  getLosers: (limit: number) => api.get('/scanners/movers/losers', { params: { limit } }),
  getMostActive: (limit: number) => api.get('/scanners/movers/volume', { params: { limit } }),
}

export const workspacesAPI = {
  createWorkspace: (data: any) => api.post('/workspaces', data),
  getWorkspaces: () => api.get('/workspaces'),
  getWorkspace: (id: number) => api.get(`/workspaces/${id}`),
  updateWorkspace: (id: number, data: any) => api.put(`/workspaces/${id}`, data),
  deleteWorkspace: (id: number) => api.delete(`/workspaces/${id}`),
}
