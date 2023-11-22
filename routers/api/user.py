from fastapi import APIRouter,Depends
from datetime import timedelta
from schemas.User import UserBase
from config import ACCESS_TOKEN_EXPIRE_MINUTES,STATUS
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token
from models.user import UserModel
router = APIRouter()


@router.post("/register")
async def register(user: UserBase):

    if await UserModel.filter(username=user.username).first():
        return {
            "status": STATUS.ERROR,
            "msg": "账号已存在"
        }
    password_hash = get_password_hash(user.password)
    core_suer = await UserModel.create(username=user.username,password=password_hash)
    return {
            "status": STATUS.SUCCESS,
            "msg": "注册成功",
        }



async def check_user(username, password):
    """
    校验用户（真实的应该是跟DB进行校验，这里只是做演示）
    :param username:
    :param password:
    :return:
    """
    user = await UserModel.filter(username=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

@router.post("/login",)
async def login_for_access_token(user: UserBase):
    user =await check_user(user.username, user.password)
    if not user:
        return {
            "status": STATUS.ERROR,
            "msg": "用户名密码错误",
        }
    # 过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 把id进行username加密，要使用str类型
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
 
    return {
            "status": STATUS.SUCCESS,
            "msg": "登录成功",
            "token":access_token
        }

@router.get("/info", dependencies=[Depends(check_jwt_token)])
async def get_projects(*, user: UserBase = Depends(check_jwt_token)):

    return {
            "status": STATUS.SUCCESS,
            "msg": "成功",
            "data": user
        }


@router.post("/activate")
async def get_projects(*, user: UserBase = Depends(check_jwt_token)):

    return {
            "status": STATUS.SUCCESS,
            "msg": "成功",
            "data": user
        }
