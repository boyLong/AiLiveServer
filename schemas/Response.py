from typing import Optional
from datetime import datetime
from typing import List, Optional,Union
from pydantic import BaseModel, EmailStr, AnyHttpUrl

class UserInfoBase(BaseModel):
    '"id","username",  "is_allow","created_at","updated_at","Expire_at"'
    id: int
    username: str=None
    is_allow: bool=False
    created_at: Optional[datetime]=None
    Expire_at: Optional[datetime]=None

class TokenBase(BaseModel):
    token: str

# Shared properties
class ResponseBase(BaseModel):
    data: Union[None,UserInfoBase,TokenBase]
    status: int = None
    msg: str = "成功"



