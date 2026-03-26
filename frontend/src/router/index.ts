import { createRouter, createWebHashHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      noAuth: true // 不需要登录即可访问
    }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      noAuth: false // 需要登录才能访问
    }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// 路由守卫，判断是否登录
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('oa_token')
  if (to.meta.noAuth) {
    next()
  } else {
    if (token) {
      next()
    } else {
      next('/login')
    }
  }
})

export default router
