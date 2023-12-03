

from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.User import UserInfoBase
from typing import ClassVar

from models.videos import GroupModel
from pydantic import BaseModel,AnyHttpUrl


class GroupSchemas(pydantic_model_creator(GroupModel)):
    user: UserInfoBase
    id: int
    GroupName: str


class GroupReqSchemas(BaseModel):
    name: str

class GroupDelReqSchemas(BaseModel):
    id: int

class TagDelReqSchemas(BaseModel):
    tag_id: int
    group_id: int

class TagWordReqSchemas(BaseModel):
    tag_id: int
    group_id: int
    word: str

class TagReqSchemas(BaseModel):
    tag_name: str
    keywords: list
    group_id: int
    voice_link: AnyHttpUrl


class voiceReqSchemas(BaseModel):
    category_id: int = 1
    group_id: int
    voice_link: AnyHttpUrl