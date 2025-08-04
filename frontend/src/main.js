import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Create the Vue app
const app = createApp(App)

// Use plugins
app.use(store)
app.use(router)
app.config.globalProperties.$axios = axios

// Mount the app
app.mount('#app')

// Check authentication status when the app starts
store.dispatch('checkAuth')
