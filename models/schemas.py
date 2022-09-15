#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2022/9/14 17:39
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : schemas.py
@Describe: 接口请求时，请求体的模型校验
@License : myself learn
"""
from pydantic import BaseModel,Field
from typing import Optional, List


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    """
    请求模型验证
    """
    password: str
    role: int
    jobnum: Optional[int] = None
    studentnum: Optional[int] = None
    sex: str = "男"
    age: int


class UserLogin(UserBase):
    password: str


class UsernameRole(UserBase):
    role: str
