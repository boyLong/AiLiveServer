import datetime
from fastapi import APIRouter,Depends
from datetime import timedelta
from schemas.User import UserLoginBase,UserRegisterBase,EXCodeBase,EXBase
from schemas.Response import ResponseBase,UserInfoBase
from config import ACCESS_TOKEN_EXPIRE_MINUTES,STATUS
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token
from models.user import UserModel,ExCodeModel
import uuid 
from tortoise import transactions

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
        
        return {"status":STATUS.ERROR,"msg": "账号已存在" }
    password_hash = get_password_hash(user.password)
    core_suer = await UserModel.create(username=user.username,password=password_hash)
    return {"status":STATUS.SUCCESS,"msg": "注册成功" }




@router.post("/login",response_model=ResponseBase,response_model_include=["status","msg", "token","data"])
async def login_for_access_token(user: UserLoginBase):
    device_id = user.device_id
    user =await check_user(user.username, user.password)
    if not user:
        return {"status":STATUS.ERROR,"msg": "用户名密码错误","token": '',"data":{}} 
   
    # 过期时间
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 把id进行username加密，要使用str类型
    access_token = create_access_token(
        data={"sub": user.username,"device_id":device_id}, expires_delta=access_token_expires
    )
    quota=(user.Expire_at.replace(tzinfo=None)-datetime.datetime.now()).days
    if quota<0:
        quota = 0

    return {"status":STATUS.SUCCESS,"msg": "登录成功","token": access_token,"data":{"username": user.username,"is_allow": user.is_allow, 
                                                                                "quota": quota,
                                                                                "expire_time":user.Expire_at.strftime("%Y-%m-%d %H:%M:%S"),
                                                                                "create_time":user.created_at.strftime("%Y-%m-%d %H:%M:%S")}}


@router.get("/info", dependencies=[Depends(check_jwt_token)],response_model=ResponseBase, response_model_include=["status","msg","user"])
async def get_projects(*, user: UserInfoBase = Depends(check_jwt_token)):
    return {"status": STATUS.SUCCESS, "msg":"成功", "user": user}





@router.post("/activate",dependencies=[Depends(check_jwt_token)],response_model=ResponseBase, response_model_include=["status","msg","user"])
async def activate(*,ExCode: EXCodeBase, user: UserInfoBase = Depends(check_jwt_token)):
    ex_code = ExCode.ex_code

    ex_code = await ExCodeModel.filter(code=ex_code).first()
    if ex_code.used:


        return {
            "status": STATUS.ERROR,
            "msg": "兑换码已使用",
            "user": user
        }
    ex_time = ex_code.ex_time

    async with transactions.in_transaction():
        user = await UserModel.filter(id=user["id"]).first()
        expire_at = user.Expire_at
        expire_at = expire_at + datetime.timedelta(ex_time)
        user.Expire_at = expire_at
        await user.save()
        ex_code.used=True
        await ex_code.save()
  
    return {
            "status": STATUS.SUCCESS,
            "msg": "成功",
            "user": user
        }

@router.post("/generate_code",dependencies=[Depends(check_jwt_token)],response_model=ResponseBase, response_model_include=["status","msg","data"])
async def get_projects(*,ex: EXBase, user: UserInfoBase = Depends(check_jwt_token)):
    code = uuid.uuid4().hex
    user = await UserModel.filter(id=user["id"]).first()
    ex_code = ExCodeModel(ex_time=ex.ex_time, code=code, remark=ex.remark,user=user)
    await ex_code.save()
    return {
        "msg": "创建成功",
        "status": STATUS.SUCCESS,
        "data":{
            "code": code
        }
    }