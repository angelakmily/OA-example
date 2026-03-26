# OA系统前端

基于Vue3 + TypeScript + Vite + Element Plus开发的OA系统前端项目

## 技术栈
- Vue 3.3+
- TypeScript
- Vite 5
- Element Plus
- Vue Router 4
- Axios

## 项目结构
```
src/
├── router/          # 路由配置
├── views/           # 页面组件
│   ├── Login.vue    # 登录页面
│   └── Home.vue     # 首页
├── utils/           # 工具类
│   └── request.ts   # axios封装
├── App.vue
└── main.ts
```

## 安装依赖
```bash
npm install
```

## 本地开发启动
```bash
npm run dev
```
默认访问地址：http://localhost:5173

## 生产环境构建
```bash
npm run build
```

## 接口约定
- 登录接口：POST /api/auth/login
  请求参数：{ username: string, password: string }
  响应参数：{ token: string, user: { username: string, [key: string]: any } }

- 所有需要鉴权的接口请求头需要携带Authorization: Bearer {token}
- 接口返回401状态码时自动跳转到登录页
