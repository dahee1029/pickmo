import './assets/main.css'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import "vue3-carousel-3d/dist/index.css"
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Carousel3d } from 'vue3-carousel-3d'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.component('Carousel3d', Carousel3d);


app.mount('#app')
