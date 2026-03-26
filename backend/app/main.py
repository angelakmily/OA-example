from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import random
import string
import io
import base64
import jwt
from datetime import datetime, timedelta
from typing import Optional, List

# 配置项
SECRET_KEY = "oa-example-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # 默认24小时
REMEMBER_ME_EXPIRE_MINUTES = 7 * 24 * 60  # 记住我7天

app = FastAPI(title="OA-example后端接口", version="1.0")
security = HTTPBearer()

# 内存存储（演示用，实际生产换数据库/Redis）
captcha_store = {}  # captcha_id: captcha_value
token_store = {}  # token: user_info

# 模拟用户数据
mock_users = {
    "admin": {
        "id": 1,
        "username": "admin",
        "password": "e10adc3949ba59abbe56e057f20f883e",  # 123456的MD5
        "name": "管理员",
        "avatar": "https://img1.baidu.com/it/u=2136932716,3172073075&fm=26&fmt=auto"
    }
}

# 模拟菜单数据
mock_menus = [
    {"id": 1, "name": "首页", "path": "/home"},
    {"id": 2, "name": "审批管理", "path": "/approval"},
    {"id": 3, "name": "任务管理", "path": "/task"}
]

# 模拟首页数据
mock_home_data = {
    "welcome": "欢迎回来，管理员",
    "todos": [
        {"id": 1, "title": "请假审批", "count": 3},
        {"id": 2, "title": "报销审批", "count": 2},
        {"id": 3, "title": "待办任务", "count": 5}
    ],
    "notices": [
        {"id": 1, "title": "系统升级通知", "create_time": "2024-05-20"},
        {"id": 2, "title": "五一放假安排", "create_time": "2024-04-25"},
        {"id": 3, "title": "新员工入职培训", "create_time": "2024-05-10"}
    ]
}

# 请求模型
class LoginRequest(BaseModel):
    username: str
    password: str
    captcha: str
    captcha_id: str
    remember_me: Optional[bool] = False

# 统一返回格式
def success_response(data=None, msg="操作成功"):
    return {"code": 200, "msg": msg, "data": data}

def fail_response(code=400, msg="操作失败"):
    return {"code": code, "msg": msg, "data": None}

# 生成验证码
def generate_captcha():
    # 生成4位随机字符
    chars = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(chars) for _ in range(4))
    
    # 创建图片
    width, height = 120, 40
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # 画干扰线
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line(((x1, y1), (x2, y2)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=1)
    
    # 写验证码
    try:
        font = ImageFont.truetype('arial.ttf', 28)
    except:
        font = ImageFont.load_default()
    
    for i, char in enumerate(captcha_text):
        draw.text((10 + i * 25, 5), char, font=font, fill=(random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)))
    
    # 转base64
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
    
    return captcha_text, f"data:image/png;base64,{img_base64}"

# 生成token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 校验token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in token_store:
        raise HTTPException(status_code=401, detail="登录状态已失效")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="无效的登录凭证")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="无效的登录凭证")
    user = mock_users.get(username)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user

# 接口实现
@app.get("/api/auth/captcha", summary="获取验证码")
async def get_captcha():
    captcha_text, captcha_img = generate_captcha()
    captcha_id = ''.join(random.choice(string.hexdigits) for _ in range(16))
    captcha_store[captcha_id] = captcha_text.lower()  # 统一转小写，不区分大小写
    # 5分钟过期，这里演示就不处理过期了
    return success_response({
        "captcha_id": captcha_id,
        "captcha_img": captcha_img
    })

@app.post("/api/auth/login", summary="登录接口")
async def login(request: LoginRequest):
    # 校验验证码
    if request.captcha_id not in captcha_store or captcha_store[request.captcha_id] != request.captcha.lower():
        return fail_response(msg="验证码错误或已过期")
    # 删除已使用的验证码
    del captcha_store[request.captcha_id]
    
    # 校验用户
    user = mock_users.get(request.username)
    if not user or user["password"] != request.password:
        return fail_response(msg="账号或密码错误")
    
    # 生成token
    expire_minutes = REMEMBER_ME_EXPIRE_MINUTES if request.remember_me else ACCESS_TOKEN_EXPIRE_MINUTES
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=expire_minutes)
    )
    token_store[access_token] = user
    
    return success_response({
        "token": access_token,
        "user_info": {
            "id": user["id"],
            "username": user["username"],
            "name": user["name"]
        }
    }, msg="登录成功")

@app.post("/api/auth/logout", summary="退出登录")
async def logout(current_user = Depends(get_current_user), credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token in token_store:
        del token_store[token]
    return success_response(msg="退出成功")

@app.get("/api/user/info", summary="获取用户信息和菜单")
async def get_user_info(current_user = Depends(get_current_user)):
    return success_response({
        "user_info": {
            "name": current_user["name"],
            "avatar": current_user["avatar"]
        },
        "menus": mock_menus
    })

@app.get("/api/home/data", summary="获取首页数据")
async def get_home_data(current_user = Depends(get_current_user)):
    return success_response(mock_home_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
