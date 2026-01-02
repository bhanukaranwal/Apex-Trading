import { create } from 'zustand'

interface AuthState {
  isAuthenticated: boolean
  user: any | null
  login: (user: any, tokens: { access_token: string; refresh_token: string }) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: !!localStorage.getItem('access_token'),
  user: null,
  login: (user, tokens) => {
    localStorage.setItem('access_token', tokens.access_token)
    localStorage.setItem('refresh_token', tokens.refresh_token)
    set({ isAuthenticated: true, user })
  },
  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ isAuthenticated: false, user: null })
  },
}))
