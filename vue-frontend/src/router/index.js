import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/removed',
    name: 'remove',
    component: () => import('../views/removed.vue')
  },
  {
    path: '/history',
    name: 'history',
    component: () => import('../views/history.vue')
  },
  {
    path: '/edit',
    name: '/edit',
    component: () => import('../views/edit.vue')
  }
]


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
