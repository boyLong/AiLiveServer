from fastapi import APIRouter,Depends
from datetime import timedelta
from schemas.Videos import GroupSchemas,GroupReqSchemas,GroupDelReqSchemas
from schemas.Response import ResponseBase,UserInfoBase
from models.user import UserModel
from models.videos import GroupModel
from config import STATUS
from models.videos import ReplyTagModel
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token

router = APIRouter()

@router.post("/add_group",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_group(group: GroupReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):

    user = await UserModel(id=user["id"]).first()
    core_suer = await GroupModel.create(user=user,groupName=group.name)
    return {"status":STATUS.SUCCESS,"msg": "添加成功"}

@router.get("/group",dependencies=[Depends(check_jwt_token)], )
async def group(user: UserInfoBase = Depends(check_jwt_token)):

    user = await UserModel(id=user["id"]).first()
    groups = await GroupModel.filter(user=user).all()
    return {"status":STATUS.SUCCESS,"msg": "查询成功","data":groups}

@router.post("/del_group",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_group(group: GroupDelReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):

    res = await GroupModel.filter(id=group.id).delete()
    print(res)
    return {"status":STATUS.SUCCESS,"msg": "删除成功"}