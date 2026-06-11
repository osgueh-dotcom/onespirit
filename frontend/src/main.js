import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import './assets/index.css'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

if (apiBaseUrl) {
  axios.defaults.baseURL = apiBaseUrl
}

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
