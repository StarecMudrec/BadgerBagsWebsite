import { createStore } from 'vuex'

export default createStore({
  state: {
    isAuthenticated: false,
    userId: null,
  },
  mutations: {
    SET_AUTH(state, { isAuthenticated, userId }) {
      state.isAuthenticated = isAuthenticated
      state.userId = userId
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    REMOVE_SEASON(state, seasonUuid) {
      state.seasons = state.seasons.filter(season => season.uuid !== seasonUuid);
    },
  },
  actions: {
    async checkAuth({ commit }) {
      try {
        const { isAuthenticated, userId } = await checkAuth()
        commit('SET_AUTH', { isAuthenticated, userId })
      } catch (error) {
        console.error('Auth check failed:', error)
      }
    },
    async logout({ commit }) {
      try {
        await fetch('/auth/logout', { 
          method: 'POST',
          credentials: 'include'
        })
        commit('SET_AUTH', { isAuthenticated: false, userId: null })
        window.location.reload();
      } catch (error) {
        console.error('Logout failed:', error)
      }
    },
  }
})