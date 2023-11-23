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

from pydantic import BaseModel, EmailStr, AnyHttpUrl


# Shared properties
class UserLoginBase(BaseModel):
    username: int = None
    password: str = None


class TokenModel(BaseModel):
    token: str = None

