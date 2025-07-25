import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Login from '@/components/Login.vue'
import CardDetail from '@/views/CardDetail.vue'
import AddCard from '@/views/AddCard.vue'
import About from '@/views/About.vue' // Import the About component
import BagDetail from '@/views/BagDetail.vue'
import AddItem from '@/views/AddItem.vue'

const routes = [
  {
    path: '/',
    name: 'Cards',
    component: Home
  },
  {
    path: '/home',
    redirect: '/' // Перенаправление с /home на /
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/card/:uuid',
    name: 'CardDetail',
    component: CardDetail,
    props: true
  },
  {
    path: '/add-card',
    name: 'AddCard',
    component: AddCard
  },
  {
    path: '/logout',
    beforeEnter: (to, from, next) => {
      // Логика выхода
      next('/') // Перенаправление на главную после выхода
    }
  },
  {
    path: '/about',
    name: 'About',
    component: About // Add the new route
  },
  { 
    path: '/bag/:id',
    name: 'BagDetail',
    component: BagDetail,
    props: true
  },
  {
    path: '/add-item',
    name: 'AddItem',
    component: AddItem
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior (to, from, savedPosition) {
    return { top: 0 }
  }
})

export default router
