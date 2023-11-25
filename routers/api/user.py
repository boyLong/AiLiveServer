from fastapi import APIRouter,Depends
from datetime import timedelta
from schemas.User import UserLoginBase,UserRegisterBase
from schemas.Response import ResponseBase,UserInfoBase
from config import ACCESS_TOKEN_EXPIRE_MINUTES,STATUS
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token
from models.user import UserModel
router = APIRouter()
async def check_user(username, password,):
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


@router.post("/register",response_model=ResponseBase,response_model_include=["status","msg"])
async def register(user: UserRegisterBase):
    """
    
    返回字段
        status:   成功->200, 失败->500
        msg: 错误提示原因
    """
    if await UserModel.filter(username=user.username).first():
        
        return {"status":STATUS.ERROR,"msg": "账号已存在","data":{}}
    password_hash = get_password_hash(user.password)
    core_suer = await UserModel.create(username=user.username,password=password_hash)
    return {"status":STATUS.SUCCESS,"msg": "注册成功","data":{}}




@router.post("/login",response_model=ResponseBase,response_model_include=["status","msg", "token"])
async def login_for_access_token(user: UserLoginBase):
    device_id = user.device_id
    user =await check_user(user.username, user.password)
    if not user:
        return {"status":STATUS.ERROR,"msg": "用户名密码错误","token": ''} 
   
    # 过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 把id进行username加密，要使用str类型
    access_token = create_access_token(
        data={"sub": user.username,"device_id":device_id}, expires_delta=access_token_expires
    )

    return {"status":STATUS.SUCCESS,"msg": "登录成功","token": access_token}


@router.get("/info", dependencies=[Depends(check_jwt_token)],response_model=ResponseBase, response_model_include=["status","msg","user"])
async def get_projects(*, user: UserInfoBase = Depends(check_jwt_token)):
    print(user)
    return {"status": STATUS.SUCCESS, "msg":"成功", "user": user}




# @router.post("/activate")
# async def get_projects(*, user: UserBase = Depends(check_jwt_token)):

#     return {
#             "status": STATUS.SUCCESS,
#             "msg": "成功",
#             "data": user
#         }
