

from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.User import UserInfoBase
from models.videos import GroupModel
from pydantic import BaseModel


class GroupSchemas(pydantic_model_creator(GroupModel)):
    user: UserInfoBase
    id: int
    GroupName: str


class GroupReqSchemas(BaseModel):
    name: str