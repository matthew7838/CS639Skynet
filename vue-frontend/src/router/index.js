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
    },
    {
        path: '/version',
        name: 'Version',
        component: () => import('../views/Version.vue')
    }
]


const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/register']; // Paths of public pages that can be accessed without logging in
    const authRequired = !publicPages.includes(to.path); // Pages that require authentication
    const loggedIn = localStorage.getItem('authToken'); // Check if the token exists in local storage

    if (authRequired && !loggedIn) {
        return next('/login'); // Redirect to login page if authentication is required but user is not logged in
    }

    next(); // Otherwise, continue with the normal routing
});

export default router
