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


class UsersToken(UserBase):
    token: str


class UserChangePassword(BaseModel):
    password: str
    newPassword: str


class MessageConnect(BaseModel):
    userId: int
    connect: str


class Messages(BaseModel):
    id: int
    senduser: str
    acceptusers: str
    read: bool
    sendtime: str
    addtime: str
    context: str


class MessagePid(Messages):
    pid: int


class MessageOne(Messages):
    pid: List[MessagePid] = []


class RebackMessageConnet(MessageConnect):
    rebackId: int

class Courses(BaseModel):
    name: str
    icon: Optional[str]
    desc: Optional[str]
    catalog: Optional[str]
    likenum: int