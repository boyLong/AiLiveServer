#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/16 13:43
# @Author  : CoderCharm
# @File    : sys_user_schema.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""
管理员表的 字段model模型 验证 响应(没写)等
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, AnyHttpUrl


# Shared properties
class UserRegisterBase(BaseModel):
    username: int = None
    password: str = None


class UserLoginBase(BaseModel):
    username: int = None
    password: str = None
    device_id: str



class UserInfoBase(BaseModel):
    '"id","username",  "is_allow","created_at","updated_at","Expire_at"'
    id: int
    username: int=None
    is_allow: bool=False
    created_at: Optional[datetime]=None
    Expire_at: Optional[datetime]=None

class EXBase(BaseModel):
    ex_time: int
    remark: str=""
class EXCodeBase(BaseModel):
    ex_code: str