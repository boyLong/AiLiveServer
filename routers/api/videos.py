import uuid
import aiofiles 
from fastapi import APIRouter,Depends,UploadFile,File
from datetime import timedelta
from schemas.Videos import GroupSchemas,GroupReqSchemas,GroupDelReqSchemas,TagReqSchemas,TagDelReqSchemas,TagWordReqSchemas
from schemas.Response import ResponseBase,UserInfoBase
from models.user import UserModel
from models.videos import GroupModel,ReplyTagModel
from config import STATUS, FILE_PATH
from models.videos import ReplyTagModel
from common.auth import create_access_token,verify_password,get_password_hash,check_jwt_token

router = APIRouter()

@router.post("/add_group",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_group(group: GroupReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """添加组"""
    user = await UserModel.filter(id=user["id"]).first()
    core_suer = await GroupModel.create(user=user,groupName=group.name)
    return {"status":STATUS.SUCCESS,"msg": "添加成功"}

@router.get("/group",dependencies=[Depends(check_jwt_token)], )
async def group(user: UserInfoBase = Depends(check_jwt_token)):
    """查询组"""
    user = await UserModel(id=user["id"]).first()
    groups = await GroupModel.filter(user=user).all()
    return {"status":STATUS.SUCCESS,"msg": "查询成功","data":groups}

@router.post("/del_group",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_group(group: GroupDelReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """删除组"""
    res = await GroupModel.filter(id=group.id).delete()
    print(res)
    return {"status":STATUS.SUCCESS,"msg": "删除成功"}



@router.post("/add_tag",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_tag(tag: TagReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """添加标签"""
    print(tag)
    print(user["id"])
    user = await UserModel.filter(id=user["id"]).first()
    group_id = await GroupModel.filter(id=tag.group_id,user=user).first()
    if not group_id or not user:
        return {"status":STATUS.ERROR,"msg": "信息不存在,无法创建"}

    core_suer = await ReplyTagModel.create(group_id=group_id,
                                           tag_name=tag.tag_name,
                                           voice_link=tag.voice_link,
                                           keywords=tag.keywords)
    return {"status":STATUS.SUCCESS,"msg": "添加成功"}

@router.get("/tag/group_id={group_id}",dependencies=[Depends(check_jwt_token)])
async def query_tag( group_id:int,user: UserInfoBase = Depends(check_jwt_token)):
    """
    查询组下面的语音
    """
    user = await UserModel.filter(id=user["id"]).first()
    group_id = await GroupModel.filter(id=group_id,user=user).first()
    if not group_id or not user:
        return {"status":STATUS.ERROR,"msg": "信息不存在,无法查询"}
    tags =await ReplyTagModel.filter(group_id=group_id).all()

    return {"status":STATUS.SUCCESS,"msg": "查询成功","data":tags}
    
@router.post("/del_tag",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_group(tag: TagDelReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """
    删除组的语音
    """
    user = await UserModel.filter(id=user["id"]).first()
    group_id = await GroupModel.filter(id=tag.group_id,user=user).first()
    if not group_id or not user:
        return {"status":STATUS.ERROR,"msg": "信息不存在,无法删除"}

    res = await ReplyTagModel.filter(id=tag.tag_id,group_id=group_id).delete()
    return {"status":STATUS.SUCCESS,"msg": "删除成功"}

@router.post("/add_word",dependencies=[Depends(check_jwt_token)], response_model=ResponseBase,response_model_include=["status","msg"])
async def add_word(tag: TagWordReqSchemas, user: UserInfoBase = Depends(check_jwt_token)):
    """添加匹配关键词
    """
    user = await UserModel.filter(id=user["id"]).first()
    group_id = await GroupModel.filter(id=tag.group_id,user=user).first()
    res = await ReplyTagModel.filter(id=tag.tag_id,group_id=group_id).first()
    if not res:
        return {"status":STATUS.ERROR,"msg": "标签不存在"}
    res.keywords.append(tag.word)
    await res.save()
    return {"status":STATUS.SUCCESS,"msg": "添加成功"}



@router.post("/upload")
async def upload_voice(file: UploadFile = File(...)):
    try:
        filename = f"/voice/{uuid.uuid4()}-{file.filename}"
        async with aiofiles.open(FILE_PATH + filename, 'wb') as w:
            await w.write(await file.read() )
        return {"status": STATUS.SUCCESS, "msg": "上传成功","voice_link": "/static"+ filename}
    except:
        return {"status": STATUS.ERROR, "msg": "上传失败","voice_link":""}