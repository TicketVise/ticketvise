import { createApp } from 'vue'

import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import './assets/tailwind.css'

import AppLayout from '@/layouts/AppLayout.vue'

createApp(App)
  .use(store)
  .use(router)
  .component('AppLayout', AppLayout)
  .mount('#app')
