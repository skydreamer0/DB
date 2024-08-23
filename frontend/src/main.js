import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './assets/styles/global.css'
import './assets/styles/app.css'
const app = createApp(App)

// 設置 Axios 的基礎 URL
axios.defaults.baseURL = 'http://localhost:3000/'

// 使用 VueAxios 插件
app.use(VueAxios, axios)

// 使用 Vue Router
app.use(router)

// 掛載 Vue 應用
app.mount('#app')