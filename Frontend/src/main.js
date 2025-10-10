import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import {router} from "./routes.js"
import axios from 'axios'

createApp(App).use(router).mount('#app')
