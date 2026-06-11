import { defineStore } from 'pinia'
import axios from 'axios'
import {
  canAccessItem,
  canUseDeveloperTools,
  canViewPnl,
  hasAnyRole,
  hasPermission,
  isAdminUser
} from '../utils/access'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => isAdminUser(state.user),
    roleName: (state) => state.user?.role?.name || '',
    permissions: (state) => state.user?.role?.permissions || []
  },
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const formData = new FormData()
        formData.append('username', email)
        formData.append('password', password)

        const response = await axios.post('/api/v1/auth/login', formData)
        const token = response.data.access_token
        
        this.token = token
        localStorage.setItem('token', token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        
        await this.fetchMe()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Authentication failed'
        this.logout()
        return false
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      if (!this.token) return
      
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
      try {
        const response = await axios.get('/api/v1/auth/me')
        this.user = response.data
      } catch (err) {
        this.logout()
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },
    hasPermission(perm) {
      return hasPermission(this.user, perm)
    },
    hasAnyRole(roleNames) {
      return hasAnyRole(this.user, roleNames)
    },
    canAccessItem(item) {
      return canAccessItem(this.user, item)
    },
    canViewPnl() {
      return canViewPnl(this.user)
    },
    canUseDeveloperTools() {
      return canUseDeveloperTools(this.user)
    }
  }
})
