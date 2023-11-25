from typing import Optional

from typing import List, Optional,Union
from pydantic import BaseModel, EmailStr, AnyHttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator
from schemas.User import UserInfoBase
from models.videos import GroupModel


# Shared properties
class ResponseBase(BaseModel):
    data: dict=None
    status: int = None
    msg: str = "成功"
    token: str=None
    user: UserInfoBase=None


