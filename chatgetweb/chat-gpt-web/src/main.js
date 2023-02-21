import App from './App.vue'
import { createApp } from 'vue'
import Layui from '@layui/layui-vue'
import Router from './router'
import '@layui/layui-vue/lib/index.css'

createApp(App).use(Layui).use(Router).mount('#app')