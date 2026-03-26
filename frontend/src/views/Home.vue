<template>
  <div class="home-container">
    <el-header class="home-header">
      <div class="header-left">
        <h1 class="logo">OA系统</h1>
      </div>
      <div class="header-right">
        <span class="user-name">欢迎您，{{ userInfo?.username || '管理员' }}</span>
        <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
      </div>
    </el-header>
    <el-main class="home-main">
      <div class="welcome-card">
        <el-page-header @back="handleBack" content="首页" />
        <div class="welcome-content">
          <h2>欢迎登录OA系统</h2>
          <p>登录时间：{{ loginTime }}</p>
          <el-divider />
          <div class="info-grid">
            <el-card class="info-item">
              <div class="info-title">待办事项</div>
              <div class="info-count">0</div>
            </el-card>
            <el-card class="info-item">
              <div class="info-title">已办事项</div>
              <div class="info-count">0</div>
            </el-card>
            <el-card class="info-item">
              <div class="info-title">公告通知</div>
              <div class="info-count">0</div>
            </el-card>
          </div>
        </div>
      </div>
    </el-main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const userInfo = ref<any>(null)
const loginTime = ref('')

onMounted(() => {
  // 获取用户信息
  const userInfoStr = localStorage.getItem('oa_user_info')
  if (userInfoStr) {
    userInfo.value = JSON.parse(userInfoStr)
  }
  // 格式化当前时间
  const now = new Date()
  loginTime.value = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
})

const handleBack = () => {
  ElMessage.info('已经是首页了')
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    // 清除本地存储
    localStorage.removeItem('oa_token')
    localStorage.removeItem('oa_user_info')
    ElMessage.success('退出登录成功')
    // 跳转到登录页
    router.push('/login')
  }).catch(() => {
    // 取消退出
  })
}
</script>

<style scoped>
.home-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.home-header {
  background: #242f42;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  color: white;
}

.logo {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-name {
  font-size: 14px;
}

.home-main {
  flex: 1;
  background: #f0f2f5;
  padding: 20px;
}

.welcome-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.welcome-content {
  margin-top: 20px;
  text-align: center;
}

.welcome-content h2 {
  color: #333;
  margin-bottom: 10px;
}

.welcome-content p {
  color: #666;
  font-size: 14px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.info-item {
  text-align: center;
}

.info-title {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
}

.info-count {
  color: #409eff;
  font-size: 32px;
  font-weight: 600;
}
</style>
