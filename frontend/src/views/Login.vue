<template>
  <div class="login-container">
    <div class="login-card">
      <h2 class="login-title">OA系统登录</h2>
      <el-form ref="loginForm" :model="loginForm" label-width="80px" class="login-form">
        <el-form-item label="用户名" prop="username" :rules="[
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ]">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" :rules="[
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" @click="handleLogin" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '../utils/request'

const router = useRouter()
const loading = ref(false)
const loginForm = ref({
  username: '',
  password: ''
})

const handleLogin = async () => {
  loading.value = true
  try {
    // 调用登录接口
    const res = await request.post('/auth/login', {
      username: loginForm.value.username,
      password: loginForm.value.password
    }) as any
    // 保存token和用户信息
    localStorage.setItem('oa_token', res.token)
    localStorage.setItem('oa_user_info', JSON.stringify(res.user))
    ElMessage.success('登录成功')
    // 跳转到首页
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  width: 400px;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.login-form {
  width: 100%;
}

.login-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
}
</style>
