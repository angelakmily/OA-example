# OA-example后端服务

## 1. 环境依赖
Python 3.8+

## 2. 安装依赖
```bash
pip install -r requirements.txt
```

## 3. 启动服务
```bash
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 4. 接口文档
启动后访问 http://localhost:8000/docs 可以查看Swagger在线接口文档，可直接调试接口

## 5. 测试账号
- 账号：admin
- 密码：123456（MD5加密后值：e10adc3949ba59abbe56e057f20f883e）

## 6. 接口说明
所有接口严格遵循需求文档中的接口约定，返回格式统一：
```json
{"code": 200/400/401/500, "msg": "提示信息", "data": {}}
```
