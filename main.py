

from fastapi import Depends, FastAPI, Header, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from config import TORTOISE_ORM
from routers.api import user,videos
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    # generate_schemas=True,  # 如果数据库为空，则自动生成对应表单，生产环境不要开
    # add_exception_handlers=True,  # 生产环境不要开，会泄露调试信息
)
async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


app.include_router(user.router, prefix="/api/user",tags=["用户"])

app.include_router(videos.router, prefix="/api/video",tags=["视频"])
