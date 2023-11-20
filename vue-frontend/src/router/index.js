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
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  }
]


const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
