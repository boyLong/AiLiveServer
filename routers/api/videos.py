from fastapi import APIRouter,Depends
from datetime import timedelta
from schemas.Videos import GroupSchemas,GroupReqSchemas
from schemas.Response import ResponseBase,UserInfoBase
from models.user import UserModel
from models.videos import GroupModel
from config import STATUS
from models.videos import ReplyTagModel
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token

router = APIRouter()

@router.post("/add_group",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg","data"])
async def add_group(group: GroupReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """
    
    返回字段
        status:   成功->200, 失败->500
        msg: 错误提示原因
    """
    
    core_suer = await GroupModel.create(user=user,name=group.name)

    
    return {"status":STATUS.SUCCESS,"msg": "添加 成功","data":{}}
