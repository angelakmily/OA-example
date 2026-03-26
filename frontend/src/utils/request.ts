import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000
})

// 请求拦截器，添加token
request.interceptors.request.use(config => {
  const token = localStorage.getItem('oa_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器，处理错误
request.interceptors.response.use(response => {
  return response.data
}, error => {
  if (error.response) {
    switch (error.response.status) {
      case 401:
        // 未登录，跳转到登录页
        localStorage.removeItem('oa_token')
        ElMessage.error('登录已过期，请重新登录')
        router.push('/login')
        break
      case 403:
        ElMessage.error('没有权限访问该资源')
        break
      case 500:
        ElMessage.error('服务器内部错误')
        break
      default:
        ElMessage.error(error.response.data.message || '请求失败')
    }
  } else {
    ElMessage.error('网络连接失败，请检查网络')
  }
  return Promise.reject(error)
})

export default request
