import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    isAuthenticated: false,
    userId: null,
    user: null,  // Added to store full user object
    error: null
  },
  mutations: {
    SET_AUTH(state, { isAuthenticated, userId }) {
      state.isAuthenticated = isAuthenticated
      state.userId = userId
    },
    SET_USER(state, user) {
      state.user = user
      state.userId = user?.id || null
      state.isAuthenticated = !!user
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    REMOVE_SEASON(state, seasonUuid) {
      state.seasons = state.seasons.filter(season => season.uuid !== seasonUuid)
    }
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        const response = await axios.get('/api/user')
        if (response.data) {
          commit('SET_USER', response.data)
          return true
        }
      } catch (error) {
        if (error.response?.status === 401) {
          // Expected behavior for logged-out users
          commit('SET_USER', null)
        } else {
          console.error('Auth error:', error)
        }
        return false
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('/auth/logout', {}, {
          withCredentials: true
        })
        commit('SET_USER', null)
        // Optional: reload to clear any cached data
        window.location.reload()
      } catch (error) {
        console.error('Logout failed:', error)
        commit('SET_ERROR', error)
      }
    }
  },
  getters: {
    isAdmin: (state) => {
      return state.user?.is_admin || false
    },
    currentUser: (state) => {
      return state.user
    }
  }
})