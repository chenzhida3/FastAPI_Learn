#!/usr/bin/env python
"""
-*- coding: utf-8 -*-
@Time    : 2023/5/30 17:27
@Author  : Chenzhida
@Email   : chenzhida3@163.com
@File    : course.py
@Describe: 课程接口
@License : myself learn
"""
from fastapi import APIRouter, Depends
from models.crud import *
from models.get_db import get_db
from common.jwtTool import *
from common.jsontools import *
from fastapi.encoders import jsonable_encoder
from common.configLog import Logger
from config import *
logger = Logger('routers.courese').getLog()

courseRouter = APIRouter()

@courseRouter.post(path="/create")
async def create(course: Courses, db: Session = Depends(get_db), user: UsernameRole=Depends(JWT_tool.get_cure_user)):
    """创建课程接口"""
    user_ = get_user_username(db=db, username=user.username)
    user_role = get_role_name(db=db, id=user_.role)
    if not user_role or user_role.name == '学生':
        return resp_200(code=101004, message="只有老师才能创建课程", data={})
    if len(course.name) < 2 or len(course.name)>51:
        return resp_200(code=101005, message='课程长度应该在2-50', data={})
    # 创建的课程名字不能重复=
    courese_name = db_get_courese_name(db=db, name=course.name)
    if courese_name:
        return resp_200(code=101002, message="课程名称不能重复", data={})
    couse = db_create_course(db=db, course=course, user=user_.id)
    return resp_200(code=200, message="创建成功", data=jsonable_encoder(couse))
    